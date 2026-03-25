import reflex as rx
from .layout import academia_layout, OLIVE, TEXT_DARK, plan_row, back_button, CARD_STYLE
from .state import AcademiaState

_MARCAS = [
    ("Flexiones",     "17 reps", "12 reps"),
    ("Plancha",       "60 seg",  "40 seg"),
    ("Carrera 2000m", "11:00",   "13:00"),
    ("Agilidad",      "25 seg",  "27 seg"),
]

@rx.page(route="/academia/planificacion", title="Academia Online - Planificación", on_load=AcademiaState.check_login)
def planificacion() -> rx.Component:
    return academia_layout(
        rx.text("PLANIFICACIÓN DEL ENTRENAMIENTO", font_size="1.9em", font_weight="900", color="white"),
        rx.hstack(
            rx.vstack(
                rx.text("📋 PLANES DE ENTRENAMIENTO", font_size="1em", font_weight="800", color=OLIVE, letter_spacing="0.05em"),
                plan_row("Plan Iniciación", "6 semanas · Nivel básico"),
                plan_row("Plan Avanzado",   "8 semanas · Nivel medio-alto"),
                plan_row("Plan Pro",        "12 semanas · Máximo rendimiento"),
                spacing="3", **CARD_STYLE, padding="2em", flex="1", min_width="280px", align="start",
            ),
            rx.vstack(
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
                                rx.table.cell(prueba,   color="black"),
                                rx.table.cell(hombres,  color="black"),
                                rx.table.cell(mujeres,  color="black"),
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
