import csv
import os
import uuid
from datetime import datetime

CSV_FILE_PATH = "reports.csv"

def generate_report_id():
    return str(uuid.uuid4())

def log_report(report_id, client_name, dt_str, status_or_html):
    """
    Appends a record to the reports.csv file.
    Columns: Unique report ID, Client Name, Datetime, Status
    """
    file_exists = os.path.isfile(CSV_FILE_PATH)
    
    with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Unique report ID', 'Name of the client', 'datetime', 'Full report HTML Code or Error as output'])
        writer.writerow([report_id, client_name, dt_str, status_or_html])
