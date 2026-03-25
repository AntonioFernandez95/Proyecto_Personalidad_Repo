import reflex as rx
import re
import Personalidad.styles.utils as utils

from Personalidad.styles.fonts import Font
from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color
from Personalidad.components.navbar import navbar
from Personalidad.states.login_state import IndexState, ButtonClick
#from reflex_google_recaptcha_v2 import google_recaptcha_v2

"""

reflex run

"""

@rx.page(route="/prueba", title="PRUEBA")
def prueba():
    return rx.box(
        utils.lang(),
        navbar(),
        rx.vstack(
        rx.container(
            rx.box(
                rx.vstack(
                    rx.heading(
                        "Test de Personalidad",
                        font_size=Size.MEDIUM_BIG,
                        font_family=Font.DEFAULT,
                        text_align="center"
                    ),
                    rx.text(
                        ButtonClick.description,
                        text_align="center",
                        margin_top=Size.SMALL
                    ),
                    rx.form.root(
                        rx.form.field(
                            rx.flex(
                                rx.form.control(
                                    rx.input(
                                        placeholder="Correo electrónico",
                                        is_password=False,
                                        #value=IndexState.email,
                                        on_change=IndexState.update_email,
                                        display="block",
                                        type="email",
                                        radius="none",
                                        size="3",
                                    ),
                                    as_child=True,
                                ),
                                rx.form.message(
                                    "Introduzca un email válido",
                                    match="typeMismatch",
                                ),
                                align="center",
                                spacing="2",
                                max_width="60em",
                                margin_bottom=Size.SMALL,
                            ),
                            name="email",
                        ),
                        rx.form.field(
                            rx.flex(
                                rx.form.control(
                                    rx.input(
                                        placeholder="Contraseña",
                                        is_password=True,
                                        #value=IndexState.password,
                                        on_change=IndexState.update_password,
                                        display=ButtonClick.display,
                                        type="password",
                                        radius="none",
                                        size="3",
                                    ),
                                    as_child=True,
                                ),
                                rx.form.message(
                                    "Introduzca la contraseña",
                                    match="typeMismatch",
                                ),
                                rx.form.submit(
                                    rx.button(
                                        "Acceder",
                                        size="3",
                                        #on_click=ButtonClick.click_event
                                    ),
                                    as_child=True,
                                ),
                                direction="column",
                                spacing="2",
                                align="stretch",
                            ),
                            name="password",
                        ),
                        on_submit=ButtonClick.click_event,
                        reset_on_submit=False,
                    ),
                    align="center",
                    spacing="2",
                    max_width="60em",
                ), 
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
        background="linear-gradient(rgba(0,0,0,0.8), rgba(27,154,175,0.8)), url('/tropa.jpg')",
        background_size="cover",
        position="relative",
        background_position="center", 
    )


class RadixFormState(rx.State):
    # These track the user input real time for validation
    user_entered_username: str
    user_entered_email: str

    # These are the submitted data
    username: str
    email: str

    mock_username_db: list[str] = ["reflex", "admin"]

    @rx.var
    def invalid_email(self) -> bool:
        return not re.match(
            r"[^@]+@[^@]+.[^@]+", self.user_entered_email
        )

    @rx.var
    def username_empty(self) -> bool:
        return not self.user_entered_username.strip()

    @rx.var
    def username_is_taken(self) -> bool:
        return (
            self.user_entered_username
            in self.mock_username_db
        )

    @rx.var
    def input_invalid(self) -> bool:
        return (
            self.invalid_email
            or self.username_is_taken
            or self.username_empty
        )

    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.username = form_data.get("username")
        self.email = form_data.get("email")


def radix_form_example():
    return rx.flex(
        rx.form.root(
            rx.flex(
                rx.form.field(
                    rx.flex(
                        rx.form.label("Username"),
                        rx.form.control(
                            rx.input(
                                placeholder="Username",
                                # workaround: `name` seems to be required when on_change is set
                                on_change=RadixFormState.set_user_entered_username,
                                name="username",
                            ),
                            as_child=True,
                        ),
                        # server side validation message can be displayed inside a rx.cond
                        rx.cond(
                            RadixFormState.username_empty,
                            rx.form.message(
                                "Username cannot be empty",
                                color="var(--red-11)",
                            ),
                        ),
                        # server side validation message can be displayed by `force_match` prop
                        rx.form.message(
                            "Username already taken",
                            # this is a workaround:
                            # `force_match` does not work without `match`
                            # This case does not want client side validation
                            # and intentionally not set `required` on the input
                            # so "valueMissing" is always false
                            match="valueMissing",
                            force_match=RadixFormState.username_is_taken,
                            color="var(--red-11)",
                        ),
                        direction="column",
                        spacing="2",
                        align="stretch",
                    ),
                    name="username",
                    server_invalid=RadixFormState.username_is_taken,
                ),
                rx.form.field(
                    rx.flex(
                        rx.form.label("Email"),
                        rx.form.control(
                            rx.input(
                                placeholder="Email Address",
                                on_change=RadixFormState.set_user_entered_email,
                                name="email",
                            ),
                            as_child=True,
                        ),
                        rx.form.message(
                            "A valid Email is required",
                            match="valueMissing",
                            force_match=RadixFormState.invalid_email,
                            color="var(--red-11)",
                        ),
                        direction="column",
                        spacing="2",
                        align="stretch",
                    ),
                    name="email",
                    server_invalid=RadixFormState.invalid_email,
                ),
                rx.form.submit(
                    rx.button(
                        "Submit",
                        disabled=RadixFormState.input_invalid,
                    ),
                    as_child=True,
                ),
                direction="column",
                spacing="4",
                width="25em",
            ),
            on_submit=RadixFormState.handle_submit,
            reset_on_submit=True,
        ),
        rx.divider(size="4"),
        rx.text(
            "Username submitted: ",
            rx.text(
                RadixFormState.username,
                weight="bold",
                color="var(--accent-11)",
            ),
        ),
        rx.text(
            "Email submitted: ",
            rx.text(
                RadixFormState.email,
                weight="bold",
                color="var(--accent-11)",
            ),
        ),
        direction="column",
        spacing="4",
    )