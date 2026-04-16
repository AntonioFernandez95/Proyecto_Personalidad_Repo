import reflex as rx
from Personalidad.pages.academia.layout import academia_layout, OLIVE, TEXT_DARK, GRAY_LIGHT, back_button, CARD_STYLE, BTN_PRIMARY_BASE
from Personalidad.states.fisicas_state import FisicasState
from Personalidad.states.detallesTecnicas_state import DetallesTecnicasState

# Función reutilizable para los items de la lista
def item_lista(texto: str) -> rx.Component:
    return rx.hstack(
        rx.icon("chevron-right", color=OLIVE, size=18),
        rx.text(texto, font_size="0.95em", color="black"),
        align="start",
        spacing="2"
    )

@rx.page(
    route="/academia/tecnica/agilidad", 
    title="Academia Online - Técnica de Agilidad", 
    on_load=[FisicasState.check_plan_fisicas, DetallesTecnicasState.cargar_datos_prueba]
)
def agilidad() -> rx.Component:
    return academia_layout(
        rx.vstack(
            # TÍTULO
            rx.text(
                "CIRCUITO DE AGILIDAD-VELOCIDAD", 
                font_size="1.8em", font_weight="900", color="white", text_align="center"
            ),
            
            # CONTENEDOR BLANCO PRIMARY
            rx.box(
                rx.vstack(
                    # VÍDEO TÉCNICO
                    rx.center(
                        rx.vstack(
                            rx.icon("play-circle", size=46, color="white"),
                            rx.text("VÍDEO TÉCNICO", color="white", font_size="0.84em", font_weight="bold"),
                            align="center",
                        ),
                        background="black", border_radius="12px",
                        width="100%", height="200px", margin_bottom="1em"
                    ),

                    # POSICIÓN INICIAL
                    rx.text("POSICIÓN INICIAL", font_size="1.1em", font_weight="800", color=TEXT_DARK, letter_spacing="0.05em"),
                    rx.text(DetallesTecnicasState.posicion_inicial, font_size="0.95em", color="black"),

                    # IMAGEN ESPECÍFICA
                    rx.image(
                        src="/ESQUEMA CIRCUITO AGILIDAD-VELOCIDAD.webp",
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
                    
                    # TIEMPOS E INTENTOS
                    rx.hstack(
                        rx.text(f"Tiempo máximo: {DetallesTecnicasState.tiempo}", font_weight="bold", color=OLIVE),
                        rx.text("|", color=TEXT_DARK),
                        rx.text(f"Intentos: {DetallesTecnicasState.intentos}", font_weight="bold", color=OLIVE),
                        spacing="4"
                    ),

                    align="start",
                    width="100%",
                ),
                **CARD_STYLE, padding="2.5em", width="100%", max_width="780px", margin_top="1em"
            ),
            
            # BOTÓN DESCARGA PDF
            rx.center(
                rx.link(
                    rx.button(
                        rx.hstack(
                            rx.icon("file-text", size=20),
                            rx.text("Descargar Guía Técnica en PDF"),
                            spacing="2",
                        ),
                        **BTN_PRIMARY_BASE,
                        width="fit-content",
                        padding="1.5em",
                    ),
                    href="/circuito_2026.pdf",
                    is_external=True,
                    underline="none",
                ),
                width="100%",
                margin_top="3em",
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
