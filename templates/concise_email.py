"""
Concise Email Template - Gmail-safe, matches full report design
KPIs + AI Insights + View Full Report Button
"""

from datetime import datetime, timedelta
import json
from utils import format_value, format_time_for_display, md_to_html


# Icon URLs - hosted on your server
ICON_URLS = {
    'total_sales': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon(5).png',
    'today_sale': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon.png',
    'mom_growth': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon(1).png',
    'gross_profit': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon(4).png',
    'avg_invoice': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon(3).png',
    'total_invoices': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon(2).png',
    'insights_header': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon(6).png',
    'performance': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon(7).png',
    'channel': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon(8).png',
    'growth': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon(9).png',
    'strategic': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon(10).png',
}


def generate_concise_email_template(report_date, report_time, kpis, insights, full_report_url, dashboard_url=None, currency_unit='PKR', report_title='Daily Sales Report'):
    """Generate concise email template with KPIs and AI Insights only - Gmail safe"""
    
    def load_config_from_json(config_path='config.json'):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)   
            return config
        except Exception as e:
            raise
    current_date = datetime.strptime(report_date, '%Y-%m-%d')
    previous_date = current_date - timedelta(days=1)
    display_time = format_time_for_display(report_time)
    date_range_str = f"({previous_date.strftime('%B %d')}, {display_time} - {current_date.strftime('%B %d')}, {display_time})"
    config = load_config_from_json()
    formatted_footer_date = current_date.strftime('%A %d %B %Y')
    
    mom_growth = kpis.get('mom_growth', 0)
    mom_color = '#10B981' if mom_growth >= 0 else '#EF4444'
    mom_icon = '↑' if mom_growth >= 0 else '↓'
    mom_badge_bg = '#A4F4CF' if mom_growth >= 0 else '#FFC9C9'
    mom_badge_color = '#007A55' if mom_growth >= 0 else '#C10007'
    
    # Format KPI values
    total_sales = format_value(kpis.get('total_sales', 0), 'sale')[0]
    today_sale = format_value(kpis.get('today_sale', 0), 'sale')[0]
    total_gp = format_value(kpis.get('total_gp', 0), 'gp')[0]
    avg_invoice = format_value(kpis.get('avg_invoice_value', 0), 'avg_invoice_value')[0]
    total_invoices = format_value(kpis.get('total_invoices', 0), 'count')[0]
    
    # Format insights
    insight_1 = md_to_html(insights[0]) if len(insights) > 0 else ''
    insight_2 = md_to_html(insights[1]) if len(insights) > 1 else ''
    insight_3 = md_to_html(insights[2]) if len(insights) > 2 else ''
    insight_4 = md_to_html(insights[3]) if len(insights) > 3 else ''
    
    # Generate KPI cards
    kpi_cards_desktop = _generate_kpi_section_desktop(total_sales, today_sale, mom_growth, mom_color, total_gp, avg_invoice, total_invoices)
    kpi_cards_mobile = _generate_kpi_section_mobile(total_sales, today_sale, mom_growth, mom_color, total_gp, avg_invoice, total_invoices)
    
    # Generate insight cards
    insight_cards_desktop = _generate_insights_section_desktop(total_sales, mom_growth, mom_icon, mom_badge_bg, mom_badge_color, insight_1, insight_2, insight_3, insight_4, currency_unit=currency_unit)
    insight_cards_mobile = _generate_insights_section_mobile(total_sales, mom_growth, mom_icon, mom_badge_bg, mom_badge_color, insight_1, insight_2, insight_3, insight_4, currency_unit=currency_unit)
    
    html_template = f"""
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="x-apple-disable-message-reformatting">
    <meta name="color-scheme" content="light">
    <meta name="supported-color-schemes" content="light">
    <title>{report_title}</title>
    <!--[if mso]>
    <noscript>
        <xml>
            <o:OfficeDocumentSettings>
                <o:AllowPNG/>
                <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
        </xml>
    </noscript>
    <![endif]-->
    <style type="text/css">
        body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
        table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
        img {{ -ms-interpolation-mode: bicubic; border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }}
        body {{ height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }}
        
        @media screen and (max-width: 600px) {{
            .wrapper {{ width: 100% !important; max-width: 100% !important; }}
            .mobile-padding {{ padding: 16px !important; }}
            .mobile-padding-header {{ padding: 32px 20px !important; }}
            .mobile-hide {{ display: none !important; }}
            .mobile-show {{ display: block !important; }}
            .header-title {{ font-size: 24px !important; }}
        }}
    </style>
</head>
<body style="margin: 0; padding: 0; background-color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
    
        {report_title}: Total Sales {total_sales} | MoM Growth {mom_growth:.1f}%
    
    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f1f5f9;">
        <tr>
            <td align="center" style="padding: 20px 10px;">
                
                <table role="presentation" class="wrapper" cellpadding="0" cellspacing="0" width="600" style="max-width: 600px; background-color: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12);">
                    
                    <!-- Header -->
                    <tr>
                        <td class="mobile-padding-header" style="background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #9333EA 100%); padding: 48px 32px; text-align: center;">
                            <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="center">
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center">
                                        <h1 class="header-title" style="margin: 0 0 8px; font-size: 32px; font-weight: 700; color: #ffffff; letter-spacing: -0.5px;">{report_title}</h1>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center">
                                        <p style="margin: 0; font-size: 14px; color: rgba(255,255,255,0.9); font-weight: 500;">{date_range_str}</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- KPI Section -->
                    <tr>
                        <td class="mobile-padding" style="padding: 32px; background-color: #f8fafc;">
                            <!-- Desktop Grid -->
                            <div class="mobile-hide">
                                {kpi_cards_desktop}
                            </div>
                            <!-- Mobile Stacked -->
                            <div class="mobile-show" style="display: none;">
                                {kpi_cards_mobile}
                            </div>
                        </td>
                    </tr>
                    
                    <!-- AI Insights Section -->
                    <tr>
                        <td class="mobile-padding" style="padding: 0 32px 32px; background-color: #f8fafc;">
                            
                            <!-- Insights Wrapper -->
                            <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background: linear-gradient(135deg, #FEF9E7 0%, #FEF3C7 100%); border-radius: 12px; overflow: hidden;">
                                
                                <!-- Insights Header -->
                                <tr>
                                    <td style="padding: 16px 20px; border-bottom: 1px solid rgba(245, 158, 11, 0.2);">
                                        <table role="presentation" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td style="padding-right: 10px; vertical-align: middle;">
                                                    <img src="{ICON_URLS['insights_header']}" alt="Insights" width="22" height="22" style="display: block;">
                                                </td>
                                                <td style="vertical-align: middle;">
                                                    <p style="margin: 0; font-size: 18px; font-weight: 400; color: #1D293D;">Professional Analysis & Insights</p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                
                                <!-- Insights Content -->
                                <tr>
                                    <td style="padding: 20px; background-color: #FFFFFF;">
                                        <!-- Desktop Grid -->
                                        <div class="mobile-hide">
                                            {insight_cards_desktop}
                                        </div>
                                        <!-- Mobile Stacked -->
                                        <div class="mobile-show" style="display: none;">
                                            {insight_cards_mobile}
                                        </div>
                                    </td>
                                </tr>
                            </table>
                            
                        </td>
                    </tr>
                    
                    <!-- View Full Report Button -->
                    <tr>
                        <td style="padding: 0 32px 32px; background-color: #f8fafc;" align="center">
                            <table role="presentation" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); border-radius: 12px; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);">
                                        <a href="{full_report_url}" target="_blank" style="display: inline-block; padding: 16px 40px; font-size: 16px; font-weight: 600; color: #ffffff; text-decoration: none; letter-spacing: 0.3px;">
                                            📊 View Full Report with Charts & Tables
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8fafc; padding: 24px 32px; text-align: center; border-top: 1px solid #E2E8F0;">
                            <p style="margin: 0 0 4px; font-size: 12px; color: #64748B;"><strong>Generated:</strong> {formatted_footer_date}</p>
                            <p style="margin: 0 0 4px; font-size: 11px; color: #DC2626;"><strong>Disclaimer:</strong> Data availability subject to server connectivity and branch replication status.</p>
                            <p style="margin: 0; font-size: 12px; color: #64748B;">AI-Powered Sales Analytics | Professional Data Analysis{f" | <a href='{dashboard_url}' style='color: #4F46E5; text-decoration: none; font-weight: 700;' target='_blank'>View Interactive Dashboard</a>" if dashboard_url else ""}</p>
                        </td>
                    </tr>
                    
                </table>
                
            </td>
        </tr>
    </table>
    
</body>
</html>
    """
    
    return html_template


