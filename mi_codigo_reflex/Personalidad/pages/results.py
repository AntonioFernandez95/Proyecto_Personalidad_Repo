import reflex as rx
import Personalidad.styles.utils as utils

from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color
from Personalidad.components.navbar import navbar
from Personalidad.components.progress import show_progress
from Personalidad.states.results_state import ResultsState
from Personalidad.states.base_state import State
from Personalidad.states.historial_state import HistorialSimplificado_State
from Personalidad.components.historial_table import historial_table_component

@rx.page(route="/results", title="Resultados", on_load=[State.check_personalidad_access, ResultsState.calculate_results, HistorialSimplificado_State.cargar_historial])
def index():
    
    def get_progress_percentage(score: int) -> float:
        # Puntuación máxima aproximada 95 para la barra
        return (score / 95) * 100

    return rx.box(
        utils.lang(),
        rx.vstack(
            navbar(),
            rx.container(
                rx.vstack(
                    # CUADRO DE RESULTADOS
                    rx.box(
                        rx.vstack(
                            rx.cond(
                                ResultsState.isUserApto,
                                rx.hstack(
                                    rx.icon("circle-check-big", color=Color.SECONDARY, stroke_width=3),
                                    rx.heading("Apto", color=Color.SECONDARY),
                                    align="center", spacing="2",
                                ),
                                rx.hstack(
                                    rx.icon("circle-x", color=Color.PRIMARY, stroke_width=3),
                                    rx.heading("No apto", color=Color.PRIMARY),
                                    align="center", spacing="2",
                                )
                            ),
                            rx.heading("Resultados del test", size="4"),
                            
                            rx.text("Sinceridad", font_size="0.85em", font_weight="bold"),
                            show_progress(get_progress_percentage(ResultsState.score_item_1), Size.ZERO, ResultsState.is_1_ok),
                            
                            rx.text("Extraversión", font_size="0.85em", font_weight="bold"),
                            show_progress(get_progress_percentage(ResultsState.score_item_2), Size.ZERO, ResultsState.is_2_ok),
                            
                            rx.text("Depresión", font_size="0.85em", font_weight="bold"),
                            show_progress(get_progress_percentage(ResultsState.score_item_3), Size.ZERO, ResultsState.is_3_ok),
                            
                            rx.text("Neuroticismo", font_size="0.85em", font_weight="bold"),
                            show_progress(get_progress_percentage(ResultsState.score_item_4), Size.ZERO, ResultsState.is_4_ok),
                            
                            rx.text("Psicoticismo", font_size="0.85em", font_weight="bold"),
                            show_progress(get_progress_percentage(ResultsState.score_item_5), Size.ZERO, ResultsState.is_5_ok),
                            
                            rx.text("Paranoidismo", font_size="0.85em", font_weight="bold"),
                            show_progress(get_progress_percentage(ResultsState.score_item_6), Size.ZERO, ResultsState.is_6_ok),
                            
                            rx.text("Desviación Psicopática", font_size="0.85em", font_weight="bold"),
                            show_progress(get_progress_percentage(ResultsState.score_item_7), Size.ZERO, ResultsState.is_7_ok),
                            
                            rx.button(
                                "SALIR AL DASHBOARD",
                                on_click=rx.redirect("/academia"),
                                margin_top="1.5em",
                                color_scheme="orange",
                                width="100%",
                            ),
                            align="center",
                            spacing="2",
                        ),
                        width="100%",
                        max_width="480px",
                        background=rx.color_mode_cond(light="white", dark="#333"),
                        padding="2em 3em",
                        border_radius="20px",
                        box_shadow="0 10px 25px rgba(0,0,0,0.3)",
                    ),
                    # HISTORIAL FILTRADO
                    rx.box(
                        historial_table_component(tipo_filtro="PERSONALIDAD"),
                        width="100%",
                        max_width="850px",
                        margin_top="3em",
                    ),
                    align="center",
                    width="100%",
                ),
                width="100%",
                max_width="900px",
                margin_top="3em",
                margin_bottom="4em",
                align="center",
            ),
            align="center",
            width="100%",
            height="100vh",
            overflow_y="auto",
        ),
        height="100vh",
        width="100%",
        background="linear-gradient(rgba(0,0,0,0.8), rgba(27,154,175,0.8)), url('/tropa.jpg')",
        background_size="cover",
        background_attachment="fixed",
        position="relative",
        background_position="center", 
        background_repeat="no-repeat"
    )