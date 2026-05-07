import reflex as rx
from Personalidad.pages.academia.layout import academia_layout, OLIVE, TEXT_DARK, TEXT_MID, BTN_PRIMARY_BASE, CARD_STYLE, back_button
from Personalidad.states.fisicas_state import FisicasState
from Personalidad.states.calculadora_state import CalculadoraState


@rx.page(route="/academia/curso", title="Academia Online - Curso", on_load=CalculadoraState.check_fisicas_access)
def curso() -> rx.Component:
    return academia_layout(
        rx.box(
            rx.hstack(
                rx.box(
                    rx.el.iframe(
                        src="https://player.mediadelivery.net/embed/634843/99f51822-0894-4df5-9334-8cf6bdd300a0?autoplay=false&loop=false&muted=false&preload=true&responsive=false",
                        border="none",
                        height="100%",
                        width="100%",
                        allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture; fullscreen",
                        allow_full_screen=True,
                        style={
                            "position": "absolute",
                            "top": "0",
                            "left": "0",
                        }
                    ),
                    style={
                        "position": "relative",
                        "padding-top": "56.25%",
                        "width": "100%",
                        "max_width": "350px",
                        "border_radius": "12px",
                        "overflow": "hidden",
                    }
                ),
                rx.vstack(
                    rx.text("BIENVENIDA AL CURSO", font_size="1.45em", font_weight="800", color=OLIVE),
                    rx.text(
                        "En este curso encontrarás todo lo necesario para superar las pruebas físicas "
                        "de tu oposición. Sigue los módulos en orden para obtener el máximo rendimiento.",
                        color=TEXT_MID, font_size="0.92em",
                    ),
                    rx.vstack(
                        rx.hstack(rx.icon("file-text", size=15, color=OLIVE), rx.text("Normativa de las pruebas",    font_size="0.9em", color=OLIVE)),
                        rx.hstack(rx.icon("calendar",  size=15, color=OLIVE), rx.text("Calendario de convocatorias", font_size="0.9em", color=OLIVE)),
                        rx.hstack(rx.icon("pen-line",  size=15, color=OLIVE), rx.text("Proceso de inscripción",      font_size="0.9em", color=OLIVE)),
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
                rx.text("📣 COMUNIDAD", font_size="1em", font_weight="700", color=TEXT_DARK, letter_spacing="0.1em"),
                rx.hstack(
                    rx.button(
                        "✈️  Telegram – Grupo Pruebas Físicas",
                        **BTN_PRIMARY_BASE,
                        padding="0.6em 1.4em",
                        width="100%",
                        on_click=rx.redirect("https://t.me/+1ftMK4D17I1iYzg0")
                    ),
                    rx.button(
                        "💬  WhatsApp – Tutorías (676917128)",
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
