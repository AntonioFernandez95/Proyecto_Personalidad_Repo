import reflex as rx


from Personalidad.styles.fonts import Font
from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color
from Personalidad.states.base_state import State
from Personalidad.states.login_state import ButtonClick


def navbar() -> rx.Component:
    return rx.hstack(
        # 1. Logo (Extremo Izquierdo)
        rx.hstack(
            rx.image(
                src="/metodos_naranja_thick.svg",
                width=Size.BIG
            ),
            rx.heading(
                "Métodos",
                font_size=Size.BIG,
                font_family=Font.LOGO,
                color=rx.color_mode_cond(light=Color.TEXT, dark="white"),
            ),
            align="center",
            spacing="3",
            cursor="pointer",
            on_click=rx.redirect("/"),
        ),
       
        # 2. Enlaces (Centro Flex)
        rx.center(
            rx.cond(
                State.logged_in,
                rx.hstack(
                    rx.link(
                        rx.text("Simulacro Presencial", color=rx.color_mode_cond(light=Color.TEXT, dark="white"), font_weight="500", _hover={"color": "#ee6a19"}),
                        href="/academia/simulacro",
                        underline="none",
                    ),
                    # ENLACE PANEL ADMIN (Ahora en el centro)
                    rx.cond(
                        State.is_admin,
                        rx.link(
                            rx.text("Panel Admin", color=rx.color_mode_cond(light=Color.TEXT, dark="white"), font_weight="500", _hover={"color": "#ee6a19"}),
                            href="/academia/admin_panel",
                            underline="none",
                        ),
                        rx.fragment()
                    ),
                    spacing="4",
                    align="center",
                    wrap="wrap",
                ),
                rx.box()
            ),
            flex="1",
        ),
       
        # 3. Iconos y Modo Oscuro (Extremo Derecho)
        rx.hstack(
            rx.cond(
                State.logged_in,
                rx.hstack(
                    rx.link(
                        rx.icon("instagram", size=20, color=rx.color_mode_cond(light=Color.TEXT, dark="white")),
                        href="https://www.instagram.com/academiametodos/",
                        is_external=True,
                        _hover={"color": "#ee6a19"}
                    ),
                    rx.link(
                        rx.icon("send", size=20, color=rx.color_mode_cond(light=Color.TEXT, dark="white")),
                        href="https://telegram.org",
                        is_external=True,
                        _hover={"color": "#ee6a19"}
                    ),
                    rx.button(
                        rx.icon("log-out", size=18, stroke_width=2),
                        background_color=rx.color_mode_cond(light="#2b2b2b", dark="#555555"),
                        color="white",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        padding_x="0.75em",
                        on_click=State.logout,
                        _hover={"background_color": "#ee6a19"},
                    ),
                    spacing="5",
                    align="center",
                ),
                rx.box()
            ),
            rx.spacer(width="2"),
            rx.color_mode.icon(),
            rx.color_mode.switch(),
            align="center",
            spacing="4",
        ),
       
        position="fixed",
        top="0px",
        background_color=rx.color_mode_cond(light="white", dark=Color.TEXT),
        box_shadow=rx.color_mode_cond(light="0px 2px 4px rgba(0,0,0,0.1)", dark="none"),
        padding_x=Size.BIG,
        padding_y=Size.DEFAULT,
        min_height=Size.EXTRA_BIG,
        height="auto",
        width="100%",
        align_items="center",
        justify_content=["center", "center", "space-between", "space-between"],
        z_index="5",
        wrap="wrap",
    )
