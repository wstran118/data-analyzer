# Finance Data Processing Pipeline

## Overview

The Finance Data Processing Pipeline automates the extraction, transformation, and reporting of financial data from a SQL database. It handles data cleaning, aggregation, backup, and automated monitoring with email notifications.

## Features

Automated data extraction from SQL databases.

Data transformation and aggregation.

Backup and archiving of reports.

Automated email notifications on pipeline success or failure.

Logging for monitoring and troubleshooting.

## Prerequisites

- Python 3.8+

- ODBC Driver 17 for SQL Server

- Pandas library

- PyODBC library

- SMTP server for email notifications

- Zip utility for backup

## Installation

1. Clone the repository:
````
git clone https://github.com/yourusername/finance-data-pipeline.git
cd finance-data-pipeline
````
2. Install required Python packages:
````
pip install pandas pyodbc
````


## Configuration

Update the following variables in the script:

- Database settings:
````
server = 'YOUR_SERVER_NAME'
database = 'YOUR_DATABASE_NAME'
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'
````
- Backup settings:
````
backup_dir = '/path/to/backup/'
````
- Email settings:
````
smtp_server = 'smtp.example.com'
sender_email = 'no-reply@example.com'
receiver_email = 'admin@example.com'
````

## Running the Pipeline

Execute the script:
````
python pipeline_script.py
````
## Output

- Extracted data: financial_data.csv

- Transformed data: financial_report.csv

- Backup file: backup_YYYYMMDD.zip

- Log file: pipeline_log.txt

## Automation

### Linux (Cron Job)

Add the script to cron to run daily at 2 am:
````
crontab -e
````
Add:
````
0 2 * * * /usr/bin/python3 /path/to/pipeline_script.py
````
### Windows (Task Scheduler)

1. Open Task Scheduler

2. Create a new task with daily trigger

3. Action: Start a program

4. Program/script: python

5. Arguments: C:\path\to\pipeline_script.py

## Troubleshooting

Database Connection Issues: Check database credentials and ODBC driver.

Email Not Sent: Verify SMTP settings and network access.

File Not Created: Check write permissions and directory paths.

Backup Fails: Ensure the zip utility is properly installed.

## License

This project is licensed under the MIT License