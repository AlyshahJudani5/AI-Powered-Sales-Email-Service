"""
Sales Report Automation - Main Class
Handles database connection, KPI calculation, AI insights, and report generation
"""

import pyodbc
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import json
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import logging

from config import TableConfig, COLORS, COUNTRY_CONFIG
from utils import clean_number, format_client_name, generate_report_id, log_report
from charts import generate_branch_chart_data, generate_channel_chart_data, generate_category_chart_data
from templates import generate_concise_email_template, generate_full_report_template

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AnalysisState(TypedDict):
    kpis: dict
    all_tables: list
    insights: list
    error: str


class SalesReportAutomation:
    def __init__(self, global_config, client_config):
        self.global_config = global_config
        self.client_config = client_config
        self.config = client_config
        self.db_connection = None
        self.all_tables_data = []
        self.second_category_table = None
        self.client_name = client_config.get('client_name')
        self.report_time = client_config.get('data_time', '06:00:00.000')
        self.colors = COLORS
        self.report_title = client_config.get('title', 'Daily Sales Report')
        
        # Set country and currency
        self.country = client_config.get('country', 'PK')
        self.currency_unit = COUNTRY_CONFIG.get(self.country, COUNTRY_CONFIG['PK'])['currency']
        
        self.llm = ChatGroq(
            api_key=os.getenv('groq_api_key'),
            model_name=os.getenv('groq_model'),
            temperature=0.7,
            max_tokens=2000
        )
        
        self.analysis_workflow = self._build_analysis_workflow()
        self.report_date = None
    
    def connect_database(self):
        try:
            connection_string = (
                f"DRIVER={{{self.client_config.get('db_driver')}}};"
                f"SERVER={self.client_config.get('db_server')};"
                f"DATABASE={self.client_config.get('db_name')};"
                f"UID={self.client_config.get('db_user')};"
                f"PWD={self.client_config.get('db_password')}"
            )
            self.db_connection = pyodbc.connect(connection_string, timeout=10)
            logger.info("Database connection established")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            self.db_connection = None
            return False
    
    def execute_sp(self, specific_date=None, branch_ids=''):
        cursor = None
        try:
            if not self.db_connection:
                self.connect_database()
            
            if not self.db_connection:
                logger.error("No database connection")
                return False
            
            cursor = self.db_connection.cursor()
            
            if not specific_date:
                self.report_date = datetime.now().strftime('%Y-%m-%d')
            else:
                self.report_date = specific_date
            
            sp_query = """
                EXEC spSaleSummaryReportAI2
                    @CategoryLevel = 1,
                    @SpecificDate = ?,
                    @CompanyBranchIds = ?,
                    @Time = ?,
                    @ForResturant = 1,
                    @SaleTypeDineInIds = '',
                    @IsRequiredGPTab = 1,
                    @IsRequiredSaleTypeTab = 1,
                    @IsRequiredTotal = 0,
                    @FromTime = NULL
            """
            
            logger.info(f"Executing SP for date: {self.report_date}, Branches: {branch_ids or 'All'}")
            cursor.execute(sp_query, self.report_date, branch_ids, self.report_time)
            
            self.all_tables_data = []
            result_set_count = 0
            
            while True:
                try:
                    columns = [column[0] for column in cursor.description] if cursor.description else []
                    result = cursor.fetchall()
                    
                    if result and columns and len(result) > 0:
                        table_data = [
                            {col: row[i] for i, col in enumerate(columns)}
                            for row in result
                        ]
                        
                        self.all_tables_data.append({
                            'table_number': result_set_count + 1,
                            'columns': columns,
                            'data': table_data
                        })
                        logger.info(f"✅ Retrieved result set {result_set_count + 1}: {len(result)} rows")
                        result_set_count += 1
                    
                    if not cursor.nextset():
                        break
                except pyodbc.ProgrammingError:
                    if not cursor.nextset():
                        break
            
            logger.info(f"Successfully retrieved {len(self.all_tables_data)} non-empty result sets")
            
            if self.client_config.get("multi_category", 0) == 1:
                cursor2 = None
                try:
                    cursor2 = self.db_connection.cursor()
                    sp_query2 = """
                        EXEC spSaleSummaryReportAI2
                            @CategoryLevel = 2,
                            @SpecificDate = ?,
                            @CompanyBranchIds = ?,
                            @Time = ?,
                            @ForResturant = 1,
                            @SaleTypeDineInIds = '',
                            @IsRequiredGPTab = 1,
                            @IsRequiredSaleTypeTab = 1,
                            @IsRequiredTotal = 0,
                            @FromTime = NULL
                    """
                    logger.info(f"Executing second SP (@CategoryLevel=2) for date: {self.report_date}, Branches: {branch_ids or 'All'}")
                    cursor2.execute(sp_query2, self.report_date, branch_ids, self.report_time)
                    second_run_tables = []
                    while True:
                        try:
                            columns = [column[0] for column in cursor2.description] if cursor2.description else []
                            result = cursor2.fetchall()
                            if result and columns and len(result) > 0:
                                second_run_tables.append({
                                    'columns': columns,
                                    'data': [{col: row[i] for i, col in enumerate(columns)} for row in result]
                                })
                            if not cursor2.nextset():
                                break
                        except pyodbc.ProgrammingError:
                            if not cursor2.nextset():
                                break
                    for table_info in second_run_tables:
                        if 'Category' in table_info['columns'] and 'CategoryShareMonth' in table_info['columns']:
                            self.second_category_table = table_info
                            logger.info("✅ Retrieved sub-category table successfully")
                            break
                except Exception as e:
                    logger.error(f"Error executing second SP: {str(e)}")
                finally:
                    if cursor2:
                        cursor2.close()
                        
            return len(self.all_tables_data) > 0
                
        except Exception as e:
            logger.error(f"Error executing SP: {str(e)}")
            return False
        finally:
            if cursor:
                cursor.close()

    def _find_table_by_columns(self, required_columns):
        for idx, table_info in enumerate(self.all_tables_data):
            table_columns = table_info['columns']
            if all(col in table_columns for col in required_columns):
                return idx
        return None
    
    def _get_branch_name_from_data(self):
        """Extract branch name from fetched data"""
        try:
            # Look through all tables for the first "Branch" field value that isn't "Sub Total"
            for table_info in self.all_tables_data:
                if 'Branch' in table_info['columns']:
                    table_data = table_info['data']
                    for row in table_data:
                        branch_name = str(row.get('Branch', '')).strip()
                        if branch_name and branch_name.lower() != 'sub total':
                            return branch_name
            return None
        except Exception as e:
            logger.error(f"Error extracting branch name: {str(e)}")
            return None
    
    def calculate_kpis(self):
        try:
            kpis = {}
            
            if not self.all_tables_data:
                return {}
            
            first_table = self.all_tables_data[0]['data']
            if not first_table:
                return {}

            branch_col = next((col for col in ['Branch', 'BranchType'] if col in first_table[0]), None)
            if branch_col:
                filtered_table = [row for row in first_table 
                                if str(row.get(branch_col, '')).strip().lower() != 'sub total']
            else:
                filtered_table = first_table

            sale_col = next((col for col in ['MonthSale', 'Sale', 'TotalAmount'] 
                            if col in filtered_table[0]), None)
            if sale_col:
                kpis['total_sales'] = sum(clean_number(row.get(sale_col, 0)) 
                                        for row in filtered_table)
            
            if 'Total' in filtered_table[0]:
                kpis['today_sale'] = sum(clean_number(row.get('Total', 0)) 
                                        for row in filtered_table)
            
            if 'LastMonthSaleSameDay' in filtered_table[0]:
                kpis['last_month_same_day'] = sum(clean_number(row.get('LastMonthSaleSameDay', 0)) 
                                                for row in filtered_table)
            
            if 'MonthGP' in filtered_table[0]:
                kpis['total_gp'] = sum(clean_number(row.get('MonthGP', 0)) 
                                    for row in filtered_table)
            
            if 'MonthInvCount' in filtered_table[0]:
                kpis['total_invoices'] = sum(clean_number(row.get('MonthInvCount', 0)) 
                                            for row in filtered_table)
            
            if 'RetCount' in filtered_table[0]:
                kpis['total_returns'] = sum(clean_number(row.get('RetCount', 0)) 
                                            for row in filtered_table)
            
            if 'TotalQuantity' in filtered_table[0]:
                kpis['total_quantity'] = sum(clean_number(row.get('TotalQuantity', 0)) 
                                            for row in filtered_table)
            
            if 'LastMonthSale' in filtered_table[0]:
                kpis['last_month_sales'] = sum(clean_number(row.get('LastMonthSale', 0)) 
                                            for row in filtered_table)
            
            if kpis.get('total_sales') and kpis.get('total_gp'):
                kpis['gp_percentage'] = (kpis['total_gp'] / kpis['total_sales']) * 100
            
            if kpis.get('total_sales') and kpis.get('last_month_sales') and kpis['last_month_sales'] > 0:
                kpis['mom_growth'] = ((kpis['total_sales'] - kpis['last_month_sales']) / kpis['last_month_sales']) * 100
            
            if kpis.get('today_sale') and kpis.get('last_month_same_day') and kpis['last_month_same_day'] > 0:
                kpis['daily_growth'] = ((kpis['today_sale'] - kpis['last_month_same_day']) / kpis['last_month_same_day']) * 100
            
            if kpis.get('total_invoices') and kpis.get('total_sales'):
                kpis['avg_invoice_value'] = kpis['total_sales'] / kpis['total_invoices']
            
            if branch_col:
                kpis['active_branches'] = len(set(row.get(branch_col) 
                                                for row in filtered_table if row.get(branch_col)))
            
            logger.info(f"KPIs calculated: {kpis}")
            return kpis
            
        except Exception as e:
            logger.error(f"Error calculating KPIs: {str(e)}")
            return {}

    def _prepare_analysis_data(self):
        """Prepare comprehensive metadata for AI analysis"""
        data_summary = {
            'branch_performance': [],
            'channel_analysis': [],
            'category_breakdown': []
        }
        
        if len(self.all_tables_data) > 0:
            first_table = self.all_tables_data[0]['data']
            for row in first_table[:10]:
                data_summary['branch_performance'].append({
                    'branchtype': row.get('BranchType', 'N/A'),
                    'branch': row.get('Branch', 'N/A'),
                    'sales': clean_number(row.get('MonthSale', 0)),
                    'growth': clean_number(row.get('MonthPercNew', 0)),
                    'gp_margin': clean_number(row.get('MonthGPPer', 0))
                })
        
        if len(self.all_tables_data) > 1:
            second_table = self.all_tables_data[1]['data']
            for row in second_table:
                data_summary['channel_analysis'].append({
                    'channel': row.get('SaleType', 'N/A'),
                    'branch': row.get('Branch', 'N/A'),
                    'sales': clean_number(row.get('MonthAmount', 0)),
                    'growth': clean_number(row.get('MonthPercNew', 0))
                })
        
        if len(self.all_tables_data) > 3:
            fourth_table = self.all_tables_data[3]['data']
            for row in fourth_table[:8]:
                data_summary['category_breakdown'].append({
                    'category': row.get('Category', 'N/A'),
                    'sales': clean_number(row.get('MonthSale', 0)),
                    'share': clean_number(row.get('CategoryShareMonth', 0))
                })
        
        return data_summary
    
    def _build_analysis_workflow(self):
        def analyze_data(state: AnalysisState) -> AnalysisState:
            try:
                logger.info("Analyzing sales data with professional lens...")
                kpis = state['kpis']
                data_summary = self._prepare_analysis_data()
                
                analysis_prompt = f"""
                You are a professional data analyst with expertise in retail/restaurant business analytics. 
                Analyze the following sales metrics and provide 4 specific, actionable insights.
                
                KEY METRICS:
                - Total Sales: {kpis.get('total_sales', 0):,.0f}
                - Today's Sale: {kpis.get('today_sale', 0):,.0f}
                - Daily Growth: {kpis.get('daily_growth', 0):.1f}%
                - Month-over-Month Growth: {kpis.get('mom_growth', 0):.1f}%
                - Gross Profit Margin: {kpis.get('gp_percentage', 0):.1f}%
                - Average Invoice Value: {kpis.get('avg_invoice_value', 0):,.0f}
                - Total Invoices: {kpis.get('total_invoices', 0):,}
                - Active Branches: {kpis.get('active_branches', 0)}
                
                TOP PERFORMING BRANCHES:
                {json.dumps(data_summary.get('branch_performance', [])[:5], indent=2)}
                
                CHANNEL PERFORMANCE:
                {json.dumps(data_summary.get('channel_analysis', [])[:10], indent=2)}
                
                CATEGORY BREAKDOWN:
                {json.dumps(data_summary.get('category_breakdown', [])[:8], indent=2)}
                
                Provide exactly 4 insights:
                1. [Performance trend insight with % or value]
                2. [Channel or operational efficiency insight]
                3. [Growth opportunity or risk insight]
                4. [Actionable recommendation based on data]
                
                Keep each insight to 1-2 sentences. Use specific numbers. Use {self.currency_unit} for currency. for branch performance analyze retail shops and w.house seperately via branch type column
                """
                with open("top_performing_branches.txt", "w", encoding="utf-8") as f:
                    f.write(json.dumps(data_summary.get('branch_performance', [])[:5], indent=2))
                messages = [
                    SystemMessage(content="You are a professional business data analyst. Provide specific, data-driven insights."),
                    HumanMessage(content=analysis_prompt)
                ]
                
                response = self.llm.invoke(messages)
                insights_text = response.content.strip()
                
                insights = []
                for line in insights_text.split('\n'):
                    if line.strip() and any(line.startswith(str(i)) for i in range(1, 5)):
                        insight = line.lstrip('1234. ').strip()
                        if insight:
                            insights.append(insight)
                
                if len(insights) < 4:
                    insights = [
                        f"Sales increased {kpis.get('mom_growth', 0):.1f}% MoM, indicating positive market momentum",
                        f"Operating at {kpis.get('gp_percentage', 0):.1f}% gross margin with {kpis.get('active_branches', 0)} active branches",
                        "Multiple sales channels performing - analyze channel mix for revenue optimization",
                        "Focus on high-performing categories and underperforming segments for growth initiatives"
                    ]
                
                state['insights'] = insights[:4]
                
            except Exception as e:
                logger.error(f"Error in analysis: {str(e)}")
                state['insights'] = [
                    "Daily sales momentum building across channels",
                    "Gross profit margins stable with focused cost management",
                    "Branch network efficiency improving with transactions",
                    "Category diversification supporting revenue streams"
                ]
            
            return state
        
        workflow = StateGraph(AnalysisState)
        workflow.add_node("analyze", analyze_data)
        workflow.set_entry_point("analyze")
        workflow.add_edge("analyze", END)
        return workflow.compile()
    
    def generate_ai_insights(self, kpis):
        try:
            initial_state: AnalysisState = {
                'kpis': kpis,
                'all_tables': self.all_tables_data,
                'insights': [],
                'error': ''
            }
            
            final_state = self.analysis_workflow.invoke(initial_state)
            insights = final_state['insights']
            
            while len(insights) < 4:
                insights.append("Continue monitoring performance metrics for optimization")
            
            return insights[:4]
            
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return [
                "Monitor daily sales trends across channels",
                "Optimize receivables management",
                "Track customer acquisition metrics",
                "Analyze category performance"
            ]

    def save_full_report_html(self, html_content, report_id):
        """Save full report HTML to server for hosting"""
        try:
            html_filename = f'{report_id}.html'
            client_dir = (self.client_name or 'default').replace(" ", "")
            
            base_path = os.path.normpath(f"D:\\Technosys\\AI_service\\Email_services\\Chart_images_pngs\\Sales_Email_Service\\{client_dir}")
            os.makedirs(base_path, exist_ok=True)
            
            html_path = os.path.join(base_path, html_filename)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Full report saved as HTML: {html_path}")
            return html_filename
            
        except Exception as e:
            logger.error(f"Error saving full report as HTML: {str(e)}")
            return None
    
    def send_email(self, html_content, recipients, subject_title=None):
        """Send the email with the template"""
        try:
            if isinstance(recipients, str):
                recipients = [recipients]
            recipients = [email.strip() for email in (recipients or []) if email and email.strip()]
            if not recipients:
                raise ValueError("No valid recipients provided for email sending")

            msg = MIMEMultipart('alternative')
            msg['From'] = os.getenv('email_from', '')
            msg['To'] = ', '.join(recipients)
            display_title = subject_title if subject_title else self.report_title
            msg['Subject'] = f"{display_title} - {datetime.strptime(self.report_date, '%Y-%m-%d').strftime('%B %d, %Y')}"
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(os.getenv('smtp_server', ''), int(os.getenv('smtp_port', 25))) as server:
                if os.getenv('smtp_use_tls', 'True').lower() == 'true':
                    server.starttls()
                
                if os.getenv('smtp_user') and os.getenv('smtp_password'):
                    server.login(os.getenv('smtp_user'), os.getenv('smtp_password'))
                
                server.send_message(msg, to_addrs=recipients)
            
            logger.info(f"Email sent to {len(recipients)} recipients")
            return True
            
        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            return False
    def generate_and_send_report(self, specific_date=None, branch_ids='', recipients=None, is_branch=False):
        """Helper to generate and send a report (either company-wide or branch-specific)"""
        try:
            scope = f"Branch {branch_ids}" if is_branch else "General"
            logger.info(f"Processing {scope} report...")
            
            if not self.execute_sp(specific_date, branch_ids):
                logger.error(f"Failed to execute stored procedure for {scope}")
                return False
            
            kpis = self.calculate_kpis()
            if not kpis:
                kpis = {}
            
            insights = self.generate_ai_insights(kpis)
            
            # Generate chart data
            branch_chart_data = generate_branch_chart_data(self.all_tables_data, self._find_table_by_columns)
            channel_chart_data = generate_channel_chart_data(self.all_tables_data, self._find_table_by_columns)
            category_chart_data = generate_category_chart_data(self.all_tables_data, self._find_table_by_columns)
            
            # Prepare titles
            branch_display = ""
            if is_branch:
                branch_name = self._get_branch_name_from_data()
                branch_display = branch_name if branch_name else str(branch_ids)

            # 1. Template Title (for internal HTML report content)
            report_title = self.report_title
            if is_branch:
                report_title = f"{report_title} ({branch_display})"

            # 2. Email Subject Base (for the subject line)
            if is_branch:
                email_subject_base = f"{self.client_name} ({branch_display}): AI Generated Daily Sales Report"
            else:
                email_subject_base = f"{self.client_name} : AI Generated Daily Sales Report"

            # Generate and save full report HTML
            full_report_html = generate_full_report_template(
                self.report_date,
                self.report_time,
                kpis,
                insights,
                self.all_tables_data,
                self._find_table_by_columns,
                branch_chart_data,
                channel_chart_data,
                category_chart_data,
                dashboard_url=self.client_config.get('dashboard_url'),
                currency_unit=self.currency_unit,
                multi_category_enabled=self.client_config.get("multi_category", 0),
                second_category_table=self.second_category_table,
                report_title=report_title,
                visibility=self.client_config.get('visibility', {})
            )
            report_id = generate_report_id()
            full_report_filename = self.save_full_report_html(full_report_html, report_id)
            
            client_dir = (self.client_name or 'default').replace(" ", "")
            # Generate full report URL
            base_url = f"https://salesanalytics.technosyserp.com/Sales_Email_Service/{client_dir}"
            full_report_url = f"{base_url}/{full_report_filename}" if full_report_filename else "#"
            
            try:
                datetime_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log_status = "Success" if full_report_filename else "Failed to save HTML"
                log_report(report_id, self.client_name or 'default', datetime_str, log_status)
            except Exception as e:
                logger.error(f"Failed to log to reports.csv: {e}")
            
            # Generate concise email (KPIs + Insights + Button to full report)
            concise_email_html = generate_concise_email_template(
                self.report_date,
                self.report_time,
                kpis,
                insights,
                full_report_url,
                dashboard_url=self.client_config.get('dashboard_url'),
                currency_unit=self.currency_unit,
                report_title=report_title
            )
            
            if not recipients:
                recipients = self.config.get('default_recipients', [])
            
            if not recipients:
                logger.error(f"No recipients specified for {scope} report")
                return False
            
            if self.send_email(concise_email_html, recipients, subject_title=email_subject_base):
                logger.info(f"{scope} report email generated and sent successfully to {len(recipients)} recipients")
                return True
            else:
                logger.error(f"Failed to send {scope} email")
                return False
                
        except Exception as e:
            logger.error(f"Error generating/sending {scope} report: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    def run(self, specific_date=None):
        """Main execution method - handles general report and branch-level reports"""
        try:
            logger.info(f"==================================================")
            logger.info(f"STARTING SALES REPORT AUTOMATION: {self.client_name}")
            logger.info(f"==================================================")
            
            # Step 1: General Company Report
            logger.info("PHASE 1: Generating General Company Report")
            general_recipients = self.config.get('default_recipients', [])
            self.generate_and_send_report(
                specific_date=specific_date,
                branch_ids='', 
                recipients=general_recipients,
                is_branch=False
            )
            
            # Step 2: Branch-Level Reports
            branch_configs = self.config.get('company_branches', [])
            if branch_configs:
                logger.info(f"PHASE 2: Generating {len(branch_configs)} Branch-Level Reports")
                for branch in branch_configs:
                    branch_id = str(branch.get('CompanyBranchId'))
                    branch_recipients = branch.get('recipients', [])
                    
                    if not branch_recipients:
                        logger.warning(f"Skipping Branch {branch_id}: No recipients configured")
                        continue
                    
                    logger.info(f"--- Processing Branch ID: {branch_id} ---")
                    self.generate_and_send_report(
                        specific_date=specific_date,
                        branch_ids=branch_id,
                        recipients=branch_recipients,
                        is_branch=True
                    )
            else:
                logger.info("PHASE 2: No branch-level reports configured")
                
            logger.info(f"==================================================")
            logger.info(f"COMPLETED ALL REPORTS FOR: {self.client_name}")
            logger.info(f"==================================================")
            return True
                
        except Exception as e:
            logger.error(f"Critical error in execution run: {str(e)}")
            return False
        finally:
            if self.db_connection:
                try:
                    self.db_connection.close()
                    logger.info("Database connection closed")
                except:
                    pass
