import reflex as rx
from enum import Enum
from Personalidad.styles.colors import Color

#Constants
MAX_WIDTH = "600px"

#Sizes
class Size(Enum):
    ZERO="0em"
    NAH="0.2em"
    SMALL="0.5em"
    DEFAULT="1em"
    MEDIUM_BIG="1.5em"
    BIG="2em"
    EXTRA_BIG="4em"
    
    
STYLESHEETS = [
    "https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;0,700;0,900;1,400;1,500;1,700;1,900&display=swap",
    "https://fonts.googleapis.com/css2?family=Bitter:ital,wght@0,100..900;1,100..900&family=Roboto:ital,wght@0,400;0,500;0,700;0,900;1,400;1,500;1,700;1,900&display=swap",
    "https://db.onlinewebfonts.com/c/ab596f21664c5582567537d241e2a53e?family=DIN+Next+Rounded+LT+W01+Regular"
]



#Styles
BASE_STYLE = {
    "user_select": "none",
    "webkit_user_select": "none",
    "moz_user_select": "none",
    "ms_user_select": "none",
    "background_image": "url('/fondo-soldados (1).png')",
    "background_size": "cover",
    "background_attachment": "fixed",
    rx.button: {
        "padding": Size.DEFAULT.value,
        "border_radius": "0",
        "background_color": Color.PRIMARY.value,
        "_hover": {
            "background_color": Color.SECONDARY.value
        }
    },
    rx.link: {
        "text_decoration": "none",
        "_hover": {}
    }
}

TEST_STYLE = {
    "padding": "2em",
    "border_radius": "25px",
    "border": f"1px solid {rx.color('accent', 12)}",
    "box_shadow": f"0px 0px 10px 0px {rx.color('gray', 11)}",
    "bg": rx.color("gray", 1),
}

QUESTION_STYLE = TEST_STYLE | {"width": "100%"}