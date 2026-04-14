"""
Full Report Template - HTML Generation
"""

from datetime import datetime, timedelta
from utils import format_value, format_time_for_display, md_to_html, get_trend_indicator, calculate_daily_growth, calculate_table_totals
from config import TableConfig
from .full_report_styles import get_full_report_styles


def generate_table_html_desktop(table_data, all_columns, table_config, table_index, format_value_func, get_trend_func, calc_growth_func, calc_totals_func):
    """Generate HTML table for DESKTOP view"""
    
    if table_index == 0 and 'Total' in all_columns:
        table_data = sorted(
            table_data,
            key=lambda x: (
                str(x.get('Branch', '')).strip().lower() == 'sub total',
                -float(x.get('Total') or 0)
            )
        )

    display_cols = [col for col in table_config['columns'] if col in all_columns]
    
    if not display_cols or not table_data:
        return ""
    
    headers_html = ""
    for col in display_cols:
        display_name = table_config['display_names'].get(col, col)
        headers_html += f'<th class="table-header">{display_name}</th>'
    
    if table_index == 0 and 'Total' in display_cols and 'LastMonthSaleSameDay' in display_cols:
        headers_html += '<th class="table-header">Daily Growth %</th>'

    rows_html = ""
    for idx, row in enumerate(table_data):
        branch_name = str(row.get("Branch", "")).strip().lower()
        is_subtotal = branch_name == "sub total"
        
        row_class = "subtotal-row" if is_subtotal else ("even-row" if idx % 2 == 0 else "odd-row")
        
        rows_html += f'<tr class="{row_class}">'
        
        for col in display_cols:
            value = row.get(col)
            formatted, color_class = format_value_func(value, col)
            trend = get_trend_func(col, value)
            
            cell_class = f"table-cell {color_class}"
            rows_html += f'<td class="{cell_class}">{formatted}{trend}</td>'
        
        if table_index == 0 and 'Total' in display_cols and 'LastMonthSaleSameDay' in display_cols:
            growth_pct, growth_color = calc_growth_func(row.get('Total'), row.get('LastMonthSaleSameDay'))
            trend_icon = '↑' if growth_pct > 0 else ('↓' if growth_pct < 0 else '')
            cell_class = f"table-cell {growth_color}"
            rows_html += f'<td class="{cell_class}">{growth_pct:.2f}%{trend_icon}</td>'
        
        rows_html += "</tr>"
    
    totals = calc_totals_func(table_data, all_columns, table_config)
    totals_html = '<tr class="totals-row">'
    
    for idx, col in enumerate(display_cols):
        if col in totals:
            formatted, _ = format_value_func(totals[col], col)
            totals_html += f'<td class="table-cell totals-cell"><strong>{formatted}</strong></td>'
        else:
            if idx == 0:
                totals_html += '<td class="table-cell totals-cell"><strong>Total</strong></td>'
            else:
                totals_html += '<td class="table-cell totals-cell"></td>'
    
    if table_index == 0 and 'Total' in totals and 'LastMonthSaleSameDay' in totals:
        growth_pct, _ = calc_growth_func(totals.get('Total'), totals.get('LastMonthSaleSameDay'))
        trend = '↑' if growth_pct > 0 else ('↓' if growth_pct < 0 else '')
        totals_html += f'<td class="table-cell totals-cell"><strong>{growth_pct:.2f}%{trend}</strong></td>'
    
    totals_html += "</tr>"
    
    return f"""
        <table class="data-table">
            <thead>
                <tr>{headers_html}</tr>
            </thead>
            <tbody>
                {rows_html}
                {totals_html}
            </tbody>
        </table>
    """


