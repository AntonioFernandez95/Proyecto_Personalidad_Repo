import reflex as rx
from Personalidad.states.base_state import State
from Personalidad.db.client import db_client

class FisicasState(State):
    """Estado de Seguridad para la sección de Pruebas Físicas"""
   
    def check_plan_fisicas(self):
        """
        Evento para el on_load de la página de físicas.
        Bloquea a los usuarios sin el plan correcto.
        """
        # 1. Comprobar si el usuario ha iniciado sesión
        # Recuerda que en tu base_state.py, self.user guarda el email
        if not self.user:
            # Si no hay sesión, lo mandamos a la pantalla de inicio (login)
            return rx.redirect("/")
           
        # 2. Buscar al usuario en la BD para ver qué plan tiene
        try:
            # Usamos el cliente de tus compañeros para buscar por email
            user_data = db_client.find_one("personalidad.users", "email", self.user)
           
            if user_data:
                # Sacamos el plan (si no han añadido la columna aún, por defecto será "basico")
                plan_actual = user_data.get("user_plan", "basico").lower()
               
                # 3. La barrera: ¿Tiene el plan correcto?
                if "fisicas" not in plan_actual and plan_actual != "premium":
                    return rx.window_alert("ACCESO DENEGADO: Necesitas el plan de Pruebas Físicas para acceder a esta sección.")
                    # Si prefieres echarlo a otra página en vez de solo mostrar la alerta, descomenta esto:
                    # return rx.redirect("/info")
            else:
                return rx.window_alert("Error de seguridad: Usuario no encontrado.")
               
        except Exception as e:
            print(f"Error al comprobar permisos de físicas: {e}")
            return rx.window_alert("Hubo un problema al verificar tus permisos.")

