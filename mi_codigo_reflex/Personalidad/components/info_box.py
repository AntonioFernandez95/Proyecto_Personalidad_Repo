import reflex as rx


from Personalidad.styles.fonts import Font
from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color


def info_box(text: str) -> rx.Component:
    return rx.box(
        text,
        color=Color.GREEN.value,
        background_color=rx.color_mode_cond(light="#FDF2E9", dark=Color.MID_GRAY.value),
        border_radius="3px",
        padding="8px",
        text_align="center"
    )
