# Personalidad.py
from Personalidad.pages import login, test, info, results, academia
from Personalidad.styles.styles import BASE_STYLE, STYLESHEETS
import reflex as rx

# Define the app with the given theme and styles
app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="tomato"
    ),
    stylesheets=STYLESHEETS,
    style=BASE_STYLE,
)
