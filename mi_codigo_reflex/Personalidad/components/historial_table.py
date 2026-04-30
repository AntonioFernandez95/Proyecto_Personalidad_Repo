import reflex as rx
from Personalidad.states.historial_state import HistorialSimplificado_State
from Personalidad.styles.academia_styles import OLIVE, BADGE_RED, CARD_STYLE

def historial_table_component(tipo_filtro: str = None) -> rx.Component:
    """
    Componente reutilizable de la tabla de historial con cabeceras dinámicas.
    Si tipo_filtro == "PERSONALIDAD", muestra las 7 aptitudes.
    """
    
    # 1. Cabeceras dinámicas
    if tipo_filtro == "PERSONALIDAD":
        headers = ["Fecha", "Sinc", "Extr", "Depr", "Neur", "Psic", "Para", "Desv", "Resultado"]
    elif tipo_filtro == "FÍSICAS":
        headers = ["Fecha", "Flexiones", "Plancha", "Carrera", "Agilidad", "Resultado"]
    else:
        headers = ["Fecha", "Tipo", "Flex/Sinc", "Plan/Extr", "Carr/Neur", "Agil/Psic", "Resultado"]

    return rx.vstack(
        rx.text("📜 HISTORIAL RECIENTE", font_size="1.2em", font_weight="800", color=OLIVE, margin_top="1em"),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    *[rx.table.column_header_cell(h, color=OLIVE, font_size="0.75em") for h in headers]
                )
            ),
            rx.table.body(
                rx.foreach(
                    HistorialSimplificado_State.historial,
                    lambda item: rx.cond(
                        rx.cond(tipo_filtro is None, True, item["tipo"] == tipo_filtro),
                        rx.table.row(
                            rx.table.cell(item["fecha"], color=OLIVE, font_size="0.75em"),
                            
                            # Si no hay filtro, mostramos el tipo
                            rx.cond(tipo_filtro is None, 
                                rx.table.cell(rx.badge(item["tipo"], color_scheme="blue", variant="outline", font_size="0.6em")),
                                rx.fragment()
                            ),

                            # Columnas de datos según el tipo de fila
                            rx.cond(
                                item["tipo"] == "PERSONALIDAD",
                                rx.fragment(
                                    rx.table.cell(item["sinceridad"], color=OLIVE, font_size="0.8em"),
                                    rx.table.cell(item["extraversion"], color=OLIVE, font_size="0.8em"),
                                    rx.table.cell(item["depresion"], color=OLIVE, font_size="0.8em"),
                                    rx.table.cell(item["neuroticismo"], color=OLIVE, font_size="0.8em"),
                                    rx.table.cell(item["psicoticismo"], color=OLIVE, font_size="0.8em"),
                                    rx.table.cell(item["paranoidismo"], color=OLIVE, font_size="0.8em"),
                                    rx.table.cell(item["desviacion_psicopatica"], color=OLIVE, font_size="0.8em"),
                                ),
                                rx.fragment(
                                    rx.table.cell(item["flexiones"], color=rx.cond(item["flex_ok"], OLIVE, BADGE_RED), font_size="0.8em"),
                                    rx.table.cell(item["plancha"],   color=rx.cond(item["plan_ok"], OLIVE, BADGE_RED), font_size="0.8em"),
                                    rx.table.cell(item["km2000"],    color=rx.cond(item["carr_ok"], OLIVE, BADGE_RED), font_size="0.8em"),
                                    rx.table.cell(item["agilidad"],  color=rx.cond(item["agil_ok"], OLIVE, BADGE_RED), font_size="0.8em"),
                                )
                            ),

                            # Resultado final
                            rx.table.cell(
                                rx.box(
                                    rx.text(item["resultado"], font_size="0.75em", font_weight="700", color="white"),
                                    background=item["color"], 
                                    border_radius="20px", 
                                    padding="0.2em 0.8em",
                                    display="inline-flex", 
                                    align_items="center",
                                )
                            ),
                        ),
                        rx.fragment()
                    )
                )
            ),
            width="100%",
            variant="surface",
        ),
        **CARD_STYLE, padding="1.5em", width="100%", max_width="900px" if tipo_filtro == "PERSONALIDAD" else "780px", overflow="auto",
        align="center",
    )
