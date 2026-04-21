import reflex as rx
import Personalidad.styles.utils as utils
from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color
from Personalidad.components.progress import show_progress
from Personalidad.states.results_state import ResultsState
from Personalidad.states.base_state import State
from Personalidad.pages.academia.layout import academia_layout, OLIVE, BTN_PRIMARY_BASE

@rx.page(route="/results", title="Resultados", on_load=[State.check_login, ResultsState.calculate_results, ResultsState.cargar_historial])
def index():
    
    def get_progress_percentage(score: int) -> float:
        return (score / 95) * 100

    return academia_layout(
        # CARD PRINCIPAL (POSICIÓN Y COORDENADAS ORIGINALES)
        rx.box(
            rx.vstack(
                rx.cond(
                    ResultsState.isUserApto,
                    rx.hstack(
                        rx.icon("circle-check-big", color=Color.SECONDARY, stroke_width=3, margin_top=Size.NAH.value),
                        rx.heading("Apto", color=Color.SECONDARY),
                    ),
                    rx.hstack(
                        rx.icon("circle-x", color=Color.PRIMARY, stroke_width=3, margin_top=Size.NAH.value),
                        rx.heading("No apto", color=Color.PRIMARY)
                    )
                ),
                rx.heading("RESULTADOS ACTUALIZADOS"),
                rx.text("Sinceridad"),
                show_progress(get_progress_percentage(ResultsState.score_item_1), Size.ZERO.value, ResultsState.is_1_ok),
                rx.text("Extraversión"),
                show_progress(get_progress_percentage(ResultsState.score_item_2), Size.ZERO.value, ResultsState.is_2_ok),
                rx.text("Depresión"),
                show_progress(get_progress_percentage(ResultsState.score_item_3), Size.ZERO.value, ResultsState.is_3_ok),
                rx.text("Neuroticismo"),
                show_progress(get_progress_percentage(ResultsState.score_item_4), Size.ZERO.value, ResultsState.is_4_ok),
                rx.text("Psicoticismo"),
                show_progress(get_progress_percentage(ResultsState.score_item_5), Size.ZERO.value, ResultsState.is_5_ok),
                rx.text("Paranoidismo"),
                show_progress(get_progress_percentage(ResultsState.score_item_6), Size.ZERO.value, ResultsState.is_6_ok),
                rx.text("Desviación Psicopática"),
                show_progress(get_progress_percentage(ResultsState.score_item_7), Size.ZERO.value, ResultsState.is_7_ok),
                
                rx.button(
                    "SALIR",
                    on_click=rx.redirect("/academia"),
                    **BTN_PRIMARY_BASE,
                    margin_top="1.5em",
                    width="100%",
                ),
                align="center",
                spacing="2",
            ),
            width="100%",
            max_width="450px",
            background=rx.color_mode_cond(light="white", dark=Color.TEXT),
            padding="40px 60px 40px",
            border_radius="16px",
            box_shadow="0 8px 32px rgba(0,0,0,0.2)",
        ),

        # RESUMEN DE LOS 2 ÚLTIMOS TESTS (ESTÁTICO)
        rx.vstack(
            rx.heading("Resumen intentos anteriores", font_size="1em", color="white", margin_bottom="0.5em"),
            rx.foreach(
                ResultsState.historial_resultados[1:3],  # Python slicing en lugar de .slice()
                lambda item: rx.hstack(
                    rx.text(item["fecha"], font_size="0.8em", color="white", flex="1"),
                    rx.badge(
                        item["es_apto"],
                        color_scheme=rx.cond(item["es_apto"] == "APTO", "green", "red"),
                        variant="soft",
                        size="1",
                    ),
                    width="100%",
                    padding="0.5em 1em",
                    background="rgba(255,255,255,0.1)",
                    border_radius="8px",
                    align="center",
                )
            ),
            width="100%",
            max_width="450px",
            spacing="2",
            margin_top="1em",
        ),

        # DESPLEGABLE DE HISTORIAL COMPLETO (MÁS ABAJO)
        rx.vstack(
            rx.button(
                rx.hstack(
                    rx.icon("history", size=18),
                    rx.cond(
                        ResultsState.show_history, 
                        rx.text("Ocultar historial completo"), 
                        rx.text("Ver todo el historial")
                    ),
                    spacing="2",
                ),
                on_click=ResultsState.toggle_history,
                variant="ghost",
                color=rx.color_mode_cond(light=OLIVE, dark="white"),
                margin_top="2em",
            ),
            rx.cond(
                ResultsState.show_history,
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Fecha"),
                                rx.table.column_header_cell("Sinc."),
                                rx.table.column_header_cell("Ext."),
                                rx.table.column_header_cell("Neur."),
                                rx.table.column_header_cell("Psic."),
                                rx.table.column_header_cell("Result."),
                            )
                        ),
                        rx.table.body(
                            rx.foreach(
                                ResultsState.historial_resultados,
                                lambda item: rx.table.row(
                                    rx.table.cell(item["fecha"], font_size="0.65em"),
                                    rx.table.cell(item["sinceridad"], font_size="0.75em"),
                                    rx.table.cell(item["extraversion"], font_size="0.75em"),
                                    rx.table.cell(item["neuroticismo"], font_size="0.75em"),
                                    rx.table.cell(item["psicoticismo"], font_size="0.75em"),
                                    rx.table.cell(
                                        rx.badge(
                                            item["es_apto"],
                                            color_scheme=rx.cond(item["es_apto"] == "APTO", "green", "red"),
                                            variant="soft",
                                            size="1",
                                        )
                                    ),
                                )
                            )
                        ),
                        width="100%",
                        variant="surface",
                    ),
                    background=rx.color_mode_cond(light="white", dark=Color.TEXT),
                    padding="1em",
                    border_radius="12px",
                    width="100%",
                    overflow_x="auto",
                )
            ),
            width="100%",
            max_width="450px",
            align="center",
            padding_bottom="4em",
        ),
        spacing="4",
    )