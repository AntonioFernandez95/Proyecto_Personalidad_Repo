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
from Personalidad.states.test_state import TestState
#from reflex_google_recaptcha_v2 import google_recaptcha_v2




"""




reflex run




"""




@rx.page(route="/info", title="Info", on_load=[State.check_personalidad_access, TestState.reset_test]) #
def info() -> rx.Component:
    return rx.box(
        utils.langg(),
        navbar(),
        rx.center(
            rx.vstack(
                header(),
                rx.hstack(
                    rx.button("Comenzar test", on_click=rx.redirect("/test"), background_color="#6B704C", color="white", size="3", _hover={"opacity": 0.8}),
                    rx.button("Salir", on_click=rx.redirect("/"), background_color="#808558", color="white", size="3", _hover={"opacity": 0.8}),
                    spacing="4",
                    width="100%",
                    justify="center"
                ),
                flex="1",
                max_width=MAX_WIDTH,
                width=["95%", "85%", "60%", "50%"],
                margin_y= Size.BIG,
                align="center"
            ),
            padding_top=Size.EXTRA_BIG
        ),
        footer(),
        background= rx.color_mode_cond(light="white", dark=Color.TEXT),
        min_height="100vh",
    )
