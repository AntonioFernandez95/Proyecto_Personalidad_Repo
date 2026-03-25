import reflex as rx

from Personalidad.styles.fonts import Font
from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color

def info_box(text: str) -> rx.Component:
    return rx.box(
        text,
        background_color=rx.color_mode_cond(light=Color.CREAM.value, dark=Color.MID_GRAY.value),
        border_radius="3px",
        padding="8px",
        width="100%",
        text_align="center"
    )