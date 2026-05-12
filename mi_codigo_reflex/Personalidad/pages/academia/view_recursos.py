import reflex as rx
from Personalidad.states.admin_state import AdminState
from Personalidad.pages.academia.layout import academia_layout
from Personalidad.styles.academia_styles import TEXT_DARK, TEXT_MID


def resource_list_item(recurso: dict) -> rx.Component:
    """Item individual de la lista de recursos adaptable al modo oscuro con botón de ver y borrar."""
    return rx.hstack(
        rx.center(
            rx.cond(
                recurso["tipo"] == "pdf",
                rx.icon("file-text", size=20, color="#5B733A"),
                rx.icon("video", size=20, color="#5B733A"),
            ),
            width="40px",
            height="40px",
            border_radius="10px",
            background=rx.color_mode_cond("rgba(91, 115, 58, 0.1)", "rgba(91, 115, 58, 0.2)"),
        ),
        rx.vstack(
            rx.text(
                recurso["nombre"],
                font_weight="bold",
                font_size="0.95em",
                color=rx.color_mode_cond(TEXT_DARK, "white")
            ),
            rx.text(
                recurso["tipo"].to(str).upper(),
                font_size="0.7em",
                color=rx.color_mode_cond(TEXT_MID, "rgba(255,255,255,0.6)"),
                font_weight="900",
                letter_spacing="1px"
            ),
            spacing="0", align="start"
        ),
        rx.spacer(),
        rx.hstack(
            # BOTÓN VER
            rx.link(
                rx.button(
                    rx.icon("eye", size=16),
                    variant="ghost",
                    color_scheme="gray",
                    size="1",
                    padding="0.6em",
                    border_radius="8px",
                    _hover={"background_color": "rgba(91, 115, 58, 0.1)", "transform": "scale(1.1)"},
                ),
                href=recurso["url"].to(str),
                is_external=True,
            ),
            # BOTÓN BORRAR
            rx.button(
                rx.icon("trash-2", size=16),
                on_click=lambda: AdminState.borrar_recurso(recurso),
                variant="ghost",
                color_scheme="red",
                size="1",
                padding="0.6em",
                border_radius="8px",
                _hover={"background_color": "rgba(255, 0, 0, 0.1)", "transform": "scale(1.1)"},
                transition="all 0.2s"
            ),
            spacing="2"
        ),
        width="100%",
        padding="1em",
        border_radius="15px",
        background=rx.color_mode_cond("rgba(255, 255, 255, 0.6)", "rgba(255, 255, 255, 0.05)"),
        border=rx.color_mode_cond("1px solid rgba(255, 255, 255, 0.8)", "1px solid rgba(255, 255, 255, 0.1)"),
        box_shadow="0 2px 8px rgba(0,0,0,0.02)",
        _hover={
            "border": "1px solid #5B733A",
            "transform": "translateX(5px)",
            "background_color": rx.color_mode_cond("white", "rgba(255, 255, 255, 0.1)")
        },
        transition="all 0.3s"
    )


def category_card(title: str, icon_name: str, resources: list) -> rx.Component:
    """Tarjeta de categoría adaptable al modo oscuro con Glassmorphism."""
    return rx.vstack(
        rx.hstack(
            rx.center(
                rx.icon(icon_name, size=22, color="white"),
                width="45px",
                height="45px",
                border_radius="12px",
                background="#5B733A",
                box_shadow="0 4px 10px rgba(91, 115, 58, 0.3)",
            ),
            rx.heading(
                title.capitalize(),
                size="5",
                color=rx.color_mode_cond(TEXT_DARK, "white"),
                font_weight="bold"
            ),
            spacing="3",
            align="center",
            margin_bottom="1.5em",
        ),
        rx.vstack(
            rx.foreach(resources, resource_list_item),
            width="100%",
            spacing="3",
        ),
        rx.cond(
            resources.length() == 0,
            rx.center(
                rx.vstack(
                    rx.icon("inbox", size=30, color=rx.color_mode_cond("#ccc", "rgba(255,255,255,0.2)")),
                    rx.text("Sin recursos aún", color=rx.color_mode_cond("#999", "rgba(255,255,255,0.4)"), font_size="0.85em"),
                    spacing="2",
                ),
                width="100%",
                padding="2em",
            )
        ),
        padding="2em",
        background=rx.color_mode_cond("rgba(255, 255, 255, 0.7)", "rgba(15, 15, 15, 0.8)"),
        backdrop_filter="blur(15px)",
        border_radius="30px",
        border=rx.color_mode_cond("1px solid rgba(255, 255, 255, 0.5)", "1px solid rgba(255, 255, 255, 0.1)"),
        box_shadow=rx.color_mode_cond("0 20px 40px rgba(0,0,0,0.05)", "0 20px 40px rgba(0,0,0,0.4)"),
        width="100%",
        min_width="380px",
        min_height="400px",
        _hover={
            "transform": "translateY(-10px)",
            "box_shadow": rx.color_mode_cond("0 30px 60px rgba(0,0,0,0.1)", "0 30px 60px rgba(0,0,0,0.6)")
        },
        transition="all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)"
    )


