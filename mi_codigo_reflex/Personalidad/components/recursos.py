import reflex as rx
from Personalidad.states.detallesTecnicas_state import DetallesTecnicasState


OLIVE = "#5B733A"
TEXT_DARK = "#2b2b2b"
TEXT_MID = "#666666"
GRAY_LIGHT = "#f5f5f5"


def video_section() -> rx.Component:
    """Sección de vídeos dinámicos para las pruebas."""
    return rx.vstack(
        rx.foreach(
            DetallesTecnicasState.videos,
            lambda vid: rx.center(
                rx.cond(
                    vid["url"].to(str).contains("embed") | vid["url"].to(str).contains("player"),
                    rx.box(
                        rx.el.iframe(
                            src=vid["url"].to(str),
                            border="none",
                            height="100%",
                            width="100%",
                            allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture; fullscreen",
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
                        }
                    ),
                    rx.video(
                        url=vid["url"].to(str),
                        width="100%",
                        height="auto",
                        border_radius="12px",
                    ),
                ),
                width="100%",
                margin_bottom="1.5em"
            )
        ),
        # Si no hay vídeos, mostramos el placeholder
        rx.cond(
            DetallesTecnicasState.videos.length() == 0,
            rx.center(
                rx.vstack(
                    rx.icon("circle-play", size=46, color="white"),
                    rx.text("PRÓXIMAMENTE VÍDEO TÉCNICO", color="white", font_size="0.84em", font_weight="bold"),
                    align="center",
                ),
                background="black", border_radius="12px",
                width="100%", height="200px", margin_bottom="1em"
            )
        ),
        width="100%"
    )


def render_pdf_item(pdf: dict) -> rx.Component:
    """Renderiza un ítem individual de PDF con icono, nombre y botón de descarga."""
    return rx.link(
        rx.hstack(
            rx.icon("file-text", color=OLIVE, size=20),
            rx.text(pdf["nombre"], font_size="0.75em", color=TEXT_DARK, font_weight="500", flex="1"),
            rx.icon("download", color=TEXT_MID, size=18),
            width="100%",
            padding="0.8em 1.2em",
            border_radius="10px",
            _hover={"background": "#e8f5e9", "transform": "translateX(5px)"},
            transition="all 0.2s ease"
        ),
        href=pdf["url"].to(str),
        is_external=True,
        underline="none",
        width="100%"
    )


def pdf_section(pdfs_list: rx.Var = None) -> rx.Component:
    """Sección de PDFs dinámicos con componente desplegable (Accordion)."""
    # Si no se proporciona una lista, usamos la de DetallesTecnicasState por defecto
    target_pdfs = pdfs_list if pdfs_list is not None else DetallesTecnicasState.pdfs
   
    return rx.box(
        rx.vstack(
            rx.text(
                "RECURSOS Y GUÍAS PDF",
                font_size="1.1em",
                font_weight="800",
                color=rx.color_mode_cond(light=TEXT_DARK, dark="#e2e2e2"),
                letter_spacing="0.05em",
                margin_bottom="0.5em"
            ),
            rx.accordion.root(
                rx.accordion.item(
                    rx.accordion.trigger(
                        rx.hstack(
                            rx.icon("file-text", size=16, color=OLIVE),
                            rx.text("VER RECURSOS Y GUÍAS PDF", font_size="0.75em", font_weight="700", color=TEXT_DARK),
                            rx.spacer(),
                            rx.accordion.icon(color=TEXT_MID, size=16),
                            width="100%",
                            padding="0.4em 0.8em",
                            background_color="white",
                            border_radius="6px",
                            _hover={"background_color": "#f8f9fa"},
                        ),
                        style={
                            "background_color": "white !important",
                            "padding": "0",
                            "width": "100%",
                            "border": "none",
                        },
                        _hover={"background_color": "white !important"},
                    ),
                    rx.accordion.content(
                        rx.vstack(
                            rx.cond(
                                target_pdfs.length() > 0,
                                rx.vstack(
                                    rx.foreach(target_pdfs, render_pdf_item),
                                    width="100%",
                                    spacing="0",
                                    padding="0.2em 0",
                                    background_color="white"
                                ),
                                rx.center(
                                    rx.vstack(
                                        rx.icon("info", size=14, color=TEXT_MID),
                                        rx.text("Sin recursos", font_size="0.7em", font_style="italic", color=TEXT_MID),
                                        spacing="2",
                                        padding="0.8em"
                                    ),
                                    width="100%",
                                    background_color="white"
                                )
                            ),
                            width="100%",
                            background_color="white"
                        ),
                        width="100%",
                        padding="0",
                        background_color="white"
                    ),
                    value="resources",
                    border="none",
                    background_color="white"
                ),
                width="100%",
                collapsible=True,
                accent_color="grass",
                style={
                    "border": "1px solid #e2e2e2",
                    "border_radius": "8px",
                    "overflow": "hidden",
                    "max_width": "700px",
                    "background_color": "white !important",
                }
            ),
            align="start",
            width="100%",
            spacing="0"
        ),
        background_color="white",
        width="100%",
        margin_top="0.5em"
    )