def _generate_kpi_card(icon_url, icon_bg, label, sublabel, value, value_color):
    """Generate a single KPI card"""
    return f"""
        <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff; border: 2px solid #e2e8f0; border-radius: 12px;">
            <tr>
                <td style="padding: 16px;">
                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td width="32" style="vertical-align: middle;">
                                <div style="width: 32px; height: 32px; background-color: {icon_bg}; border-radius: 50%; text-align: center; line-height: 32px;">
                                    <img src="{icon_url}" alt="" width="16" height="16" style="display: inline-block; vertical-align: middle;">
                                </div>
                            </td>
                            <td style="padding-left: 12px; vertical-align: middle;">
                                <p style="margin: 0; font-size: 14px; font-weight: 400; color: #0f172b;">{label}</p>
                                <p style="margin: 2px 0 0; font-size: 12px; color: #62748E; text-transform: uppercase; letter-spacing: 0.3px; font-weight: 400;">{sublabel}</p>
                            </td>
                            <td style="text-align: right; vertical-align: middle;">
                                <p style="margin: 0; font-size: 24px; font-weight: 400; color: {value_color};">{value}</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    """


def _generate_kpi_section_desktop(total_sales, today_sale, mom_growth, mom_color, total_gp, avg_invoice, total_invoices):
    """Generate desktop KPI grid (3x2)"""
    return f"""
        <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td width="33.33%" style="padding: 8px;">
                    {_generate_kpi_card(ICON_URLS['total_sales'], '#EFF6FF', 'Total Sales', 'MONTH TO DATE', total_sales, '#0f172b')}
                </td>
                <td width="33.33%" style="padding: 8px;">
                    {_generate_kpi_card(ICON_URLS['today_sale'], '#EEF2FF', "Today's Sale", 'DAILY PERFORMANCE', today_sale, '#0f172b')}
                </td>
                <td width="33.33%" style="padding: 8px;">
                    {_generate_kpi_card(ICON_URLS['mom_growth'], '#F5F3FF', 'MoM Growth', 'GROWTH TREND', f"{mom_growth:.1f}%", mom_color)}
                </td>
            </tr>
            <tr>
                <td width="33.33%" style="padding: 8px;">
                    {_generate_kpi_card(ICON_URLS['gross_profit'], '#ECFEFF', 'Gross Profit', 'TOTAL MARGIN', total_gp, '#0f172b')}
                </td>
                <td width="33.33%" style="padding: 8px;">
                    {_generate_kpi_card(ICON_URLS['avg_invoice'], '#FAF5FF', 'Avg Invoice Value', 'PER TRANSACTION', avg_invoice, '#0f172b')}
                </td>
                <td width="33.33%" style="padding: 8px;">
                    {_generate_kpi_card(ICON_URLS['total_invoices'], '#EFF6FF', 'Total Invoices', 'MTD TRANSACTIONS', total_invoices, '#0f172b')}
                </td>
            </tr>
        </table>
    """