def carousel_indicator(index: int, current_index: int) -> rx.Component:
    """Punto indicador de posición del carrusel."""
    return rx.box(
        width=rx.cond(current_index == index, "25px", "8px"),
        height="8px",
        border_radius="full",
        background=rx.cond(
            current_index == index,
            "#5B733A",
            rx.color_mode_cond("#ccc", "rgba(255,255,255,0.2)")
        ),
        transition="all 0.3s ease",
    )


def resource_carousel(categories_data: list, current_index: rx.Var, next_action, prev_action) -> rx.Component:
    """Genera un carrusel de categorías con flechas de navegación."""
    return rx.vstack(
        rx.box(
            # Visor del Carrusel
            rx.box(
                rx.hstack(
                    *[category_card(title, icon, resources) for title, icon, resources in categories_data],
                    width="250%",
                    transform=f"translateX(-{current_index * 20}%)",
                    transition="transform 0.8s cubic-bezier(0.65, 0, 0.35, 1)",
                    spacing="6",
                    padding_x="10px",
                    align_items="start",
                ),
                overflow="hidden",
                width="100%",
                padding_y="2em",
            ),
            
            # Flecha Izquierda
            rx.center(
                rx.icon("chevron-left", size=32),
                on_click=prev_action,
                position="absolute",
                left="-30px",
                top="0",
                bottom="0",
                margin_y="auto",
                z_index="40",
                width="50px",
                height="50px",
                border_radius="50%",
                background_color="white",
                color="#5B733A",
                cursor="pointer",
                box_shadow="0 10px 25px rgba(0,0,0,0.2)",
                display=rx.cond(current_index > 0, "flex", "none"),
                _hover={"transform": "scale(1.1)", "background_color": "#f0f4f0"},
                transition="all 0.2s",
            ),
            
            # Flecha Derecha
            rx.center(
                rx.icon("chevron-right", size=32),
                on_click=next_action,
                position="absolute",
                right="-30px",
                top="0",
                bottom="0",
                margin_y="auto",
                z_index="40",
                width="50px",
                height="50px",
                border_radius="50%",
                background_color="white",
                color="#5B733A",
                cursor="pointer",
                box_shadow="0 10px 25px rgba(0,0,0,0.2)",
                display=rx.cond(current_index < 4, "flex", "none"),
                _hover={"transform": "scale(1.1)", "background_color": "#f0f4f0"},
                transition="all 0.2s",
            ),
            
            position="relative",
            width="100%",
        ),
        # Indicadores de Puntos
        rx.hstack(
            rx.foreach(rx.Var.create([0, 1, 2, 3, 4]), lambda i: carousel_indicator(i, current_index)),
            rx.text(
                recurso["tipo"].to(str).upper(),
                font_size="0.7em",
                color=rx.color_mode_cond(TEXT_MID, "rgba(255,255,255,0.6)"),
                font_weight="900",
                letter_spacing="1px"
            ),
            spacing="0", align="start"
        ),
        rx.spacer(),
        rx.hstack(
            # BOTÓN VER
            rx.link(
                rx.button(
                    rx.icon("eye", size=16),
                    variant="ghost",
                    color_scheme="gray",
                    size="1",
                    padding="0.6em",
                    border_radius="12px",
                    _hover={"background_color": "rgba(91, 115, 58, 0.1)", "transform": "scale(1.1)"},
                ),
                href=recurso["url"].to(str),
                is_external=True,
            ),
            # BOTÓN BORRAR
            rx.button(
                rx.icon("trash-2", size=16),
                on_click=lambda: AdminState.borrar_recurso(recurso),
                variant="ghost",
                color_scheme="red",
                size="1",
                padding="0.6em",
                border_radius="12px",
                _hover={"background_color": "rgba(255, 0, 0, 0.1)", "transform": "scale(1.1)"},
                transition="all 0.2s"
            ),
            spacing="2"
        ),
        width=["100%", "100%", "48%"],
        min_width="140px",
        padding="0.8em",
        border_radius="20px",
        background=rx.color_mode_cond("rgba(255, 255, 255, 0.6)", "rgba(255, 255, 255, 0.05)"),
        border=rx.color_mode_cond("1px solid rgba(255, 255, 255, 0.8)", "1px solid rgba(255, 255, 255, 0.1)"),
        box_shadow="0 2px 8px rgba(0,0,0,0.02)",
        _hover={
            "border": "1px solid #5B733A",
            "transform": "translateY(-3px)",
            "background_color": rx.color_mode_cond("white", "rgba(255, 255, 255, 0.1)")
        },
        transition="all 0.3s"
    )


