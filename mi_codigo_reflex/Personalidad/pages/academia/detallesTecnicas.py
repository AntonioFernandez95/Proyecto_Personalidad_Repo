import reflex as rx
from Personalidad.pages.academia.layout import academia_layout, OLIVE, TEXT_DARK, GRAY_LIGHT, back_button, CARD_STYLE

# Importamos los estados que gestionan la seguridad y los datos
from Personalidad.states.fisicas_state import FisicasState
from Personalidad.states.detallesTecnicas_state import DetallesTecnicasState

# Pequeña función de diseño para que los puntos de ejecución y normas queden bonitos
def item_lista(texto: str) -> rx.Component:
    return rx.hstack(
        rx.icon("chevron-right", color=OLIVE, size=18),
        rx.text(texto, font_size="0.95em", color="black"),
        align="start",
        spacing="2"
    )

@rx.page(
    route="/academia/tecnica/[prueba_id]", 
    title="Academia Online - Detalles de Técnica", 
    on_load=[FisicasState.check_plan_fisicas, DetallesTecnicasState.cargar_datos_prueba]
)
def detalles_tecnicas() -> rx.Component:
    return academia_layout(
        rx.vstack(
            # 1. TÍTULO GENERAL
            rx.text(
                DetallesTecnicasState.titulo, 
                font_size="1.8em", font_weight="900", color="white", text_align="center"
            ),
            
            # CONTENEDOR BLANCO PRINCIPAL (Tipo Tarjeta)
            rx.box(
                rx.vstack(
                    # 2. VÍDEO TÉCNICO (Placeholder)
                    rx.center(
                        rx.vstack(
                            rx.icon("play-circle", size=46, color="white"),
                            rx.text("VÍDEO TÉCNICO", color="white", font_size="0.84em", font_weight="bold"),
                            align="center",
                        ),
                        background="black", border_radius="12px",
                        width="100%", height="200px", margin_bottom="1em"
                    ),

                    # 3. POSICIÓN INICIAL
                    rx.text("POSICIÓN INICIAL", font_size="1.1em", font_weight="800", color=TEXT_DARK, letter_spacing="0.05em"),
                    rx.text(DetallesTecnicasState.posicion_inicial, font_size="0.95em", color="black"),

                    # 4. IMAGEN (Placeholder)
                    rx.center(
                        rx.vstack(
                            rx.icon("image", size=40, color="gray"),
                            rx.text("IMAGEN", color="gray", font_size="0.8em"),
                            align="center",
                        ),
                        background=GRAY_LIGHT, border_radius="12px",
                        width="100%", height="150px", margin_y="1.5em"
                    ),
                    
                    rx.divider(margin_bottom="1em"),

                    # 5. EJECUCIÓN
                    rx.text("EJECUCIÓN", font_size="1.1em", font_weight="800", color=TEXT_DARK, letter_spacing="0.05em"),
                    rx.vstack(
                        rx.foreach(
                            DetallesTecnicasState.ejecucion,
                            item_lista
                        ),
                        align="start", width="100%", spacing="3"
                    ),

                    rx.divider(margin_y="1.5em"),

                    # 6. NORMAS CRÍTICAS
                    rx.text("NORMAS CRÍTICAS", font_size="1.1em", font_weight="800", color=TEXT_DARK, letter_spacing="0.05em"),
                    rx.vstack(
                        rx.foreach(
                            DetallesTecnicasState.normas,
                            item_lista
                        ),
                        align="start", width="100%", spacing="3"
                    ),

                    rx.divider(margin_y="1.5em"),
                    
                    # 7. TIEMPOS E INTENTOS
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
            
            # 8. BOTÓN VOLVER
            back_button(label="← Volver", href="/academia/tecnica"),
            
            align="center",
            width="100%",
            padding_top="1em",
            padding_bottom="4em",
            spacing="4"
        )
    )