import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Personalidad.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_SERVER, EMAIL_PORT
from Personalidad.constants import AUTHORIZED_DOMAINS, TEST_EMAILS

def is_authorized_email(email: str) -> bool:
    """Verifica si el email pertenece a un dominio autorizado."""
    email_lower = email.lower()
    return (
        any(email_lower.endswith(domain) for domain in AUTHORIZED_DOMAINS) or 
        email_lower in TEST_EMAILS
    )

def _send_email_base(to_email: str, subject: str, body: str, html_content: str):
    """Función base para envío de correos SMTP."""
    if not is_authorized_email(to_email):
        print(f"Envío abortado: {to_email} no está en dominios autorizados.")
        return False

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = EMAIL_SENDER
    message["To"] = to_email

    message.attach(MIMEText(body, "plain"))
    message.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_email, message.as_string())
        print(f"Email '{subject}' enviado con éxito a {to_email}")
        return True
    except Exception as e:
        print(f"Error enviando email a {to_email}: {e}")
        return False

def send_credentials_email(email: str, password: str):
    """Envía las credenciales de acceso inicial."""
    subject = 'Acceso Test de Personalidad - Academia Métodos'
    body = f"Tu usuario: {email}\nTu contraseña: {password}"
    html = f"<html><body><p>Usuario: <b>{email}</b></p><p>Contraseña: <b>{password}</b></p></body></html>"
    return _send_email_base(email, subject, body, html)

def send_recovery_email(email: str, password: str):
    """Envía un correo de recuperación de contraseña."""
    subject = 'Recuperación de Contraseña - Academia Métodos'
    body = f"Hola,\n\nHas solicitado recuperar tu contraseña.\nTu contraseña actual es: {password}"
    html = f"""
    <html>
        <body>
            <h3>Recuperación de acceso</h3>
            <p>Has solicitado recuperar tu contraseña para el Test de Personalidad.</p>
            <p>Tu contraseña es: <b>{password}</b></p>
            <p>Ya puedes volver a la web e iniciar sesión.</p>
        </body>
    </html>
    """
    return _send_email_base(email, subject, body, html)
