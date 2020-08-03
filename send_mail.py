import smtplib
from email.mime.text import MIMEText


def send_mail(name, number, date, message):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '147458d6d065d8'
    password = 'e57c37b34cb554'
    message = f"<h3>New Customer Submission</h3><ul><li>Name: {name}</li><li>People: {number}</li><li>Date: {date}</li><li>Message: {message}</li></ul>"

    sender_email = 'email3@example.com'
    receiver_email = 'email4@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Catering Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
