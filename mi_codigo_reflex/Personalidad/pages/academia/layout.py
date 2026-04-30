import reflex as rx

# ─────────────────────────────────────────────
# COLORES Y CONSTANTES (Importados de academia_styles)
# ─────────────────────────────────────────────
from Personalidad.styles.academia_styles import (
    OLIVE, OLIVE_DARK, OLIVE_LIGHT, CARD_BG, NAV_BG, 
    TEXT_DARK, TEXT_MID, GRAY_LIGHT, BADGE_GREEN, BADGE_RED, BADGE_GRAY,
    CARD_STYLE, BTN_PRIMARY_BASE, BTN_SECONDARY_BASE, BTN_BACK_BASE
)

PAGE_BG = (
    "linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)), "
    "url('/fondo-soldados (1).png')"
)


# COMPONENTES COMPARTIDOS
# ─────────────────────────────────────────────
from Personalidad.components.navbar import navbar


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
            min_height="calc(100vh - 5em)",
        ),
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
            rx.button(btn_label, **BTN_PRIMARY_BASE, padding="0.6em 1.4em"),
            href=href, margin_top="0.8em",
        ),
        align="center", spacing="3",
        **CARD_STYLE, padding="2em",
        width="280px", min_height="280px", justify="center",
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
        rx.text(nombre, font_size="1em", font_weight="600", color="black", flex="1"),
        rx.link(
            rx.button("Ver técnica →", **BTN_SECONDARY_BASE, padding="0.6em 1.4em", font_size="0.85em"),
            href=href,
        ),
        width="100%", align="center", padding="1em",
        background="white", border_radius="12px",
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
            rx.text(title,    font_size="1em",    font_weight="700", color="black"),
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