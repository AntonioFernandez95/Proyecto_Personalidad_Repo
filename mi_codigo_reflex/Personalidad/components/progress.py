import reflex as rx


from Personalidad.styles.fonts import Font
from Personalidad.styles.styles import Size
from Personalidad.styles.colors import Color


def show_progress_test(progress: float, margin: Size):
        """Barra de progreso durante el test con color oliva manual."""
        return rx.chakra.box(
            rx.chakra.box(
                width=f"{progress}%",
                height="100%",
                background_color=Color.PRIMARY.value,
                transition="width 0.5s ease-in-out",
            ),
            width="100%",
            height="10px",
            background_color="#E2E8F0", # Color gris suave de fondo
            margin_bottom=margin,
            border_radius="none",
            overflow="hidden",
        )


def show_progress(progress: float, margin: Size, isOk: bool):
        """Barra de resultados con el color oliva exacto del botón."""
        return rx.chakra.box(
            rx.chakra.box(
                width=f"{progress}%",
                height="100%",
                background_color=Color.PRIMARY.value,
                transition="width 0.5s ease-in-out",
            ),
            width="100%",
            height="12px",
            background_color="#E2E8F0",
            margin_bottom=margin,
            border_radius="none",
            overflow="hidden",
        )