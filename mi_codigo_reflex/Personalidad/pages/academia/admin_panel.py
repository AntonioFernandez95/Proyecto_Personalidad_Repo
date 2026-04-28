import reflex as rx
from Personalidad.states.base_state import State
from Personalidad.states.admin_state import AdminState
from Personalidad.pages.academia.layout import academia_layout, BTN_PRIMARY_BASE, BTN_SECONDARY_BASE, CARD_STYLE


def admin_header() -> rx.Component:
    return rx.vstack(
        rx.heading("Panel de Control - Administración", size="8", color="white", font_weight="900"),
        rx.badge("CONEXIÓN REAL ESTABLECIDA", color_scheme="green", variant="solid", margin_top="0.5em"),
        rx.text(
            "Gestión centralizada de usuarios y configuración del sitio.",
            color="rgba(255,255,255,0.7)",
            font_size="1.1em",
        ),
        align="center",
        width="100%",
        margin_bottom="3em",
    )


def user_management_row(user: dict) -> rx.Component:
    """Representa una fila de usuario con datos reales de la BD."""
    return rx.hstack(
        rx.vstack(
            rx.hstack(
                rx.text(user["full_name"], font_weight="800", color="black", font_size="1.1em"),
                rx.badge(user["rol"], color_scheme=rx.cond(user["rol"] == "admin", "tomato", "blue"), size="1"),
            ),
            rx.text(user["email"], font_size="0.85em", color="#666"),
            spacing="1", align="start",
        ),
        rx.spacer(),
        rx.vstack(
            rx.text("Accesos", font_size="0.75em", color="#888"),
            rx.text(user["count_login"], font_weight="800", color="#5B733A", font_size="1.1em"),
            spacing="0", align="end"
        ),
        rx.menu.root(
            rx.menu.trigger(
                rx.button(
                    rx.icon("more-vertical", size=20),
                    variant="soft",
                    color_scheme="gray",
                    background_color="#7a8c5f",
                    color="black",
                    height="3.5em",
                    width="2.5em"
                ),
            ),
            rx.menu.content(
                rx.menu.item(
                    "Gestionar Planes / Perfil",
                    on_select=AdminState.select_user(user),
                    icon="settings"
                ),
                rx.menu.separator(),
                rx.menu.item(
                    "Eliminar Usuario (Permanente)", 
                    color="white", 
                    background_color="#e5484d",
                    on_select=rx.window_alert("Función de borrado permanente deshabilitada por seguridad.")
                ),
            ),
            padding="0",
        ),
        width="100%",
        padding="1.2em",
        border_radius="12px",
        background="white",
        box_shadow="0 4px 12px rgba(0,0,0,0.08)",
        align="center",
        opacity="1",
    )


def admin_card(title: str, icon_name: str, *children, **kwargs) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon(icon_name, size=24, color="#5B733A"),
            rx.heading(title, size="5", color="black", font_weight="800"),
            spacing="2",
            align="center",
            margin_bottom="1.5em",
        ),
        *children,
        **kwargs,
        background="white",
        border_radius="20px",
        box_shadow="0 8px 32px rgba(0,0,0,0.12)",
        padding="2em",
        width="100%",
        align="start",
    )


@rx.page(route="/academia/admin_panel", title="Panel de Control - Administración", on_load=AdminState.on_load)
def admin_panel() -> rx.Component:
    return academia_layout(
        admin_header(),
        rx.hstack(
            # COLUMNA IZQUIERDA: GESTIÓN DE USUARIOS
            admin_card(
                "Búsqueda y Gestión", "users",
                rx.vstack(
                    rx.hstack(
                        rx.input(
                            placeholder="Buscar por email o nombre...",
                            width="100%",
                            border_radius="10px",
                            background="white",
                            height="3em",
                            color="black",
                            border="1px solid #ddd",
                            on_change=AdminState.set_search_query,
                        ),
                        rx.select(
                            ["todos", "estudiante", "admin"],
                            value=AdminState.filter_role,
                            on_change=AdminState.set_filter_role,
                            placeholder="Rol",
                            height="3em",
                            width="150px",
                            color="black",
                        ),
                        width="100%",
                        spacing="3",
                    ),
                    rx.hstack(
                        rx.text("Lista de Usuarios", font_size="1em", color="#aaa", margin_top="1.5em"),
                        rx.spacer(),
                        rx.cond(
                            AdminState.is_loading,
                            rx.spinner(size="1", color="#5B733A"),
                            rx.fragment()
                        ),
                        width="100%",
                    ),
                    rx.vstack(
                        rx.foreach(
                            AdminState.filtered_users,
                            user_management_row
                        ),
                        width="100%",
                        spacing="4",
                    ),
                    rx.cond(
                        ~AdminState.filtered_users,
                        rx.text("No se han encontrado usuarios.", color="#999", margin_top="2em"),
                        rx.fragment()
                    ),
                    width="100%",
                ),
                flex="1.6",
            ),

            # COLUMNA DERECHA: RECURSOS
            admin_card(
                "Recursos", "upload-cloud",
                rx.upload(
                    rx.vstack(
                        rx.button(
                            "Subir PDF",
                            background_color="#7d804e",
                            color="white",
                            width="100%",
                        ),
                        rx.text("Arrastra archivos aquí", font_size="0.8em", color="#888"),
                        spacing="2",
                    ),
                    id="upload_resources",
                    border="2px dashed #ddd",
                    padding="1.5em",
                    width="100%",
                ),
                flex="0.8",
            ),
            spacing="8",
            width="100%",
            align_items="stretch",
            max_width="1200px",
        ),
        align="center",
        width="100%",
    )