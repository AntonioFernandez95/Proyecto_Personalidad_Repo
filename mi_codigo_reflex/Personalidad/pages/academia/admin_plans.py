import reflex as rx
from typing import Any
from Personalidad.states.base_state import State
from Personalidad.states.admin_state import AdminState
from Personalidad.pages.academia.layout import academia_layout, BTN_PRIMARY_BASE, BTN_SECONDARY_BASE, BTN_BACK_BASE, CARD_STYLE

def admin_plans_header() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.heading(
                rx.cond(
                    AdminState.selected_user["full_name"],
                    rx.text(f"Gestionar: {AdminState.selected_user['full_name']}"),
                    rx.text(f"Gestionar: {AdminState.selected_user['email']}")
                ),
                size="9", color="white", font_weight="900"
            ),
            rx.text("Configuración individual de perfil y planes.", color="rgba(255,255,255,0.8)", font_size="1.1em"),
            align_items="start",
            spacing="1",
        ),
        rx.spacer(),
        rx.link(
            rx.button(
                rx.icon("arrow-left", size=18),
                rx.text("Volver al Panel", white_space="nowrap"),
                background_color="white",
                color="#5B733A",
                font_weight="bold",
                height="3.5em",
                padding_x="2em",
                border_radius="12px",
                _hover={"background_color": "#f0f0f0", "transform": "scale(1.02)"},
            ),
            href="/academia/admin_panel",
            underline="none",
        ),
        align="center",
        width="100%",
        padding_top="5em",
        padding_bottom="3em",
        flex_direction=["column", "row"],
        gap="2em",
    )

def edit_profile_card() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon("user-cog", size=28, color="#5B733A"),
            rx.heading("Perfil del Alumno", size="6", color="black", font_weight="900"),
            spacing="3",
            align="center",
            margin_bottom="1.5em",
        ),
        rx.flex(
            rx.vstack(
                rx.text("Nombre Completo:", font_size="0.9em", color="#444", font_weight="bold"),
                rx.input(
                    value=AdminState.new_name,
                    on_change=AdminState.set_new_name,
                    width="100%",
                    background="white",
                    color="black",
                    border="1px solid #ddd",
                    height="3.5em",
                    border_radius="10px",
                ),
                width="100%", flex="1",
            ),
            rx.vstack(
                rx.text("Correo Electrónico:", font_size="0.9em", color="#444", font_weight="bold"),
                rx.input(
                    value=AdminState.new_email,
                    on_change=AdminState.set_new_email,
                    width="100%",
                    background="white",
                    color="black",
                    border="1px solid #ddd",
                    height="3.5em",
                    border_radius="10px",
                ),
                width="100%", flex="1",
            ),
            width="100%",
            spacing="6",
            flex_direction=["column", "row"],
        ),
        rx.button(
            "Guardar Cambios de Perfil",
            on_click=AdminState.guardar_perfil,
            background_color="#5B733A",
            color="white",
            width="100%",
            height="4em",
            margin_top="2em",
            font_weight="bold",
            border_radius="12px",
        ),
        **CARD_STYLE,
        padding="2.5em",
        width="100%",
        margin_bottom="3em",
        opacity="1",
    )

def plan_management_card(plan_name: str, status: rx.Var, expiration: rx.Var, on_alargar: Any, on_toggle: Any) -> rx.Component:
    is_active_cond = (status == "Activo")
    
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading(plan_name, size="5", color="black", font_weight="800"),
                rx.badge(
                    status, 
                    color_scheme=rx.cond(is_active_cond, "green", "gray"),
                    variant="solid",
                    size="2"
                ),
                spacing="1", align="start",
            ),
            rx.spacer(),
            rx.icon("calendar-clock", color=rx.cond(is_active_cond, "#5B733A", "#ccc"), size=36),
            width="100%", align="center",
        ),
        rx.divider(margin_y="1.5em", border_color="#eee"),
        rx.vstack(
            rx.text("Vencimiento Actual:", font_size="0.9em", color="#666", font_weight="bold"),
            rx.text(
                expiration, 
                font_weight="900", 
                font_size="1.5em", 
                color=rx.cond(is_active_cond, "#5B733A", "#999")
            ),
            width="100%", align="start",
        ),
        rx.vstack(
            rx.text("Añadir tiempo (días):", font_size="0.85em", color="#444", margin_top="1em"),
            rx.hstack(
                rx.input(
                    placeholder="Ej: 30", 
                    width="100%",
                    value=AdminState.days_to_add,
                    on_change=AdminState.set_days_to_add,
                    background="white",
                    color="black",
                    border="1px solid #ddd",
                    height="3em",
                    border_radius="10px",
                ),
                rx.button(
                    "Alargar", 
                    on_click=on_alargar,
                    # Eliminamos BTN_SECONDARY_BASE para evitar conflicto de border_radius
                    background_color="#5B733A",
                    color="white",
                    height="3em",
                    border_radius="10px",
                    padding_x="1em",
                ),
                width="100%", spacing="3",
            ),
            width="100%",
        ),
        rx.button(
            rx.cond(is_active_cond, "Dar de Baja", "Reactivar Plan"),
            background_color=rx.cond(is_active_cond, "#7d804e", "#5B733A"),
            color="white",
            width="100%", 
            height="4em",
            margin_top="2em",
            on_click=on_toggle,
            font_weight="bold",
            border_radius="12px",
        ),
        **CARD_STYLE,
        padding="2.5em",
        width="100%",
        opacity="1",
        flex="1",
    )

@rx.page(route="/academia/admin_plans", title="Gestión de Alumno", on_load=AdminState.on_load)
def admin_plans() -> rx.Component:
    return academia_layout(
        rx.flex(
            admin_plans_header(),
            
            edit_profile_card(),

            rx.flex(
                plan_management_card(
                    "Test Personalidad", 
                    rx.cond(AdminState.selected_user["disabled_personalidad"], "Inactivo", "Activo"),
                    AdminState.selected_user["hasta_personalidad"],
                    AdminState.alargar_vencimiento_plan("personalidad"),
                    AdminState.toggle_baja_plan("personalidad")
                ),
                plan_management_card(
                    "Pruebas Físicas", 
                    rx.cond(AdminState.selected_user["disabled_fisicas"], "Inactivo", "Activo"),
                    AdminState.selected_user["hasta_fisicas"],
                    AdminState.alargar_vencimiento_plan("fisicas"),
                    AdminState.toggle_baja_plan("fisicas")
                ),
                width="100%",
                spacing="8",
                flex_direction=["column", "column", "row"],
                align_items="stretch",
            ),
            
            direction="column",
            width="100%",
            max_width="1400px",
            align_items="center",
            padding_bottom="5em",
            padding_x=["1em", "2em", "4em"],
        )
    )
