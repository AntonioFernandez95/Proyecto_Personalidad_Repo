import reflex as rx
from Personalidad.states.base_state import State
from Personalidad.pages.academia.layout import academia_layout, BTN_PRIMARY_BASE, BTN_SECONDARY_BASE, CARD_STYLE

# --- ESTADO CON AUTO-SINCRONIZACIÓN ---
class UploadState(State):
    lista_archivos: list[str] = []

    def sync_files(self, files: list[str]):
        """Esta función se ejecuta sola y añade lo nuevo a la lista"""
        for file in files:
            if file not in self.lista_archivos:
                self.lista_archivos.append(file)

def admin_header() -> rx.Component:
    return rx.vstack(
        rx.heading("Panel de Control - Administración", size="8", color="white", font_weight="900"),
        rx.badge("INTERFAZ FRONTEND - SIN CONEXIÓN DB", color_scheme="orange", variant="solid", margin_top="0.5em"),
        rx.text(
            "Gestión centralizada de usuarios y configuración del sitio.",
            color="rgba(255,255,255,0.7)",
            font_size="1.1em",
        ),
        align="center",
        width="100%",
        margin_bottom="3em",
    )

def user_management_row(email: str, username: str, expiration: str) -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.text(username, font_weight="800", color="black", font_size="1.1em"),
            rx.text(email, font_size="0.85em", color="#666"),
            spacing="0", align="start",
        ),
        rx.spacer(),
        rx.vstack(
            rx.text("Vencimiento", font_size="0.75em", color="#888"),
            rx.text(expiration, font_weight="800", color="#5B733A", font_size="1.1em"),
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
                rx.menu.item("Cambiar Correo", on_click=rx.window_alert("Función de cambio de email (UI)")),
                rx.menu.item("Reenviar Claves", on_click=rx.window_alert("Función de reenvío (UI)")),
                rx.menu.separator(),
                rx.menu.item(
                    rx.link("Gestionar Planes", href="/admin/planes", color="inherit", underline="none"),
                ),
                rx.menu.item("Desactivar Usuario", color="white", background_color="#e5484d"),
            ),
            padding="0",
        ),
        width="100%",
        padding="1.2em",
        border_radius="12px",
        background="white",
        box_shadow="0 4px 12px rgba(0,0,0,0.08)",
        align="center",
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

@rx.page(route="/admin", title="Panel de Control - Administración", on_load=State.check_login)
def admin_panel() -> rx.Component:
    return academia_layout(
        admin_header(),
        rx.hstack(
            # COLUMNA IZQUIERDA
            admin_card(
                "Búsqueda y Gestión", "users",
                rx.hstack(
                    rx.input(placeholder="Buscar por email o nombre...", width="100%", border_radius="10px", background="#f9f9f9", height="3em"),
                    rx.button(rx.icon("search"), background_color="#5B733A", color="white", height="3em", width="3em", border_radius="10px"),
                    width="100%",
                    spacing="3",
                ),
                rx.vstack(
                    rx.text("Lista de Usuarios", font_size="1em", color="#aaa", margin_top="1.5em", margin_bottom="0.5em"),
                    user_management_row("ejemplo1@gmail.com", "juan_perez", "2026-12-31"),
                    user_management_row("admin_test@academiametodos.com", "admin_demo", "2027-01-15"),
                    width="100%",
                    spacing="4",
                ),
                flex="1.4",
            ),
            
            # COLUMNA DERECHA
            admin_card(
                "Recursos Académicos", "upload-cloud",
                rx.text("Subir PDFs o Clases", font_size="0.9em", color="#888", margin_bottom="0.5em"),
                
                # ÁREA DE UPLOAD
                rx.vstack(
                    rx.upload(
                        rx.vstack(
                            rx.button(
                                "Seleccionar Archivo", 
                                background_color="#7d804e", 
                                color="white", 
                                padding_x="2em",
                                height="3em",
                                border_radius="4px",
                            ),
                            rx.text("Arrastra aquí tu contenido", font_size="0.9em", color="#333", font_weight="500"),
                            spacing="2",
                        ),
                        id="upload_resources",
                        multiple=True,
                        border="2px dashed #ddd",
                        padding="2em",
                        width="100%",
                    ),
                    
                    # --- EL TRUCO MAGAL ---
                    # Este componente detecta cuando pasas el ratón por encima o cerca del área
                    # y sincroniza la lista automáticamente sin botones.
                    on_mouse_over=UploadState.sync_files(rx.selected_files("upload_resources")),
                    on_mouse_leave=UploadState.sync_files(rx.selected_files("upload_resources")),
                    width="100%",
                ),

                rx.vstack(
                    rx.cond(
                        UploadState.lista_archivos,
                        rx.text("Archivos seleccionados:", font_size="0.8em", color="#aaa", margin_top="1em"),
                        rx.fragment()
                    ),
                    rx.foreach(
                        UploadState.lista_archivos,
                        lambda file: rx.hstack(
                            rx.icon("file-text", size=20, color="#5B733A"),
                            rx.text(file, font_size="0.9em", color="#222", font_weight="700"),
                            rx.spacer(),
                            rx.icon("circle-check-big", size=18, color="#5B733A"),
                            width="100%",
                            background="white",
                            padding="0.8em 1.2em",
                            border_radius="10px",
                            box_shadow="0 2px 6px rgba(0,0,0,0.05)",
                            border="1px solid #eee",
                        )
                    ),
                    spacing="3",
                    width="100%",
                    margin_top="1em",
                ),
                flex="1",
            ),
            spacing="8",
            width="100%",
            align_items="stretch",
            max_width="1200px",
        ),
        align="center",
        width="100%",
    )