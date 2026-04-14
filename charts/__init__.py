"""
Chart.js data generators for sales report visualizations
"""

import json
import logging

logger = logging.getLogger(__name__)


def generate_branch_chart_data(all_tables_data, find_table_func):
    """Generate Chart.js branch performance chart data"""
    try:
        if not all_tables_data or len(all_tables_data) == 0:
            return ""

        signature_cols = ['Branch', 'MonthSale', 'MonthGP']
        table_idx = find_table_func(signature_cols)
        if table_idx is None:
            return ""
        first_table = all_tables_data[table_idx]['data']

        def clean_num(v):
            if v is None or v == '': return 0
            try: return float(str(v).replace(',', ''))
            except: return 0
        
        branches_data = []
        for row in first_table:
            branch = str(row.get('Branch', 'N/A')).strip()
            if branch.lower() in ['sub total', 'subtotal']:
                continue

            month_sale = clean_num(row.get('MonthSale', 0))
            last_month_sale = clean_num(row.get('LastMonthSale', 0))
            branches_data.append({
                'branch': branch,
                'this_month': month_sale,
                'last_month': last_month_sale
            })
        
        branches_data.sort(key=lambda x: x['this_month'], reverse=True)
        top_5 = branches_data[:5]
        
        if not top_5:
            return ""
        
        chart_data = {
            'labels': [b['branch'] for b in top_5],
            'this_month': [b['this_month'] for b in top_5],
            'last_month': [b['last_month'] for b in top_5]
        }
        
        return json.dumps(chart_data)
    except Exception as e:
        logger.error(f"Error generating branch chart data: {str(e)}")
        return ""


def generate_channel_chart_data(all_tables_data, find_table_func):
    """Generate Chart.js sales channel chart data"""
    try:
        signature_cols = ['SaleType', 'TotalAmount']
        table_idx = find_table_func(signature_cols)
        if table_idx is None:
            return ""
            
        channel_table = all_tables_data[table_idx]['data']
        
        def clean_num(v):
            if v is None or v == '': return 0
            try: return float(str(v).replace(',', ''))
            except: return 0
        
        channel_data = {}
        for row in channel_table:
            channel = row.get('SaleType', 'Other')
            sales = clean_num(row.get('TotalAmount', 0))
            quantity = clean_num(row.get('NoInv', 0))
            if channel in channel_data:
                channel_data[channel]['sales'] += sales
                channel_data[channel]['quantity'] += quantity
            else:
                channel_data[channel] = {'sales': sales, 'quantity': quantity}
        
        if not channel_data:
            return ""
        
        sorted_channels = sorted(channel_data.items(), key=lambda x: x[1]['sales'], reverse=True)
        
        chart_data = {
            'labels': [item[0] for item in sorted_channels],
            'sales': [item[1]['sales'] for item in sorted_channels],
            'quantities': [item[1]['quantity'] for item in sorted_channels],
            'amounts': [item[1]['sales'] for item in sorted_channels]
        }
        
        return json.dumps(chart_data)
    except Exception as e:
        logger.error(f"Error generating channel chart data: {str(e)}")
        return ""


def generate_category_chart_data(all_tables_data, find_table_func):
    """Generate Chart.js category performance chart data"""
    try:
        signature_cols = ['Category', 'CategoryShareMonth']
        table_idx = find_table_func(signature_cols)
        if table_idx is None:
            return ""
        category_table = all_tables_data[table_idx]['data']
        
        def clean_num(v):
            if v is None or v == '': return 0
            try: return float(str(v).replace(',', ''))
            except: return 0
        
        categories = []
        sales = []
        
        for row in category_table[:8]:
            cat = row.get('Category', 'N/A')
            sale = clean_num(row.get('MonthSale', 0))
            if sale > 0:
                categories.append(cat[:25])
                sales.append(sale)
        
        if not categories:
            return ""
        
        chart_data = {
            'labels': categories,
            'sales': sales
        }
        
        return json.dumps(chart_data)
    except Exception as e:
        logger.error(f"Error generating category chart data: {str(e)}")
        return ""