def _generate_kpi_section_mobile(total_sales, today_sale, mom_growth, mom_color, total_gp, avg_invoice, total_invoices):
    """Generate mobile KPI stack"""
    return f"""
        {_generate_kpi_card_mobile(ICON_URLS['total_sales'], '#EFF6FF', 'Total Sales', 'MONTH TO DATE', total_sales, '#0f172b')}
        {_generate_kpi_card_mobile(ICON_URLS['today_sale'], '#EEF2FF', "Today's Sale", 'DAILY PERFORMANCE', today_sale, '#0f172b')}
        {_generate_kpi_card_mobile(ICON_URLS['mom_growth'], '#F5F3FF', 'MoM Growth', 'GROWTH TREND', f"{mom_growth:.1f}%", mom_color)}
        {_generate_kpi_card_mobile(ICON_URLS['gross_profit'], '#ECFEFF', 'Gross Profit', 'TOTAL MARGIN', total_gp, '#0f172b')}
        {_generate_kpi_card_mobile(ICON_URLS['avg_invoice'], '#FAF5FF', 'Avg Invoice Value', 'PER TRANSACTION', avg_invoice, '#0f172b')}
        {_generate_kpi_card_mobile(ICON_URLS['total_invoices'], '#EFF6FF', 'Total Invoices', 'MTD TRANSACTIONS', total_invoices, '#0f172b')}
    """


