import reflex as rx
from Personalidad.states.base_state import State
from Personalidad.states.admin_state import AdminState
from Personalidad.pages.academia.layout import academia_layout, BTN_PRIMARY_BASE, BTN_SECONDARY_BASE, CARD_STYLE


def admin_header() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.heading("Administración", size="9", color="white", font_weight="900"),
            rx.text(
                "Gestión de alumnos y recursos de la academia.",
                color="rgba(255,255,255,0.8)",
                font_size="1.2em",
            ),
            align="start",
            spacing="1",
        ),
        rx.spacer(),
        rx.link(
            rx.button(
                rx.icon("home", size=20),
                "Ir a Academia",
                background_color="transparent",
                color="white",
                border="2px solid white",
                height="3.5em",
                _hover={"background_color": "rgba(255,255,255,0.1)"},
            ),
            href="/academia", # EL ÍNDICE DE ACADEMIA
            underline="none",
        ),
        align="center",
        width="100%",
        margin_bottom="4em",
        padding_y="1em",
    )


def user_management_row(user: dict) -> rx.Component:
    """Fila de usuario flexible, espaciosa y sólida."""
    return rx.flex(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.text(user["full_name"], font_weight="800", color="black", font_size="1.2em"),
                    rx.badge(user["rol"], color_scheme=rx.cond(user["rol"] == "admin", "tomato", "blue"), variant="solid"),
                    align="center",
                    spacing="3",
                ),
                rx.text(user["email"], font_size="1em", color="#444", font_weight="500"),
                spacing="2", align="start",
            ),
            spacing="4",
        ),
        rx.spacer(),
        rx.hstack(
            rx.vstack(
                rx.text("Accesos", font_size="0.85em", color="#666", font_weight="bold"),
                rx.text(user["count_login"], font_weight="900", color="#5B733A", font_size="1.4em"),
                spacing="0", align="center"
            ),
            rx.menu.root(
                rx.menu.trigger(
                    rx.button(
                        rx.icon("settings-2", size=22),
                        "Gestionar",
                        background_color="#5B733A",
                        color="white",
                        height="3.5em",
                        padding_x="1.5em",
                        border_radius="12px",
                        _hover={"transform": "scale(1.05)"},
                    ),
                ),
                rx.menu.content(
                    rx.menu.item(
                        "Planes y Perfil",
                        on_select=AdminState.select_user(user),
                        icon="user"
                    ),
                    rx.menu.separator(),
                    rx.menu.item(
                        "Eliminar", 
                        color="white", 
                        background_color="#e5484d",
                        on_select=rx.window_alert("Protegido.")
                    ),
                ),
            ),
            spacing="6",
            align="center",
        ),
        width="100%",
        padding="2em", # MÁS ESPACIO INTERNO
        border_radius="18px",
        background="white",
        border="1px solid #eee",
        box_shadow="0 6px 15px rgba(0,0,0,0.06)",
        align="center",
        margin_bottom="1.5em", # MÁS ESPACIO ENTRE FILAS
    )


def admin_card(title: str, icon_name: str, *children, **kwargs) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon(icon_name, size=32, color="#5B733A"),
            rx.heading(title, size="7", color="black", font_weight="900"),
            spacing="4",
            align="center",
            margin_bottom="2.5em",
        ),
        rx.vstack(
            *children,
            width="100%",
            spacing="5", # MÁS ESPACIO ENTRE ELEMENTOS HIJOS
        ),
        **kwargs,
        background="white",
        border_radius="28px",
        padding="3em", # MÁS ESPACIO INTERNO EN LA TARJETA
        width="100%",
        align="start",
        box_shadow="0 12px 45px rgba(0,0,0,0.12)",
    )


@rx.page(route="/academia/admin_panel", title="Panel Admin", on_load=AdminState.on_load)
def admin_panel() -> rx.Component:
    return academia_layout(
        rx.flex(
            admin_header(),
            
            # FILTROS Y BÚSQUEDA MÁS ESPACIADOS
            rx.flex(
                rx.input(
                    placeholder="Buscar alumno por nombre o email...",
                    width=["100%", "100%", "65%"],
                    background="white",
                    height="4em",
                    color="black",
                    font_weight="500",
                    font_size="1.1em",
                    border="2px solid #5B733A",
                    padding_x="1.5em",
                    on_change=AdminState.set_search_query,
                ),
                rx.select(
                    ["todos", "estudiante", "admin"],
                    value=AdminState.filter_role,
                    on_change=AdminState.set_filter_role,
                    height="4em",
                    width=["100%", "100%", "30%"],
                    background="white",
                    color="black",
                    font_weight="600",
                    border="2px solid #5B733A",
                ),
                width="100%",
                spacing="6",
                flex_wrap="wrap",
                margin_bottom="3em",
                justify="between",
            ),

            rx.flex(
                # SECCIÓN IZQUIERDA: LISTA
                admin_card(
                    "Listado de Alumnos", "users",
                    rx.cond(
                        AdminState.is_loading,
                        rx.center(rx.spinner(size="3", color="#5B733A"), width="100%", padding="4em"),
                        rx.vstack(
                            rx.foreach(AdminState.filtered_users, user_management_row),
                            width="100%",
                        )
                    ),
                    flex="1.8",
                ),
                
                # SECCIÓN DERECHA: EXTRAS
                rx.vstack(
                    admin_card(
                        "Subir Recursos", "upload",
                        rx.upload(
                            rx.center(
                                rx.vstack(
                                    rx.icon("cloud-upload", size=50, color="#5B733A"),
                                    rx.text("Arrastre archivos aquí", font_weight="bold", font_size="1.1em"),
                                    rx.text("PDF, Imágenes o Vídeos", font_size="0.8em", color="#777"),
                                    spacing="3",
                                ),
                                width="100%",
                                height="200px",
                            ),
                            border="2px dashed #5B733A",
                            border_radius="20px",
                        ),
                    ),
                    width=["100%", "100%", "400px"],
                    spacing="8",
                ),
                width="100%",
                spacing="8",
                flex_direction=["column", "column", "row"],
                align_items="start",
            ),
            
            direction="column",
            width="100%",
            max_width="1500px", # MÁS ANCHO TOTAL
            padding_x=["1em", "2em", "4em"],
            padding_bottom="5em",
            align_items="center",
        )
    )