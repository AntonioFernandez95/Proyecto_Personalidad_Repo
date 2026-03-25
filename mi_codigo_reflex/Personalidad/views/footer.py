import reflex as rx
import datetime

from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color

def footer()-> rx.Component: 
    return rx.vstack(
        rx.hstack(
            rx.link(
                f"© 2015-{datetime.date.today().year} Métodos Centro de Formación Integral S.L.U.", 
                href= "https://academiametodos.com/",
                is_external=True,
                size="2",
                color=Color.PRIMARY,
                padding_bottom="15px",
                text_align="center"
            )
        ),
        align="center",
        margin=Size.DEFAULT
    )