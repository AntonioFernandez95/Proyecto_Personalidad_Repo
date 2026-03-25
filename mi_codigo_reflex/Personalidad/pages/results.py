import reflex as rx
import Personalidad.styles.utils as utils

from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color
from Personalidad.components.navbar import navbar
from Personalidad.components.progress import show_progress
from Personalidad.states.results_state import ResultsState
from Personalidad.states.base_state import State

@rx.page(route="/results", title="Resultados", on_load=[State.check_login, ResultsState.calculate_results])
def index():
    
    def get_progress_percentage(score: int) -> float:
        return (score / 95) * 100

    return rx.box(
        utils.lang(),
        rx.vstack(
            navbar(),
            rx.container(
                rx.box(
                    rx.vstack(
                        rx.cond(
                            ResultsState.isUserApto,
                            rx.hstack(
                                rx.icon("circle-check-big", color=Color.SECONDARY, stroke_width=3, margin_top=Size.NAH),
                                rx.heading("Apto", color=Color.SECONDARY),
                            ),
                            rx.hstack(
                                rx.icon("circle-x", color=Color.PRIMARY, stroke_width=3, margin_top=Size.NAH),
                                rx.heading("No apto", color=Color.PRIMARY)
                            )
                        ),
                        rx.heading(
                            "Resultados del test"
                        ),
                        rx.text("Sinceridad"),
                        show_progress(get_progress_percentage(ResultsState.score_item_1), Size.ZERO, ResultsState.is_1_ok),
                        rx.text("Extraversión"),
                        show_progress(get_progress_percentage(ResultsState.score_item_2), Size.ZERO, ResultsState.is_2_ok),
                        rx.text("Depresión"),
                        show_progress(get_progress_percentage(ResultsState.score_item_3), Size.ZERO, ResultsState.is_3_ok),
                        rx.text("Neuroticismo"),
                        show_progress(get_progress_percentage(ResultsState.score_item_4), Size.ZERO, ResultsState.is_4_ok),
                        rx.text("Psicoticismo"),
                        show_progress(get_progress_percentage(ResultsState.score_item_5), Size.ZERO, ResultsState.is_5_ok),
                        rx.text("Paranoidismo"),
                        show_progress(get_progress_percentage(ResultsState.score_item_6), Size.ZERO, ResultsState.is_6_ok),
                        rx.text("Desviación Psicopática"),
                        show_progress(get_progress_percentage(ResultsState.score_item_7), Size.ZERO, ResultsState.is_7_ok),
                        rx.button(
                            "Salir",
                            on_click=State.logout,
                        ),
                        align="center",
                        spacing="2",
                        max_width="60em",
                    ), 
                ),
                width= "90%",
                max_width= "450px",
                margin_top = "4.5em",
                margin_bottom="50%",
                background= rx.color_mode_cond(light="white", dark=Color.TEXT),
                padding= "40px 60px 40px",
                align= "center",
                box_shadow="0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)"
            ),
            align="center",
            width="100%",
            height="100vh",
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