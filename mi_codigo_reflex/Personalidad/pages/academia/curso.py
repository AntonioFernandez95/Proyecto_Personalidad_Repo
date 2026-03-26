import reflex as rx
from Personalidad.pages.academia.layout import academia_layout, OLIVE, TEXT_MID, BTN_PRIMARY_BASE, CARD_STYLE, back_button
from Personalidad.states.fisicas_state import FisicasState
from Personalidad.states.calculadora_state import CalculadoraState

@rx.page(route="/academia/curso", title="Academia Online - Curso", on_load=CalculadoraState.check_login)
def curso() -> rx.Component:
    return academia_layout(
        rx.box(
            rx.hstack(
                rx.center(
                    rx.vstack(
                        rx.icon("play-circle", size=52, color="white"),
                        rx.text("Vídeo de Bienvenida", color="white", font_size="0.88em"),
                        align="center",
                    ),
                    background="black", border_radius="12px",
                    width="300px", height="190px", flex_shrink="0",
                ),
                rx.vstack(
                    rx.text("BIENVENIDA AL CURSO", font_size="1.45em", font_weight="800", color=OLIVE),
                    rx.text(
                        "En este curso encontrarás todo lo necesario para superar las pruebas físicas "
                        "de tu oposición. Sigue los módulos en orden para obtener el máximo rendimiento.",
                        color=TEXT_MID, font_size="0.92em",
                    ),
                    rx.vstack(
                        rx.hstack(rx.icon("file-text", size=15, color=OLIVE), rx.text("Normativa de las pruebas",    font_size="0.9em")),
                        rx.hstack(rx.icon("calendar",  size=15, color=OLIVE), rx.text("Calendario de convocatorias", font_size="0.9em")),
                        rx.hstack(rx.icon("pen-line",  size=15, color=OLIVE), rx.text("Proceso de inscripción",      font_size="0.9em")),
                        spacing="2", margin_top="0.5em",
                    ),
                    spacing="3", flex="1",
                ),
                spacing="5", align="start", wrap="wrap",
            ),
            **CARD_STYLE, padding="2em", width="100%", max_width="800px",
        ),
        rx.box(
            rx.vstack(
                rx.text("📣 COMUNIDAD", font_size="1em", font_weight="700", color="black", letter_spacing="0.1em"),
                rx.hstack(
                    rx.button("✈️  Telegram – Grupo Privado", **BTN_PRIMARY_BASE, padding="0.6em 1.4em", width="100%"),
                    rx.button(
                        "💬  WhatsApp – Tutorías",
                        background="#25D366", color="white", border_radius="8px",
                        padding="0.6em 1.4em", font_weight="600",
                        _hover={"background": "#1ebe57"}, width="100%",
                    ),
                    spacing="3", width="100%", wrap="wrap",
                ),
                spacing="3", width="100%",
            ),
            **CARD_STYLE, padding="2em", width="100%", max_width="800px",
        ),
        back_button(),
        align="center", spacing="4", padding_top="2em",
    )
