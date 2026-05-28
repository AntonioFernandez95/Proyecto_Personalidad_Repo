import reflex as rx
import Personalidad.styles.utils as utils


from Personalidad.styles.fonts import Font
from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color
from Personalidad.components.navbar import navbar
from Personalidad.states.login_state import LoginState, ButtonClick




@rx.page(route="/", title="Login", on_load=ButtonClick.check_authenticated)
def index():
    return rx.box(
        utils.langg(),
        navbar(),
        rx.vstack(
            rx.container(
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "CURSO SEGUNDA FASE",
                            font_size=Size.MEDIUM_BIG,
                            font_family=Font.DEFAULT,
                            text_align="center"
                        ),
                        rx.heading(
                            "Tropa y Marinería",
                            font_size=Size.DEFAULT,
                            font_family=Font.DEFAULT,
                            text_align="center"
                        ),
                        rx.text(
                            "Introduce tus credenciales para acceder",
                            text_align="center",
                            margin_top=Size.SMALL
                        ),
                        # --- CAMPO EMAIL ---
                        rx.input(
                            placeholder="Correo electrónico",
                            value=ButtonClick.email,
                            on_change=ButtonClick.update_email,
                            type="email",
                            radius="none",
                            size="3",
                            width="100%",
                        ),
                        # --- CAMPO CONTRASEÑA ---
                        rx.input(
                            placeholder="Contraseña",
                            type="password",
                            value=ButtonClick.password,
                            on_change=ButtonClick.update_password,
                            radius="none",
                            size="3",
                            width="100%",
                        ),
                        # Alerta Email Inválido
                        rx.callout.root(
                            rx.callout.text("Introduce un correo válido"),
                            display=ButtonClick.show_email_alert,
                            size="1",
                            width="100%",
                        ),
                        # Alerta Contraseña Incorrecta
                        rx.cond(
                            ButtonClick.showPasswordAlert == "block",
                            rx.callout.root(
                                rx.callout.icon(rx.icon(tag="shield_alert", size=18)),
                                rx.callout.text(
                                    "Contraseña incorrecta",
                                    font_size="0.8em",
                                ),
                                color_scheme="red",
                                width="100%",
                            ),
                        ),
                        # Alerta Usuario No Encontrado
                        rx.cond(
                            ButtonClick.showEmailNotFoundAlert,
                            rx.callout.root(
                                rx.callout.icon(rx.icon(tag="triangle_alert", size=18)),
                                rx.callout.text(
                                    "No existe una cuenta asociada a este correo",
                                    font_size="0.8em",
                                    font_style="italic",
                                ),
                                color_scheme="red",
                                role="alert",
                                width="100%",
                            ),
                        ),


                        # --- OPCIÓN RECUPERACIÓN DE CONTRASEÑA ---
                        rx.box(
                            rx.link(
                                "¿Has olvidado tu contraseña?",
                                on_click=ButtonClick.recover_password,
                                font_size="0.8em",
                                color_scheme="gray",
                                cursor="pointer",
                                text_decoration="underline",
                            ),
                            width="100%",
                            text_align="right",
                        ),


                        # Botón Acceder
                        rx.button(
                            "Acceder",
                            size="3",
                            loading=ButtonClick.isWaiting,
                            on_click=ButtonClick.click_event,
                            disabled=ButtonClick.checkStatusButton,
                            background_color=Color.ACCENT,
                            width="100%",
                        ),
                        # Botón Comprar / Renovar Plazo
                        rx.link(
                            rx.button(
                                "Renueva tu suscripción aquí",
                                size="3",
                                background_color=Color.ACCENT,
                                width="100%",
                                cursor="pointer",
                            ),
                            href="https://academiametodos.com/tienda/#tropa_y_marineria",
                            is_external=True,
                            width="100%",
                            text_decoration="none",
                        ),
                        align="center",
                        spacing="3",
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
        background="url('/fondo-soldado(1).png')",
        background_size="cover",
        position="relative",
        background_position="center",
    )
