import reflex as rx
from .layout import academia_layout, OLIVE, TEXT_MID, back_button, CARD_STYLE
from .state import AcademiaState

@rx.page(route="/academia/simulacro", title="Academia Online - Simulacro Presencial", on_load=AcademiaState.check_login)
def simulacro() -> rx.Component:
    return academia_layout(
        rx.text("SIMULACRO PRESENCIAL", font_size="2.2em", font_weight="900", color="white", letter_spacing="0.1em"),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("map-pin", size=24, color=OLIVE),
                    rx.text("PRÓXIMA CONVOCATORIA", font_size="1.2em", font_weight="800", color=OLIVE),
                    spacing="2", align="center",
                ),
                rx.divider(),
                rx.hstack(
                    rx.vstack(
                        rx.text("Fecha:", font_weight="700", color="black"),
                        rx.text("25 de Abril, 2026", color=TEXT_MID),
                        align="start", spacing="0",
                    ),
                    rx.spacer(),
                    rx.vstack(
                        rx.text("Ubicación:", font_weight="700", color="black"),
                        rx.text("Centro Deportivo Municipal", color=TEXT_MID),
                        align="start", spacing="0",
                    ),
                    width="100%",
                ),
                rx.text(
                    "El simulacro presencial recrea las condiciones reales de examen "
                    "con jueces federados y cronometraje electrónico oficial.",
                    font_size="0.95em", color=TEXT_MID, margin_top="1em",
                ),
                rx.button(
                    "RESERVAR PLAZA",
                    background=OLIVE, color="white", border_radius="8px",
                    padding="0.8em 2em", font_weight="700", width="100%",
                    margin_top="1.5em",
                    _hover={"transform": "scale(1.02)", "background": "#3E5228"},
                ),
                spacing="3", align="start",
            ),
            **CARD_STYLE, padding="2.5em", width="100%", max_width="600px",
        ),
        back_button(label="← Volver al inicio", href="/academia"),
        align="center", spacing="4", padding_top="3em",
    )
