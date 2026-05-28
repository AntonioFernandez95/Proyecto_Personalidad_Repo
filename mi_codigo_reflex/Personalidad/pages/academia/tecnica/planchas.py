import reflex as rx
from Personalidad.pages.academia.layout import academia_layout, OLIVE, TEXT_DARK, GRAY_LIGHT, back_button, CARD_STYLE
from Personalidad.components.recursos import video_section, pdf_section
from Personalidad.states.base_state import State
from Personalidad.states.fisicas_state import FisicasState
from Personalidad.states.detallesTecnicas_state import DetallesTecnicasState


# Función reutilizable para los items de la lista
def item_lista(texto: str) -> rx.Component:
    return rx.hstack(
        rx.icon("chevron-right", color=OLIVE, size=18),
        rx.text(texto, font_size="0.95em", color=TEXT_DARK),
        align="start",
        spacing="2"
    )


@rx.page(
    route="/academia/tecnica/plancha",
    title="Academia Online - Técnica de Planchas",
    on_load=[State.check_fisicas_access, DetallesTecnicasState.cargar_datos_prueba]
)
def planchas() -> rx.Component:
    return academia_layout(
        rx.vstack(
            # TÍTULO
            rx.text(
                "PLANCHA ISOMÉTRICA",
                font_size="1.8em", font_weight="900", color="white", text_align="center"
            ),
           
            # CONTENEDOR BLANCO PRIMARY
            rx.box(
                rx.vstack(
                    # VÍDEO TÉCNICO DINÁMICO
                    video_section(),


                    # POSICIÓN INICIAL
                    rx.text("POSICIÓN INICIAL", font_size="1.1em", font_weight="800", color=TEXT_DARK, letter_spacing="0.05em"),
                    rx.text(DetallesTecnicasState.posicion_inicial, font_size="0.95em", color=TEXT_DARK),


                    # IMAGEN ESPECÍFICA (Reemplaza el placeholder)
                    rx.image(
                        src="/EJERCICIO_METODOS_PLANCHA.webp",
                        width="100%",
                        height="auto",
                        border_radius="12px",
                        margin_y="1.5em"
                    ),
                   
                    rx.divider(margin_bottom="1em"),


                    # EJECUCIÓN
                    rx.text("EJECUCIÓN", font_size="1.1em", font_weight="800", color=TEXT_DARK, letter_spacing="0.05em"),
                    rx.vstack(
                        rx.foreach(
                            DetallesTecnicasState.ejecucion,
                            item_lista
                        ),
                        align="start", width="100%", spacing="3"
                    ),


                    rx.divider(margin_y="1.5em"),


                    # NORMAS CRÍTICAS
                    rx.text("NORMAS CRÍTICAS", font_size="1.1em", font_weight="800", color=TEXT_DARK, letter_spacing="0.05em"),
                    rx.vstack(
                        rx.foreach(
                            DetallesTecnicasState.normas,
                            item_lista
                        ),
                        align="start", width="100%", spacing="3"
                    ),


                    rx.divider(margin_y="1.5em"),
                   
                    rx.vstack(
                        rx.hstack(
                            rx.icon("timer", color=OLIVE, size=20),
                            rx.text(f"Tiempo: {DetallesTecnicasState.tiempo}", font_weight="bold", color=OLIVE),
                            spacing="2",
                            align="center"
                        ),
                        rx.hstack(
                            rx.icon("rotate-ccw", color=OLIVE, size=20),
                            rx.text(f"Intentos: {DetallesTecnicasState.intentos}", font_weight="bold", color=OLIVE),
                            spacing="2",
                            align="center"
                        ),
                        spacing="2",
                        align="start",
                    ),


                    rx.divider(margin_y="1.5em"),
                   
                    # RECURSOS PDF DINÁMICOS
                    pdf_section(),


                    align="start",
                    width="100%",
                ),
                **CARD_STYLE, padding="2.5em", width="100%", max_width="780px", margin_top="1em"
            ),
           
            # BOTÓN VOLVER
            back_button(label="← Volver", href="/academia/tecnica"),
           
            align="center",
            width="100%",
            padding_top="1em",
            padding_bottom="4em",
            spacing="4"
        )
    )