def category_card(title: str, icon_name: str, resources: list) -> rx.Component:
    """Tarjeta de categoría adaptable al modo oscuro con Glassmorphism."""
    return rx.vstack(
        rx.hstack(
            rx.center(
                rx.icon(icon_name, size=22, color="white"),
                width="45px",
                height="45px",
                border_radius="12px",
                background="#5B733A",
                box_shadow="0 4px 10px rgba(91, 115, 58, 0.3)",
            ),
            rx.heading(
                title.capitalize(),
                size="5",
                color=rx.color_mode_cond(TEXT_DARK, "white"),
                font_weight="bold"
            ),
            spacing="3",
            align="center",
            margin_bottom="1.5em",
        ),
        # CAMBIO: Ahora los elementos se ponen al lado del otro
        rx.flex(
            rx.foreach(resources, resource_list_item),
            width="100%",
            spacing="3",
            flex_wrap="wrap",
            gap="3",
            justify="start",
        ),
        rx.cond(
            resources.length() == 0,
            rx.center(
                rx.vstack(
                    rx.icon("inbox", size=30, color=rx.color_mode_cond("#ccc", "rgba(255,255,255,0.2)")),
                    rx.text("Sin recursos aún", color=rx.color_mode_cond("#999", "rgba(255,255,255,0.4)"), font_size="0.85em"),
                    spacing="2",
                ),
                width="100%",
                padding="2em",
            )
        ),
        padding="2em",
        background=rx.color_mode_cond("rgba(255, 255, 255, 0.7)", "rgba(15, 15, 15, 0.8)"),
        backdrop_filter="blur(15px)",
        border_radius="35px",
        border=rx.color_mode_cond("1px solid rgba(255, 255, 255, 0.5)", "1px solid rgba(255, 255, 255, 0.1)"),
        box_shadow=rx.color_mode_cond("0 20px 40px rgba(0,0,0,0.05)", "0 20px 40px rgba(0,0,0,0.4)"),
        width="100%",
        min_width="380px",
        min_height="400px",
        _hover={
            "transform": "translateY(-10px)",
            "box_shadow": rx.color_mode_cond("0 30px 60px rgba(0,0,0,0.1)", "0 30px 60px rgba(0,0,0,0.6)")
        },
        transition="all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)"
    )


def carousel_indicator(index: int, current_index: int) -> rx.Component:
    """Punto indicador de posición del carrusel."""
    return rx.box(
        width=rx.cond(current_index == index, "25px", "8px"),
        height="8px",
        border_radius="full",
        background=rx.cond(
            current_index == index,
            "#5B733A",
            rx.color_mode_cond("#ccc", "rgba(255,255,255,0.2)")
        ),
        transition="all 0.3s ease",
    )


def resource_carousel(categories_data: list, current_index: rx.Var, next_action, prev_action) -> rx.Component:
    """Genera un carrusel de categorías con flechas de navegación."""
    return rx.vstack(
        rx.box(
            # Visor del Carrusel
            rx.box(
                rx.hstack(
                    *[category_card(title, icon, resources) for title, icon, resources in categories_data],
                    width="250%",
                    transform=f"translateX(-{current_index * 20}%)",
                    transition="transform 0.8s cubic-bezier(0.65, 0, 0.35, 1)",
                    spacing="6",
                    padding_x="10px",
                    align_items="start",
                ),
                overflow="hidden",
                width="100%",
                padding_y="1em",
            ),
            
            # Flecha Izquierda
            rx.center(
                rx.icon("chevron-left", size=32),
                on_click=prev_action,
                position="absolute",
                left="-30px",
                top="0",
                bottom="0",
                margin_y="auto",
                z_index="40",
                width="50px",
                height="50px",
                border_radius="50%",
                background_color="white",
                color="#5B733A",
                cursor="pointer",
                box_shadow="0 10px 25px rgba(0,0,0,0.2)",
                display=rx.cond(current_index > 0, "flex", "none"),
                _hover={"transform": "scale(1.1)", "background_color": "#f0f4f0"},
                transition="all 0.2s",
            ),
            
            # Flecha Derecha
            rx.center(
                rx.icon("chevron-right", size=32),
                on_click=next_action,
                position="absolute",
                right="-30px",
                top="0",
                bottom="0",
                margin_y="auto",
                z_index="40",
                width="50px",
                height="50px",
                border_radius="50%",
                background_color="white",
                color="#5B733A",
                cursor="pointer",
                box_shadow="0 10px 25px rgba(0,0,0,0.2)",
                display=rx.cond(current_index < 4, "flex", "none"),
                _hover={"transform": "scale(1.1)", "background_color": "#f0f4f0"},
                transition="all 0.2s",
            ),
            
            position="relative",
            width="100%",
        ),
        # Indicadores de Puntos
        rx.hstack(
            rx.foreach(rx.Var.create([0, 1, 2, 3, 4]), lambda i: carousel_indicator(i, current_index)),
            spacing="2",
            margin_top="0.5em",
        ),
        width="100%",
        align="center",
    )


