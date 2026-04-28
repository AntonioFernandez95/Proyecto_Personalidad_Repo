import reflex as rx
from typing import Any
from Personalidad.states.base_state import State
from Personalidad.states.admin_state import AdminState
from Personalidad.pages.academia.layout import academia_layout, BTN_PRIMARY_BASE, BTN_SECONDARY_BASE, BTN_BACK_BASE, CARD_STYLE

def edit_profile_card() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("user-cog", size=24, color="#5B733A"),
            rx.heading("Editar Datos del Perfil", size="5", color="black"),
            spacing="2",
            align="center",
            margin_bottom="1em",
        ),
        rx.vstack(
            rx.text("Nombre Completo:", font_size="0.85em", color="#666"),
            rx.input(
                value=AdminState.new_name,
                on_change=AdminState.set_new_name,
                placeholder="Nombre y Apellidos",
                width="100%",
                background_color="white",
                color="black",
            ),
            width="100%", align="start",
        ),
        rx.vstack(
            rx.text("Correo Electrónico:", font_size="0.85em", color="#666", margin_top="1em"),
            rx.input(
                value=AdminState.new_email,
                on_change=AdminState.set_new_email,
                placeholder="email@ejemplo.com",
                width="100%",
                background_color="white",
                color="black",
            ),
            width="100%", align="start",
        ),
        rx.button(
            "Guardar Cambios de Perfil",
            on_click=AdminState.guardar_perfil,
            background_color="#5B733A",
            color="white",
            width="100%",
            margin_top="1.5em",
        ),
        **CARD_STYLE,
        padding="2em",
        width="100%",
        margin_bottom="2em",
    )

def plan_management_card(plan_name: str, status: rx.Var, expiration: rx.Var, on_alargar: Any, on_toggle: Any) -> rx.Component:
    is_active_cond = (status == "Activo")
    
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading(plan_name, size="5", color="black"),
                rx.badge(
                    status, 
                    color_scheme=rx.cond(is_active_cond, "green", "gray"),
                    variant="solid"
                ),
                spacing="1", align="start",
            ),
            rx.spacer(),
            rx.icon("calendar-clock", color=rx.cond(is_active_cond, "#5B733A", "#ccc"), size=32),
            width="100%", align="center",
        ),
        rx.divider(margin_y="1em"),
        rx.vstack(
            rx.text("Fecha de Vencimiento Actual:", font_size="0.85em", color="#666"),
            rx.text(
                expiration, 
                font_weight="bold", 
                font_size="1.2em", 
                color=rx.cond(is_active_cond, "#5B733A", "#999")
            ),
            width="100%", align="start",
        ),
        rx.hstack(
            rx.input(
                placeholder="Días a sumar", 
                width="100%",
                value=AdminState.days_to_add,
                on_change=AdminState.set_days_to_add,
                background_color="white",
                color="black",
            ),
            rx.button(
                "Alargar", 
                on_click=on_alargar,
                **BTN_SECONDARY_BASE
            ),
            width="100%", spacing="2", margin_top="1em",
        ),
        rx.button(
            rx.cond(is_active_cond, "Dar de Baja", "Reactivar Plan"),
            background_color=rx.cond(is_active_cond, "#7d804e", "#5B733A"),
            color="white",
            width="100%", 
            margin_top="1.5em",
            on_click=on_toggle
        ),
        **CARD_STYLE,
        padding="2em",
        width="100%",
        opacity="1",
    )

@rx.page(route="/academia/admin_plans", title="Gestión de Planes - Administración", on_load=AdminState.on_load)
def admin_plans() -> rx.Component:
    return academia_layout(
        rx.vstack(
            rx.hstack(
                rx.link(
                    rx.button("← Volver al Panel", **BTN_BACK_BASE),
                    href="/academia/admin_panel",
                    underline="none",
                ),
                rx.spacer(),
                align="center",
                width="100%",
                margin_bottom="2em",
            ),
            rx.heading(
                rx.cond(
                    AdminState.selected_user["full_name"],
                    rx.text(f"Gestionar: {AdminState.selected_user['full_name']}"),
                    rx.text(f"Gestionar: {AdminState.selected_user['email']}")
                ),
                size="8", color="white", font_weight="800"
            ),
            rx.text("Configuración independiente por cada plan de estudios.", color="rgba(255,255,255,0.7)"),
            
            # NUEVA TARJETA DE EDICIÓN DE PERFIL
            edit_profile_card(),

            rx.hstack(
                # Tarjeta 1: Plan Academia / Personalidad
                plan_management_card(
                    "Test Personalidad", 
                    rx.cond(AdminState.selected_user["disabled_personalidad"], "Inactivo", "Activo"),
                    AdminState.selected_user["hasta_personalidad"],
                    AdminState.alargar_vencimiento_plan("personalidad"),
                    AdminState.toggle_baja_plan("personalidad")
                ),
                # Tarjeta 2: Plan Pruebas Físicas
                plan_management_card(
                    "Pruebas Físicas", 
                    rx.cond(AdminState.selected_user["disabled_fisicas"], "Inactivo", "Activo"),
                    AdminState.selected_user["hasta_fisicas"],
                    AdminState.alargar_vencimiento_plan("fisicas"),
                    AdminState.toggle_baja_plan("fisicas")
                ),
                spacing="9",
                width="100%",
                margin_top="1em",
                align_items="stretch",
            ),
            
            rx.text(
                "Nota: Cada plan se gestiona de forma aislada. La baja en uno no afecta al otro.",
                font_size="0.85em", color="rgba(255,255,255,0.6)", margin_top="3em", text_align="center"
            ),
            
            align="center",
            width="100%",
            max_width="1000px",
        )
    )
