import reflex as rx
import Personalidad.styles.utils as utils

from Personalidad.styles.styles import Size
from Personalidad.states.base_state import State
from Personalidad.styles.colors import Color
from Personalidad.components.navbar import navbar
from Personalidad.components.progress import show_progress_test
from Personalidad.components.alert_dialog import alert_dialog
from Personalidad.components.round_button import round_button_left_icon, round_button_right_icon
from Personalidad.states.test_state import TestState

"""
reflex run

"""

@rx.page(route="/test", title="Test", on_load=[State.check_login, TestState.crear_test])
def index():

    def showlist(item: rx.Var, index: int):        
        return rx.vstack(
            rx.text(
                rx.text.span(index + 1 + (TestState.pag_actual * TestState.num_preguntas), font_weight="bold", margin_right="0.5em"),
                item["PREGUNTA"],
                font_size="1.1em",
            ),
            rx.radio(
                ["Si", "Muchas veces", "Alguna vez", "Pocas veces", "No"],
                on_change=lambda val: TestState.set_page_answer(index, val),
                value=TestState.page_answers[index],
                color_scheme="orange",
                direction="row",
                spacing="4",
            ),
            padding_y="1em",
            border_bottom="1px solid #f0f0f0",
            align_items="start",
            width="100%",
            flex_shrink="0",
            key=(TestState.pag_actual * TestState.num_preguntas + index).to_string(),
        )

    return rx.box(
        utils.lang(),
        rx.vstack(
            navbar(),
            rx.container(
                rx.box(
                    rx.center(
                        rx.heading(
                            "Progreso Test Personalidad",
                        ),
                        margin_bottom=Size.DEFAULT.value
                    ),
                    show_progress_test(TestState.current_progress, Size.DEFAULT.value),
                    rx.box(
                        rx.vstack(
                            rx.vstack(
                                rx.foreach(
                                    TestState.current_data, 
                                    lambda item, index: showlist(item, index)
                                ),
                                width="100%",
                            ),
                            rx.tablet_and_desktop(
                                rx.hstack(
                                    round_button_left_icon("Anterior","arrow-big-left", TestState.previous_page),
                                    rx.spacer(),
                                    rx.cond(
                                        (TestState.pag_actual + 1) == TestState.total_pages,
                                        alert_dialog("Finalizar test", "¿Has revisado todas tus respuestas? Esta acción no es reversible.", "Revisar", "Sí, finalizar", TestState.finalizar_test),
                                        round_button_right_icon("Siguiente", "arrow-big-right", TestState.next_page),
                                    ),
                                    margin_top=Size.MEDIUM_BIG.value,
                                    width="100%"
                                )
                            ),
                            rx.mobile_only(
                                rx.hstack(
                                    round_button_left_icon("Anterior","arrow-big-left", TestState.previous_page),
                                    rx.spacer(),
                                    rx.cond(
                                        (TestState.pag_actual + 1) == TestState.total_pages,
                                        rx.fragment(),
                                        round_button_right_icon("Siguiente", "arrow-big-right", TestState.next_page),
                                    ),
                                    margin_top=Size.MEDIUM_BIG.value,
                                    width="100%"
                                ),
                                rx.cond(
                                    (TestState.pag_actual + 1) == TestState.total_pages,
                                    rx.center(
                                        alert_dialog("Finalizar test", "¿Has revisado todas tus respuestas? Esta acción no es reversible.", "Revisar", "Sí, finalizar", TestState.finalizar_test),
                                        margin_top=Size.DEFAULT.value,
                                    ),
                                    rx.fragment(),
                                )
                            ),
                            width="100%",
                            align="center",
                            spacing="2",
                            max_width="60em",
                        ),
                    ),
                ),
                width= "90%",
                max_width= "50em",
                margin = "0 auto",
                margin_top="100px",
                margin_bottom="4em",
                background= rx.color_mode_cond(light="white", dark=Color.TEXT),
                padding= "3.1em 1.8em",
                min_height="50vh",
                border_radius="10px",
                align= "center",
                box_shadow="0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)"
            ),
            align="center",
            width="100%",
            min_height="100vh",
        ),
        min_height="100vh",
        width="100%",
        background="linear-gradient(rgba(0,0,0,0.8), rgba(27,154,175,0.8)), url('/tropa.jpg')",
        background_size="cover",
        background_attachment="fixed",
        position="relative",
        background_position="center", 
        background_repeat="no-repeat"
    )