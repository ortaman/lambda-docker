import csv
import email.message
import json
import os
import pandas as pd
import psycopg2
import smtplib
import logging

from io import StringIO


logger = logging.getLogger()
logger.setLevel(logging.INFO)


EMAIL_SUBJECT = 'STORI CHALLENGE'
CSV_DIR = 'data/transactions.csv'
DB_TABLE_NAME = 'transactions'


POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_PORT = os.environ['POSTGRES_PORT']


class CSVTransactions:
    months = {
        '1': 'January',
        '2': 'February',
        '3': 'March',
        '4': 'April',
        '5': 'May',
        '6': 'June',
        '7': 'July',
        '8': 'August',
        '9': 'September', 
        '10': 'October',
        '11': 'November',
        '12': 'December',
    }

    def _get_transactions(self):
        with open(CSV_DIR, "r") as csv_file:
            total_balance = 0
            debit_average = 0
            debit_transactions_number =  0
            credit_average = 0
            credit_transactions_number = 0
            transactions_by_month = {}
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                date = row.get('Date')
                month_number = date.split('-')[1]
                month_name = self.months[month_number]

                transactions_by_month[month_name] = transactions_by_month.get(month_name, 0) + 1
                total_balance += float(row.get("Transaction", 0))

                row_transaction = float(row.get("Transaction", 0))
    
                if row_transaction > 0:
                    debit_average += float(row.get("Transaction", 0))
                    debit_transactions_number += 1
                else:
                    credit_average = float(row.get("Transaction", 0))
                    credit_transactions_number += 1

        transactions_resume = {
            'average_debit': debit_average/debit_transactions_number,
            'average_credit': credit_average/credit_transactions_number,
            'total_balance': total_balance,
        }

        return transactions_by_month, transactions_resume


    def _generate_body(self):
        transactions_by_month, transactions_resume = self._get_transactions()

        body = f"""
            <html>
                <head>
                    <link rel="stylesheet">
                </head>
                <body>
                    <img style="max-width: 100%; display: block; margin-left: auto; margin-right: auto;" src="https://man-bucket-test.s3.us-west-1.amazonaws.com/stori_logo.png"/>
                    <h2 style="text-align: center; font-weight: bold">
                        Transactions Summary
                    </h2>
                    <table style="width: 100%; padding: 0px 100px 0px 100px;">
                        <tbody style="font-size: 14px;">
                            <tr>
                                <td style="
                                    text-align: left;
                                    vertical-align: middle;
                                    text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.1);
                                    border-bottom: 1px solid #C1C3D1;
                                    padding: 15px 20px 15px 20px;
                                    width: 50%;">
                                Average debit amount: {transactions_resume['average_debit']}</td>
                                <td style="
                                    text-align: left;
                                    vertical-align: middle;
                                    text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.1);
                                    border-bottom: 1px solid #C1C3D1;
                                    padding: 15px 20px 15px 20px;
                                    width: 50%;">
                                Average credit amount: {transactions_resume['average_credit']} </td>
                            </tr>
                            <tr>
                                <td style="
                                    text-align: left;
                                    vertical-align: middle;
                                    text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.1);
                                    border-bottom: 1px solid #C1C3D1;
                                    padding: 15px 20px 15px 20px;
                                    width: 50%;">
                                Total balance is: {transactions_resume['total_balance']}
                                </td>
                            </tr>
                            <tr>
                        </tbody>
                    </table>
                    <h2 style="text-align: center; font-weight: bold; margin-top: 50px;">
                        Transactions by Month
                    </h2>
                    <table style="width: 100%; padding: 0px 100px 0px 100px;">
                        <tbody style="font-size: 14px;">
                            <tr>
            """


        for transaction in enumerate(transactions_by_month.items()):
            index = transaction[0]
            
            if index % 2 == 0 and index != 0:
                body += "<tr></tr>"
                
            body += f"""
                <td style="
                    text-align: left;
                    vertical-align: middle;
                    text-shadow: -1px -1px 1px rgba(0, 0, 0, 0.1);
                    border-bottom: 1px solid #C1C3D1;
                    padding: 15px 20px 15px 20px;
                    width: 50%;">
                Number of transactions in {transaction[1][0]}: {transaction[1][1]} </td>
            """

        body += """
                            </tr>
                        </tbody>
                    </table>
                    <p style="text-align: center; font-size:12px">
                        Este correo es informativo, favor no responder a esta direccion de correo.
                    </p>
                </body>
            </html>
        """
        return body

    def send_email_smtp(self, emails_to_send):
        msg = email.message.Message()

        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = os.environ['EMAIL_FROM']
        msg['To'] = emails_to_send

        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(self._generate_body())

        with smtplib.SMTP(host=os.environ['EMAIL_HOST'], port=os.environ['EMAIL_PORT']) as server:
            server.starttls()
            server.login(user=os.environ['EMAIL_USER'], password=os.environ['EMAIL_PASS'])

            server.sendmail(
                from_addr=os.environ['EMAIL_FROM'],
                to_addrs=emails_to_send,
                msg=msg.as_string()
            )

    def insert_data_from_file(self):
        try:
            connection = psycopg2.connect(
                database=POSTGRES_DB,
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD
            )

        except psycopg2.OperationalError as exception:
            logger.error("ERROR: Error connecting to the database")
            logger.error(exception)

        df = pd.read_csv(CSV_DIR)
        df.set_index('Id', inplace=True)

        buffer = StringIO()
        df.to_csv(buffer, index_label='Id', header=False)
        buffer.seek(0)

        contents = buffer.getvalue()
        print(contents)

        try:
            cursor = connection.cursor()
            cursor.copy_from(file=buffer, table=DB_TABLE_NAME, sep=',')
            connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            logger.error("ERROR: Inserting data in transactions table")
            logger.error("Error: %s" % error)
            connection.rollback()

        finally:
            if connection is not None:
                connection.close()


def handler(event, context):

    if not event.get('body'):
        return {
            'statusCode': 400,
            'body': 'body empty'
        }

    body = json.loads(event['body'])

    if not body.get('emails'):
        return {
            'statusCode': 400,
            'body': 'emails field empty',
        }
    
    emails_to_send = body['emails']

    csv_transactions = CSVTransactions()
    csv_transactions.send_email_smtp(emails_to_send)
    csv_transactions.insert_data_from_file()

    return {
        'statusCode': 200,
        'body': 'email sended'
    }


# csv_transactions = CSVTransactions()
# csv_transactions.send_email_smtp('ente011@gmail.com')
# csv_transactions.insert_data_from_file()
