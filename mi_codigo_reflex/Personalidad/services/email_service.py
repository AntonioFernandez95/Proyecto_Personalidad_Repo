import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Personalidad.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_SERVER, EMAIL_PORT
from Personalidad.constants import AUTHORIZED_DOMAINS, TEST_EMAILS


def is_authorized_email(email: str) -> bool:
    """Verifica si el email pertenece a un dominio autorizado (DESACTIVADO PARA PERMITIR TODOS)."""
    return True


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


def send_credentials_email(email: str, password: str, full_name: str = "Alumno"):
    """Envía las credenciales de acceso inicial con el nuevo diseño profesional."""
    subject = '¡Bienvenido a Academia Métodos! - Tus credenciales'
    body = f"¡Bienvenido {full_name}!\n\nTu usuario: {email}\nTu contraseña: {password}\nAcceso: http://tropa.academiametodos.com"
   
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: 'Roboto', sans-serif; font-size: 14px; color: #333333; line-height: 1.6; }}
            .container {{ text-align: center; max-width: 600px; margin: 0 auto; border: 1px solid #eee; padding: 20px; border_radius: 10px; }}
            .logo {{ display: block; margin: 0 auto; max-width: 250px; width: 100%; }}
            .welcome {{ font-weight: bold; font-size: 18px; color: #5B733A; margin-top: 20px; text-transform: uppercase; }}
            .link {{ color: #FC4F00; font-weight: bold; text-decoration: none; }}
            table {{ width: auto; border-collapse: collapse; margin: 25px auto; background-color: #f9f9f9; }}
            table, th, td {{ border: 1px solid #ddd; }}
            th, td {{ padding: 12px 20px; text-align: left; }}
            th {{ background-color: #5B733A; color: white; font-weight: bold; }}
            .social img {{ max-width: 35px; margin: 0 10px; }}
            .contact-info {{ color: #FC4F00; font-weight: bold; }}
            .legal-cell {{ text-align: justify; background-color: #FAFAFA; font-size: 11px; color: #666; padding: 15px; border-top: 3px solid #FC4F00; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <img class="logo" src="http://tropa.academiametodos.com/Logo_tumbado.png" alt="Academia Métodos">
            <p class="welcome">¡BIENVENIDO {full_name.upper()}!</p>
            <p>Te damos la bienvenida a <b>Métodos</b>. Con estos datos podrás acceder al curso a través del siguiente enlace:</p>
            <p><a class="link" href="http://tropa.academiametodos.com">ACCEDER A LA PLATAFORMA</a></p>
            <table>
                <tr>
                    <th>Tu usuario</th>
                    <td>{email}</td>
                </tr>
                <tr>
                    <th>Tu contraseña</th>
                    <td>{password}</td>
                </tr>
            </table>
            <p>Si tienes algún problema puedes contactar con nosotros en <span class="contact-info">metodos@academiametodos.com</span> o llamando al <span class="contact-info">954 650 700</span>.</p>
            <p>Antes de comenzar, te recomendamos que revises la <b>guía de uso</b> del curso que encontrarás al entrar en él.</p>
            <br>
            <div class="social">
                <a href="https://www.facebook.com/academiametodos/"><img src="http://tropa.academiametodos.com/FB.png" alt="FB"></a>
                <a href="https://www.instagram.com/academiametodos/"><img src="http://tropa.academiametodos.com/INSTA.png" alt="IG"></a>
                <a href="https://www.youtube.com/channel/UC9yYj498kx_vUxlX-R5ne1A"><img src="http://tropa.academiametodos.com/YOUTUBE.png" alt="YT"></a>
            </div>
            <div class="legal-cell">
                <b>AVISO LEGAL:</b> Por motivos de seguridad, las claves son secretas y para uso privado. Este mensaje es confidencial. Si lo ha recibido por error, por favor notifíquelo a metodos@academiametodos.com. Queda prohibida la distribución o copia de este mensaje.
            </div>
        </div>
    </body>
    </html>
    """
    return _send_email_base(email, subject, body, html)


def send_recovery_email(email: str, password: str):
    """Envía un correo de recuperación de contraseña con el diseño corporativo."""
    subject = 'Recuperación de Contraseña - Academia Métodos'
    body = f"Has solicitado recuperar tu contraseña.\nTu contraseña actual es: {password}"
   
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <style>
            body {{ font-family: 'Roboto', sans-serif; font-size: 14px; color: #333333; }}
            .container {{ text-align: center; max-width: 600px; margin: 0 auto; border: 1px solid #eee; padding: 20px; }}
            .header {{ font-weight: bold; font-size: 18px; color: #FC4F00; margin-top: 20px; }}
            .pass-box {{ background-color: #5B733A; color: white; padding: 15px; font-size: 20px; font-weight: bold; display: inline-block; margin: 20px 0; border_radius: 5px; }}
            .link {{ color: #5B733A; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="http://tropa.academiametodos.com/Logo_tumbado.png" width="200">
            <p class="header">RECUPERACIÓN DE ACCESO</p>
            <p>Has solicitado recuperar tu contraseña para el Test de Personalidad de Métodos.</p>
            <p>Tu contraseña de acceso es:</p>
            <div class="pass-box">{password}</div>
            <p>Ya puedes volver a la web e iniciar sesión:</p>
            <p><a class="link" href="http://tropa.academiametodos.com">Volver a la Academia</a></p>
        </div>
    </body>
    </html>
    """
    return _send_email_base(email, subject, body, html)


def send_access_extended_email(email: str, new_expiration: str, full_name: str = "Alumno"):
    """Envía una notificación de que el acceso a la plataforma ha sido ampliado."""
    subject = '¡Tu acceso a la plataforma ha sido renovado! - Academia Métodos'
    body = f"¡Hola {full_name}!\n\nTe informamos de que tu acceso a la plataforma ha sido ampliado hasta el {new_expiration}.\n\nYa puedes seguir practicando: http://tropa.academiametodos.com"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: 'Roboto', sans-serif; font-size: 14px; color: #333333; line-height: 1.6; }}
            .container {{ text-align: center; max-width: 600px; margin: 0 auto; border: 1px solid #eee; padding: 20px; border-radius: 10px; }}
            .logo {{ display: block; margin: 0 auto; max-width: 250px; width: 100%; }}
            .welcome {{ font-weight: bold; font-size: 18px; color: #5B733A; margin-top: 20px; text-transform: uppercase; }}
            .link {{ color: #FC4F00; font-weight: bold; text-decoration: none; }}
            .info-box {{ background-color: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin: 25px auto; max-width: 80%; border-radius: 5px; }}
            .date {{ font-size: 16px; color: #5B733A; font-weight: bold; }}
            .social img {{ max-width: 35px; margin: 0 10px; }}
            .contact-info {{ color: #FC4F00; font-weight: bold; }}
            .legal-cell {{ text-align: justify; background-color: #FAFAFA; font-size: 11px; color: #666; padding: 15px; border-top: 3px solid #FC4F00; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <img class="logo" src="http://tropa.academiametodos.com/Logo_tumbado.png" alt="Academia Métodos">
            <p class="welcome">¡ACCESO RENOVADO, {full_name.upper()}!</p>
            <p>Te informamos de que hemos ampliado o renovado tu período de acceso a la plataforma para que puedas seguir preparándote al máximo.</p>
            <div class="info-box">
                <p>Nueva fecha límite de acceso:</p>
                <p class="date">{new_expiration}</p>
            </div>
            <p><a class="link" href="http://tropa.academiametodos.com">SEGUIR ESTUDIANDO AHORA</a></p>
            <p>Si tienes cualquier duda, estamos a tu disposición en <span class="contact-info">metodos@academiametodos.com</span> o en el <span class="contact-info">954 650 700</span>.</p>
            <br>
            <div class="social">
                <a href="https://www.facebook.com/academiametodos/"><img src="http://tropa.academiametodos.com/FB.png" alt="FB"></a>
                <a href="https://www.instagram.com/academiametodos/"><img src="http://tropa.academiametodos.com/INSTA.png" alt="IG"></a>
                <a href="https://www.youtube.com/channel/UC9yYj498kx_vUxlX-R5ne1A"><img src="http://tropa.academiametodos.com/YOUTUBE.png" alt="YT"></a>
            </div>
            <div class="legal-cell">
                <b>AVISO LEGAL:</b> Este correo es confidencial y va dirigido exclusivamente a su destinatario. Si lo ha recibido por error, por favor notifíquelo a metodos@academiametodos.com.
            </div>
        </div>
    </body>
    </html>
    """
    return _send_email_base(email, subject, body, html)
