import reflex as rx
from Personalidad.states.base_state import State
from Personalidad.pages.academia.layout import academia_layout, BTN_PRIMARY_BASE, BTN_SECONDARY_BASE, BTN_BACK_BASE, CARD_STYLE

# TODO: Pendiente la conexión con la base de datos para la gestión real de planes.
# Funcionalidad: Ver planes activos, Alargar vencimiento, Dar de baja por plan.

def plan_management_card(plan_name: str, status: str, expiration: str) -> rx.Component:
    is_active = status == "Activo"
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading(plan_name, size="5", color="black"),
                rx.badge(
                    status, 
                    color_scheme="green" if is_active else "gray",
                    variant="solid"
                ),
                spacing="1", align="start",
            ),
            rx.spacer(),
            rx.icon("calendar-clock", color="#5B733A" if is_active else "#ccc", size=32),
            width="100%", align="center",
        ),
        rx.divider(margin_y="1em"),
        rx.vstack(
            rx.text("Fecha de Vencimiento Actual:", font_size="0.85em", color="#666"),
            rx.text(expiration, font_weight="bold", font_size="1.2em", color="#5B733A" if is_active else "#999"),
            width="100%", align="start",
        ),
        rx.hstack(
            rx.input(placeholder="Nueva fecha (AAAA-MM-DD)", width="100%"),
            rx.button("Alargar", **BTN_SECONDARY_BASE),
            width="100%", spacing="2", margin_top="1em",
        ),
        rx.button(
            "Dar de Baja en este Plan", 
            background_color="#7d804e", # Color verdoso/oscuro
            color="white", # TEXTO EN BLANCO SOLICITADO
            width="100%", 
            margin_top="1.5em",
            on_click=rx.window_alert(f"Baja de {plan_name} (UI)")
        ),
        **CARD_STYLE,
        padding="2em",
        width="100%",
        opacity="1" if is_active else "0.7",
    )

@rx.page(route="/admin/planes", title="Gestión de Planes - Administración", on_load=State.check_login)
def admin_plans() -> rx.Component:
    return academia_layout(
        rx.vstack(
            rx.hstack(
                rx.link(
                    rx.button("← Volver al Panel", **BTN_BACK_BASE),
                    href="/admin",
                    underline="none",
                ),
                rx.spacer(),
                align="center",
                width="100%",
                margin_bottom="2em",
            ),
            rx.heading("Gestión de Planes por Usuario", size="8", color="white", font_weight="800"),
            rx.text("Configura el acceso individual a cada uno de los planes activos.", color="rgba(255,255,255,0.7)"),
            
            # Grid de los 2 Planes (Sustituido por Hstack para mejor control de espacio)
            rx.hstack(
                plan_management_card("Pruebas Físicas", "Activo", "2026-10-15"),
                plan_management_card("Test de Personalidad", "Activo", "2026-08-20"),
                spacing="9",
                width="100%",
                margin_top="2em",
                align_items="stretch",
            ),
            
            rx.text(
                "Nota: Los usuarios pueden tener 1 o 2 planes activos simultáneamente. La baja de un plan no afecta al otro.",
                font_size="0.85em", color="rgba(255,255,255,0.6)", margin_top="3em", text_align="center"
            ),
            
            align="center",
            width="100%",
            max_width="1000px",
        )
    )
