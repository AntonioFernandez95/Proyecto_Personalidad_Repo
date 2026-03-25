import reflex as rx

from Personalidad.styles.colors import Color

def custoom_button(text: str, link: str)-> rx.Component:
    return rx.vstack(
        rx.button(
        text, 
        size= '3',
        background_color= Color.PRIMARY,
        on_click=rx.redirect(link)   
        )
    )