def _generate_kpi_card_mobile(icon_url, icon_bg, label, sublabel, value, value_color):
    """Generate a mobile KPI card"""
    return f"""
        <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff; border: 2px solid #e2e8f0; border-radius: 12px; margin-bottom: 12px;">
            <tr>
                <td style="padding: 14px;">
                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td width="32" style="vertical-align: middle;">
                                <div style="width: 32px; height: 32px; background-color: {icon_bg}; border-radius: 50%; text-align: center; line-height: 32px;">
                                    <img src="{icon_url}" alt="" width="16" height="16" style="display: inline-block; vertical-align: middle;">
                                </div>
                            </td>
                            <td style="padding-left: 12px; vertical-align: middle;">
                                <p style="margin: 0; font-size: 14px; font-weight: 400; color: #0f172b;">{label}</p>
                                <p style="margin: 2px 0 0; font-size: 12px; color: #62748E; text-transform: uppercase; letter-spacing: 0.3px;">{sublabel}</p>
                            </td>
                            <td style="text-align: right; vertical-align: middle;">
                                <p style="margin: 0; font-size: 20px; font-weight: 400; color: {value_color};">{value}</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    """


# def _generate_insight_card(icon_url, title, subtitle, badge_text, badge_bg, badge_color, metric1='', metric2='', insight_text=''):
#     """Generate a single insight card"""
    
#     metrics_html = ''
#     if metric1 or metric2:
#         metrics_html = f"""
#             <tr>
#                 <td style="padding: 12px 0;">
#                     {'<p style="margin: 0 0 4px; font-size: 12px; color: #64748B;">' + metric1 + '</p>' if metric1 else ''}
#                     {'<p style="margin: 0; font-size: 12px; color: #64748B;">' + metric2 + '</p>' if metric2 else ''}
#                 </td>
#             </tr>
#         """
    
#     return f"""
#         <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff; border-radius: 10px; border: 1px solid #ddd6ff; box-shadow: 0px 1px 2px -1px rgba(0, 0, 0, 0.1), 0px 1px 3px 0px rgba(0, 0, 0, 0.1);">
#             <tr>
#                 <td style="padding: 20px 24px;">
#                     <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
#                         <tr>
#                             <td>
#                                 <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
#                                     <tr>
#                                         <td width="40" style="vertical-align: top;">
#                                             <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #615FFF 0%, #4F39F6 100%); border-radius: 10px; text-align: center; line-height: 40px; box-shadow: 0px 1px 2px -1px rgba(0, 0, 0, 0.1), 0px 1px 3px 0px rgba(0, 0, 0, 0.1);">
#                                                 <img src="{icon_url}" alt="" width="20" height="20" style="display: inline-block; vertical-align: middle;">
#                                             </div>
#                                         </td>
#                                         <td style="padding-left: 10px; vertical-align: middle;">
#                                             <p style="margin: 0; font-size: 16px; font-weight: 400; color: #0F172B;">{title}</p>
#                                             <p style="margin: 0; font-size: 12px; font-weight: 400; color: #45556C;">{subtitle}</p>
#                                         </td>
#                                         <td style="text-align: right; vertical-align: top;">
#                                             <span style="display: inline-block; background-color: {badge_bg}; color: {badge_color}; font-size: 10px; font-weight: 400; padding: 4px 10px; border-radius: 8px; text-transform: uppercase; letter-spacing: 0.25px;">{badge_text}</span>
#                                         </td>
#                                     </tr>
#                                 </table>
#                             </td>
#                         </tr>
#                         {metrics_html}
#                         <tr>
#                             <td style="padding-top: 12px; border-top: 1px solid #E2E8F0;">
#                                 <p style="margin: 0; font-size: 12px; color: #45556C; line-height: 1.6;"><strong style="color: #475569;">Insight:</strong> {insight_text}</p>
#                             </td>
#                         </tr>
#                     </table>
#                 </td>
#             </tr>
#         </table>
#     """


