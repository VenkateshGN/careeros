import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger("careeros.email")

def send_password_reset_email(to_email: str, token: str) -> bool:
    frontend_url = os.getenv("FRONTEND_URL", "https://careeros-psi-seven.vercel.app").rstrip("/")
    reset_link = f"{frontend_url}/reset-password?token={token}&email={to_email}"

    logger.info(f"=== PASSWORD RESET LINK GENERATED FOR {to_email} ===")
    logger.info(reset_link)
    logger.info("==================================================")

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("SENDER_EMAIL", smtp_username or "noreply@careeros.com")

    # If no SMTP configured, we skip but return True (printed to log)
    if not smtp_username or not smtp_password:
        logger.warning("SMTP credentials not configured in .env. Reset email not sent, printed reset link above.")
        return True

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = "Reset Your CareerOS Password"

        body = f"""
        Hi there,

        We received a request to reset your CareerOS password. Click the link below to choose a new password:

        {reset_link}

        If you did not request a password reset, you can ignore this email.

        Thanks,
        The CareerOS Team
        """
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        logger.info(f"Password reset email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False