def generate_table_html_mobile(table_data, all_columns, table_config, table_index, format_value_func):
    """Generate HTML table for MOBILE view - Card-based layout"""
    
    if table_index == 0 and 'Total' in all_columns:
        table_data = sorted(
            table_data,
            key=lambda x: (
                str(x.get('Branch', '')).strip().lower() == 'sub total',
                -float(x.get('Total') or 0)
            )
        )

    display_cols = [col for col in table_config['columns'] if col in all_columns]
    
    if not display_cols or not table_data:
        return ""
    
    if table_index == 0:
        cards_html = ""
        for row in table_data:
            branch_name = str(row.get("Branch", "")).strip()
            if branch_name.lower() == "sub total":
                continue
            
            branch_type = row.get("BranchType", "")
            mom_pct = format_value_func(row.get('MonthPercNew', 0), 'perc')[0]
            gp_pct = format_value_func(row.get('MonthGPPer', 0), 'perc')[0]
            
            mom_val = float(row.get('MonthPercNew', 0) or 0)
            gp_val = float(row.get('MonthGPPer', 0) or 0)
            
            mom_class = 'badge-positive' if mom_val >= 0 else 'badge-negative'
            gp_class = 'badge-positive' if gp_val >= 100 else 'badge-info'
            
            cards_html += f"""
            <div class="mobile-card">
                <div class="mobile-card-header">
                    <div>
                        <h3 class="mobile-card-title">{branch_name}</h3>
                        <p class="mobile-card-subtitle">{branch_type}</p>
                    </div>
                    <div class="mobile-card-badges">
                        <span class="badge {mom_class}">MoM {mom_pct}</span>
                        <span class="badge badge-outline {gp_class}">GP {gp_pct}</span>
                    </div>
                </div>
                <div class="mobile-card-grid">
                    <div class="mobile-card-metric">
                        <span class="metric-label">TODAY SALE</span>
                        <span class="metric-value">{format_value_func(row.get('Total', 0), 'sale')[0]}</span>
                    </div>
                    <div class="mobile-card-metric">
                        <span class="metric-label">SAME DAY LAST MONTH</span>
                        <span class="metric-value">{format_value_func(row.get('LastMonthSaleSameDay', 0), 'sale')[0]}</span>
                    </div>
                    <div class="mobile-card-metric">
                        <span class="metric-label">MTD SALE</span>
                        <span class="metric-value">{format_value_func(row.get('MonthSale', 0), 'sale')[0]}</span>
                    </div>
                    <div class="mobile-card-metric">
                        <span class="metric-label">LAST MTD SALE</span>
                        <span class="metric-value">{format_value_func(row.get('LastMonthSale', 0), 'sale')[0]}</span>
                    </div>
                    <div class="mobile-card-metric">
                        <span class="metric-label">DAILY AVG SALE</span>
                        <span class="metric-value">{format_value_func(row.get('AverageSale', 0), 'sale')[0]}</span>
                    </div>
                    <div class="mobile-card-metric">
                        <span class="metric-label">GROSS PROFIT</span>
                        <span class="metric-value">{format_value_func(row.get('MonthGP', 0), 'gp')[0]}</span>
                    </div>
                </div>
            </div>
            """
        
        return cards_html
    
    # Generic card layout for other tables
    cards_html = ""
    for row in table_data:
        first_col = display_cols[0]
        title = str(row.get(first_col, 'N/A'))
        
        metrics_html = ""
        for col in display_cols[1:]:
            display_name = table_config['display_names'].get(col, col)
            formatted, color_class = format_value_func(row.get(col), col)
            
            value_class = 'metric-value'
            if color_class == 'positive':
                value_class += ' style="color: #10B981;"'
            elif color_class == 'negative':
                value_class += ' style="color: #EF4444;"'
            
            metrics_html += f"""
            <div class="mobile-card-metric">
                <span class="metric-label">{display_name}</span>
                <span class="{value_class}">{formatted}</span>
            </div>
            """
        
        cards_html += f"""
        <div class="mobile-card">
            <div class="mobile-card-header">
                <h3 class="mobile-card-title">{title}</h3>
            </div>
            <div class="mobile-card-grid">
                {metrics_html}
            </div>
        </div>
        """
    
    return cards_html


