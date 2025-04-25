# email_alerts.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(platform, search_term, results):
    EMAIL_FROM = os.environ.get("EMAIL_FROM")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    EMAIL_TO = os.environ.get("EMAIL_TO")

    if not EMAIL_FROM or not EMAIL_PASSWORD or not EMAIL_TO:
        print("Email credentials not fully set in environment variables.")
        return

    subject = f"New {platform} listings for '{search_term}'"
    body = "\n\n".join([
        f"Title: {r['title']}\nPrice: {r['price']}\nURL: {r['url']}" for r in results
    ])

    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        print(f"Email sent to {EMAIL_TO} with {len(results)} new listings.")
    except Exception as e:
        print(f"Failed to send email: {e}")
