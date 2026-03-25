import reflex as rx
from .layout import academia_layout, OLIVE, TEXT_DARK, TEXT_MID, GRAY_LIGHT, BTN_PRIMARY_BASE, CARD_STYLE, back_button, BADGE_GREEN, BADGE_GRAY
from .state import AcademiaState

@rx.page(route="/academia/calculadora", title="Academia Online - Calculadora", on_load=AcademiaState.check_login)
def calculadora() -> rx.Component:
    return academia_layout(
        rx.text("CALCULADORA DE RESULTADOS", font_size="1.9em", font_weight="900", color="white"),
        rx.hstack(
            # Formulario
            rx.vstack(
                rx.text("Introduce tus marcas", font_size="1.1em", font_weight="700", color=OLIVE),
                rx.vstack(
                    rx.text("Género", font_size="0.85em", font_weight="600", color=TEXT_MID),
                    rx.radio_group(
                        ["male", "female"],
                        default_value="male",
                        on_change=AcademiaState.set_gender,
                        direction="row",
                    ),
                    spacing="1", align="start", width="100%",
                ),
                rx.vstack(
                    rx.text("Flexiones (repeticiones)", font_size="0.85em", font_weight="600", color=TEXT_MID),
                    rx.input(placeholder="Ej: 20", type="number",
                             on_change=AcademiaState.set_flexiones,
                             border_radius="8px", width="100%"),
                    spacing="1", align="start", width="100%",
                ),
                rx.vstack(
                    rx.text("Plancha (segundos)", font_size="0.85em", font_weight="600", color=TEXT_MID),
                    rx.input(placeholder="Ej: 90", type="number",
                             on_change=AcademiaState.set_plancha,
                             border_radius="8px", width="100%"),
                    spacing="1", align="start", width="100%",
                ),
                rx.vstack(
                    rx.text("Carrera 2000m (mm:ss)", font_size="0.85em", font_weight="600", color=TEXT_MID),
                    rx.input(placeholder="Ej: 10:30",
                             on_change=AcademiaState.set_km2000,
                             border_radius="8px", width="100%"),
                    spacing="1", align="start", width="100%",
                ),
                rx.vstack(
                    rx.text("Agilidad (segundos)", font_size="0.85em", font_weight="600", color=TEXT_MID),
                    rx.input(placeholder="Ej: 24.5", type="number",
                             on_change=AcademiaState.set_agilidad,
                             border_radius="8px", width="100%"),
                    spacing="1", align="start", width="100%",
                ),
                rx.button(
                    "CALCULAR",
                    on_click=AcademiaState.calcular,
                    **BTN_PRIMARY_BASE,
                    width="100%", font_size="1em", padding="0.8em", margin_top="0.5em",
                ),
                spacing="4", **CARD_STYLE, padding="2em", width="310px", align="start",
            ),
            # Resultado
            rx.vstack(
                rx.text("TU RESULTADO", font_size="1em", font_weight="800", color=OLIVE, letter_spacing="0.1em"),
                rx.center(
                    rx.vstack(
                        rx.icon(
                            "gauge", size=68,
                            color=rx.cond(AcademiaState.resultado == "APTO", BADGE_GREEN, "#aaa"),
                        ),
                        rx.text(
                            AcademiaState.porcentaje,
                            "% del objetivo",
                            font_size="1.05em", font_weight="700", color="black",
                        ),
                        align="center", spacing="2",
                    ),
                    background=GRAY_LIGHT, border_radius="50%",
                    width="185px", height="185px",
                ),
                rx.cond(
                    AcademiaState.resultado != "",
                    rx.box(
                        rx.hstack(
                            rx.cond(
                                AcademiaState.resultado == "APTO",
                                rx.icon("check-circle", size=20, color="white"),
                                rx.icon("x-circle",     size=20, color="white"),
                            ),
                            rx.text(
                                AcademiaState.resultado,
                                font_size="1.35em", font_weight="900",
                                color="white", letter_spacing="0.1em",
                            ),
                            spacing="2", align="center",
                        ),
                        background=rx.cond(AcademiaState.resultado == "APTO", BADGE_GREEN, BADGE_GRAY),
                        border_radius="12px", padding="0.7em 2em",
                        box_shadow="0 4px 16px rgba(0,0,0,0.2)",
                    ),
                    rx.text(
                        "Rellena el formulario y pulsa Calcular",
                        font_size="0.9em", color=TEXT_MID, text_align="center",
                    ),
                ),
                spacing="4", align="center",
                **CARD_STYLE, padding="2em", flex="1", min_width="260px", justify="center",
            ),
            spacing="5", width="100%", max_width="780px", align="start", wrap="wrap",
        ),
        back_button(),
        align="center", spacing="4", padding_top="2em", width="100%",
    )