# def _generate_insights_section_desktop(total_sales, mom_growth, mom_icon, mom_badge_bg, mom_badge_color, insight_1, insight_2, insight_3, insight_4):
#     """Generate desktop insights grid (2x2)"""
#     return f"""
#         <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
#             <tr>
#                 <td width="50%" style="padding: 8px; vertical-align: top;">
#                     {_generate_insight_card(ICON_URLS['performance'], 'Performance', 'Trend Analysis', 'CRITICAL', '#FFC9C9', '#C10007', 
#                         f'Total Revenue: <strong style="color: #1E293B;">PKR {total_sales}</strong>', 
#                         f'MoM Growth: <span style="display: inline-block; background-color: {mom_badge_bg}; color: {mom_badge_color}; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 6px;">{mom_icon} {mom_growth:.1f}%</span>',
#                         insight_1)}
#                 </td>
#                 <td width="50%" style="padding: 8px; vertical-align: top;">
#                     {_generate_insight_card(ICON_URLS['channel'], 'Channel', 'Performance', 'INSIGHT', '#DDD6FF', '#7008E7', '', '', insight_2)}
#                 </td>
#             </tr>
#             <tr>
#                 <td width="50%" style="padding: 8px; vertical-align: top;">
#                     {_generate_insight_card(ICON_URLS['growth'], 'Growth', 'Opportunity', 'OPPORTUNITY', '#A4F4CF', '#007A55', '', '', insight_3)}
#                 </td>
#                 <td width="50%" style="padding: 8px; vertical-align: top;">
#                     {_generate_insight_card(ICON_URLS['strategic'], 'Strategic', 'Recommendations', 'ACTION REQUIRED', '#F1F5F9', '#314158', '', '', insight_4)}
#                 </td>
#             </tr>
#         </table>
#     """
def _generate_insights_section_desktop(total_sales, mom_growth, mom_icon, mom_badge_bg, mom_badge_color, insight_1, insight_2, insight_3, insight_4, currency_unit='PKR'):
    """Generate desktop insights grid (2x2) with equal height cards"""
    return f"""
        <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td width="50%" style="padding: 8px; vertical-align: top;">
                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" height="100%">
                        <tr>
                            <td height="100%">
                                {_generate_insight_card(ICON_URLS['performance'], 'Performance', 'Trend Analysis', 'CRITICAL', '#FFC9C9', '#C10007', 
                                    f'Total Revenue: <strong style="color: #1E293B;">{currency_unit} {total_sales}</strong>', 
                                    f'MoM Growth: <span style="display: inline-block; background-color: {mom_badge_bg}; color: {mom_badge_color}; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 6px;">{mom_icon} {mom_growth:.1f}%</span>',
                                    insight_1)}
                            </td>
                        </tr>
                    </table>
                </td>
                <td width="50%" style="padding: 8px; vertical-align: top;">
                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" height="100%">
                        <tr>
                            <td height="100%">
                                {_generate_insight_card(ICON_URLS['channel'], 'Channel', 'Performance', 'INSIGHT', '#DDD6FF', '#7008E7', '', '', insight_2)}
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td width="50%" style="padding: 8px; vertical-align: top;">
                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" height="100%">
                        <tr>
                            <td height="100%">
                                {_generate_insight_card(ICON_URLS['growth'], 'Growth', 'Opportunity', 'OPPORTUNITY', '#A4F4CF', '#007A55', '', '', insight_3)}
                            </td>
                        </tr>
                    </table>
                </td>
                <td width="50%" style="padding: 8px; vertical-align: top;">
                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" height="100%">
                        <tr>
                            <td height="100%">
                                {_generate_insight_card(ICON_URLS['strategic'], 'Strategic', 'Recommendations', 'ACTION REQUIRED', '#F1F5F9', '#314158', '', '', insight_4)}
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    """


