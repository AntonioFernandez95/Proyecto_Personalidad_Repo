import os

# Configuración de la Base de Datos
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "db_personalidad_proyecto")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Prefor2026!")
DB_PORT = os.getenv("DB_PORT", "5432")

# Configuración del servidor de Email (SMTP)
EMAIL_SENDER = "metodos@academiametodos.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "*Agentes_010?")
EMAIL_SERVER = "smtp.office365.com"
EMAIL_PORT = 587
