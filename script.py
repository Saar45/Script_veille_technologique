import feedparser
import pandas as pd
from email.message import EmailMessage
import ssl
import smtplib
from pretty_html_table import build_table
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

RSS_URLS = ['https://cloudblogs.microsoft.com/quantum/feed', 'https://quantumcomputingreport.com/feed/']
data = {"Titre Article": [], "URL": [], "Date de publication": []}

for url in RSS_URLS:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        data["Titre Article"].append(entry.title)
        data["URL"].append(entry.link)
        data["Date de publication"].append(entry.published)

df = pd.DataFrame(data)

def send_email(df):
    #Set the sender infos 
    email_sender = "example@gmail.com"
    email_password = "passwordHere" 
    email_receiver = "example@gmail.com" #Receiver email

    subject = "Weekly RSS Feed - Quantum Computing"

    html = f"""
    <html>
    <head>
    </head>

    <body>
            {build_table(df, 'green_dark', text_align='center')}
    </body>

    </html>
    """

    body = MIMEText(html, "html")

    em = EmailMessage()

    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject

    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

send_email(df)