def _generate_insight_card(icon_url, title, subtitle, badge_text, badge_bg, badge_color, metric1='', metric2='', insight_text=''):
    """Generate a single insight card with flexible height"""
    
    metrics_html = ''
    if metric1 or metric2:
        metrics_html = f"""
            <tr>
                <td style="padding: 12px 0;">
                    {'<p style="margin: 0 0 4px; font-size: 12px; color: #64748B;">' + metric1 + '</p>' if metric1 else ''}
                    {'<p style="margin: 0; font-size: 12px; color: #64748B;">' + metric2 + '</p>' if metric2 else ''}
                </td>
            </tr>
        """
    
    return f"""
        <table role="presentation" cellpadding="0" cellspacing="0" width="100%" height="100%" style="background-color: #ffffff; border-radius: 10px; border: 1px solid #ddd6ff; box-shadow: 0px 1px 2px -1px rgba(0, 0, 0, 0.1), 0px 1px 3px 0px rgba(0, 0, 0, 0.1);">
            <tr>
                <td style="padding: 20px 24px;" height="100%">
                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" height="100%">
                        <tr>
                            <td>
                                <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                        <td width="40" style="vertical-align: top;">
                                            <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #615FFF 0%, #4F39F6 100%); border-radius: 10px; text-align: center; line-height: 40px; box-shadow: 0px 1px 2px -1px rgba(0, 0, 0, 0.1), 0px 1px 3px 0px rgba(0, 0, 0, 0.1);">
                                                <img src="{icon_url}" alt="" width="20" height="20" style="display: inline-block; vertical-align: middle;">
                                            </div>
                                        </td>
                                        <td style="padding-left: 10px; vertical-align: middle;">
                                            <p style="margin: 0; font-size: 16px; font-weight: 400; color: #0F172B;">{title}</p>
                                            <p style="margin: 0; font-size: 12px; font-weight: 400; color: #45556C;">{subtitle}</p>
                                        </td>
                                        <td style="text-align: right; vertical-align: top;">
                                            <span style="display: inline-block; background-color: {badge_bg}; color: {badge_color}; font-size: 10px; font-weight: 400; padding: 4px 10px; border-radius: 8px; text-transform: uppercase; letter-spacing: 0.25px;">{badge_text}</span>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        {metrics_html}
                        <tr>
                            <td style="padding-top: 12px; border-top: 1px solid #E2E8F0;">
                                <p style="margin: 0; font-size: 12px; color: #45556C; line-height: 1.6;"><strong style="color: #475569;">Insight:</strong> {insight_text}</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    """

def _generate_insights_section_mobile(total_sales, mom_growth, mom_icon, mom_badge_bg, mom_badge_color, insight_1, insight_2, insight_3, insight_4, currency_unit='PKR'):
    """Generate mobile insights stack"""
    return f"""
        <div style="margin-bottom: 16px;">
            {_generate_insight_card(ICON_URLS['performance'], 'Performance', 'Trend Analysis', 'CRITICAL', '#FFC9C9', '#C10007', 
                f'Total Revenue: <strong style="color: #1E293B;">{currency_unit} {total_sales}</strong>', 
                f'MoM Growth: <span style="display: inline-block; background-color: {mom_badge_bg}; color: {mom_badge_color}; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 6px;">{mom_icon} {mom_growth:.1f}%</span>',
                insight_1)}
        </div>
        <div style="margin-bottom: 16px;">
            {_generate_insight_card(ICON_URLS['channel'], 'Channel', 'Performance', 'INSIGHT', '#DDD6FF', '#7008E7', '', '', insight_2)}
        </div>
        <div style="margin-bottom: 16px;">
            {_generate_insight_card(ICON_URLS['growth'], 'Growth', 'Opportunity', 'OPPORTUNITY', '#A4F4CF', '#007A55', '', '', insight_3)}
        </div>
        <div>
            {_generate_insight_card(ICON_URLS['strategic'], 'Strategic', 'Recommendations', 'ACTION REQUIRED', '#F1F5F9', '#314158', '', '', insight_4)}
        </div>
    """
