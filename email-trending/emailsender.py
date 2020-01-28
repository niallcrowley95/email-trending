import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Error(Exception):
    """Base class for other exceptions"""
    pass


class ToManySenders(Error):
    """Raised when error in scraping article"""
    pass


def send_email(sender, sender_pwd, to_list, html_content, subject):
    """Sends email from gmail account
    Params (required):
    - sender: from email address
    - sender_pwd: from password
    - to_list: list of email recipient addresses
    - html_content: email body content
    - subject: email subject
    """
    sender_email = sender
    password = sender_pwd

    if len(to_list) > 10:
        logging.warning("Sender list cannot be greater than 10")
        raise ToManySenders("Sender list cannot be greater than 10")

    for receiver in to_list:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver.strip()

        # Create the plain-text and HTML version of message
        text = "HTML content cannot be displayed"
        html = html_content

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email,
                            receiver,
                            message.as_string())
