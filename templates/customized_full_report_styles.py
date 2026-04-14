"""
Full Report Template - Hosted HTML with Charts + Tables
Responsive desktop/mobile with integrated Chart.js charts
Dynamically themed via theme_config parameter
"""

from datetime import datetime, timedelta
from utils import format_value, format_time_for_display, md_to_html, get_trend_indicator, calculate_daily_growth, calculate_table_totals
from config import TableConfig


def get_full_report_styles(theme_config=None):
    """
    Return the CSS styles for the full report. 
    Accepts a theme_config dictionary for dynamic styling.
    """
    if theme_config is None:
        theme_config = {}
    
    theme = theme_config.get('theme', {})
    
    # Theme colors with defaults
    primary = theme.get('primary', '#D11E26')
    secondary = theme.get('secondary', '#FDC010')
    bg_color = theme.get('background', '#FFFFFF')
    text_main = theme.get('text_main', '#333333')
    text_light = theme.get('text_light', '#FFFFFF')
    success = theme.get('accent_success', '#10B981')
    warning = theme.get('accent_warning', '#F59E0B')
    danger = theme.get('accent_danger', '#EF4444')

    # Header gradient using primary color
    header_gradient = f'linear-gradient(135deg, {primary} 0%, {primary} 100%)'

    return f"""
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: {bg_color};
            color: {text_main};
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1100px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        }}
        
        /* Header with primary gradient and secondary border */
        .header {{
            background: {header_gradient};
            color: {secondary};
            padding: 48px 32px;
            text-align: center;
            border-bottom: 4px solid {secondary};
            position: relative;
        }}
        .header-top-left {{
            position: absolute;
            top: 20px;
            left: 24px;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            color: {secondary};
            opacity: 0.9;
            font-weight: 600;
        }}
        .header-top-left img {{
            height: 20px;
            width: auto;
        }}
        .header-content {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
        }}
        .header-logo {{
            height: 100px;
            width: auto;
            border-radius: 50px;
        }}

        .header-icon {{ font-size: 36px; margin-bottom: 12px; }}
        .header h1 {{ font-size: 32px; font-weight: 700; margin-bottom: 8px; letter-spacing: -0.5px; color: {text_light}; }}
        .header p {{ font-size: 14px; opacity: 0.9; font-weight: 500; color: {secondary}; }}
        
        /* Content */
        .content {{ padding: 32px; background-color: {bg_color}; }}
        
        /* KPI Grid - Desktop */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 32px;
        }}
        .kpi-card {{
            background: #ffffff;
            border: 1px solid {secondary};
            border-radius: 12px;
            padding: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        }}
        .kpi-icon {{
            width: 38px;
            height: 38px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            flex-shrink: 0;
            background: {bg_color};
            color: {secondary};
        }}
        .kpi-icon-blue, .kpi-icon-purple, .kpi-icon-pink, .kpi-icon-green, .kpi-icon-red, .kpi-icon-purp {{
            background-color: {bg_color};
        }}
        
        .kpi-content {{ flex: 1; }}
        .kpi-label {{ font-size: 14px; font-weight: 600; color: {primary}; }}
        
        .kpi-sublabel {{ font-size: 11px; color: {primary}; opacity: 0.8; text-transform: uppercase; letter-spacing: 0.3px; margin-top: 2px; font-weight: 500;}}
        .kpi-value {{ font-size: 24px; font-weight: 700; color: {text_main}; text-align: right; }}
        .kpi-value.positive {{ color: {success}; }}
        .kpi-value.negative {{ color: {danger}; }}
        
        /* Insights Section with secondary border */
        .insights-wrapper {{
            background: #FFFFFF;
            border-radius: 12px;
            margin-bottom: 32px;
            overflow: hidden;
            border: 1px solid {secondary};
        }}
        .insights-header {{
            background: {secondary};
            padding: 16px 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .insights-header-icon {{ font-size: 22px; color: {primary}; }}
        .insights-header h2 {{ font-size: 18px; font-weight: 700; color: {primary}; margin: 0; }}
        
        .insights-content {{ padding: 20px; background-color: #FFFFFF; }}
        .insights-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }}
        
        .insight-card {{
            background: #ffffff;
            border-radius: 10px;
            padding: 20px 24px;
            border: 1px solid {secondary};
            box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.05);
        }}

        .insight-card.purple {{}}
        .insight-card.amber {{}}
        .insight-card.blue {{}}
        .insight-card.green {{}}
        
        .insight-header {{ display: flex; align-items: flex-start; gap: 10px; margin-bottom: 12px; }}

        .insight-icon {{
            width: 36px;
            height: 36px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            flex-shrink: 0;
            background: {secondary};
            color: {primary};
        }}

        .insight-icon img, .insight-icon svg {{ width: 20px; height: 20px; }}

        .insight-titles {{ flex: 1; }}
        .insight-title {{ font-size: 16px; font-weight: 700; color: {primary}; }}
        .insight-subtitle {{ font-size: 12px; font-weight: 500; color: {primary}; opacity: 0.8; }}
        
        .badge {{
            font-size: 10px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.25px;
        }}
        .badge-critical {{ background-color: #FFE4E6; color: {danger}; }}
        .badge-insight {{ background-color: {bg_color}; color: #B45309; }}
        .badge-opportunity {{ background-color: #ECFDF5; color: {success}; }}
        .badge-action {{ background-color: #F3F4F6; color: {text_main}; }}
        
        .insight-metrics {{ margin-bottom: 12px; }}
        .insight-metrics p {{ font-size: 12px; color: #64748B; margin-bottom: 4px; }}
        .insight-metrics strong {{ color: #334155; }}
        
        .metric-badge {{
            display: inline-block;
            font-size: 11px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 6px;
        }}
        .metric-badge.positive {{ background-color: #ECFDF5; color: {success}; }}
        .metric-badge.negative {{ background-color: #FEF2F2; color: {danger}; }}
        
        .insight-text {{
            border-top: 1px solid #E2E8F0;
            padding-top: 12px;
            font-size: 12px;
            color: #4B5563;
            line-height: 1.6;
        }}
        .insight-text strong {{ color: {primary}; }}
        
        /* Charts Section with secondary border-top */
        .charts-section {{ margin-bottom: 32px; }}
        .chart-container {{
            background: #ffffff;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid #E5E7EB;
            border-top: 3px solid {secondary};
        }}
        .chart-title {{
            font-size: 18px;
            font-weight: 700;
            color: {primary};
            margin-bottom: 20px;
            text-align: center;
        }}
        .chart-row {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }}
        .chart-canvas-container {{ position: relative; height: 320px; }}
        
        /* Tables Section with primary header and secondary border */
        .table-section {{ margin-bottom: 32px; }}
        .table-header-bar {{
            background: {primary};
            padding: 16px 24px;
            border-radius: 12px 12px 0 0;
            border-bottom: 3px solid {secondary};
        }}
        .table-header-bar h3 {{ font-size: 17px; font-weight: 700; color: #ffffff; margin: 0; }}
        
        .table-wrapper {{
            overflow-x: auto;
            border: 1px solid #E5E7EB;
            border-top: none;
            border-radius: 0 0 12px 12px;
            background: #ffffff;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        .table-header {{
            background: {bg_color};
            color: {primary};
            font-weight: 700;
            text-align: left;
            padding: 14px 12px;
            font-size: 11px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            white-space: nowrap;
            border-bottom: 2px solid {secondary};
        }}
        .table-cell {{
            padding: 12px;
            border-bottom: 1px solid #F3F4F6;
            white-space: nowrap;
            color: #334155;
            font-weight: 500;
        }}
        .table-cell.positive {{ color: {success}; font-weight: 700; }}
        .table-cell.negative {{ color: {danger}; font-weight: 700; }}
        
        .even-row {{ background-color: #ffffff; }}
        .odd-row {{ background-color: {bg_color}; }}
        
        /* Specific override for subtotal/totals */
        .subtotal-row {{ background-color: {bg_color} !important; }}
        .subtotal-row .table-cell {{ font-weight: 700; color: {primary}; }}
        
        .totals-row {{ background: {primary}; }}
        .totals-cell {{ color: {secondary} !important; font-weight: 800 !important; }}
        
        /* Mobile Cards */
        .mobile-cards {{ display: none; padding: 16px; background-color: {bg_color}; border-radius: 0 0 12px 12px; }}
        .mobile-card {{
            background: #ffffff;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            border: 1px solid #E5E7EB;
            border-left: 4px solid {secondary};
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        }}
        .mobile-card:last-child {{ margin-bottom: 0; }}
        .mobile-card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }}
        .mobile-card-title {{ font-size: 18px; font-weight: 700; color: {primary}; }}
        .mobile-card-subtitle {{ font-size: 13px; color: {primary}; opacity: 0.8; margin-top: 2px; }}
        .mobile-card-badges {{ display: flex; gap: 8px; flex-wrap: wrap; }}
        .mobile-card-badges .badge {{
            font-size: 10px;
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 700;
        }}
        .badge-positive {{ background-color: #ECFDF5; color: {success}; }}
        .badge-negative {{ background-color: #FEF2F2; color: {danger}; }}
        .badge-info {{ background-color: #DBEAFE; color: #2563EB; }}
        .badge-outline {{ background: transparent; border: 1px solid currentColor; }}
        
        .mobile-card-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }}
        .mobile-card-metric {{ }}
        .metric-label {{
            display: block;
            font-size: 10px;
            font-weight: 600;
            color: {primary};
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin-bottom: 1px;
        }}
        .metric-value {{
            display: block;
            font-size: 16px;
            font-weight: 600;
            color: {text_main};
        }}
        
        /* Footer with secondary background and primary border-top */
        .footer {{
            background: {secondary};
            padding: 24px 32px;
            text-align: center;
            border-top: 4px solid {primary};
            color: {primary};
        }}
        .footer p {{ margin: 4px 0; font-size: 12px; color: {primary}; font-weight: 600; }}
        .footer .disclaimer {{ color: {text_main}; font-size: 11px; font-weight: 400; opacity: 0.9; }}
        
        /* Desktop View */
        .desktop-view {{ display: block; }}
        .mobile-view {{ display: none; }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            body {{ padding: 10px; background-color: {bg_color}; }}
            .header {{ padding: 32px 20px; }}
            .header h1 {{ font-size: 24px; }}
            .content {{ padding: 16px; }}
            
            .kpi-grid {{ grid-template-columns: 1fr; gap: 12px; }}
            .insights-grid {{ grid-template-columns: 1fr; }}
            .chart-row {{ grid-template-columns: 1fr; }}
            
            .desktop-view {{ display: none; }}
            .mobile-view {{ display: block; }}

            .mobile-card {{
                width: 100%;
                margin: 0 auto 12px;
                padding: 16px;
            }}
            .mobile-cards {{ padding: 12px; }}
            .table-wrapper {{ display: none; }}
        }}
    """
