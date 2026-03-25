import reflex as rx
import Personalidad.styles.utils as utils

from Personalidad.styles.styles import Size
from Personalidad.styles.fonts import Font
from Personalidad.styles.colors import Color
from Personalidad.components.info_box import info_box


def header()-> rx.Component:
    
    return rx.box(
        rx.vstack(
            rx.image(
                src="/ic_test_personalidad.png", 
                align="center",
                width="100px", 
                height="auto" , 
                display="flex",
                direction="column",
            ),
            rx.heading(
                utils.titulo,
                color=Color.SECONDARY,
                font_family=Font.DEFAULT,
                ),
            rx.text(utils.descripcion),
            rx.spacer(),
            rx.tablet_and_desktop(
                rx.hstack(
                    info_box(utils.op_1),
                    info_box(utils.op_2),
                    info_box(utils.op_3),
                    info_box(utils.op_4),
                    info_box(utils.op_5),
                    text_align="center"
                ),
                width="100%",
            ),
            rx.mobile_only(
                rx.vstack(
                    info_box(utils.op_1),
                    info_box(utils.op_2),
                    info_box(utils.op_3),
                    info_box(utils.op_4),
                    info_box(utils.op_5),
                    text_align="center"
                ), 
                width="100%",
            ),
            rx.spacer(),
            rx.heading(
                utils.titulo_2,
                color=Color.SECONDARY,
                font_family=Font.DEFAULT,
                size="5"
            ),
            rx.mobile_only(
                rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger(utils.item_1 , value="tab1"),
                    rx.tabs.trigger(utils.item_2, value="tab2"),
                    rx.tabs.trigger(utils.item_3, value="tab3"),
                    rx.tabs.trigger(utils.item_4, value="tab4"),
                    rx.tabs.trigger(utils.item_5, value="tab5"),
                    rx.tabs.trigger(utils.item_6, value="tab6"),
                    rx.tabs.trigger(utils.item_7, value="tab7"),
                    class_name="flex-col",
                ),
                rx.tabs.content(
                    rx.text(utils.desc_1),
                    value="tab1", padding="8px", 
                ),
                rx.tabs.content(
                    rx.text(utils.desc_2),
                    value="tab2", padding="8px",
                ),
                rx.tabs.content(
                    rx.text(utils.desc_3),
                    value="tab3",padding="8px",
                ),
                rx.tabs.content(
                    rx.text(utils.desc_4),
                    value="tab4",padding="8px",
                ),
                rx.tabs.content(
                    rx.text(utils.desc_5),
                    value="tab5",padding="8px",
                ),
                rx.tabs.content(
                    rx.text(utils.desc_6),
                    value="tab6",padding="8px",
                ),
                rx.tabs.content(
                    rx.text(utils.desc_7),
                    value="tab7",padding="8px",
                ),
                default_value="tab1",
                orientation="vertical",
                ),
            ),
            rx.tablet_and_desktop(
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger(utils.item_1 , value="tab1"),
                        rx.tabs.trigger(utils.item_2, value="tab2"),
                        rx.tabs.trigger(utils.item_3, value="tab3"),
                        rx.tabs.trigger(utils.item_4, value="tab4"),
                        rx.tabs.trigger(utils.item_5, value="tab5"),
                        rx.tabs.trigger(utils.item_6, value="tab6"),
                        rx.tabs.trigger(utils.item_7, value="tab7"),
                    ),
                    rx.tabs.content(
                        rx.text(utils.desc_1),
                        value="tab1", padding="8px", 
                    ),
                    rx.tabs.content(
                        rx.text(utils.desc_2),
                        value="tab2", padding="8px",
                    ),
                    rx.tabs.content(
                        rx.text(utils.desc_3),
                        value="tab3",padding="8px",
                    ),
                    rx.tabs.content(
                        rx.text(utils.desc_4),
                        value="tab4",padding="8px",
                    ),
                    rx.tabs.content(
                        rx.text(utils.desc_5),
                        value="tab5",padding="8px",
                    ),
                    rx.tabs.content(
                        rx.text(utils.desc_6),
                        value="tab6",padding="8px",
                    ),
                    rx.tabs.content(
                        rx.text(utils.desc_7),
                        value="tab7",padding="8px",
                    ),
                    default_value="tab1",
                ),
            align="center"
            ),
            align="center"
        ),
        margin=Size.DEFAULT
    )