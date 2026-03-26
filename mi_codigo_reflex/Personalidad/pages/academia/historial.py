import reflex as rx
from .layout import academia_layout, OLIVE, back_button, CARD_STYLE, BADGE_GREEN, BADGE_GRAY
from Personalidad.states.fisicas import FisicasState

_HISTORIAL = [
    ("12/03/2026", "Simulacro #04", "APTO",    BADGE_GREEN),
    ("28/02/2026", "Simulacro #03", "NO APTO", BADGE_GRAY),
    ("14/02/2026", "Simulacro #02", "APTO",    BADGE_GREEN),
    ("01/02/2026", "Simulacro #01", "NO APTO", BADGE_GRAY),
]

def badge_resultado(texto: str, color: str) -> rx.Component:
    return rx.box(
        rx.text(texto, font_size="0.82em", font_weight="700", color="white"),
        background=color, border_radius="20px", padding="0.25em 0.9em",
        display="inline-flex", align_items="center",
    )

@rx.page(
    route="/academia/historial", 
    title="Academia Online - Historial", 
    on_load=[FisicasState.check_plan_fisicas, AcademiaState.cargar_historial]
)
def historial() -> rx.Component:
    return academia_layout(
        rx.text("MI HISTORIAL DE SIMULACROS", font_size="1.9em", font_weight="900", color="white"),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Fecha",     font_weight="700", color=OLIVE),
                        rx.table.column_header_cell("Test",      font_weight="700", color=OLIVE),
                        rx.table.column_header_cell("Resultado", font_weight="700", color=OLIVE),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        AcademiaState.historial,
                        lambda item: rx.table.row(
                            rx.table.cell(item["fecha"], color="black"),
                            rx.table.cell(item["test"], color="black"),
                            rx.table.cell(badge_resultado(item["resultado"], item["color"])),
                        )
                    )
                ),
                width="100%",
            ),
            **CARD_STYLE, padding="2em", width="100%", max_width="680px", overflow="auto",
        ),
        back_button(label="← Volver al inicio", href="/academia"),
        align="center", spacing="4", padding_top="2em", width="100%",
    )
