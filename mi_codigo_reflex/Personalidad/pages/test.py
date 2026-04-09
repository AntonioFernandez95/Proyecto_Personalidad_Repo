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

    def showlist(item: dict, index: int, page: int, num_per_page: int):
        
        global_index = page * num_per_page + index
        
        return rx.vstack(
            rx.heading(f"{global_index + 1}. {item['PREGUNTA']}"),
            rx.radio(
                ["Si", 
                "Muchas veces", 
                "Alguna vez", 
                "Pocas veces", 
                "No"],
                key=global_index, #key única para obligar a hacer un refresh y deje de quedarse la opción marcada al cambiar de página
                color_scheme="orange",
                on_change=lambda value: TestState.set_selection(global_index, value),
                value= TestState.selections[global_index], #así setteamos el value con lo que había respondido el user anteriormente 
            ),
            margin_top=Size.DEFAULT,
            
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
                        margin_bottom=Size.DEFAULT
                    ),
                    show_progress_test(TestState.current_progress, Size.DEFAULT),
                    rx.box(
                        rx.vstack(
                            rx.vstack(
                                rx.foreach(
                                    TestState.current_data, 
                                    lambda item, index: showlist(item, index, TestState.pag_actual, TestState.num_preguntas)
                                ),
                                width="100%",
                            ),
                            rx.tablet_and_desktop(
                                rx.hstack(
                                round_button_left_icon("Anterior","arrow-big-left", TestState.previous_page),
                                rx.spacer(),
                                alert_dialog("Finalizar test", "¿Quieres finalizar el test? Esta acción no es reversible.", "No, seguir el test", "Sí, finalizar", rx.redirect('/results')),
                                rx.spacer(),
                                round_button_right_icon("Siguiente", "arrow-big-right", TestState.next_page),
                                margin_top=Size.MEDIUM_BIG,
                                width="100%"
                                )
                            ),
                            rx.mobile_only(
                                rx.hstack(
                                    round_button_left_icon("Anterior","arrow-big-left", TestState.previous_page),
                                    rx.spacer(),
                                    round_button_right_icon("Siguiente", "arrow-big-right", TestState.next_page),
                                    margin_top=Size.MEDIUM_BIG,
                                    width="100%"
                                ),
                                rx.center(
                                    alert_dialog("Finalizar test", "¿Quieres finalizar el test? Esta acción no es reversible.", "No, seguir el test", "Sí, finalizar", rx.redirect('/results')),
                                    margin_top=Size.DEFAULT,
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
                max_width= "37.5em",
                margin = "0 auto",
                background= rx.color_mode_cond(light="white", dark=Color.TEXT),
                padding= "3.1em 1.8em",
                transform="translate(-50%, -50%)",
                top="50%",
                left="50%",
                position="absolute",
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