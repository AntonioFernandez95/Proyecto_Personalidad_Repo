import reflex as rx

from Personalidad.styles.styles import Size

def round_button(button_text: str, click: rx.State)-> rx.Component:
    return rx.button(
                button_text,
                on_click=click,
                border_radius="25px",
                padding=Size.MEDIUM_BIG
            )

def round_button_left_icon(button_text: str, icon: str, click: rx.State)-> rx.Component:
    return rx.button(
                rx.icon(icon),
                button_text,
                on_click=click,
                border_radius="25px",
                padding=Size.MEDIUM_BIG
            )
    
def round_button_right_icon(button_text: str, icon: str, click: rx.State)-> rx.Component:
    return rx.button(
                button_text,
                rx.icon(icon),
                on_click=click,
                border_radius="25px",
                padding=Size.MEDIUM_BIG
            )