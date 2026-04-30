import reflex as rx


from Personalidad.styles.fonts import Font
from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color


def show_progress_test(progress: float, margin: Size):
        """Barra de progreso durante el test usando Chakra para estabilidad."""
        return rx.chakra.progress(
            value=progress,
            color_scheme="green",
            margin_bottom=margin,
            width="100%",
            border_radius="none",
        )


def show_progress(progress: float, margin: Size, isOk: bool):
        """Barra de resultados usando Chakra para estabilidad."""
        return rx.chakra.progress(
            value=progress,
            # Forzamos un esquema verde para los resultados
            color_scheme="green",
            margin_bottom=margin,
            width="100%",
            border_radius="none",
        )