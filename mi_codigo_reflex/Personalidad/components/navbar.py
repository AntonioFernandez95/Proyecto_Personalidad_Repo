import reflex as rx

from Personalidad.styles.fonts import Font
from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color

def navbar() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.image(
                src="/metodos_naranja_thick.svg", 
                width=Size.BIG
                ),
            rx.heading(
                "Métodos",
                font_size=Size.BIG, 
                font_family=Font.LOGO,
                color=rx.color_mode_cond(light=Color.TEXT, dark="white")
                ),
        ),
        rx.spacer(),
        rx.color_mode.icon(),
        rx.color_mode.switch(),
        position="fixed",
        top="0px",
        background_color=rx.color_mode_cond(light="white", dark=Color.TEXT),
        padding=Size.DEFAULT,
        height=Size.EXTRA_BIG,
        width="100%",
        z_index="5",
    )