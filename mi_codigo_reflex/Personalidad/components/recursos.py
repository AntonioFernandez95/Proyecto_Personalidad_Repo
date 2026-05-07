import reflex as rx
from Personalidad.states.detallesTecnicas_state import DetallesTecnicasState

OLIVE = "#5B733A"
TEXT_DARK = "#2b2b2b"
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

def pdf_section() -> rx.Component:
    """Sección de PDFs dinámicos para las pruebas."""
    return rx.cond(
        DetallesTecnicasState.pdfs.length() > 0,
        rx.vstack(
            rx.text("RECURSOS Y GUÍAS PDF", font_size="1.1em", font_weight="800", color=TEXT_DARK, letter_spacing="0.05em"),
            rx.vstack(
                rx.foreach(
                    DetallesTecnicasState.pdfs,
                    lambda pdf: rx.link(
                        rx.hstack(
                            rx.icon("file-down", color=OLIVE),
                            rx.text(pdf["nombre"], font_size="0.95em", color="black", font_weight="500"),
                            rx.spacer(),
                            rx.icon("chevron-right", color="gray", size=18),
                            width="100%",
                            padding="1em",
                            border_radius="10px",
                            background=GRAY_LIGHT,
                            _hover={"background": "#e2e2e2"}
                        ),
                        href=pdf["url"].to(str),
                        is_external=True,
                        width="100%",
                        underline="none"
                    )
                ),
                width="100%",
                spacing="3"
            ),
            align="start",
            width="100%",
            margin_top="1.5em"
        )
    )
