import reflex as rx
import Personalidad.styles.utils as utils

from Personalidad.styles.fonts import Font
from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color
from Personalidad.components.navbar import navbar
from Personalidad.states.index_state import RadixFormSubmissionState


@rx.page(route="/", title="Login")
def index():
    return rx.box(
        utils.lang(),
        navbar(),
        rx.vstack(
        rx.container(
            rx.form.root(
                rx.vstack(
                    rx.heading(
                        "Test de Personalidad",
                        font_size=Size.MEDIUM_BIG,
                        font_family=Font.DEFAULT,
                        text_align="center"
                    ),
                    rx.input(
                        name="email",
                        type="text",
                        placeholder="Correo electrónico",
                        required=True,
                        radius="none",
                        size="3",
                    ),
                    rx.input(
                        name="password",
                        type="password",
                        placeholder="Contraseña",
                        required=True,
                        radius="none",
                        size="3",
                    ),
                    rx.form.submit(
                        rx.button(
                            "Acceso",
                            type="submit",
                            size="3",
                        ),
                        as_child=True,
                    ),
                    rx.text(
                        "¿Tu contraseña ha caducado? Haz click aquí para recibir otra.",
                        text_align="center"
                        ),
                    align="center",
                    spacing="2",
                    max_width="60em",
                ),
                on_submit=RadixFormSubmissionState.handle_submit, 
            ),
            width= "90%",
            max_width= "450px",
            position= "absolute",
            top= "50%",
            left= "50%",
            transform= "translate(-50%,-50%)",
            background= rx.color_mode_cond(light="white", dark=Color.TEXT),
            padding= "40px 60px 40px",
            align= "center",
            box_shadow="0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)"
        ),
        align="center",
        width="100%",
        height="100vh",
        ),
        height="100vh",
        width="100%",
        background="linear-gradient(rgba(0,0,0,0.8), rgba(27,154,175,0.8)), url('/personalidad2.jpg')",
        background_size="cover",
        position="relative",
        background_position="center", 
    )
