"""
Concise Email Template - Gmail-safe, matches full report design
KPIs + AI Insights + View Full Report Button
Dynamically themed via theme_config parameter
"""

from datetime import datetime, timedelta
from utils import format_value, format_time_for_display, md_to_html

# Default Icon URLs - can be overridden by theme_config
DEFAULT_ICON_URLS = {
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


def generate_concise_email_template(report_date, report_time, kpis, insights, full_report_url, theme_config=None, dashboard_url=None, currency_unit='PKR', report_title='Daily Sales Report'):
    """Generate concise email template with KPIs and AI Insights only - Gmail safe"""
    
    if theme_config is None:
        theme_config = {}

    theme = theme_config.get('theme', {})
    branding = theme_config.get('branding', {})
    icons_config = theme_config.get('icons', {})

    # Extract theme colors with defaults
    primary = theme.get('primary', '#D11E26')
    secondary = theme.get('secondary', '#FDC010')
    bg_color = theme.get('background', '#FFFFFF')
    text_main = theme.get('text_main', '#333333')
    text_light = theme.get('text_light', '#FFFFFF')
    success = theme.get('accent_success', '#10B981')
    danger = theme.get('accent_danger', '#EF4444')

    # Build icon URLs from theme config or use defaults
    kpi_icons = theme_config.get('kpi', {})
    insight_icons = theme_config.get('insights', {})
    
    ICON_URLS = {
        'total_sales': kpi_icons.get('total_sales', DEFAULT_ICON_URLS['total_sales']),
        'today_sale': kpi_icons.get('today_sale', DEFAULT_ICON_URLS['today_sale']),
        'mom_growth': kpi_icons.get('mom_growth', DEFAULT_ICON_URLS['mom_growth']),
        'gross_profit': kpi_icons.get('gross_profit', DEFAULT_ICON_URLS['gross_profit']),
        'avg_invoice': kpi_icons.get('avg_invoice', DEFAULT_ICON_URLS['avg_invoice']),
        'total_invoices': kpi_icons.get('total_invoices', DEFAULT_ICON_URLS['total_invoices']),
        'insights_header': insight_icons.get('header', DEFAULT_ICON_URLS['insights_header']),
        'performance': insight_icons.get('performance', DEFAULT_ICON_URLS['performance']),
        'channel': insight_icons.get('channel', DEFAULT_ICON_URLS['channel']),
        'growth': insight_icons.get('growth', DEFAULT_ICON_URLS['growth']),
        'strategic': insight_icons.get('strategic', DEFAULT_ICON_URLS['strategic']),
    }

    # Extract branding
    company_logo = branding.get('company_logo_url', '')
    provider_logo = branding.get('service_provider_logo_url', '')
    show_powered_by = branding.get('show_powered_by', True)

    # Header gradient using primary color
    header_gradient = f'linear-gradient(135deg, {primary} 0%, {primary} 100%)'

    current_date = datetime.strptime(report_date, '%Y-%m-%d')
    previous_date = current_date - timedelta(days=1)
    display_time = format_time_for_display(report_time)
    date_range_str = f"({previous_date.strftime('%B %d')}, {display_time} - {current_date.strftime('%B %d')}, {display_time})"
    formatted_footer_date = current_date.strftime('%A %d %B %Y')
    
    mom_growth = kpis.get('mom_growth', 0)
    mom_color = success if mom_growth >= 0 else danger
    mom_icon = '↑' if mom_growth >= 0 else '↓'
    mom_badge_bg = '#ECFDF5' if mom_growth >= 0 else '#FEF2F2'
    mom_badge_color = success if mom_growth >= 0 else danger
    
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

    # Logo HTML - show if company logo exists
    logo_html = ""
    if company_logo:
        logo_html = f'<img src="{company_logo}" alt="Company Logo" style="height: 80px; border-radius: 50px; width: auto; max-width: 200px; display: block; margin: 0 auto 16px;">'
    
    # Generate KPI cards
    kpi_cards_desktop = _generate_kpi_section_desktop(
        total_sales, today_sale, mom_growth, mom_color, total_gp, avg_invoice, total_invoices,
        text_main, primary, secondary, bg_color, ICON_URLS
    )
    kpi_cards_mobile = _generate_kpi_section_mobile(
        total_sales, today_sale, mom_growth, mom_color, total_gp, avg_invoice, total_invoices,
        text_main, primary, secondary, bg_color, ICON_URLS
    )
    
    # Generate insight cards
    insight_cards_desktop = _generate_insights_section_desktop(
        total_sales, mom_growth, mom_icon, mom_badge_bg, mom_badge_color,
        insight_1, insight_2, insight_3, insight_4,
        text_main, primary, secondary, bg_color, ICON_URLS, currency_unit=currency_unit
    )
    insight_cards_mobile = _generate_insights_section_mobile(
        total_sales, mom_growth, mom_icon, mom_badge_bg, mom_badge_color,
        insight_1, insight_2, insight_3, insight_4,
        text_main, primary, secondary, bg_color, ICON_URLS, currency_unit=currency_unit
    )
    
    # Powered By HTML
    powered_by_html = ""
    if show_powered_by and provider_logo:
        powered_by_html = f"""
        <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="margin-top: 16px;">
            <tr>
                <td align="center" style="text-align: center;">
                    <span style="font-size: 14px; color: {primary}; opacity: 0.8; vertical-align: middle;">Powered by</span>
                    <img src="{provider_logo}" alt="Provider Logo" style="height: 24px; width: auto; vertical-align: middle; display: inline-block; margin-left: 8px;">
                </td>
            </tr>
        </table>
        """

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
<body style="margin: 0; padding: 0; background-color: {bg_color}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
    
    <div style="display: none; max-height: 0; overflow: hidden;">
        {report_title}: Total Sales {total_sales} | MoM Growth {mom_growth:.1f}%
    </div>
    
    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background-color: {bg_color};">
        <tr>
            <td align="center" style="padding: 20px 10px;">
                
                <table role="presentation" class="wrapper" cellpadding="0" cellspacing="0" width="600" style="max-width: 600px; background-color: {bg_color}; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12);">
                    
                    <!-- Header with primary gradient and secondary border-bottom -->
                    <tr>
                        <td class="mobile-padding-header" style="background: {header_gradient}; padding: 48px 32px; text-align: center; border-bottom: 4px solid {secondary};">
                            <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="center">
                                        {logo_html}
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center">
                                        <h1 class="header-title" style="margin: 0 0 8px; font-size: 32px; font-weight: 700; color: {text_light}; letter-spacing: -0.5px;">{report_title}</h1>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center">
                                        <p style="margin: 0; font-size: 14px; color: {secondary}; font-weight: 500;">{date_range_str}</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- KPI Section -->
                    <tr>
                        <td class="mobile-padding" style="padding: 32px; background-color: #ffffff;">
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
                        <td class="mobile-padding" style="padding: 0 32px 32px; background-color: #ffffff;">
                            
                            <!-- Insights Wrapper with secondary border -->
                            <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background-color: {bg_color}; border: 1px solid {secondary}; border-radius: 12px; overflow: hidden;">
                                
                                <!-- Insights Header with secondary background -->
                                <tr>
                                    <td style="padding: 16px 20px; border-bottom: 1px solid {secondary}; background-color: {secondary};">
                                        <table role="presentation" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td style="padding-right: 10px; vertical-align: middle;">
                                                    <img src="{ICON_URLS['insights_header']}" alt="Insights" width="22" height="22" style="display: block;">
                                                </td>
                                                <td style="vertical-align: middle;">
                                                    <p style="margin: 0; font-size: 18px; font-weight: 700; color: {primary};">Professional Analysis & Insights</p>
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
                        <td style="padding: 0 32px 32px; background-color: #ffffff;" align="center">
                            <table role="presentation" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="background: {header_gradient}; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
                                        <a href="{full_report_url}" target="_blank" style="display: inline-block; padding: 16px 40px; font-size: 16px; font-weight: 600; color: {text_light}; text-decoration: none; letter-spacing: 0.3px;">
                                            View Full Report with Charts & Tables
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Footer with secondary background and primary border-top -->
                    <tr>
                        <td style="background-color: {secondary}; padding: 30px; text-align: center; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; border-top: 4px solid {primary};">
                            <p style="margin: 0 0 8px; font-size: 14px; color: {primary}; font-weight: 700;">Generated: {formatted_footer_date}</p>
                            <p style="margin: 0 0 16px; font-size: 11px; color: {text_main}; opacity: 0.8;">Disclaimer: Data availability subject to server connectivity and branch replication status.</p>
                            <p style="margin: 0 0 4px; font-size: 12px; color: {primary}; font-weight: 600;">AI-Powered Sales Analytics | Professional Data Analysis{f" | <a href='{dashboard_url}' style='color: {primary}; text-decoration: none; font-weight: 700;' target='_blank'>View Interactive Dashboard</a>" if dashboard_url else ""}</p>
                            {powered_by_html}
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


def _generate_kpi_card(icon_url, label, sublabel, value, value_color, text_main, primary, secondary, bg_color):
    """Generate a single KPI card with secondary border and bg_color icon background"""
    return f"""
        <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff; border: 1px solid {secondary}; border-radius: 12px;">
            <tr>
                <td style="padding: 16px;">
                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td width="38" style="vertical-align: middle;">
                                <div style="width: 38px; height: 38px; background-color: {bg_color}; border-radius: 10px; text-align: center; line-height: 38px;">
                                    <img src="{icon_url}" alt="" width="20" height="20" style="display: inline-block; vertical-align: middle;">
                                </div>
                            </td>
                            <td style="padding-left: 12px; vertical-align: middle;">
                                <p style="margin: 0; font-size: 14px; font-weight: 600; color: {primary};">{label}</p>
                                <p style="margin: 2px 0 0; font-size: 11px; color: {primary}; text-transform: uppercase; letter-spacing: 0.3px; font-weight: 500; opacity: 0.8;">{sublabel}</p>
                            </td>
                            <td style="text-align: right; vertical-align: middle;">
                                <p style="margin: 0; font-size: 24px; font-weight: 700; color: {value_color};">{value}</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    """


def _generate_kpi_section_desktop(total_sales, today_sale, mom_growth, mom_color, total_gp, avg_invoice, total_invoices, text_main, primary, secondary, bg_color, icon_urls):
    """Generate desktop KPI grid (3x2)"""
    return f"""
        <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td width="33.33%" style="padding: 8px;">
                    {_generate_kpi_card(icon_urls['total_sales'], 'Total Sales', 'MONTH TO DATE', total_sales, text_main, text_main, primary, secondary, bg_color)}
                </td>
                <td width="33.33%" style="padding: 8px;">
                    {_generate_kpi_card(icon_urls['today_sale'], "Today's Sale", 'DAILY PERFORMANCE', today_sale, text_main, text_main, primary, secondary, bg_color)}
                </td>
                <td width="33.33%" style="padding: 8px;">
                    {_generate_kpi_card(icon_urls['mom_growth'], 'MoM Growth', 'GROWTH TREND', f"{mom_growth:.1f}%", mom_color, text_main, primary, secondary, bg_color)}
                </td>
            </tr>
            <tr>
                <td width="33.33%" style="padding: 8px;">
                    {_generate_kpi_card(icon_urls['gross_profit'], 'Gross Profit', 'TOTAL MARGIN', total_gp, text_main, text_main, primary, secondary, bg_color)}
                </td>
                <td width="33.33%" style="padding: 8px;">
                    {_generate_kpi_card(icon_urls['avg_invoice'], 'Avg Invoice Value', 'PER TRANSACTION', avg_invoice, text_main, text_main, primary, secondary, bg_color)}
                </td>
                <td width="33.33%" style="padding: 8px;">
                    {_generate_kpi_card(icon_urls['total_invoices'], 'Total Invoices', 'MTD TRANSACTIONS', total_invoices, text_main, text_main, primary, secondary, bg_color)}
                </td>
            </tr>
        </table>
    """


def _generate_kpi_section_mobile(total_sales, today_sale, mom_growth, mom_color, total_gp, avg_invoice, total_invoices, text_main, primary, secondary, bg_color, icon_urls):
    """Generate mobile KPI stack"""
    return f"""
        {_generate_kpi_card_mobile(icon_urls['total_sales'], 'Total Sales', 'MONTH TO DATE', total_sales, text_main, text_main, primary, secondary, bg_color)}
        {_generate_kpi_card_mobile(icon_urls['today_sale'], "Today's Sale", 'DAILY PERFORMANCE', today_sale, text_main, text_main, primary, secondary, bg_color)}
        {_generate_kpi_card_mobile(icon_urls['mom_growth'], 'MoM Growth', 'GROWTH TREND', f"{mom_growth:.1f}%", mom_color, text_main, primary, secondary, bg_color)}
        {_generate_kpi_card_mobile(icon_urls['gross_profit'], 'Gross Profit', 'TOTAL MARGIN', total_gp, text_main, text_main, primary, secondary, bg_color)}
        {_generate_kpi_card_mobile(icon_urls['avg_invoice'], 'Avg Invoice Value', 'PER TRANSACTION', avg_invoice, text_main, text_main, primary, secondary, bg_color)}
        {_generate_kpi_card_mobile(icon_urls['total_invoices'], 'Total Invoices', 'MTD TRANSACTIONS', total_invoices, text_main, text_main, primary, secondary, bg_color)}
    """


def _generate_kpi_card_mobile(icon_url, label, sublabel, value, value_color, text_main, primary, secondary, bg_color):
    """Generate a mobile KPI card"""
    return f"""
        <table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff; border: 1px solid {secondary}; border-radius: 12px; margin-bottom: 12px;">
            <tr>
                <td style="padding: 14px;">
                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td width="38" style="vertical-align: middle;">
                                <div style="width: 38px; height: 38px; background-color: {bg_color}; border-radius: 10px; text-align: center; line-height: 38px;">
                                    <img src="{icon_url}" alt="" width="20" height="20" style="display: inline-block; vertical-align: middle;">
                                </div>
                            </td>
                            <td style="padding-left: 12px; vertical-align: middle;">
                                <p style="margin: 0; font-size: 14px; font-weight: 600; color: {primary};">{label}</p>
                                <p style="margin: 2px 0 0; font-size: 11px; color: {primary}; text-transform: uppercase; letter-spacing: 0.3px; opacity: 0.8;">{sublabel}</p>
                            </td>
                            <td style="text-align: right; vertical-align: middle;">
                                <p style="margin: 0; font-size: 20px; font-weight: 700; color: {value_color};">{value}</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    """


def _generate_insight_card(icon_url, title, subtitle, badge_text, badge_bg, badge_color, metric1, metric2, insight_text, text_main, primary, secondary, bg_color):
    """Generate a single insight card with secondary icon background"""
    
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
        <table role="presentation" cellpadding="0" cellspacing="0" width="100%" height="100%" style="background-color: #ffffff; border-radius: 10px; border: 1px solid {secondary}; box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.05);">
            <tr>
                <td style="padding: 20px 24px;" height="100%">
                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" height="100%">
                        <tr>
                            <td>
                                <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                        <td width="40" style="vertical-align: top;">
                                            <div style="width: 40px; height: 40px; background-color: {secondary}; border-radius: 10px; text-align: center; line-height: 40px;">
                                                <img src="{icon_url}" alt="" width="20" height="20" style="display: inline-block; vertical-align: middle;">
                                            </div>
                                        </td>
                                        <td style="padding-left: 10px; vertical-align: middle;">
                                            <p style="margin: 0; font-size: 16px; font-weight: 700; color: {primary};">{title}</p>
                                            <p style="margin: 0; font-size: 12px; font-weight: 500; color: {primary}; opacity: 0.8;">{subtitle}</p>
                                        </td>
                                        <td style="text-align: right; vertical-align: top;">
                                            <span style="display: inline-block; background-color: {badge_bg}; color: {badge_color}; font-size: 10px; font-weight: 700; padding: 4px 10px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.25px;">{badge_text}</span>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        {metrics_html}
                        <tr>
                            <td style="padding-top: 12px; border-top: 1px solid #E2E8F0;">
                                <p style="margin: 0; font-size: 12px; color: #4B5563; line-height: 1.6;"><strong style="color: {primary};">Insight:</strong> {insight_text}</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    """


def _generate_insights_section_desktop(total_sales, mom_growth, mom_icon, mom_badge_bg, mom_badge_color, insight_1, insight_2, insight_3, insight_4, text_main, primary, secondary, bg_color, icon_urls, currency_unit='PKR'):
    """Generate desktop insights grid (2x2) with equal height cards"""
    return f"""
        <table role="presentation" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td width="50%" style="padding: 8px; vertical-align: top;">
                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" height="100%">
                        <tr>
                            <td height="100%">
                                {_generate_insight_card(icon_urls['performance'], 'Performance', 'Trend Analysis', 'CRITICAL', '#FFE4E6', '#C10007', 
                                    f'Total Revenue: <strong style="color: {text_main};">{currency_unit} {total_sales}</strong>', 
                                    f'MoM Growth: <span style="display: inline-block; background-color: {mom_badge_bg}; color: {mom_badge_color}; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 6px;">{mom_icon} {mom_growth:.1f}%</span>',
                                    insight_1, text_main, primary, secondary, bg_color)}
                            </td>
                        </tr>
                    </table>
                </td>
                <td width="50%" style="padding: 8px; vertical-align: top;">
                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" height="100%">
                        <tr>
                            <td height="100%">
                                {_generate_insight_card(icon_urls['channel'], 'Channel', 'Performance', 'INSIGHT', bg_color, '#B45309', '', '', insight_2, text_main, primary, secondary, bg_color)}
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
                                {_generate_insight_card(icon_urls['growth'], 'Growth', 'Opportunity', 'OPPORTUNITY', '#ECFDF5', '#10B981', '', '', insight_3, text_main, primary, secondary, bg_color)}
                            </td>
                        </tr>
                    </table>
                </td>
                <td width="50%" style="padding: 8px; vertical-align: top;">
                    <table role="presentation" cellpadding="0" cellspacing="0" width="100%" height="100%">
                        <tr>
                            <td height="100%">
                                {_generate_insight_card(icon_urls['strategic'], 'Strategic', 'Recommendations', 'ACTION REQUIRED', '#F3F4F6', text_main, '', '', insight_4, text_main, primary, secondary, bg_color)}
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    """


def _generate_insights_section_mobile(total_sales, mom_growth, mom_icon, mom_badge_bg, mom_badge_color, insight_1, insight_2, insight_3, insight_4, text_main, primary, secondary, bg_color, icon_urls, currency_unit='PKR'):
    """Generate mobile insights stack"""
    return f"""
        <div style="margin-bottom: 16px;">
            {_generate_insight_card(icon_urls['performance'], 'Performance', 'Trend Analysis', 'CRITICAL', '#FFE4E6', '#C10007', 
                f'Total Revenue: <strong style="color: {text_main};">{currency_unit} {total_sales}</strong>', 
                f'MoM Growth: <span style="display: inline-block; background-color: {mom_badge_bg}; color: {mom_badge_color}; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 6px;">{mom_icon} {mom_growth:.1f}%</span>',
                insight_1, text_main, primary, secondary, bg_color)}
        </div>
        <div style="margin-bottom: 16px;">
            {_generate_insight_card(icon_urls['channel'], 'Channel', 'Performance', 'INSIGHT', bg_color, '#B45309', '', '', insight_2, text_main, primary, secondary, bg_color)}
        </div>
        <div style="margin-bottom: 16px;">
            {_generate_insight_card(icon_urls['growth'], 'Growth', 'Opportunity', 'OPPORTUNITY', '#ECFDF5', '#10B981', '', '', insight_3, text_main, primary, secondary, bg_color)}
        </div>
        <div>
            {_generate_insight_card(icon_urls['strategic'], 'Strategic', 'Recommendations', 'ACTION REQUIRED', '#F3F4F6', text_main, '', '', insight_4, text_main, primary, secondary, bg_color)}
        </div>
    """