@rx.page(route="/academia/view_recursos", title="Biblioteca de Recursos", on_load=AdminState.on_load)
def view_recursos() -> rx.Component:
    # Datos para los carruseles
    pdf_categories = [
        ("Flexiones", "armchair", AdminState.recursos_flexiones_pdf),
        ("Plancha", "shield", AdminState.recursos_plancha_pdf),
        ("Agilidad", "zap", AdminState.recursos_agilidad_pdf),
        ("Carrera", "timer", AdminState.recursos_carrera_pdf),
        ("Planificación", "calendar", AdminState.recursos_planificacion_pdf),
    ]
    
    video_categories = [
        ("Flexiones", "armchair", AdminState.recursos_flexiones_video),
        ("Plancha", "shield", AdminState.recursos_plancha_video),
        ("Agilidad", "zap", AdminState.recursos_agilidad_video),
        ("Carrera", "timer", AdminState.recursos_carrera_video),
        ("Planificación", "calendar", AdminState.recursos_planificacion_video),
    ]

    return academia_layout(
        rx.vstack(
            # Header
            rx.flex(
                rx.link(
                    rx.button(
                        rx.icon("chevron-left", size=18),
                        "Volver",
                        background_color="white",
                        color="#5B733A",
                        border_radius="20px",
                        box_shadow="0 4px 10px rgba(0,0,0,0.1)",
                        _hover={"transform": "scale(1.05)"},
                    ),
                    href="/academia/admin_panel",
                    underline="none",
                ),
                rx.vstack(
                    rx.heading(
                        "Biblioteca de Recursos",
                        size="8",
                        color="white",
                        font_weight="900",
                        text_shadow="0 4px 15px rgba(0,0,0,0.5)",
                        letter_spacing="-1px"
                    ),
                    rx.text(
                        "Gestiona el contenido de la academia",
                        color="white",
                        font_weight="bold",
                        text_shadow="0 2px 4px rgba(0,0,0,0.5)",
                        font_size="0.9em",
                    ),
                    align="end",
                    spacing="0",
                ),
                width="100%",
                justify="between",
                align="center",
                padding_top="3em",
                padding_bottom="2em",
            ),
           
            # ACORDEÓN DE RECURSOS
            rx.accordion.root(
                # SECCIÓN 1: PDFs
                rx.accordion.item(
                    header=rx.hstack(
                        rx.icon("file-text", color="#5B733A", size=22),
                        rx.text("BIBLIOTECA DE PDFs", font_weight="bold", font_size="1.1em", color="#5B733A"),
                        spacing="3",
                        width="100%",
                    ),
                    content=rx.box(
                        resource_carousel(
                            pdf_categories, 
                            AdminState.carousel_index_pdf,
                            AdminState.next_slide_pdf,
                            AdminState.prev_slide_pdf
                        ),
                        width="100%",
                    ),
                    value="pdfs",
                    background="rgba(255, 255, 255, 0.98)",
                    backdrop_filter="blur(10px)",
                    border_radius="35px",
                    border="1px solid rgba(255,255,255,0.8)",
                    box_shadow="0 15px 35px rgba(0,0,0,0.2)",
                    margin_bottom="1.5em",
                    padding="0.5em",
                ),

                # SECCIÓN 2: VÍDEOS
                rx.accordion.item(
                    header=rx.hstack(
                        rx.icon("video", color="#5B733A", size=22),
                        rx.text("BIBLIOTECA DE VÍDEOS", font_weight="bold", font_size="1.1em", color="#5B733A"),
                        spacing="3",
                        width="100%",
                    ),
                    content=rx.box(
                        resource_carousel(
                            video_categories, 
                            AdminState.carousel_index_video,
                            AdminState.next_slide_video,
                            AdminState.prev_slide_video
                        ),
                        width="100%",
                    ),
                    value="videos",
                    background="rgba(255, 255, 255, 0.98)",
                    backdrop_filter="blur(10px)",
                    border_radius="35px",
                    border="1px solid rgba(255,255,255,0.8)",
                    box_shadow="0 15px 35px rgba(0,0,0,0.2)",
                    padding="0.5em",
                ),
                width="100%",
                variant="ghost",
                collapsible=True,
                default_value=["pdfs"],
            ),
           
            width="100%",
            padding_bottom="4em",
            position="relative",
        ),
        container_max_width="1100px",
    )
