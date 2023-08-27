import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = 'GuardinhaDoPP@outlook.com'
SENDER_PASSWORD = 'umaSenhaMuitoBoa123!'

def send_email(recipient_email, subject, message):
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    try:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
    except Exception as e:
        raise Exception("Não foi possível enviar o email, tente novamente mais tarde")
    finally:
        server.quit()

