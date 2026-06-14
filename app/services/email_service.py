import smtplib
import logging
from email.mime.text import MIMEText

from app.core.config import settings

logger = logging.getLogger(__name__)


def send_recovery_email(email: str, token: str) -> bool:
    if not settings.SMTP_HOST:
        logger.info("SMTP no configurado. Token para %s: %s", email, token)
        return True

    reset_link = f"http://localhost:5173/restablecer?token={token}"
    body = (
        f"Usá este enlace para restablecer tu contraseña:\n\n"
        f"{reset_link}\n\n"
        f"Si no solicitaste esto, ignorá este mensaje."
    )

    msg = MIMEText(body)
    msg["Subject"] = "Recuperación de contraseña - AdoptAR"
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = email

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        logger.info("Email de recuperación enviado a %s", email)
        return True
    except Exception as e:
        logger.error("Error al enviar email a %s: %s", email, e)
        return False
