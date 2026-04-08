import reflex as rx
from Personalidad.states.base_state import State
from Personalidad.db.client import db_client

class FisicasState(State):
    """Estado de Seguridad para la sección de Pruebas Físicas"""
   
    def check_plan_fisicas(self):
        """
        Seguridad estricta: Solo permite el acceso si el usuario es el admin 
        o si tiene explícitamente el 'plan fisico'.
        """
        # 1. Si no hay sesión, al login de cabeza
        if not self.user:
            return rx.redirect("/")
            
        try:
            # 2. Buscamos tu usuario en la base de datos
            user_data = db_client.find_one("personalidad.users", "email", self.user)
            
            if user_data:
                # Sacamos el plan, si no tiene nada, por defecto es "sin_plan"
                plan_actual = user_data.get("user_plan", "sin_plan").lower()
                
                # --- FILTRO EXCLUSIVO PARA TI ---
                # Sustituye 'tu_email@ejemplo.com' por el email con el que te logueas tú
                if self.user == "claudia@academiametodos.com":
                    return None # Acceso total para ti, sin preguntas.

                # --- FILTRO PARA EL RESTO ---
                # Solo deja pasar si el texto es exactamente "plan fisico"
                if plan_actual != "plan fisico":
                    return rx.window_alert("Necesitas el 'plan fisico' para ver esta sección.")
                    # O si prefieres echarlo: return rx.redirect("/academia")
            else:
                return rx.redirect("/")
                
        except Exception as e:
            print(f"Error de seguridad: {e}")
            return rx.redirect("/")
