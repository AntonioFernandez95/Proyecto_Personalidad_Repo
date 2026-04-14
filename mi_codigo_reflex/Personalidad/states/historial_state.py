import reflex as rx
from Personalidad.states.base_state import State
from Personalidad.db.crud import consultar_historial_usuario

class HistorialSimplificado_State(State):
    """
    Capa de Historial.
    Se encarga de cargar y refrescar la tabla de simulacros.
    """
    historial: list[dict] = []

    def cargar_historial(self):
        """
        Carga el historial real del usuario desde la base de datos.
        """
        user_id = self.user if self.user else "anónimo"
        print(f"DEBUG: Cargando historial para {user_id}")
        
        # Importamos aquí para evitar circulares si fuera necesario, 
        # aunque en este caso consultar_historial_usuario está en crud.py
        from Personalidad.db.crud import consultar_historial_usuario
        registros = consultar_historial_usuario(user_id)
        
        self.historial = []
        for r in registros:
            # Si r.fecha ya es un string (por el importador), lo usamos tal cual
            if isinstance(r.fecha, str):
                fecha_str = r.fecha[:10] # Solo pillamos YYYY-MM-DD
            else:
                fecha_str = r.fecha.strftime("%d/%m/%Y")
            color = "#787C4D" if r.resultado == "APTO" else "#4A4D4E"
            
            porcentaje_str = r.porcentaje if r.porcentaje else ""
            
            # Color para el componente Badge de Radix/Reflex
            color_name = "green" if r.resultado == "APTO" else "gray"
            
            # ─────────────────────────────────────────────────────────────
            # LÓGICA DE VALIDACIÓN INDIVIDUAL (PARA COLORES)
            # ─────────────────────────────────────────────────────────────
            def time_to_sec(t_str):
                try:
                    if ":" in str(t_str):
                        p = str(t_str).split(":")
                        return int(float(p[0])) * 60 + int(float(p[1]))
                    return int(float(t_str))
                except: return 9999

            g = r.gender.lower() if r.gender else "masculino"
            # Umbrales
            if g == "femenino":
                t_flex, t_plan, t_carr, t_agil = 12, 40, 780, 27.0
            else:
                t_flex, t_plan, t_carr, t_agil = 17, 60, 660, 25.0

            flex_val = 0
            try: flex_val = int(float(r.flexiones)) if r.flexiones else 0
            except: pass

            plan_val = 0
            try: plan_val = int(float(r.plancha_seg)) if r.plancha_seg else 0
            except: pass

            agil_val = 999.0
            try: agil_val = float(r.agilidad_seg) if r.agilidad_seg else 999.0
            except: pass

            carr_val = time_to_sec(r.km2000)

            # Flags de éxito
            flex_ok = flex_val >= t_flex
            plan_ok = plan_val >= t_plan
            carr_ok = carr_val <= t_carr
            agil_ok = agil_val <= t_agil
            # ─────────────────────────────────────────────────────────────

            self.historial.append({
                "fecha": fecha_str,
                "test": r.simulacro_code,
                "resultado": f"{r.resultado} ({porcentaje_str}%)" if porcentaje_str else r.resultado,
                "color": color,           # Hexadecimal para componentes personalizados
                "color_name": color_name, # Para color_scheme de Reflex
                "gender": r.gender if r.gender else "-",
                "flexiones": r.flexiones if r.flexiones else "-",
                "plancha": r.plancha_seg if r.plancha_seg else "-",
                "km2000": r.km2000 if r.km2000 else "-",
                "agilidad": r.agilidad_seg if r.agilidad_seg else "-",
                "porcentaje": porcentaje_str if porcentaje_str else "-",
                "user_id": r.user_id if r.user_id else "anónimo",
                "flex_ok": flex_ok,
                "plan_ok": plan_ok,
                "carr_ok": carr_ok,
                "agil_ok": agil_ok
            })

