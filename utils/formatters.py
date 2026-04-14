"""
Utility functions for formatting, calculations, and data processing
"""

import html
import markdown


def format_value(value, col_name):
    """Format values based on column type"""
    if value is None or value == '':
        return ('-', '')
    
    amount_keywords = ['today sale', 'avg_invoice_value', 'sale', 'amount', 'MonthGP', 'cost', 'gp', 'discount', 'price', 'value', 'net', 'total']
    is_amount = any(k in col_name.lower() for k in amount_keywords)
    
    is_percentage = ('perc' in col_name.lower() or 'per' in col_name.lower() or col_name.endswith('%'))
    
    count_keywords = ['count', 'inv', 'quantity', 'person', 'sno']
    is_count = any(k in col_name.lower() for k in count_keywords)
    
    try:
        num_val = float(value) if not isinstance(value, (int, float)) else value
        color_class = ''
        
        if is_percentage:
            if num_val > 0:
                color_class = 'positive'
            elif num_val < 0:
                color_class = 'negative'
            return (f"{num_val:,.2f}%", color_class)
        elif is_amount:
            if col_name == "avg_invoice_value":
                formatted = f"{num_val:,.0f}"
                return (formatted, color_class)
            if num_val >= 1000000 or num_val <= -1000000:
                formatted = f"{num_val/1000000:.1f}M"
            elif num_val >= 1000 or num_val <= -1000:
                formatted = f"{num_val/1000:.0f}K"
            else:
                formatted = f"{num_val:,.0f}"
            
            return (formatted, color_class)
        elif is_count:
            return (f"{int(num_val):,}", color_class)
        else:
            formatted = f"{num_val:,.2f}" if not num_val.is_integer() else f"{int(num_val):,}"
            return (formatted, color_class)
    except:
        return (str(value), '')


def get_trend_indicator(col_name, value):
    """Get visual indicator for trends"""
    if 'perc' not in col_name.lower() or value is None:
        return ''
    
    try:
        num_val = float(value)
        if num_val > 0:
            return '<span style="color: #10B981; font-weight: 800; margin-left: 4px;">↑</span>'
        elif num_val < 0:
            return '<span style="color: #EF4444; font-weight: 800; margin-left: 4px;">↓</span>'
    except:
        pass
    return ''


def calculate_daily_growth(today_sale, last_month_same_day):
    """Calculate daily growth percentage"""
    try:
        today = float(today_sale) if today_sale else 0
        last_month = float(last_month_same_day) if last_month_same_day else 0
        
        if last_month == 0:
            return 0, ''
        
        growth = ((today - last_month) / last_month) * 100
        color_class = 'positive' if growth > 0 else 'negative' if growth < 0 else ''
        return growth, color_class
    except:
        return 0, ''


def clean_number(value):
    """Clean and convert value to float"""
    if value is None or value == '':
        return 0
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).replace(',', '').replace(' ', ''))
    except:
        return 0


def format_time_for_display(time_str: str) -> str:
    """Format time string for display"""
    parts = time_str.split(":")
    hour = int(parts[0])
    suffix = "AM" if hour < 12 else "PM"
    display_hour = hour if 1 <= hour <= 12 else (hour - 12 if hour > 12 else 12)
    return f"{display_hour:02d} {suffix}"


def format_client_name(name: str) -> str:
    """Format client name for display"""
    if not name or not isinstance(name, str):
        return ""
    name = name.replace("_", " ").strip()
    words = name.split()
    formatted_words = []
    for word in words:
        if word[0].islower():
            formatted_words.append(word.capitalize())
        else:
            formatted_words.append(word)
    return " ".join(formatted_words)


def md_to_html(text):
    """Convert markdown text to HTML"""
    if not text:
        return ''
    text = html.escape(text)
    html_text = markdown.markdown(text, extensions=['extra', 'sane_lists'], output_format='html')
    if html_text.startswith('<p>') and html_text.endswith('</p>'):
        html_text = html_text[3:-4]
    return html_text


def calculate_table_totals(table_data, all_columns, table_config):
    """Calculate totals for numeric columns (excluding 'Sub Total' branches)"""
    numeric_cols = table_config.get('numeric_cols', [])
    totals = {}
    
    branch_col = next((col for col in ['Branch', 'BranchType'] if col in all_columns), None)
    if branch_col:
        filtered_data = [
            row for row in table_data
            if str(row.get(branch_col, '')).strip().lower() != 'sub total'
        ]
    else:
        filtered_data = table_data

    for col in numeric_cols:
        if col in all_columns:
            totals[col] = sum(clean_number(row.get(col, 0)) for row in filtered_data)
            
    # Recalculate MOM % correctly if MonthSale and LastMonthSale exist
    for perc_col in ['MonthPercNew', 'MonthPer']:
        if perc_col in all_columns and 'MonthSale' in totals and 'LastMonthSale' in totals:
            last_mtd = totals['LastMonthSale']
            mtd = totals['MonthSale']
            if last_mtd != 0:
                totals[perc_col] = ((mtd - last_mtd) / last_mtd) * 100
            else:
                totals[perc_col] = 0

    return totals
