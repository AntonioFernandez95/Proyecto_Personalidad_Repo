import reflex as rx
from Personalidad.pages.academia.layout import academia_layout, small_card, back_button
from Personalidad.states.fisicas_state import FisicasState
from Personalidad.states.calculadora_state import CalculadoraState

@rx.page(route="/academia/fisicas", title="Academia Online - Pruebas Físicas", on_load=CalculadoraState.check_login)
def fisicas() -> rx.Component:
    return academia_layout(
        rx.text("CURSO PRUEBAS FÍSICAS", font_size="2em", font_weight="900", color="white", letter_spacing="0.1em"),
        rx.text("Selecciona un módulo para comenzar", font_size="1em", color="rgba(255,255,255,0.75)"),
        rx.grid(
            small_card("play-circle",   "Presentación",     "Introducción al curso",  "Ver módulo", "/academia/curso"),
            small_card("dumbbell",      "Técnica",          "Ejecución de pruebas",   "Entrar",     "/academia/tecnica"),
            small_card("calendar-days", "Planificación",    "Planes y tablas PDF",    "Abrir",      "/academia/planificacion"),
            small_card("calculator",    "Calculadora Apto", "Calcula tu resultado",   "Calcular",   "/academia/calculadora"),
            columns="2", spacing="4", width="100%", max_width="620px",
        ),
        back_button(label="← Volver al inicio", href="/academia"),
        align="center", padding_top="2em", spacing="4",
    )
