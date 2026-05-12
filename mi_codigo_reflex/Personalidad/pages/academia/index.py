import reflex as rx
from Personalidad.pages.academia.layout import academia_layout, big_card
from Personalidad.states.base_state import State

def notification_popup() -> rx.Component:
    """Popup de notificación de novedades para alumnos."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.center(
                    rx.icon("bell-ring", size=45, color="#5B733A"),
                    width="80px",
                    height="80px",
                    background="rgba(91, 115, 58, 0.1)",
                    border_radius="full",
                    margin_bottom="1em",
                ),
                rx.dialog.title(
                    "¡NUEVO SIMULACRO DISPONIBLE!",
                    font_weight="900",
                    size="6",
                    color="#5B733A",
                    text_align="center",
                ),
                rx.dialog.description(
                    "Se ha publicado o actualizado un simulacro presencial. ¿Quieres verlo ahora?",
                    text_align="center",
                    color="rgba(0,0,0,0.6)",
                    margin_bottom="1.5em",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cerrar",
                            variant="soft",
                            color_scheme="gray",
                            border_radius="15px",
                            on_click=State.close_notification,
                        ),
                    ),
                    rx.link(
                        rx.button(
                            "Abrir Simulacros",
                            background_color="#5B733A",
                            color="white",
                            border_radius="15px",
                            on_click=[State.close_notification, State.clear_update_flag],
                        ),
                        href="/academia/simulacro",
                    ),
                    spacing="4",
                    justify="center",
                    width="100%",
                ),
                align="center",
                padding="1em",
            ),
            background="rgba(255, 255, 255, 0.95)",
            backdrop_filter="blur(15px)",
            border_radius="35px",
            border="1px solid rgba(255, 255, 255, 0.8)",
            box_shadow="0 25px 50px -12px rgba(0, 0, 0, 0.25)",
            padding="2em",
            max_width="450px",
        ),
        open=State.show_notification,
    )

@rx.page(route="/academia", title="Academia Online - Dashboard", on_load=[State.check_login, State.refresh_user_data, State.check_for_updates])
def index() -> rx.Component:
    return academia_layout(
        rx.vstack(
            rx.vstack(
                rx.text(rx.text.span("👋 BIENVENIDO, "), rx.text.span(State.user), font_size="1.15em", color="rgba(255,255,255,0.85)", font_weight="700", letter_spacing="0.1em"),
                rx.text("ACADEMIA ONLINE", font_size="2.8em", font_weight="900", color="white", letter_spacing="0.1em"),
                rx.text("Selecciona tu área de entrenamiento", font_size="1.05em", color="rgba(255,255,255,0.8)"),
                align="center", spacing="1", margin_bottom="1.5em",
            ),
            rx.hstack(
                rx.cond(
                    State.has_personalidad_access,
                    big_card("brain",           "TEST DE PERSONALIDAD", "Historial y nuevos simulacros", "Comenzar Test",    "/info"),
                ),
                # RESTRICCIÓN: Solo se muestra la tarjeta de Físicas si el usuario tiene acceso (plan contratado o admin)
                rx.cond(
                    State.has_fisicas_access,
                    big_card("person-standing", "PRUEBAS FÍSICAS",      "Curso completo y herramientas", "Acceder al Curso", "/academia/fisicas"),
                ),
                spacing="8", wrap="wrap", justify="center", align_items="stretch",
            ),
            notification_popup(),
            width="100%",
            align="center",
        ),
    )