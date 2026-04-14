"""
Configuration and Table Settings for Sales Report Automation
Dynamically loads theme from theme_config.json
"""

import json


def load_theme_config(config_path='theme_config.json'):
    """Load theme configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load theme_config.json: {e}")
        return {}


# Load theme configuration at module level
THEME_CONFIG = load_theme_config()


class ThemeColors:
    """Theme colors loaded dynamically from theme_config.json"""
    
    _theme = THEME_CONFIG.get('theme', {})
    
    # Primary theme colors
    PRIMARY = _theme.get('primary', '#4F46E5')
    SECONDARY = _theme.get('secondary', '#7C3AED')
    BACKGROUND = _theme.get('background', '#FFFFFF')
    TEXT_MAIN = _theme.get('text_main', '#333333')
    TEXT_LIGHT = _theme.get('text_light', '#FFFFFF')
    
    # Accent colors
    ACCENT_SUCCESS = _theme.get('accent_success', '#10B981')
    ACCENT_WARNING = _theme.get('accent_warning', '#F59E0B')
    ACCENT_DANGER = _theme.get('accent_danger', '#EF4444')
    
    # Chart palette
    CHART_PALETTE = _theme.get('chart_palette', [
        '#4F46E5', '#7C3AED', '#EC4899', '#F59E0B', 
        '#10B981', '#3B82F6', '#8B5CF6', '#06B6D4'
    ])


class BrandingConfig:
    """Branding configuration loaded from theme_config.json"""
    
    _branding = THEME_CONFIG.get('branding', {})
    
    COMPANY_LOGO_URL = _branding.get('company_logo_url', '')
    SERVICE_PROVIDER_LOGO_URL = _branding.get('service_provider_logo_url', '')
    SHOW_POWERED_BY = _branding.get('show_powered_by', True)


class IconsConfig:
    """Icon URLs loaded from theme_config.json"""
    
    _icons = THEME_CONFIG.get('icons', {})
    _kpi_icons = _icons.get('kpi', {})
    _insight_icons = _icons.get('insights', {})
    
    # KPI Icons
    TOTAL_SALES = _kpi_icons.get('total_sales', '')
    TODAY_SALE = _kpi_icons.get('today_sale', '')
    MOM_GROWTH = _kpi_icons.get('mom_growth', '')
    GROSS_PROFIT = _kpi_icons.get('gross_profit', '')
    AVG_INVOICE = _kpi_icons.get('avg_invoice', '')
    TOTAL_INVOICES = _kpi_icons.get('total_invoices', '')
    
    # Insight Icons
    INSIGHTS_HEADER = _insight_icons.get('header', '')
    PERFORMANCE = _insight_icons.get('performance', '')
    CHANNEL = _insight_icons.get('channel', '')
    GROWTH = _insight_icons.get('growth', '')
    STRATEGIC = _insight_icons.get('strategic', '')


class TableConfig:
    """Configuration for which tables and columns to display"""
    
    TABLES_TO_DISPLAY = {
        0: {
            'title': 'Branch & Performance Summary',
            'columns': ['Branch', 'BranchType', 'Total', 'LastMonthSaleSameDay', 'MonthSale', 'LastMonthSale', 
                       'MonthPercNew', 'AverageSale', 'MonthGP', 'MonthGPPer', 
                       'MonthInvCount', 'RetCount', 'TotalQuantity'],
            'display_names': {
                'BranchType': 'Type',
                'Branch': 'Branch',
                'Total': 'Today Sale',
                'LastMonthSaleSameDay': 'Same Day Last Month',
                'MonthSale': 'MTD Sale',
                'LastMonthSale': 'Last MTD Sale',
                'MonthPercNew': 'MoM %',
                'AverageSale': 'Daily Avg Sale',
                'MonthGP': 'Gross Profit',
                'MonthGPPer': 'GP %',
                'MonthInvCount': 'Invoices',
                'RetCount': 'Returns',
                'TotalQuantity': 'Qty Sold'
            },
            'numeric_cols': ['Total', 'LastMonthSaleSameDay', 'MonthSale', 'LastMonthSale', 'MonthPercNew', 'AverageSale', 'MonthGP', 'MonthGPPer', 'MonthInvCount', 'RetCount', 'TotalQuantity']
        },
        2: {
            'title': 'Debtor & Receivables',
            'columns': ['Branch', 'BranchType', 'DebtorGroup', 'Sale', 'SaleReturn', 'NetSale'],
            'display_names': {
                'Branch': 'Branch',
                'BranchType': 'Type',
                'DebtorGroup': 'Debtor Type',
                'Sale': 'Sale Amount',
                'SaleReturn': 'Returns',
                'NetSale': 'Net Sale'
            },
            'numeric_cols': ['Sale', 'SaleReturn', 'NetSale']
        },
        3: {
            'title': 'Category Performance',
            'columns': ['Category', 'MonthSale','LastMonthSale','MonthPer', 'AverageSale', 'CurrentMonthDiff',
                       'MonthGPPer', 'CategoryShareMonth'],
            'display_names': {
                'Category': 'Category',
                'MonthSale': 'MTD Sale',
                'LastMonthSale': "Last MTD Sale",
                'AverageSale': 'Daily Avg Sale',
                'CurrentMonthDiff': 'MoM Diff',
                'MonthPer': 'MoM %',
                'MonthGPPer': 'GP %',
                'CategoryShareMonth': 'Category Share'
            },
            'numeric_cols': ['MonthSale','LastMonthSale','MonthPer', 'AverageSale', 'CurrentMonthDiff', 'MonthGPPer', 'CategoryShareMonth']
        },
        4: {
            'title': 'Customer & Sales Type Summary',
            'columns': ['SaleType', 'TotalAmount', 'NoInv', 'NewCount', 'OldCount',
                       'NewAmount', 'OldAmount', 'WCAmount'],
            'display_names': {
                'SaleType': 'Sale Type',
                'TotalAmount': 'Total Amount',
                'NoInv': 'Invoices',
                'NewCount': 'New Customers',
                'OldCount': 'Existing',
                'NewAmount': 'New Sales',
                'OldAmount': 'Existing Sales',
                'WCAmount': 'Wallet Credit',
            },
            'numeric_cols': ['TotalAmount', 'NoInv', 'NewCount', 'OldCount', 'NewAmount', 'OldAmount', 'WCAmount']
        }
    }


# Professional color palette - dynamically loaded from theme
COLORS = {
    'primary': ThemeColors.PRIMARY,
    'secondary': ThemeColors.SECONDARY,
    'success': ThemeColors.ACCENT_SUCCESS,
    'warning': ThemeColors.ACCENT_WARNING,
    'danger': ThemeColors.ACCENT_DANGER,
    'info': '#3B82F6',
    'chart_palette': ThemeColors.CHART_PALETTE
}
