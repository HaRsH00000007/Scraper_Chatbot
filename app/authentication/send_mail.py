import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings

def send_email_smtp(to_email: str, subject: str, body: str):
    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = settings.MAIL_PORT

    # SMTP user configuration
    smtp_username = settings.MAIL_USERNAME
    smtp_password = settings.MAIL_PASSWORD

    if not smtp_username or not smtp_password:
        raise ValueError("SMTP username or password is not set in environment variables")

    # Create the email
    message = MIMEMultipart()
    message["From"] = smtp_username
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)

    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=401, detail="Authentication failed. Check your email credentials.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

