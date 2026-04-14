"""
Configuration and Table Settings for Sales Report Automation
"""

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


# Professional color palette
COLORS = {
    'primary': '#4F46E5',
    'secondary': '#7C3AED',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'info': '#3B82F6',
    'chart_palette': ['#4F46E5', '#7C3AED', '#EC4899', '#F59E0B', '#10B981', '#3B82F6', '#8B5CF6', '#06B6D4']
}

# Country/Timezone/Currency Dictionary
COUNTRY_CONFIG = {
    'PK': {'timezone': 'Asia/Karachi', 'currency': 'PKR'},
    'SA': {'timezone': 'Asia/Riyadh', 'currency': 'SAR'},
    'AE': {'timezone': 'Asia/Dubai', 'currency': 'AED'},
    'UK': {'timezone': 'Europe/London', 'currency': 'GBP'},
    'US': {'timezone': 'America/New_York', 'currency': 'USD'},
}
