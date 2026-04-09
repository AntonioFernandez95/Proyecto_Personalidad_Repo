import reflex as rx
from Personalidad.pages.academia.layout import academia_layout, big_card
from Personalidad.states.base_state import State

@rx.page(route="/academia", title="Academia Online - Dashboard", on_load=State.check_login)
def index() -> rx.Component:
    return academia_layout(
        rx.vstack(
            rx.text(rx.text.span("👋 BIENVENIDO, "), rx.text.span(State.user), font_size="1.15em", color="rgba(255,255,255,0.85)", font_weight="700", letter_spacing="0.1em"),
            rx.text("ACADEMIA ONLINE", font_size="2.8em", font_weight="900", color="white", letter_spacing="0.1em"),
            rx.text("Selecciona tu área de entrenamiento", font_size="1.05em", color="rgba(255,255,255,0.8)"),
            align="center", spacing="1", margin_bottom="1.5em",
        ),
        rx.hstack(
            big_card("brain",           "TEST DE PERSONALIDAD", "Historial y nuevos simulacros", "Comenzar Test",    "/academia/historial"),
            # RESTRICCIÓN: Solo se muestra la tarjeta de Físicas si el usuario tiene acceso (plan contratado o admin)
            rx.cond(
                State.has_fisicas_access,
                big_card("person-standing", "PRUEBAS FÍSICAS",      "Curso completo y herramientas", "Acceder al Curso", "/academia/fisicas"),
            ),
            spacing="6", wrap="wrap", justify="center",
        ),
    )