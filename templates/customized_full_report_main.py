"""
Full Report Template - Main Generator
Combines all components into final HTML
Dynamically themed via theme_config parameter
"""

from datetime import datetime, timedelta
from utils import format_value, format_time_for_display, md_to_html, get_trend_indicator, calculate_daily_growth, calculate_table_totals
from config import TableConfig
from .customized_full_report_styles import get_full_report_styles
from .customized_full_report_components import (
    generate_table_html_desktop,
    generate_table_html_mobile,
    generate_kpi_section,
    generate_insights_section,
    generate_charts_section
)


def generate_full_report_template(report_date, report_time, kpis, insights, all_tables_data, find_table_func, branch_chart_data, channel_chart_data, category_chart_data, theme_config=None, dashboard_url=None, currency_unit='PKR', report_title='Daily Sales Report', visibility={}):
    """Generate the complete full report HTML template"""
    
    if theme_config is None:
        theme_config = {}
        
    branding = theme_config.get('branding', {})
    company_logo = branding.get('company_logo_url', '')
    provider_logo = branding.get('service_provider_logo_url', '')
    show_powered_by = branding.get('show_powered_by', True)
    
    # Extract colors for styling
    theme = theme_config.get('theme', {})
    primary = theme.get('primary', '#D11E26')
    secondary = theme.get('secondary', '#FDC010')
    text_light = theme.get('text_light', '#FFFFFF')

    current_date = datetime.strptime(report_date, '%Y-%m-%d')
    previous_date = current_date - timedelta(days=1)
    display_time = format_time_for_display(report_time)
    date_range_str = f"({previous_date.strftime('%B %d')}, {display_time} - {current_date.strftime('%B %d')}, {display_time})"
    formatted_footer_date = current_date.strftime('%A %d %B %Y')
    
    # Generate KPIs section with theme
    kpi_section = generate_kpi_section(kpis, format_value, theme_config)
    
    # Generate Insights section with theme
    insights_section = generate_insights_section(insights, kpis, format_value, md_to_html, theme_config, currency_unit=currency_unit)
    
    # Generate Charts section with theme
    charts_section = generate_charts_section(branch_chart_data, channel_chart_data, category_chart_data, theme_config, currency_unit=currency_unit, visibility=visibility.get('charts', {}))
    
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
    
    # Get CSS styles with theme
    styles = get_full_report_styles(theme_config)
    
    # Logo HTML (show if company logo exists)
    logo_html = ""
    if company_logo:
        logo_html = f'<img src="{company_logo}" alt="Company Logo" class="header-logo">'

    # Powered by HTML for footer
    powered_by_html = ""
    if show_powered_by and provider_logo:
        powered_by_html = f"""
        <div style="display: flex; align-items: center; gap: 8px; justify-content: center; margin-top: 12px;">
            <span>Powered by</span>
            <img src="{provider_logo}" alt="Provider Logo" style="height: 30px; width: auto;">
        </div>
        """

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
        <!-- Header with primary background and secondary border -->
        <div class="header">
            <div class="header-content">
                {logo_html}
                <div>
                     <h1>{report_title}</h1>
                     <p style="color: {secondary};">{date_range_str}</p>
                </div>
            </div>
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
        
        <!-- Footer with secondary background and primary border -->
        <div class="footer">
            <p><strong>Generated:</strong> {formatted_footer_date}</p>
            <p class="disclaimer"><strong>Disclaimer:</strong> Data availability subject to server connectivity and branch replication status.</p>
            <p>AI-Powered Sales Analytics | Professional Data Analysis{f" | <a href='{dashboard_url}' style='color: {primary}; text-decoration: none; font-weight: 700;' target='_blank'>View Interactive Dashboard</a>" if dashboard_url else ""}</p>
            {powered_by_html}
        </div>
    </div>
</body>
</html>
    """
    
    return html_template
