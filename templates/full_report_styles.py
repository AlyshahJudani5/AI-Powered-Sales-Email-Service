"""
Full Report Template - Hosted HTML with Charts + Tables
Responsive desktop/mobile with integrated Chart.js charts
"""

from datetime import datetime, timedelta
from utils import format_value, format_time_for_display, md_to_html, get_trend_indicator, calculate_daily_growth, calculate_table_totals
from config import TableConfig


def get_full_report_styles():
    """Return the CSS styles for the full report"""
    return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            color: #1E293B;
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1100px;
            width: 100%;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 20px;
            overflow-x: hidden;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12);
        }
        
        /* Header */
        .header {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #9333EA 100%);
            color: white;
            padding: 48px 32px;
            text-align: center;
        }
        .header-icon { font-size: 36px; margin-bottom: 12px; }
        .header h1 { font-size: 40px; font-weight: 800; margin-bottom: 10px; letter-spacing: 1px; }
        .header p { font-size: 16px; opacity: 0.95; font-weight: 600; letter-spacing: 0.5px; }
        
        /* Content */
        .content { padding: 32px; background-color: #f8fafc; }
        
        /* KPI Grid - Desktop */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 32px;
        }
        .kpi-card {
            background: #ffffff;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .kpi-icon {
            width: 32px;
            height: 32px;
            border-radius: 26843500px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            flex-shrink: 0;
        }
         .kpi-icon-blue { background-color: #EFF6FF; }
        .kpi-icon-purple { background-color: #EEF2FF; }
        .kpi-icon-pink { background-color: #FCE7F3; }
        .kpi-icon-green { background-color: #ECFEFF; }
        .kpi-icon-red { background-color: #F5F3FF; }
        .kpi-icon-purp { background-color: #FAF5FF; }
        .kpi-content { flex: 1; }
        .kpi-label { font-size: 14px; font-weight: 400; color: #0f172b; }
        
        .kpi-sublabel { font-size: 12px; color: #62748E; text-transform: uppercase; letter-spacing: 0.3px; margin-top: 2px; font-weight: 400;}
        .kpi-value { font-size: 24px; font-weight: 400; color: #0f172b; text-align: right; }
        .kpi-value.positive { color: #10B981; }
        .kpi-value.negative { color: #EF4444; }
        
        /* Insights Section */
        .insights-wrapper {
            background: linear-gradient(135deg, #FEF9E7 0%, #FEF3C7 100%);
            border-radius: 12px;
            margin-bottom: 32px;
            overflow: hidden;
        }
        .insights-header {
            padding: 16px 20px;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid rgba(245, 158, 11, 0.2);
        }
        .insights-header-icon { font-size: 22px; }
        .insights-header h2 { font-size: 18px; font-weight: 400; color: #1D293D; }
        .insights-content { padding: 20px; background-color: #FFFFFF; }
        .insights-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
        
        /* .insight-card {
            background: #ffffff;
            border-radius: 14px;
            padding: 20px 24px;
            border: 1px solid #e9e5ff;
            box-shadow: 0 4px 12px rgba(120, 92, 255, 0.08);
            align-items: flex-start;
        } */

        .insight-card {
            background: #ffffff;
            border-radius: 10px;
            padding: 20px 24px;
            border: 1px solid #ddd6ff;
            box-shadow: 0px 1px 2px -1px rgba(0, 0, 0, 0.1), 0px 1px 3px 0px rgba(0, 0, 0, 0.1);
            /* align-items: flex-start; */
            opacity: 1;
        }

        .insight-card.purple {border: 1px solid #ddd6ff;}
        .insight-card.amber { border-left-color: #F59E0B; }
        .insight-card.blue { border-left-color: #3B82F6; }
        .insight-card.green { border-left-color: #10B981; }
        
        .insight-header { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 12px; }
        /* .insight-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
        } */

        .insight-icon {
            width: 40px;
            height: 40px;

            border-radius: 10px;

            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;

            flex-shrink: 0;
            opacity: 1;

            background: linear-gradient(135deg, #615FFF 0%, #4F39F6 100%);

            box-shadow:
                0px 1px 2px -1px rgba(0, 0, 0, 0.1),
                0px 1px 3px 0px rgba(0, 0, 0, 0.1);
        }

        .insight-icon img,
        .insight-icon svg {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }

        .insight-icon.purple { background-color: #8E51FF; }
        .insight-icon.amber { background-color: #FEF3C7; }
        .insight-icon.blue { background-color: #DBEAFE; }
        .insight-icon.green { background-color: #D1FAE5; }
        
        .insight-titles { flex: 1; }
        .insight-title { font-size: 16px; font-weight: 400; color: #0F172B; }
        .insight-subtitle { font-size: 12px; font-weight: 400; color: #45556C; }
        
        .badge {
            font-size: 10px;
            font-weight: 400;
            padding: 4px 10px;
            border-radius: 8px;
            text-transform: uppercase;
            letter-spacing: 0.25px;
        }
        .badge-critical { background-color: #FFC9C9; color: #C10007; }
        .badge-insight { background-color: #DDD6FF; color: #7008E7; }
        .badge-opportunity { background-color: #A4F4CF; color: #007A55; }
        .badge-action { background-color: #F1F5F9; color: #314158; }
        
        .insight-metrics { margin-bottom: 12px; }
        .insight-metrics p { font-size: 12px; color: #64748B; margin-bottom: 4px; }
        .insight-metrics strong { color: #1E293B; }
        .metric-badge {
            display: inline-block;
            font-size: 11px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 6px;
        }
        .metric-badge.positive { background-color: #ECFDF5; color: #059669; }
        .metric-badge.negative { background-color: #FEF2F2; color: #DC2626; }
        
        .insight-text {
            border-top: 1px solid #E2E8F0;
            padding-top: 12px;
            font-size: 12px;
            color: #45556C;
            line-height: 1.6;
        }
        .insight-text strong { color: #475569; }
        
        /* Charts Section */
        .charts-section { margin-bottom: 32px; }
        .chart-container {
            background: #ffffff;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            border: 1px solid #e2e8f0;
        }
        .chart-title {
            font-size: 18px;
            font-weight: 700;
            color: #1E293B;
            margin-bottom: 20px;
            text-align: center;
        }
        .chart-row { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; width: 100%; }
        .chart-canvas-container { position: relative; height: 320px; width: 100%; }
        
       /* Tables Section */
        .table-section { margin-bottom: 32px; }
        .table-header-bar {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            padding: 18px 24px;
            border-radius: 12px 12px 0 0;
        }
        .table-header-bar h3 { font-size: 17px; font-weight: 700; color: #ffffff; margin: 0; }
        
        .table-wrapper {
            overflow-x: auto;
            border: 1px solid #e2e8f0;
            border-top: none;
            border-radius: 0 0 12px 12px;
            background: #ffffff;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        .table-header {
            background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
            color: #64748B;
            font-weight: 700;
            text-align: left;
            padding: 14px 12px;
            font-size: 10px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            white-space: nowrap;
            border-bottom: 2px solid #e2e8f0;
        }
        .table-cell {
            padding: 12px;
            border-bottom: 1px solid #f1f5f9;
            white-space: nowrap;
            color: #334155;
            font-weight: 500;
        }
        .table-cell.positive { color: #10B981; font-weight: 700; }
        .table-cell.negative { color: #EF4444; font-weight: 700; }
        
        .even-row { background-color: #fafbfc; }
        .odd-row { background-color: #ffffff; }
        .subtotal-row { background-color: #E8F4FF; }
        .subtotal-row .table-cell { font-weight: 600; }
        
        .totals-row { background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%); }
        .totals-cell { color: #ffffff !important; font-weight: 800 !important; }
        
        /* Mobile Cards */
        .mobile-cards { display: none; padding: 16px; background-color: #f8fafc; border-radius: 0 0 12px 12px; }
        .mobile-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        }
        .mobile-card:last-child { margin-bottom: 0; }
        .mobile-card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }
        .mobile-card-title { font-size: 18px; font-weight: 700; color: #1E293B; }
        .mobile-card-subtitle { font-size: 13px; color: #64748B; margin-top: 2px; }
        .mobile-card-badges { display: flex; gap: 8px; flex-wrap: wrap; }
        .mobile-card-badges .badge {
            font-size: 10px;
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 700;
        }
        .badge-positive { background-color: #ECFDF5; color: #059669; }
        .badge-negative { background-color: #FEF2F2; color: #DC2626; }
        .badge-info { background-color: #DBEAFE; color: #2563EB; }
        .badge-outline { background: transparent; border: 1px solid currentColor; }
        
        .mobile-card-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }
        .mobile-card-metric { }
        .metric-label {
            display: block;
            font-size: 10px;
            font-weight: 400;
            color: #45556C;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin-bottom: 1px;
        }
        .metric-value {
            display: block;
            font-size: 16px;
            font-weight: 400;
            color: #1E293B;
        }
        
        /* Footer */
        .footer {
            background: #f8fafc;
            padding: 24px 32px;
            text-align: center;
            border-top: 1px solid #E2E8F0;
        }
        .footer p { margin: 4px 0; font-size: 12px; color: #64748B; }
        .footer .disclaimer { color: #DC2626; font-size: 11px; }
        
        /* Desktop View */
        .desktop-view { display: block; }
        .mobile-view { display: none; }
        
        /* Responsive */
        @media (max-width: 768px) {
            body { padding: 8px; overflow-x: hidden; width: 100%; box-sizing: border-box; }
            .header { padding: 32px 16px; }
            .header h1 { font-size: 32px; letter-spacing: 0.5px; }
            .header p { font-size: 14px; }
            .content { padding: 12px; width: 100%; box-sizing: border-box; }
            
            .kpi-grid { grid-template-columns: 1fr; gap: 12px; }
            .insights-grid { grid-template-columns: 1fr; }
            .chart-row { display: flex; flex-direction: column; gap: 16px; width: 100%; }
            
            .chart-canvas-container { height: 260px; width: 100%; padding: 0; margin: 0; }
            .chart-container { padding: 12px; margin-bottom: 16px; width: 100%; box-sizing: border-box; }
            .chart-title { font-size: 16px; margin-bottom: 16px; }
            
            .desktop-view { display: none; }
            .mobile-view { display: block; }

            .mobile-card {
                width: 100%;
                margin: 0 auto 12px;
                padding: 16px;
                border-radius: 12px;
            }
            .mobile-cards {
                
                padding-left: 2px;
                padding-right: 2px;
            }
            .table-wrapper { display: none; }
        }
    """
