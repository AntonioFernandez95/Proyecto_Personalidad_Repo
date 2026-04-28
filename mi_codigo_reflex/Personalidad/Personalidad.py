import reflex as rx
from Personalidad.states.login_state import LoginState
from Personalidad.states.calculadora_state import CalculadoraState
from Personalidad.states.historial_state import HistorialSimplificado_State
from Personalidad.states.results_state import ResultsState
from Personalidad.states.fisicas_state import FisicasState
from Personalidad.states.test_state import TestState
from Personalidad.pages import login, test, info, results, academia
from Personalidad.pages.academia import admin_panel, admin_plans
from Personalidad.states.admin_state import AdminState
from Personalidad.styles.styles import BASE_STYLE, STYLESHEETS

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

# Registramos el endpoint de API directo
# (Se eliminó calculo_router por no existir el archivo calculo_api.py)
