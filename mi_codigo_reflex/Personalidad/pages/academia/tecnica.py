import reflex as rx
from .layout import academia_layout, prueba_row, back_button
from .state import AcademiaState

@rx.page(route="/academia/tecnica", title="Academia Online - Técnica", on_load=AcademiaState.check_login)
def tecnica() -> rx.Component:
    return academia_layout(
        rx.text("TÉCNICA DE PRUEBAS FÍSICAS", font_size="2em", font_weight="900", color="white"),
        rx.vstack(
            prueba_row("hand-metal", "Flexo-extensiones de brazos",   "/academia/tecnica/flexiones"),
            prueba_row("timer",      "Plancha isométrica",             "/academia/tecnica/flexiones"),
            prueba_row("zap",        "Circuito de agilidad-velocidad", "/academia/tecnica/flexiones"),
            prueba_row("footprints", "Carrera de 2000 metros",         "/academia/tecnica/flexiones"),
            spacing="3", width="100%", max_width="720px",
        ),
        back_button(),
        align="center", spacing="4", padding_top="2em", width="100%",
    )
