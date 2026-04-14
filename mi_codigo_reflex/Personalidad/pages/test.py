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
            key=(TestState.pag_actual * TestState.num_preguntas + index).to_string(),
        )

    return rx.box(
        utils.lang(),
        navbar(),
        rx.center(
            rx.container(
                rx.vstack(
                    rx.heading("Test de Personalidad", size="7", margin_bottom="0.5em"),
                    rx.text("Responde con sinceridad a todas las preguntas", color="gray"),
                    show_progress_test(TestState.current_progress, "1em"),
                    
                    rx.vstack(
                        rx.foreach(
                            TestState.current_data, 
                            lambda item, idx: showlist(item, idx)
                        ),
                        width="100%",
                        spacing="0",
                        margin_y="2em",
                    ),

                    rx.hstack(
                        round_button_left_icon("Anterior", "arrow-left", TestState.previous_page),
                        rx.spacer(),
                        rx.cond(
                            (TestState.pag_actual + 1) == TestState.total_pages,
                            alert_dialog(
                                "Finalizar test", 
                                "¿Has revisado todas tus respuestas? Una vez finalizado no podrás volver atrás.", 
                                "Revisar", 
                                "Finalizar", 
                                TestState.finalizar_test
                            ),
                            round_button_right_icon("Siguiente", "arrow-right", TestState.next_page),
                        ),
                        width="100%",
                        padding_top="1em",
                    ),
                    width="100%",
                ),
                bg=rx.color_mode_cond(light="white", dark="#1a1a1a"),
                padding="3em",
                border_radius="20px",
                box_shadow="0 10px 40px rgba(0,0,0,0.2)",
                max_width="800px",
                margin_y="6em",
            ),
            width="100%",
            min_height="100vh",
            background="linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('/tropa.jpg')",
            background_size="cover",
            background_attachment="fixed",
        )
    )