import reflex as rx
from Personalidad.pages.academia.layout import academia_layout, OLIVE, OLIVE_LIGHT, TEXT_DARK, GRAY_LIGHT, norma_item, back_button, CARD_STYLE
from Personalidad.states.fisicas_state import FisicasState
from Personalidad.states.calculadora_state import CalculadoraState

@rx.page(route="/academia/detalle", title="Academia Online - Técnica Detalle", on_load=CalculadoraState.check_login)
def detalle() -> rx.Component:
    return academia_layout(
        rx.text("POTENCIA TREN SUPERIOR", font_size="1.8em", font_weight="900", color="white"),
        rx.text("FLEXO-EXTENSIONES DE BRAZOS", font_size="1em", color=OLIVE_LIGHT, font_weight="600", letter_spacing="0.1em"),
        rx.box(
            rx.hstack(
                rx.center(
                    rx.vstack(
                        rx.icon("play-circle", size=46, color="white"),
                        rx.text("Vídeo explicativo", color="white", font_size="0.84em"),
                        align="center",
                    ),
                    background="black", border_radius="12px",
                    width="290px", height="185px", flex_shrink="0",
                ),
                rx.vstack(
                    rx.box(
                        rx.vstack(
                            rx.center(
                                rx.icon("arrow-down-to-line", size=34, color=OLIVE),
                                background=GRAY_LIGHT, border_radius="10px",
                                width="65px", height="65px",
                            ),
                            rx.text("POSICIÓN INICIAL", font_size="0.82em", font_weight="700", color=TEXT_DARK, letter_spacing="0.08em"),
                            rx.text(
                                "Manos a la anchura de los hombros, cuerpo recto, brazos extendidos.",
                                font_size="0.82em", color="black", text_align="center",
                            ),
                            align="center", spacing="2",
                        ),
                        background=GRAY_LIGHT, border_radius="12px", padding="1em", width="100%",
                    ),
                    rx.vstack(
                        rx.text("NORMAS CRÍTICAS", font_size="0.82em", font_weight="700", color=TEXT_DARK, letter_spacing="0.08em"),
                        norma_item("No utilizar almohadilla o colchoneta"),
                        norma_item("No separar los brazos del cuerpo en exceso"),
                        norma_item("No romper la alineación cuerpo-piernas"),
                        spacing="2", align="start", width="100%",
                    ),
                    spacing="3", flex="1", align="start",
                ),
                spacing="5", align="start", wrap="wrap",
            ),
            **CARD_STYLE, padding="2em", width="100%", max_width="780px",
        ),
        rx.box(
            rx.hstack(
                rx.hstack(rx.icon("clock",      size=15, color=OLIVE), rx.text("Tiempo: 2 min", font_size="0.9em", font_weight="600", color="black")),
                rx.hstack(rx.icon("refresh-cw", size=15, color=OLIVE), rx.text("Intentos: 1",   font_size="0.9em", font_weight="600", color="black")),
                spacing="5",
            ),
            **CARD_STYLE, padding="0.8em 1.8em", width="fit-content",
        ),
        back_button(label="← Volver a Técnica", href="/academia/tecnica"),
        align="center", spacing="4", padding_top="2em", width="100%",
    )
