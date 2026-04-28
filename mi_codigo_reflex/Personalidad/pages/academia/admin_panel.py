import reflex as rx
from Personalidad.states.base_state import State
from Personalidad.states.admin_state import AdminState
from Personalidad.pages.academia.layout import academia_layout, BTN_PRIMARY_BASE, BTN_SECONDARY_BASE, CARD_STYLE


def admin_header() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.heading("Panel de Administración", size="9", color="white", font_weight="900"),
            rx.text(
                "Gestión integral de alumnos y recursos.",
                color="rgba(255,255,255,0.8)",
                font_size="1.1em",
            ),
            align_items="start",
            spacing="1",
        ),
        rx.spacer(),
        rx.link(
            rx.button(
                rx.icon("log-out", size=18),
                "Salir a Academia",
                background_color="white",
                color="#5B733A",
                font_weight="bold",
                height="3em",
                padding_x="1.5em",
                border_radius="10px",
                _hover={"background_color": "#f0f0f0", "transform": "scale(1.02)"},
            ),
            href="/academia",
            underline="none",
        ),
        align="center",
        width="100%",
        padding_top="4em", # ESPACIO EXTRA ARRIBA
        padding_bottom="3em",
        flex_direction=["column", "row"],
        gap="2em",
    )


def user_management_row(user: dict) -> rx.Component:
    """Fila de usuario hiper-flexible y adaptativa."""
    return rx.flex(
        # Bloque de Información Principal
        rx.vstack(
            rx.flex(
                rx.text(user["full_name"], font_weight="800", color="black", font_size="1.2em"),
                rx.badge(user["rol"], color_scheme=rx.cond(user["rol"] == "admin", "tomato", "blue"), variant="solid"),
                spacing="3",
                align="center",
                flex_wrap="wrap",
            ),
            rx.text(user["email"], font_size="1em", color="#555", font_weight="500"),
            align_items="start",
            spacing="1",
            flex="1",
        ),
        
        # Bloque de Datos y Acciones
        rx.flex(
            rx.vstack(
                rx.text("Accesos", font_size="0.8em", color="#666", font_weight="bold"),
                rx.text(user["count_login"], font_weight="900", color="#5B733A", font_size="1.3em"),
                spacing="0", align="center",
                min_width="80px",
            ),
            rx.button(
                rx.icon("settings", size=20),
                "Gestionar",
                on_click=AdminState.select_user(user),
                background_color="#5B733A",
                color="white",
                height="3.5em",
                width=["100%", "auto"], # Ancho completo en móvil
                padding_x="2em",
                border_radius="12px",
                font_weight="bold",
                _hover={"transform": "translateY(-2px)", "box_shadow": "0 4px 12px rgba(0,0,0,0.2)"},
            ),
            spacing="6",
            align="center",
            width=["100%", "auto"], # Ancho completo en móvil
            justify="between",
        ),
        
        width="100%",
        padding="2em",
        border_radius="20px",
        background="white",
        border="1px solid #eee",
        box_shadow="0 6px 20px rgba(0,0,0,0.06)",
        align="center",
        margin_bottom="1.5em",
        flex_direction=["column", "row"], # Magia de flexibilidad
        gap="2em",
        opacity="1",
    )


def admin_card(title: str, icon_name: str, *children, **kwargs) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon(icon_name, size=30, color="#5B733A"),
            rx.heading(title, size="7", color="black", font_weight="900"),
            spacing="4",
            align="center",
            margin_bottom="2em",
        ),
        rx.vstack(
            *children,
            width="100%",
            spacing="6",
        ),
        **kwargs,
        background="white",
        border_radius="30px",
        padding=["1.5em", "3em"],
        width="100%",
        align_items="start",
        box_shadow="0 15px 50px rgba(0,0,0,0.12)",
    )


@rx.page(route="/academia/admin_panel", title="Panel Admin", on_load=AdminState.on_load)
def admin_panel() -> rx.Component:
    return academia_layout(
        rx.flex(
            admin_header(),
            
            # Filtros Adaptativos
            rx.flex(
                rx.input(
                    placeholder="Buscar alumno por nombre o email...",
                    width=["100%", "100%", "65%"],
                    background="white",
                    height="4em",
                    color="black",
                    font_size="1.05em",
                    border="1px solid #ccd1d1", # BORDE MÁS FINO Y ELEGANTE
                    padding_x="1.5em",
                    border_radius="15px",
                    on_change=AdminState.set_search_query,
                    _focus={"border": "2px solid #5B733A"},
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
                    border="1px solid #ccd1d1",
                    border_radius="15px",
                ),
                width="100%",
                spacing="4",
                flex_wrap="wrap",
                margin_bottom="3em",
                justify="between",
            ),

            rx.flex(
                # Lista de Alumnos Principal
                admin_card(
                    "Gestión de Alumnos", "users",
                    rx.cond(
                        AdminState.is_loading,
                        rx.center(rx.spinner(size="3", color="#5B733A"), width="100%", padding="5em"),
                        rx.vstack(
                            rx.foreach(AdminState.filtered_users, user_management_row),
                            width="100%",
                        )
                    ),
                    flex="2",
                ),
                
                # Recursos y Herramientas
                rx.vstack(
                    admin_card(
                        "Recursos PDF", "cloud-upload",
                        rx.upload(
                            rx.center(
                                rx.vstack(
                                    rx.icon("upload", size=45, color="#5B733A"),
                                    rx.text("Cargar Archivos", font_weight="800"),
                                    spacing="2",
                                ),
                                width="100%",
                                height="220px",
                            ),
                            border="2px dashed #5B733A",
                            border_radius="20px",
                        ),
                    ),
                    width=["100%", "100%", "420px"],
                    spacing="8",
                ),
                width="100%",
                spacing="8",
                flex_direction=["column", "column", "row"],
                align_items="start",
            ),
            
            direction="column",
            width="100%",
            max_width="1600px",
            padding_x=["1em", "2em", "5em"],
            padding_bottom="10em",
            align_items="center",
        )
    )