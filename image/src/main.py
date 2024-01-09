import csv
import email.message
import json
import os
import smtplib


EMAIL_SUBJECT = 'STORI CHALLENGE'


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
        with open("transactions.csv", "r") as csv_file:
            total_balance = 0
            average_debit = 0
            average_credit = 0
            transactions_by_month = {}
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                date = row.get('Date')
                month_number = date.split('/')[0]
                month_name = self.months[month_number]

                transactions_by_month[month_name] = transactions_by_month.get(month_name, 0) + 1
                total_balance += float(row.get("Transaction", 0))

                row_transaction = float(row.get("Transaction", 0))
    
                if row_transaction > 0:
                    average_debit += float(row.get("Transaction", 0))
                else:
                    average_credit = float(row.get("Transaction", 0))

        
        transactions_resume = {
            'average_debit': average_debit,
            'average_credit': average_credit,
            'total_balance': average_debit + average_credit,
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

    return {
        'statusCode': 200,
        'body': 'email sended'
    }