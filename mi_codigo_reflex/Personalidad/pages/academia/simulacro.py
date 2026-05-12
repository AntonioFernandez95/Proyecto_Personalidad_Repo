# pyrefly: ignore [missing-import]
import reflex as rx
from Personalidad.pages.academia.layout import academia_layout, OLIVE, TEXT_DARK, TEXT_MID, back_button, CARD_STYLE
from Personalidad.states.fisicas_state import FisicasState
from Personalidad.states.calculadora_state import CalculadoraState
from Personalidad.states.simulacro_state import SimulacroState

def simulacro_card(s: dict) -> rx.Component:
    """Componente para mostrar un simulacro individual."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("map-pin", size=24, color=OLIVE),
                rx.text(s["titulo"], font_size="1.2em", font_weight="800", color=OLIVE),
                spacing="2", align="center",
            ),
            rx.divider(),
            rx.hstack(
                rx.vstack(
                    rx.text("Fecha:", font_weight="700", color=TEXT_DARK),
                    rx.text(s["fecha"], color=TEXT_MID),
                    align="start", spacing="0",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.text("Ubicación:", font_weight="700", color=TEXT_DARK),
                    rx.text(s["ubicacion"], color=TEXT_MID),
                    align="start", spacing="0",
                ),
                width="100%",
            ),
            rx.text(
                s["descripcion"],
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
        **CARD_STYLE, 
        padding="2.5em", 
        width=["90vw", "100%"], 
        max_width="500px",
        flex_shrink="0", # Evita que se encojan en el carrusel
        scroll_snap_align="center", # Para el carrusel
    )

@rx.page(route="/academia/simulacro", title="Academia Online - Simulacro Presencial", on_load=[CalculadoraState.check_login, SimulacroState.fetch_simulacros])
def simulacro() -> rx.Component:
    return academia_layout(
        rx.vstack(
            rx.text("SIMULACROS PRESENCIALES", font_size="2.2em", font_weight="900", color="white", letter_spacing="0.1em"),
            
            rx.cond(
                SimulacroState.simulacros.length() > 0,
                # CONTENEDOR DE NAVEGACIÓN UNO A UNO
                rx.hstack(
                    # FLECHA IZQUIERDA (Solo si hay anterior)
                    rx.cond(
                        SimulacroState.current_index > 0,
                        rx.icon(
                            "chevron-left",
                            size=45,
                            color="white",
                            cursor="pointer",
                            on_click=SimulacroState.prev_simulacro,
                            _hover={"transform": "scale(1.3)", "color": OLIVE},
                            background="rgba(0,0,0,0.4)",
                            border_radius="50%",
                            padding="5px",
                        ),
                        # Espacio vacío para mantener el centro si no hay flecha
                        rx.box(width="45px")
                    ),
                    
                    # TARJETA ACTUAL
                    rx.box(
                        simulacro_card(SimulacroState.simulacros[SimulacroState.current_index]),
                        transition="all 0.5s ease-in-out",
                        width="100%",
                        max_width="600px",
                    ),

                    # FLECHA DERECHA (Solo si hay siguiente)
                    rx.cond(
                        SimulacroState.current_index < SimulacroState.simulacros.length() - 1,
                        rx.icon(
                            "chevron-right",
                            size=45,
                            color="white",
                            cursor="pointer",
                            on_click=SimulacroState.next_simulacro,
                            _hover={"transform": "scale(1.3)", "color": OLIVE},
                            background="rgba(0,0,0,0.4)",
                            border_radius="50%",
                            padding="5px",
                        ),
                        # Espacio vacío para mantener el centro si no hay flecha
                        rx.box(width="45px")
                    ),
                    
                    spacing="6",
                    width="100%",
                    align="center",
                    justify="center",
                    padding_y="2em",
                ),
                rx.box(
                    rx.text("No hay simulacros programados en este momento.", color="white", font_size="1.2em"),
                    padding="2em"
                )
            ),
            
            back_button(label="← Volver al inicio", href="/academia"),
            align="center", spacing="4", padding_top="3em",
            width="100%"
        )
    )
