import reflex as rx

from Personalidad.styles.fonts import Font
from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color

def show_progress_test(progress: float, margin: Size):
        return rx.progress.root(
            rx.progress.indicator(
                value=progress,
                max=100,
                background_color=Color.PRIMARY
            ),
            margin_bottom=margin,
            radius="none",
            
        )

def show_progress(progress: float, margin: Size, isOk: bool):
        return rx.cond(
            isOk,
            rx.progress.root(
                rx.progress.indicator(
                    value=progress,
                    max=100,
                    background_color=Color.SECONDARY
                ),
                margin_bottom=margin,
                radius="none",
            ),
            rx.progress.root(
                rx.progress.indicator(
                    value=progress,
                    max=100,
                    background_color=Color.PRIMARY
                ),
                margin_bottom=margin,
                radius="none",
            )
        )