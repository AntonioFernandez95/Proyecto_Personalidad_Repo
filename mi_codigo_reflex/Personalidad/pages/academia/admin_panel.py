import reflex as rx
from Personalidad.states.base_state import State
from Personalidad.states.admin_state import AdminState
from Personalidad.states.simulacro_state import SimulacroState
from Personalidad.pages.academia.layout import academia_layout, BTN_PRIMARY_BASE, BTN_SECONDARY_BASE, CARD_STYLE
from Personalidad.styles.academia_styles import TEXT_DARK, TEXT_MID, CARD_BG, GRAY_LIGHT

def admin_header() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.heading("Panel de Administración", size="9", color=TEXT_DARK, font_weight="900", text_align="center"),
            rx.text(
                "Gestión integral de alumnos y recursos (PDFs y Vídeos).",
                color=TEXT_MID,
                font_size="1.1em",
                text_align="center",
            ),
            align_items="center",
            spacing="1",
            width="100%",
        ),
        rx.link(
            rx.button(
                rx.icon("log-out", size=18),
                "Salir a Academia",
                background_color=CARD_BG,
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
        justify="center",
        width="100%",
        padding_top="4em",
        padding_bottom="3em",
        flex_direction="column",
        gap="2em",
    )

def user_management_row(user: dict) -> rx.Component:
    """Fila de usuario hiper-flexible y adaptativa."""
    return rx.flex(
        # Bloque de Información Principal
        rx.vstack(
            rx.flex(
                rx.text(user["full_name"], font_weight="800", color=TEXT_DARK, font_size="1.4em"),
                rx.badge(user["rol"], color_scheme=rx.cond(user["rol"] == "admin", "tomato", "blue"), variant="solid", size="3"),
                spacing="3",
                align="center",
                flex_wrap="wrap",
            ),
            rx.text(user["email"], font_size="1.1em", color=TEXT_MID, font_weight="500"),
            align_items="start",
            spacing="1",
            flex="1",
        ),
       
        # Bloque de Datos y Acciones
        rx.flex(
            rx.vstack(
                rx.text("Accesos", font_size="0.9em", color=TEXT_MID, font_weight="bold"),
                rx.text(user["count_login"], font_weight="900", color="#5B733A", font_size="1.6em"),
                spacing="0", align="center",
                min_width="80px",
            ),
            rx.button(
                rx.icon("settings", size=24),
                "Gestionar",
                on_click=AdminState.select_user(user),
                background_color="#5B733A",
                color="white",
                height="4em",
                font_size="1.1em",
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
        padding="2.5em",
        border_radius="20px",
        background=CARD_BG,
        border=rx.color_mode_cond(light="1px solid #eee", dark="1px solid #333"),
        box_shadow="0 6px 20px rgba(0,0,0,0.06)",
        align="center",
        margin_bottom="1.5em",
        flex_direction=["column", "row"], # Magia de flexibilidad
        gap="2em",
        opacity="1",
    )

def resource_item(recurso: dict) -> rx.Component:
    """Representación de un recurso (PDF o Vídeo) en la lista del admin."""
    return rx.hstack(
        rx.cond(
            recurso["tipo"] == "pdf",
            rx.icon("file-text", size=22, color="#5B733A"),
            rx.icon("video", size=22, color="#5B733A"),
        ),
        rx.vstack(
            rx.text(recurso["nombre"], font_weight="bold", font_size="1.1em", color=TEXT_DARK, max_width="250px", is_truncated=True),
            rx.text(recurso["categoria"].to(str).upper(), font_size="0.85em", color=TEXT_MID, font_weight="bold"),
            spacing="0", align="start"
        ),
        rx.spacer(),
        rx.icon(
            "trash-2",
            size=22,
            color="red",
            cursor="pointer",
            on_click=lambda: AdminState.borrar_recurso(recurso)
        ),
        width="100%",
        padding="1.2em",
        border_radius="10px",
        background=GRAY_LIGHT,
        border=rx.color_mode_cond(light="1px solid #eee", dark="1px solid #333")
    )

def simulacro_row(simulacro: dict) -> rx.Component:
    """Fila para gestionar un simulacro existente."""
    return rx.hstack(
        rx.vstack(
            rx.text(simulacro["titulo"], font_weight="bold", color=TEXT_DARK),
            rx.text(f"{simulacro['fecha']} - {simulacro['ubicacion']}", font_size="0.85em", color=TEXT_MID),
            spacing="0", align="start"
        ),
        rx.spacer(),
        rx.hstack(
            rx.icon(
                "pencil",
                size=18,
                color="#5B733A",
                cursor="pointer",
                on_click=lambda: SimulacroState.set_edit_simulacro(simulacro)
            ),
            rx.icon(
                "trash-2",
                size=18,
                color="red",
                cursor="pointer",
                on_click=lambda: SimulacroState.eliminar_simulacro_action(simulacro["id"])
            ),
            spacing="4"
        ),
        width="100%",
        padding="1em",
        border_radius="10px",
        background=GRAY_LIGHT,
        border="1px solid #eee"
    )

def admin_card(title: str, icon_name: str, *children, **kwargs) -> rx.Component:
    # Establecemos valores por defecto que se pueden sobreescribir vía kwargs
    kwargs.setdefault("width", "100%")
    kwargs.setdefault("background", CARD_BG)
    kwargs.setdefault("border_radius", "30px")
    kwargs.setdefault("padding", ["1.5em", "3em"])
    kwargs.setdefault("align_items", "center")
    kwargs.setdefault("box_shadow", "0 15px 50px rgba(0,0,0,0.12)")

    return rx.vstack(
        rx.vstack(
            rx.icon(icon_name, size=36, color="#5B733A"),
            rx.heading(title, size="8", color=TEXT_DARK, font_weight="900", text_align="center"),
            spacing="2",
            align_items="center",
            margin_bottom="2em",
            width="100%",
        ),
        rx.vstack(
            *children,
            width="100%",
            spacing="6",
        ),
        **kwargs,
    )

@rx.page(route="/academia/admin_panel", title="Panel Admin", on_load=[AdminState.on_load, SimulacroState.fetch_simulacros])
def admin_panel() -> rx.Component:
    return academia_layout(
        rx.vstack(
            admin_header(),
            rx.flex(
                # Columna Izquierda: Gestión (Alumnos + Simulacros)
                rx.vstack(
                    # Buscador
                    rx.hstack(
                        rx.icon("search", size=24, color="#888"),
                        rx.input(
                            placeholder="Buscar alumno por nombre o email...",
                            variant="surface",
                            border="none",
                            background_color="transparent",
                            width="100%",
                            color=TEXT_DARK,
                            font_size="1.2em",
                            on_change=AdminState.set_search_query,
                            _focus={"outline": "none", "border": "none", "box_shadow": "none"},
                        ),
                        background=CARD_BG,
                        border=rx.color_mode_cond(light="1px solid #ccd1d1", dark="1px solid #444"),
                        border_radius="15px",
                        padding_x="1.5em",
                        height="5.5em",
                        width="100%",
                        align="center",
                        box_shadow="0 4px 15px rgba(0,0,0,0.05)",
                        _focus_within={"border": "1px solid #5B733A"},
                        margin_bottom="1.5em",
                    ),
                   
                    # Gestión de Alumnos
                    admin_card(
                        "Gestión de Alumnos", "users",
                        rx.cond(
                            AdminState.is_loading,
                            rx.center(rx.spinner(size="3", color="#5B733A"), width="100%", padding="5em"),
                            rx.vstack(
                                # Muestra los primeros 2 usuarios siempre
                                rx.foreach(AdminState.filtered_users[:2], user_management_row),
                                
                                # El resto se oculta bajo un rx.cond (Lógica de expansión)
                                rx.cond(
                                    AdminState.mostrar_todos_alumnos,
                                    rx.vstack(
                                        rx.foreach(AdminState.filtered_users[2:], user_management_row),
                                        width="100%",
                                    ),
                                ),

                                # Botón Ver más / Ver menos (Solo si hay más de 2 usuarios)
                                rx.cond(
                                    AdminState.filtered_users.length() > 2,
                                    rx.center(
                                        rx.button(
                                            rx.hstack(
                                                rx.text(rx.cond(AdminState.mostrar_todos_alumnos, "Ver menos", "Ver más"), color="white"),
                                                rx.cond(
                                                    AdminState.mostrar_todos_alumnos,
                                                    rx.icon("chevron-up", size=20, color="white"),
                                                    rx.icon("chevron-down", size=20, color="white")
                                                ),
                                                spacing="2",
                                                align="center",
                                            ),
                                            on_click=AdminState.alternar_ver_mas,
                                            background_color="#5B733A",
                                            color="white",
                                            border_radius="25px",
                                            padding_x="2em",
                                            height="3em",
                                            font_weight="bold",
                                            margin_top="1em",
                                            _hover={"background_color": "#4a5d2f", "transform": "scale(1.05)"},
                                        ),
                                        width="100%",
                                    )
                                ),
                                width="100%",
                            )
                        ),
                    ),

                    # Gestión de Simulacros (Debajo de alumnos)
                    admin_card(
                        "Gestión de Simulacros", "calendar",
                        rx.vstack(
                            rx.text("Título / Convocatoria:", font_size="0.85em", font_weight="bold", color=TEXT_DARK),
                            rx.input(
                                placeholder="Ej: PRÓXIMA CONVOCATORIA",
                                value=SimulacroState.titulo,
                                on_change=SimulacroState.set_titulo,
                                width="100%",
                                **CARD_STYLE
                            ),
                            rx.text("Fecha del evento:", font_size="0.85em", font_weight="bold", color=TEXT_DARK),
                            rx.input(
                                placeholder="Ej: 25 de Abril, 2026",
                                value=SimulacroState.fecha,
                                on_change=SimulacroState.set_fecha,
                                width="100%",
                                **CARD_STYLE
                            ),
                            rx.text("Ubicación:", font_size="0.85em", font_weight="bold", color=TEXT_DARK),
                            rx.input(
                                placeholder="Ej: Centro Deportivo Municipal",
                                value=SimulacroState.ubicacion,
                                on_change=SimulacroState.set_ubicacion,
                                width="100%",
                                **CARD_STYLE
                            ),
                            rx.text("Descripción corta:", font_size="0.85em", font_weight="bold", color=TEXT_DARK),
                            rx.text_area(
                                placeholder="Escribe aquí los detalles del simulacro...",
                                value=SimulacroState.descripcion,
                                on_change=SimulacroState.set_descripcion,
                                width="100%",
                                height="100px",
                                **CARD_STYLE
                            ),
                            rx.vstack(
                                rx.button(
                                    rx.cond(SimulacroState.edit_id == -1, "Crear Simulacro", "Guardar Cambios"),
                                    on_click=SimulacroState.guardar_simulacro_action,
                                    width="100%",
                                    **BTN_PRIMARY_BASE,
                                    height="3.5em",
                                ),
                                rx.cond(
                                    SimulacroState.edit_id != -1,
                                    rx.button(
                                        "Descartar Cambios",
                                        on_click=SimulacroState.clear_form,
                                        width="100%",
                                        **BTN_SECONDARY_BASE,
                                        height="3.5em",
                                    )
                                ),
                                width="100%",
                                spacing="3"
                            ),
                            rx.divider(margin_y="1em"),
                            rx.text("Simulacros Actuales:", font_weight="bold", color=TEXT_DARK),
                            rx.vstack(
                                rx.foreach(SimulacroState.simulacros, simulacro_row),
                                width="100%",
                                spacing="2"
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        width="100%",
                    ),
                    flex="1.8",
                    width="100%",
                    spacing="6",
                ),
               
                # Columna Derecha: Herramientas
                rx.vstack(
                    # Alta de Alumnos
                    admin_card(
                        "Alta de Alumnos", "user-plus",
                        rx.vstack(
                            rx.text("Nombre Completo:", font_size="0.85em", font_weight="bold", color=TEXT_DARK),
                            rx.input(
                                placeholder="Ej: Juan Pérez",
                                value=AdminState.create_name,
                                on_change=AdminState.set_create_name,
                                width="100%",
                                **CARD_STYLE
                            ),
                            rx.text("Correo Electrónico:", font_size="0.85em", font_weight="bold", color=TEXT_DARK),
                            rx.input(
                                placeholder="correo@ejemplo.com",
                                value=AdminState.create_email,
                                on_change=AdminState.set_create_email,
                                width="100%",
                                **CARD_STYLE
                            ),
                            rx.text("Rol del usuario:", font_size="0.85em", font_weight="bold", color=TEXT_DARK),
                            rx.select(
                                ["estudiante", "admin"],
                                value=AdminState.create_role,
                                on_change=AdminState.set_create_role,
                                width="100%",
                                background=CARD_BG,
                                color=TEXT_DARK,
                            ),
                            rx.divider(margin_y="0.5em"),
                            rx.text("Activar planes:", font_size="0.85em", font_weight="bold", color=TEXT_DARK),
                            rx.hstack(
                                rx.checkbox(
                                    "Test",
                                    checked=AdminState.create_has_personality,
                                    on_change=AdminState.set_create_has_personality,
                                    color_scheme="green",
                                ),
                                rx.checkbox(
                                    "Físicas",
                                    checked=AdminState.create_has_physical,
                                    on_change=AdminState.set_create_has_physical,
                                    color_scheme="green",
                                ),
                                spacing="4",
                                width="100%",
                                justify="center",
                            ),
                            rx.button(
                                "Crear y Enviar Accesos",
                                on_click=AdminState.crear_usuario_manual,
                                width="100%",
                                **BTN_PRIMARY_BASE,
                                height="3.5em",
                                margin_top="1em",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        width="100%",
                    ),

                    # Gestión de Recursos
                    admin_card(
                        "Gestión de Recursos", "cloud-upload",
                        rx.text("Categoría destino:", font_size="0.95em", font_weight="bold", color=TEXT_DARK),
                        rx.select(
                            AdminState.categorias_disponibles,
                            value=AdminState.selected_categoria,
                            on_change=AdminState.set_selected_categoria,
                            width="100%",
                            background=CARD_BG,
                            color=TEXT_DARK,
                            border_radius="10px",
                        ),
                        rx.upload(
                            rx.center(
                                rx.vstack(
                                    rx.icon("upload", size=30, color="#5B733A"),
                                    rx.text("Subir archivos", font_size="1em", font_weight="700", color=TEXT_DARK),
                                    spacing="1",
                                ),
                                width="100%",
                                height="100px",
                            ),
                            id="recursos_upload",
                            border="2px dashed #5B733A",
                            border_radius="15px",
                            padding="1em",
                            width="100%",
                        ),
                        rx.button(
                            "Subir Archivos",
                            on_click=AdminState.handle_upload(rx.upload_files(upload_id="recursos_upload")),
                            width="100%",
                            background_color="#5B733A",
                            color="white",
                            height="3em",
                            border_radius="10px",
                            _hover={"opacity": 0.8}
                        ),
                        rx.divider(margin_y="1em"),
                        rx.text("Añadir vídeo manual (enlace):", font_size="0.95em", font_weight="bold", color=TEXT_DARK),
                        rx.input(
                            placeholder="Nombre del vídeo",
                            value=AdminState.video_manual_nombre,
                            on_change=AdminState.set_video_manual_nombre,
                            width="100%",
                            **CARD_STYLE
                        ),
                        rx.input(
                            placeholder="URL del vídeo (ej: YouTube, Drive...)",
                            value=AdminState.video_manual_url,
                            on_change=AdminState.set_video_manual_url,
                            width="100%",
                            **CARD_STYLE
                        ),
                        rx.button(
                            "Guardar Vídeo Manual",
                            on_click=AdminState.guardar_video_manual,
                            width="100%",
                            background_color="#5B733A",
                            color="white",
                            height="3em",
                            border_radius="10px",
                            _hover={"opacity": 0.8}
                        ),
                        rx.divider(margin_y="0.5em"),
                        rx.hstack(
                            rx.heading("Recursos (PDF y Vídeos)", size="5", color=TEXT_DARK),
                            rx.spacer(),
                            # Este es el botón nuevo que añadí para ir a la biblioteca completa
                            rx.link(
                                rx.button(
                                    "Ver más", 
                                    background_color="#5B733A",
                                    color="white",
                                    border_radius="25px",
                                    padding_x="1.5em",
                                    size="2",
                                    _hover={"background_color": "#4a5d2f", "transform": "scale(1.05)"}
                                ),
                                href="/academia/view_recursos"
                            ),
                            width="100%",
                            align="center",
                            margin_bottom="1em",
                        ),
                        rx.vstack(
                            rx.foreach(AdminState.ultimos_recursos, resource_item),
                            width="100%",
                            spacing="2",
                        ),
                        width="100%",
                    ),
                    width=["100%", "100%", "450px"],
                    spacing="8",
                    align="center",
                    flex="none",
                ),
                width="100%",
                spacing="8",
                flex_direction=["column", "column", "row"],
                align_items=["center", "center", "start"],
                justify="center",
            ),
            width="100%",
            padding_bottom="10em",
            align_items="center",
            spacing="0",
        ),
        container_max_width="1400px",
    )