# /var/www/html/PersonalidadCompleto/gunicorn_config.py

import os
import sys

# Añadir el directorio del proyecto a sys.path
sys.path.append('/var/www/html/PersonalidadCompleto')

# Configuración general de Gunicorn
bind = '0.0.0.0:8000'
workers = 3