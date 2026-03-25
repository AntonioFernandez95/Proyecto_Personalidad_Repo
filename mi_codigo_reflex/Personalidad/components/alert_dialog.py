import reflex as rx

from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color

def alert_dialog(dialog_text: str, dialog_description: str, cancel_text: str, action_text: str, click: rx.State) -> rx.Component:
    return rx.alert_dialog.root(
                    rx.alert_dialog.trigger(
                        rx.button(
                            dialog_text,
                            border_radius="25px",
                            padding=Size.MEDIUM_BIG
                        ),
                    ),
                    rx.alert_dialog.content(
                        rx.alert_dialog.title(dialog_text),
                        rx.alert_dialog.description(
                            dialog_description,
                            size="2",
                        ),
                        rx.flex(
                            rx.alert_dialog.cancel(
                                rx.button(
                                    cancel_text,
                                    variant="soft",
                                    background_color=Color.LIGHT_GRAY,
                                ),
                            ),
                            rx.alert_dialog.action(
                                rx.button(
                                    action_text,
                                    on_click=click,
                                    background_color=Color.PRIMARY,
                                    variant="solid",
                                ),
                            ),
                            spacing="3",
                            margin_top=Size.DEFAULT,
                            justify="end",
                        ),
                        style={"max_width": 450},
                        background_color=rx.color_mode_cond(light="white", dark=Color.TEXT)
                    ),
                )