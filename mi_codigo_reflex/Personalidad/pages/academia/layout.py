import reflex as rx








# ─────────────────────────────────────────────
# COLORES Y CONSTANTES (Importados de academia_styles)
# ─────────────────────────────────────────────
from Personalidad.styles.academia_styles import (
    OLIVE, OLIVE_DARK, OLIVE_LIGHT, CARD_BG, NAV_BG,
    TEXT_DARK, TEXT_MID, GRAY_LIGHT, BADGE_GREEN, BADGE_RED, BADGE_GRAY,
    CARD_STYLE, BTN_PRIMARY_BASE, BTN_SECONDARY_BASE, BTN_BACK_BASE
)








PAGE_BG = rx.color_mode_cond(
    light="url('/fondo-soldados (1).png')",
    dark="linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('/fondo-soldados (1).png')"
)
















# COMPONENTES COMPARTIDOS
# ─────────────────────────────────────────────
from Personalidad.components.navbar import navbar
















def confirm_delete_dialog() -> rx.Component:
    from Personalidad.states.admin_state import AdminState
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.center(
                    rx.icon("triangle-alert", size=45, color="red"),
                    width="80px",
                    height="80px",
                    background="rgba(255, 0, 0, 0.1)",
                    border_radius="full",
                    margin_bottom="1em",
                ),
                rx.dialog.title(
                    "¿Eliminar recurso?",
                    font_weight="900",
                    size="6",
                    color="red",
                    text_align="center",
                ),
                rx.dialog.description(
                    rx.cond(
                        AdminState.recurso_a_borrar,
                        f"¿Estás seguro de que deseas eliminar el recurso '{AdminState.recurso_a_borrar['nombre']}'? Esta acción es permanente y borrará el archivo físico del servidor.",
                        "¿Estás seguro de que deseas eliminar este recurso?"
                    ),
                    text_align="center",
                    color="rgba(0,0,0,0.6)",
                    margin_bottom="1.5em",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            background_color="#5B733A",
                            color="white",
                            border_radius="15px",
                            on_click=AdminState.cancelar_borrar_recurso,
                            cursor="pointer",
                            _hover={"opacity": 0.8},
                        ),
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Eliminar",
                            background_color="red",
                            color="white",
                            border_radius="15px",
                            on_click=AdminState.confirmar_borrar_recurso,
                            cursor="pointer",
                        ),
                    ),
                    justify="between",
                    width="100%",
                    margin_top="1em",
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
        open=AdminState.show_confirm_delete,
    )








def academia_layout(*children, **props) -> rx.Component:
    """Standard layout for all Academia pages."""
    # Establecer valores por defecto si no se pasan en props para evitar conflictos
    props.setdefault("align", "center")
    props.setdefault("spacing", "4")
   
    # NUEVO: Extraer max_width de props o usar el valor por defecto (1100px)
    # Esto permite que páginas específicas sean más anchas o estrechas
    container_max_width = props.pop("container_max_width", "1100px")








    return rx.box(
        navbar(),
        rx.center(
            rx.container(
                rx.vstack(
                    *children,
                    **props,
                ),
                max_width=container_max_width,
                width="100%",
                padding_x="1.5em",
                padding_y="2em",
            ),
            width="100%",
            padding_top="6em",
            min_height="calc(100vh - 5em)",
        ),
        confirm_delete_dialog(),
        background=PAGE_BG,
        background_size="cover",
        background_position="center",
        background_attachment="fixed",
        min_height="100vh",
        font_family="'Roboto', sans-serif",
    )
















