import reflex as rx
from Personalidad.states.base_state import State
from Personalidad.db.client import db_client

class FisicasState(State):
    """Estado de Seguridad para la sección de Pruebas Físicas"""
   
    def check_plan_fisicas(self):
        """
        Seguridad estricta: Solo permite el acceso si el usuario es de Academia Métodos
        o si tiene su acceso vigente (fecha 'hasta').
        """
        # 1. Si no hay sesión, al login de cabeza
        if not self.user:
            return rx.redirect("/")
            
        try:
            # 2. Buscamos tu usuario en la base de datos
            user_data = db_client.find_one("usuarios_metodos.usuarios_plataformas", "email", self.user)
            
            if user_data:
                # Acceso total para personal de Academia Métodos
                email_lower = self.user.lower()
                if email_lower.endswith("@academiametodos.com") or email_lower.endswith("@academiametodos.es"):
                    return None

                # Verificación de fecha de caducidad (hasta)
                # Si 'hasta' existe y es mayor que ahora, tiene acceso.
                from datetime import datetime
                hasta = user_data.get("hasta")
                
                tiene_acceso = False
                if hasta:
                    try:
                        if isinstance(hasta, str):
                            # El formato suele ser ISO o similar desde Postgres
                            fecha_hasta = datetime.fromisoformat(hasta.replace('Z', '+00:00'))
                        else:
                            fecha_hasta = hasta
                            
                        if fecha_hasta > datetime.now(fecha_hasta.tzinfo if fecha_hasta.tzinfo else None):
                            tiene_acceso = True
                    except Exception as e:
                        print(f"Error parseando fecha hasta: {e}")
                
                # --- FILTRO PARA EL RESTO ---
                if not tiene_acceso:
                    return rx.window_alert("Tu acceso ha caducado o no tienes el plan activo.")
                
                return None # Acceso concedido si tiene fecha vigente
            else:
                return rx.redirect("/")
                
        except Exception as e:
            print(f"Error de seguridad: {e}")
            return rx.redirect("/")
