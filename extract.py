import datetime
import pyodbc
import subprocess
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText

server = "SERVER_NAME"
database = "DATABASE_NAME"
username = "username"
password = "password"
backup_dir = '/path/to/backup'
data_file = 'financial_data.csv'
report_file = 'financial_report.csv'
log_file = 'pipe_log.txt'
smtp_server = 'smtp.ex@bank.com'
receiver_email = 'admin@bank.com'


# Log function
def log_message(message):
    with open(log_file,'a') as file:
        file.write(f"{datetime.datetime.now()}: message+'\n")


# Establishing connection
try:
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};DATABASE={database};'
        f'UID={username},PWD={password};'
    )
    log_message("'Database connection successful")
except Exception as e:
    log_message(f'Error connecting to database: {e}')

# SQL query to extract data
query="""
SELECT transaction_date, account_id, amount, category
FROM financial_transactions
WHERE transaction_date >= '2024-01-01';
"""

# Executing query and fecthing data
try:
    df = pd.read_sql(query,conn)
    log_message('Data extract successfully')

    #Save data to CSV file
    df.to_csv('financial_data.csv', index=False)
    log_message('Data saved to financial_data.csv')
except Exception as e:
    log_message(f'Erorr extracting data: {e}')
finally:
    conn.close()
    log_message('Connection closed')

# Data transformation
try:
    df['amount'] = df['amount'].apply(lambda x: round(x,2))
    df['category'] = df['category'].str.upper()
    log_message('Data transformation completed')
except Exception as e:
    log_message(f'Error during transformation: {e}')

# Data loading
try:
    transformed_data = df.groupby(['category']).agg({'amount': 'sum'}).reset_index()
    transformed_data.to_csv(report_file, index=False)
    log_message('Data loaded to report file')
except Exception as e:
    log_message(f'Error during loading data {e}')

# Backup
try:
    date_stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'backup_{date_stamp}.zip')
    subprocess.run(['zip','-r', backup_path, data_file, report_file])
    log_message(f'Backup created at {backup_path}')
except Exception as e:
    log_message(f'Error during backup {e}')

# Monitor
def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    with smtplib.SMTP(smtp_server) as server:
        server.send_message(msg)

try:
    if os.path.exists(report_file):
        log_message('Report generated successfully. Monitoring complete.')
        send_email('Pipeline Success', 'Financial data processing pipeline completed successfully.')
    else:
        log_message('Report not generated. Monitoring incomplete.')
        send_email('Pipeline Failure', 'Financial data processing pipeline failed to generate')
except Exception as e:
    log_message(f'Error during monitoring: {e}')
    send_email('Pipeline Error', f'An error occured during monitoring: {e}')