# ─────────────────────────────────────────────
# HELPERS DE COMPONENTES
# ─────────────────────────────────────────────
def big_card(icon_name: str, title: str, subtitle: str,
             btn_label: str, href: str) -> rx.Component:
    return rx.vstack(
        rx.center(
            rx.icon(icon_name, size=52, color=OLIVE),
            background=GRAY_LIGHT, border_radius="50%",
            width="90px", height="90px",
        ),
        rx.text(title,    font_size="1.25em", font_weight="800", color=TEXT_DARK, text_align="center"),
        rx.text(subtitle, font_size="0.9em",  color=TEXT_MID,   text_align="center"),
        rx.link(
            rx.button(btn_label, **BTN_PRIMARY_BASE, width="100%", padding="0.8em 2em"),
            href=href, margin_top="1.5em",
            width="80%", # Para que no pegue a los bordes de la tarjeta
        ),
        align="center", spacing="3",
        **CARD_STYLE, padding="2em",
        width="340px", height="380px", justify="center",
        _hover={"box_shadow": "0 12px 40px rgba(0,0,0,0.25)", "transform": "translateY(-4px)"},
        transition="all 0.25s ease",
    )
















def small_card(icon_name: str, title: str, desc: str,
               btn_label: str, href: str) -> rx.Component:
    return rx.vstack(
        rx.center(
            rx.icon(icon_name, size=36, color=OLIVE),
            background=GRAY_LIGHT, border_radius="12px",
            width="64px", height="64px",
        ),
        rx.text(title, font_size="1em",   font_weight="700", color=TEXT_DARK),
        rx.text(desc,  font_size="0.82em", color=TEXT_MID,   text_align="center"),
        rx.link(
            rx.button(btn_label, **BTN_PRIMARY_BASE, padding="0.6em 1.4em", font_size="0.85em"),
            href=href,
        ),
        align="center", spacing="2",
        **CARD_STYLE, padding="1.5em",
        _hover={"transform": "translateY(-3px)", "box_shadow": "0 12px 30px rgba(0,0,0,0.2)"},
        transition="all 0.2s ease",
    )
















def back_button(label: str = "← Volver", href: str = "/academia/fisicas") -> rx.Component:
    return rx.link(
        rx.button(label, **BTN_BACK_BASE, padding="0.5em 1.2em"),
        href=href,
        margin_top="2em",
    )
















def prueba_row(icon_name: str, nombre: str, href: str) -> rx.Component:
    return rx.hstack(
        rx.center(
            rx.icon(icon_name, size=28, color=OLIVE),
            background=GRAY_LIGHT, border_radius="10px",
            width="52px", height="52px",
        ),
        rx.text(nombre, font_size="1em", font_weight="600", color=TEXT_DARK, flex="1"),
        rx.link(
            rx.button("Ver técnica →", **BTN_SECONDARY_BASE, padding="0.6em 1.4em", font_size="0.85em"),
            href=href,
        ),
        width="100%", align="center", padding="1em",
        background=CARD_BG, border_radius="12px",
        box_shadow="0 2px 8px rgba(0,0,0,0.08)",
        _hover={"box_shadow": "0 4px 16px rgba(0,0,0,0.14)"},
        transition="all 0.2s",
    )
















def norma_item(texto: str) -> rx.Component:
    return rx.hstack(
        rx.center(
            rx.text("✗", color="white", font_weight="900", font_size="0.82em"),
            background="#e53e3e", border_radius="50%",
            width="22px", height="22px", flex_shrink="0",
        ),
        rx.text(texto, font_size="0.9em", color=TEXT_MID),
        spacing="2", align="center",
    )
















def plan_row(title: str, subtitle: str, href: str = "") -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.text(title,    font_size="1em",    font_weight="700", color=TEXT_DARK),
            rx.text(subtitle, font_size="0.82em", color=TEXT_MID),
            spacing="0", align="start",
        ),
        rx.spacer(),
        rx.link(
            rx.button(
                rx.hstack(rx.icon("download", size=14), rx.text("PDF"), spacing="1"),
                **BTN_PRIMARY_BASE, padding="0.4em 1em", font_size="0.82em",
            ),
            href=href,
            is_external=True,
        ),
        width="100%", align="center", padding="1em",
        background=GRAY_LIGHT, border_radius="10px",
    )
