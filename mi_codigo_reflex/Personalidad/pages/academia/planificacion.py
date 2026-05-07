import reflex as rx
from Personalidad.pages.academia.layout import academia_layout, OLIVE, TEXT_DARK, TEXT_MID, GRAY_LIGHT, plan_row, back_button, CARD_STYLE, BTN_PRIMARY_BASE
from Personalidad.states.planificacion_state import PlanificacionState


_MARCAS = [
    ("Flexiones",     "17 reps", "12 reps"),
    ("Plancha",       "60 seg",  "40 seg"),
    ("Carrera 2000m", "11:00",   "13:00"),
    ("Agilidad",      "25 seg",  "27 seg"),
]


@rx.page(route="/academia/planificacion", title="Academia Online - Planificación", on_load=PlanificacionState.on_load)
def planificacion() -> rx.Component:
    return academia_layout(
        rx.text("PLANIFICACIÓN DEL ENTRENAMIENTO", font_size="1.9em", font_weight="900", color="white"),
        rx.hstack(
            rx.vstack(
                rx.text("📋 PLANES DE ENTRENAMIENTO", font_size="1em", font_weight="800", color=OLIVE, letter_spacing="0.05em"),
               
                # DESPLEGABLE DE RECURSOS DINÁMICOS (Versión Radix para máxima compatibilidad)
                rx.vstack(
                    rx.text("Selecciona un recurso:", font_size="0.8em", color=TEXT_MID, font_weight="bold"),
                    rx.select.root(
                        rx.select.trigger(
                            width="100%",
                            background="transparent",
                            color=TEXT_DARK,
                            border="1px solid #ddd",
                            border_radius="10px",
                            padding="0.5em"
                        ),
                        rx.select.content(
                            rx.foreach(
                                PlanificacionState.recursos,
                                lambda r: rx.select.item(r["nombre"], value=r["full_id"].to(str))
                            ),
                        ),
                        value=PlanificacionState.selected_recurso_id,
                        on_change=PlanificacionState.set_selected_recurso_id,
                    ),
                    # Botón de acción dinámico según el tipo seleccionado
                    rx.cond(
                        PlanificacionState.selected_recurso_id != "",
                        rx.hstack(
                            rx.cond(
                                PlanificacionState.selected_recurso["tipo"] == "pdf",
                                rx.link(
                                    rx.button(
                                        rx.icon("file-down"), "Descargar PDF",
                                        background_color=OLIVE, color="white", width="100%", height="3em", border_radius="10px"
                                    ),
                                    href=PlanificacionState.selected_recurso["url"].to(str),
                                    is_external=True, width="100%", underline="none"
                                ),
                                # Si es vídeo, no mostramos nada aquí para evitar el reproductor vacío
                                rx.spacer(),
                            ),
                            width="100%", margin_top="1em"
                        )
                    ),
                    width="100%",
                    padding="1em",
                    background=GRAY_LIGHT,
                    border_radius="15px",
                    border=rx.color_mode_cond(light="1px solid #eee", dark="1px solid #444"),
                    margin_bottom="1.5em"
                ),


                rx.text("Planes Estáticos:", font_size="0.8em", color=TEXT_MID, font_weight="bold"),
                plan_row("CURSO PRUEBA FÍSICAS 2026", "6 semanas · Nivel básico", "/curso_fisicas_2026.pdf"),
                plan_row("PRUEBAS FÍSICAS 2026 CIRCUITO", "8 semanas · Nivel medio-alto", "/circuito_2026.pdf"),
                plan_row("PRUEBAS FÍSICAS FLEXIONES Y PLANCHAS", "12 semanas · Máximo rendimiento", "/flexiones_planchas.pdf"),
                plan_row("CURSO PRUEBA FÍSICAS CARRERA", "Entrenamiento específico", "/curso_carrera.pdf"),
                spacing="3", **CARD_STYLE, padding="2em", flex="1", min_width="280px", align="start",
            ),
            rx.vstack(
                rx.text("VÍDEO DE PLANIFICACIÓN", font_size="1em", font_weight="800", color=OLIVE, letter_spacing="0.05em"),
                rx.box(
                    rx.el.iframe(
                        src="https://player.mediadelivery.net/embed/634843/d0a3ef88-493c-45a6-89de-7f25c18a1161?autoplay=false&loop=false&muted=false&preload=true&responsive=false",
                        border="none",
                        height="100%",
                        width="100%",
                        allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture;",
                        allow_full_screen=True,
                        style={
                            "position": "absolute",
                            "top": "0",
                            "left": "0",
                        }
                    ),
                    style={
                        "position": "relative",
                        "padding-top": "56.25%",
                        "width": "100%",
                        "border_radius": "12px",
                        "overflow": "hidden",
                        "margin_bottom": "1.5em",
                    }
                ),
                rx.text("🏅 TABLAS DE MARCAS", font_size="1em", font_weight="800", color=OLIVE, letter_spacing="0.05em"),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Prueba",   font_weight="700", color=OLIVE),
                            rx.table.column_header_cell("Hombres",  font_weight="700", color=OLIVE),
                            rx.table.column_header_cell("Mujeres",  font_weight="700", color=OLIVE),
                        )
                    ),
                    rx.table.body(
                        *[
                            rx.table.row(
                                rx.table.cell(prueba,   color=TEXT_DARK),
                                rx.table.cell(hombres,  color=TEXT_DARK),
                                rx.table.cell(mujeres,  color=TEXT_DARK),
                            )
                            for prueba, hombres, mujeres in _MARCAS
                        ]
                    ),
                    width="100%",
                ),
                spacing="3", **CARD_STYLE, padding="2em", flex="1", min_width="260px", align="start",
            ),
            spacing="4", width="100%", max_width="900px", align="start", wrap="wrap",
        ),
        back_button(),
        align="center", spacing="4", padding_top="2em", width="100%",
    )
