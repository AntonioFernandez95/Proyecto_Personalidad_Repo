import reflex as rx
import os

config = rx.Config(
    app_name="Personalidad",
    # Intenta poner la IP de tu máquina si localhost falla, 
    # pero para Reflex en Docker lo ideal es:
    api_url=os.getenv("REFLEX_API_URL", "http://localhost:8000"), 
    db_url=os.getenv("DATABASE_URL", "postgresql://postgres:Prefor2026!@db:5432/db_personalidad_proyecto"),
)