"""
Full Report Template - Main Generator
Combines all components into final HTML
"""

from datetime import datetime, timedelta
import json
from utils import format_value, format_time_for_display, md_to_html, get_trend_indicator, calculate_daily_growth, calculate_table_totals
from config import TableConfig
from .full_report_styles import get_full_report_styles
from .full_report_components import (
    generate_table_html_desktop,
    generate_table_html_mobile,
    generate_kpi_section,
    generate_insights_section,
    generate_charts_section
)


def generate_full_report_template(report_date, report_time, kpis, insights, all_tables_data, find_table_func, branch_chart_data, channel_chart_data, category_chart_data, dashboard_url=None, currency_unit='PKR', multi_category_enabled=0, second_category_table=None, report_title='Daily Sales Report', visibility={}):
    """Generate the complete full report HTML template"""
    
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
    config2 = load_config_from_json()
    date_range_str = f"({previous_date.strftime('%B %d')}, {display_time} - {current_date.strftime('%B %d')}, {display_time})"
    formatted_footer_date = current_date.strftime('%A %d %B %Y')
    
    # Generate KPIs section
    kpi_section = generate_kpi_section(kpis, format_value)
    
    # Generate Insights section
    insights_section = generate_insights_section(insights, kpis, format_value, md_to_html, currency_unit=currency_unit)
    
    # Generate Charts section
    charts_section = generate_charts_section(branch_chart_data, channel_chart_data, category_chart_data, currency_unit=currency_unit, visibility=visibility.get('charts', {}))
    
    # Generate Tables sections
    table_signatures = {
        'branch_performance': (['Branch', 'MonthSale', 'MonthGP'], 0),
        'debtor': (['DebtorGroup', 'Sale', 'SaleReturn'], 2),
        'category': (['Category', 'CategoryShareMonth'], 3),
        'customer_sales': (['SaleType', 'NewCount', 'OldCount'], 4)
    }
    
    desktop_tables_html = ""
    
    for table_type, (signature_cols, config_idx) in table_signatures.items():
        # Check visibility
        table_visibility_key = {
            'branch_performance': 'branch',
            'category': 'category',
            'customer_sales': 'customer',
            'debtor': 'debtor'
        }.get(table_type)
        
        if table_visibility_key and visibility.get('tables', {}).get(table_visibility_key, 1) == 0:
            continue

        table_idx = find_table_func(signature_cols)
        
        if table_idx is not None and config_idx in TableConfig.TABLES_TO_DISPLAY:
            config = TableConfig.TABLES_TO_DISPLAY[config_idx]
            table_info = all_tables_data[table_idx]
            table_data = table_info['data']
            all_columns = table_info['columns']
            
            import copy
            
            if table_type == 'category' and multi_category_enabled == 1 and second_category_table:
                config_top = copy.deepcopy(config)
                config_top['display_names']['Category'] = 'Top Category'
                
                config_low = copy.deepcopy(config)
                config_low['display_names']['Category'] = 'Last Level Category'

                desktop_table_top = generate_table_html_desktop(
                    table_data, all_columns, config_top, config_idx,
                    format_value, get_trend_indicator, calculate_daily_growth, calculate_table_totals
                )
                mobile_cards_top = generate_table_html_mobile(
                    table_data, all_columns, config_top, config_idx, format_value
                )

                desktop_table_low = generate_table_html_desktop(
                    second_category_table['data'], second_category_table['columns'], config_low, config_idx,
                    format_value, get_trend_indicator, calculate_daily_growth, calculate_table_totals
                )
                mobile_cards_low = generate_table_html_mobile(
                    second_category_table['data'], second_category_table['columns'], config_low, config_idx, format_value
                )
                
                desktop_tables_html += f"""
                <div class="table-section category-table-section">
                    <div class="table-header-bar" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                        <h3>{config['title']}</h3>
                        <div class="category-toggle" style="display:flex; gap:4px; background: rgba(255,255,255,0.15); padding: 4px; border-radius: 30px;">
                            <button id="btn-top-cat" style="padding:6px 16px; background:#ffffff; color:#4F46E5; border:none; border-radius:20px; font-weight:700; cursor:pointer; font-size:12px; transition:all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" onclick="toggleCategory('top')">Top Category</button>
                            <button id="btn-low-cat" style="padding:6px 16px; background:transparent; color:#ffffff; border:none; border-radius:20px; font-weight:600; cursor:pointer; font-size:12px; transition:all 0.3s ease; box-shadow: none;" onclick="toggleCategory('low')">Last Level Category</button>
                        </div>
                    </div>
                    <div id="cat-top-view">
                        <div class="table-wrapper desktop-view">
                            {desktop_table_top}
                        </div>
                        <div class="mobile-cards mobile-view">
                            {mobile_cards_top}
                        </div>
                    </div>
                    <div id="cat-low-view" style="display:none;">
                        <div class="table-wrapper desktop-view">
                            {desktop_table_low}
                        </div>
                        <div class="mobile-cards mobile-view">
                            {mobile_cards_low}
                        </div>
                    </div>
                </div>
                """
            else:
                # Desktop table
                desktop_table = generate_table_html_desktop(
                    table_data, all_columns, config, config_idx,
                    format_value, get_trend_indicator, calculate_daily_growth, calculate_table_totals
                )
                
                # Mobile cards
                mobile_cards = generate_table_html_mobile(table_data, all_columns, config, config_idx, format_value)
                
                desktop_tables_html += f"""
                <div class="table-section">
                    <div class="table-header-bar">
                        <h3>{config['title']}</h3>
                    </div>
                    <div class="table-wrapper desktop-view">
                        {desktop_table}
                    </div>
                    <div class="mobile-cards mobile-view">
                        {mobile_cards}
                    </div>
                </div>
                """
    
    # Get CSS styles
    styles = get_full_report_styles()
    
    # Build complete HTML
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>{report_title} - Full Report</title>
    <style>
        {styles}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="header-icon"></div>
            <h1>{report_title}</h1>
            <p>{date_range_str}</p>
        </div>
        
        <div class="content">
            <!-- KPI Section -->
            {kpi_section}
            
            <!-- AI Insights Section -->
            {insights_section}
            
            <!-- Charts Section -->
            {charts_section}
            
            <!-- Tables Section -->
            {desktop_tables_html}
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p><strong>Generated:</strong> {formatted_footer_date}</p>
            <p class="disclaimer"><strong>Disclaimer:</strong> Data availability subject to server connectivity and branch replication status.</p>
            <p>AI-Powered Sales Analytics | Professional Data Analysis{f" | <a href='{dashboard_url}' style='color: #4F46E5; text-decoration: none; font-weight: 700;' target='_blank'>View Interactive Dashboard</a>" if dashboard_url else ""}</p>
        </div>
    </div>
    <script>
        function toggleCategory(level) {{
            var topView = document.getElementById('cat-top-view');
            var lowView = document.getElementById('cat-low-view');
            var btnTop = document.getElementById('btn-top-cat');
            var btnLow = document.getElementById('btn-low-cat');
            
            if (topView && lowView && btnTop && btnLow) {{
                if (level === 'top') {{
                    topView.style.display = 'block';
                    lowView.style.display = 'none';
                    btnTop.style.background = '#ffffff';
                    btnTop.style.color = '#4F46E5';
                    btnTop.style.fontWeight = '700';
                    btnTop.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
                    
                    btnLow.style.background = 'transparent';
                    btnLow.style.color = '#ffffff';
                    btnLow.style.fontWeight = '600';
                    btnLow.style.boxShadow = 'none';
                }} else {{
                    topView.style.display = 'none';
                    lowView.style.display = 'block';
                    btnLow.style.background = '#ffffff';
                    btnLow.style.color = '#4F46E5';
                    btnLow.style.fontWeight = '700';
                    btnLow.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
                    
                    btnTop.style.background = 'transparent';
                    btnTop.style.color = '#ffffff';
                    btnTop.style.fontWeight = '600';
                    btnTop.style.boxShadow = 'none';
                }}
            }}
        }}
    </script>
</body>
</html>
    """
    
    return html_template