def generate_kpi_section(kpis, format_value_func):
    """Generate the KPI cards section"""
    
    mom_growth = kpis.get('mom_growth', 0)
    mom_class = 'positive' if mom_growth >= 0 else 'negative'
    mom_icon_bg = 'kpi-icon-green' if mom_growth >= 0 else 'kpi-icon-red'

    ICON_URLS = {
    'total_sales': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon (5).svg',
    'today_sale': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon.svg',
    'mom_growth': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon (1).svg',
    'gross_profit': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon (4).svg',
    'avg_invoice': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon (3).svg',
    'total_invoices': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon (2).svg',
    'insights_header': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon (6).svg',
    'performance': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon (7).svg',
    'channel': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon (8).svg',
    'growth': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon (9).svg',
    'strategic': 'https://salesanalytics.technosyserp.com/united_king_bakery/icon (10).svg',
}

    
    kpi_configs = [
        ('<img src="https://salesanalytics.technosyserp.com/united_king_bakery/icon (5).svg" alt="Cart" class="kpi-icon-img">', 'kpi-icon-blue', 'Total Sales', 'MONTH TO DATE', format_value_func(kpis.get('total_sales', 0), 'sale')[0], ''),
        ('<img src="https://salesanalytics.technosyserp.com/united_king_bakery/icon.svg" alt="Cart" class="kpi-icon-img">', 'kpi-icon-purple', "Today's Sale", 'DAILY PERFORMANCE', format_value_func(kpis.get('today_sale', 0), 'sale')[0], ''),
        ('<img src="https://salesanalytics.technosyserp.com/united_king_bakery/icon (1).svg" alt="Cart" class="kpi-icon-img">', mom_icon_bg, 'MoM Growth', 'GROWTH TREND', f"{mom_growth:.1f}%", mom_class),
        ('<img src="https://salesanalytics.technosyserp.com/united_king_bakery/icon (4).svg" alt="Cart" class="kpi-icon-img">', 'kpi-icon-green', 'Gross Profit', 'TOTAL MARGIN', format_value_func(kpis.get('total_gp', 0), 'gp')[0], ''),
        ('<img src="https://salesanalytics.technosyserp.com/united_king_bakery/icon (3).svg" alt="Cart" class="kpi-icon-img">', 'kpi-icon-purp', 'Avg Invoice Value', 'PER TRANSACTION', format_value_func(kpis.get('avg_invoice_value', 0), 'avg_invoice_value')[0], ''),
        ('<img src="https://salesanalytics.technosyserp.com/united_king_bakery/icon (2).svg" alt="Cart" class="kpi-icon-img">', 'kpi-icon-blue', 'Total Invoices', 'MTD TRANSACTIONS', format_value_func(kpis.get('total_invoices', 0), 'count')[0], ''),
    ]
    
    cards_html = ""
    for icon, icon_class, label, sublabel, value, value_class in kpi_configs:
        cards_html += f"""
        <div class="kpi-card">
            <div class="kpi-icon {icon_class}">
                <span>{icon}</span>
            </div>
            <div class="kpi-content">
                <div class="kpi-label">{label}</div>
                <div class="kpi-sublabel">{sublabel}</div>
            </div>
            <div class="kpi-value {value_class}">{value}</div>
        </div>
        """
    
    return f'<div class="kpi-grid">{cards_html}</div>'


def generate_insights_section(insights, kpis, format_value_func, md_func, currency_unit='PKR'):
    """Generate the AI insights section"""
    
    mom_growth = kpis.get('mom_growth', 0)
    mom_icon = '↑' if mom_growth >= 0 else '↓'
    mom_badge_class = 'positive' if mom_growth >= 0 else 'negative'
    
    total_sales = format_value_func(kpis.get('total_sales', 0), 'sale')[0]
    
    insight_1 = md_func(insights[0]) if len(insights) > 0 else ''
    insight_2 = md_func(insights[1]) if len(insights) > 1 else ''
    insight_3 = md_func(insights[2]) if len(insights) > 2 else ''
    insight_4 = md_func(insights[3]) if len(insights) > 3 else ''
    
    return f"""
    <div class="insights-wrapper">
        <div class="insights-header">
            <span class="insights-header-icon"><img 
                src="https://salesanalytics.technosyserp.com/united_king_bakery/icon (6).svg" 
                alt="Cart" 
                class="kpi-icon-img"
                ></span>
            <h2>Professional Analysis & Insights</h2>
        </div>
        <div class="insights-content">
            <div class="insights-grid">
                <!-- Performance Card -->
                <div class="insight-card purple">
                    <div class="insight-header">
                        <div class="insight-icon purple"><span><img 
                src="https://salesanalytics.technosyserp.com/united_king_bakery/icon (7).svg" 
                alt="Cart" 
                class="kpi-icon-img"
                ></span></div>
                        <div class="insight-titles">
                            <div class="insight-title">Performance</div>
                            <div class="insight-subtitle">Trend Analysis</div>
                        </div>
                        <span class="badge badge-critical">CRITICAL</span>
                    </div>
                    <div class="insight-metrics">
                        <p>Total Revenue: <strong>{currency_unit} {total_sales}</strong></p>
                        <p>MoM Growth: <span class="metric-badge {mom_badge_class}">{mom_icon} {mom_growth:.1f}%</span></p>
                    </div>
                    <div class="insight-text"><strong>Insight:</strong> {insight_1}</div>
                </div>
                
                <!-- Channel Card -->
                <div class="insight-card purple">
                    <div class="insight-header">
                        <div class="insight-icon purple"><span><img 
                src="https://salesanalytics.technosyserp.com/united_king_bakery/icon (8).svg" 
                alt="Cart" 
                class="kpi-icon-img"
                ></span></div>
                        <div class="insight-titles">
                            <div class="insight-title">Channel</div>
                            <div class="insight-subtitle">Performance</div>
                        </div>
                        <span class="badge badge-insight">INSIGHT</span>
                    </div>
                    <div class="insight-text"><strong>Insight:</strong> {insight_2}</div>
                </div>
                
                <!-- Growth Card -->
                <div class="insight-card purple">
                    <div class="insight-header">
                        <div class="insight-icon purple"><span><img 
                src="https://salesanalytics.technosyserp.com/united_king_bakery/icon (9).svg" 
                alt="Cart" 
                class="kpi-icon-img"
                ></span></div>
                        <div class="insight-titles">
                            <div class="insight-title">Growth</div>
                            <div class="insight-subtitle">Opportunity</div>
                        </div>
                        <span class="badge badge-opportunity">OPPORTUNITY</span>
                    </div>
                    <div class="insight-text"><strong>Insight:</strong> {insight_3}</div>
                </div>
                
                <!-- Strategic Card -->
                <div class="insight-card purple">
                    <div class="insight-header">
                        <div class="insight-icon purple"><span><img 
                src="https://salesanalytics.technosyserp.com/united_king_bakery/icon (10).svg" 
                alt="Cart" 
                class="kpi-icon-img"
                ></span></div>
                        <div class="insight-titles">
                            <div class="insight-title">Strategic</div>
                            <div class="insight-subtitle">Recommendations</div>
                        </div>
                        <span class="badge badge-action">ACTION REQUIRED</span>
                    </div>
                    <div class="insight-text"><strong>Insight:</strong> {insight_4}</div>
                </div>
            </div>
        </div>
    </div>
    """


