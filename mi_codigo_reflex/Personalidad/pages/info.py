import reflex as rx
import Personalidad.styles.utils as utils

from Personalidad.styles.fonts import Font
from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color
from Personalidad.styles.styles import MAX_WIDTH
from Personalidad.components.navbar import navbar
from Personalidad.views.header import header
from Personalidad.components.button import custoom_button
from Personalidad.views.footer import footer
from Personalidad.states.base_state import State
#from reflex_google_recaptcha_v2 import google_recaptcha_v2

"""

reflex run

"""

@rx.page(route="/info", title="Info", on_load=State.check_login) #
def info() -> rx.Component:
    return rx.box(
        utils.langg(),
        navbar(),
        rx.center(
            rx.vstack(
                header(),
                custoom_button("Comenzar test", "/test"), 
                flex="1",
                max_width=MAX_WIDTH,
                width="100%", 
                margin_y= Size.BIG,
                align="center"
            ),
            padding_top=Size.EXTRA_BIG
        ),
        footer(),
        background= rx.color_mode_cond(light="white", dark=Color.TEXT),
    )