def generate_charts_section(branch_data, channel_data, category_data, currency_unit='PKR', visibility={}):
    """Generate the charts section with Chart.js"""
    
    if not branch_data and not channel_data and not category_data:
        return ""
    
    charts_html = '<div class="charts-section">'
    
    # Branch Performance Chart
    if branch_data and visibility.get('branch', 1) == 1:
        charts_html += f"""
        <div class="chart-container">
            <h3 class="chart-title">Top 5 Branches - Sales Comparison</h3>
            <div class="chart-canvas-container">
                <canvas id="branchChart"></canvas>
            </div>
        </div>
        """
    
    # Channel Charts (Bar and Doughnut side by side)
    if channel_data and visibility.get('channel', 1) == 1:
        charts_html += f"""
        <div class="chart-row">
            <div class="chart-container">
                <h3 class="chart-title">Daily Sales by Channel</h3>
                <div class="chart-canvas-container">
                    <canvas id="channelBarChart"></canvas>
                </div>
            </div>
            <div class="chart-container">
                <h3 class="chart-title">Invoice Distribution by channel</h3>
                <div class="chart-canvas-container">
                    <canvas id="channelPieChart"></canvas>
                </div>
            </div>
        </div>
        """
    
    # Category Performance Chart
    if category_data and visibility.get('category', 1) == 1:
        charts_html += f"""
        <div class="chart-container">
            <h3 class="chart-title">Category Revenue Contribution</h3>
            <div class="chart-canvas-container">
                <canvas id="categoryChart"></canvas>
            </div>
        </div>
        """
    
    charts_html += '</div>'
    
    # Chart.js Scripts
    charts_html += f"""
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2"></script>
    <script>
        const colors = ['#4F46E5', '#7C3AED', '#EC4899', '#F59E0B', '#10B981', '#3B82F6', '#8B5CF6', '#06B6D4'];
        
        function formatValue(value) {{
            if (value >= 1000000) return (value/1000000).toFixed(1) + 'M';
            if (value >= 1000) return (value/1000).toFixed(0) + 'K';
            return value.toFixed(0);
        }}
        
        const isMobile = window.innerWidth < 768;
    """
    
    if branch_data and visibility.get('branch', 1) == 1:
        charts_html += f"""
        // Branch Chart
        (function() {{
            const data = {branch_data};
            const ctx = document.getElementById('branchChart').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: data.labels,
                    datasets: [
                        {{ label: 'This Month', data: data.this_month, backgroundColor: '#4F46E5', borderColor: '#4338CA', borderWidth: isMobile ? 1 : 2, barThickness: isMobile ? 12 : undefined }},
                        {{ label: 'Last Month', data: data.last_month, backgroundColor: 'rgba(203, 213, 224, 0.7)', borderColor: 'rgba(160, 174, 192, 0.8)', borderWidth: isMobile ? 1 : 2, barThickness: isMobile ? 12 : undefined }}
                    ]
                }},
                options: {{
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {{ mode: 'nearest', intersect: true }},
                    plugins: {{
                        legend: {{ position: 'top', labels: {{ font: {{ size: isMobile ? 10 : 12 }}, padding: isMobile ? 8 : 15, usePointStyle: true }} }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return context.dataset.label + ': {currency_unit} ' + formatValue(context.parsed.x);
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{ ticks: {{ font: {{ size: isMobile ? 9 : 11 }}, callback: function(value) {{ return formatValue(value); }} }} }},
                        y: {{ ticks: {{ font: {{ size: isMobile ? 9 : 11 }} }}, grid: {{ display: false }} }}
                    }}
                }}
            }});
        }})();
        """
    
    if channel_data and visibility.get('channel', 1) == 1:
        charts_html += f"""
        // Channel Bar Chart
        (function() {{
            const data = {channel_data};
            const barCtx = document.getElementById('channelBarChart').getContext('2d');
            new Chart(barCtx, {{
                type: 'bar',
                data: {{
                    labels: data.labels,
                    datasets: [{{ label: 'Sales', data: data.sales || data.amounts, backgroundColor: colors.slice(0, data.labels.length), borderWidth: isMobile ? 1 : 2, maxBarThickness: isMobile ? 16 : undefined }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return context.dataset.label + ': {currency_unit} ' + formatValue(context.parsed.y);
                                }}
                            }}
                        }},
                        datalabels: {{
                            anchor: 'end', align: 'end', font: {{ size: isMobile ? 9 : 11 }},
                            formatter: function(value) {{ return formatValue(value); }}
                        }}
                    }},
                    scales: {{
                        x: {{ title: {{ display: true, text: 'Channel', font: {{ size: isMobile ? 10 : 12 }} }}, ticks: {{ font: {{ size: isMobile ? 9 : 11 }} }}, grid: {{ display: false }} }},
                        y: {{ title: {{ display: true, text: 'Sales ({currency_unit})', font: {{ size: isMobile ? 10 : 12 }} }}, ticks: {{ font: {{ size: isMobile ? 9 : 11 }}, callback: function(value) {{ return formatValue(value); }} }} }}
                    }}
                }},
                plugins: [ChartDataLabels]
            }});

            // Channel Pie Chart
            const pieCtx = document.getElementById('channelPieChart').getContext('2d');
            new Chart(pieCtx, {{
                type: 'doughnut',
                data: {{
                    labels: data.labels,
                    datasets: [{{ data: data.quantities || data.amounts, backgroundColor: colors.slice(0, data.labels.length), borderColor: 'white', borderWidth: isMobile ? 1 : 3 }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'right', labels: {{ font: {{ size: isMobile ? 9 : 11 }}, padding: isMobile ? 8 : 10, usePointStyle: true }} }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return context.label + ': ' + formatValue(context.raw);
                                }}
                            }}
                        }},
                        datalabels: {{
                            color: '#fff', font: {{ size: isMobile ? 10 : 12 }},
                            formatter: function(value, context) {{
                                const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                                return (value / total * 100).toFixed(1) + '%';
                            }}
                        }}
                    }}
                }},
                plugins: [ChartDataLabels]
            }});
        }})();
        """
    
    if category_data and visibility.get('category', 1) == 1:
        charts_html += f"""
        // Category Chart
        (function() {{
            const data = {category_data};
            const ctx = document.getElementById('categoryChart').getContext('2d');
            new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: data.labels,
                    datasets: [{{ data: data.sales, backgroundColor: colors.slice(0, data.labels.length), borderColor: 'white', borderWidth: isMobile ? 1 : 3 }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'right', labels: {{ font: {{ size: isMobile ? 9 : 11 }}, padding: isMobile ? 8 : 12, usePointStyle: true }} }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return context.label + ': {currency_unit} ' + formatValue(context.raw);
                                }}
                            }}
                        }},
                        datalabels: {{
                            color: 'white', font: {{ size: isMobile ? 10 : 13 }},
                            formatter: function(value, context) {{
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                return ((value / total) * 100).toFixed(1) + '%';
                            }}
                        }}
                    }}
                }},
                plugins: [ChartDataLabels]
            }});
        }})();
        """
    
    charts_html += '</script>'
    
    return charts_html
