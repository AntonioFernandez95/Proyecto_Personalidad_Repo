import reflex as rx
import uuid
import asyncio
import json

class CalculadoraAPI:
    """
    Capa de Conexión.
    Puente exclusivo entre el cálculo y la base de datos.
    """

    @staticmethod
    async def ejecutar_flujo_calculo(state):
        """
        Lanza el guardado en DB en segundo plano para no bloquear al usuario.
        """
        user_id = state.user if state.user else "anónimo"
        
        # Extraemos los datos del estado
        payload = {
            "gender": state.gender,
            "flexiones": state.flexiones,
            "plancha_seg": state.plancha_seg,
            "km2000": state.km2000,
            "agilidad_seg": state.agilidad_seg,
            "porcentaje": str(state.porcentaje),
            "resultado": state.resultado
        }
        
        # 3. Guardamos en DB de forma asíncrona pero esperable
        await CalculadoraAPI._guardar_en_db(user_id, payload)

    @staticmethod
    async def _guardar_en_db(user_id, payload):
        try:
            from Personalidad.db.crud import guardar_historial_fisico
            
            def safe_int(v):
                try: return int(float(v))
                except: return 0

            def safe_int_carrera(v):
                try:
                    if ":" in str(v):
                        p = str(v).split(":")
                        return int(float(p[0])) * 60 + int(float(p[1]))
                    return int(float(v))
                except: return 0
            
            def safe_float(v):
                try: return float(v)
                except: return 0.0

            print(f"DEBUG DB: Guardando para {user_id}...")
            guardar_historial_fisico(
                user_id=user_id,
                gender=payload["gender"],
                flexiones=safe_int(payload["flexiones"]),
                plancha=safe_int(payload["plancha_seg"]),
                km2000=safe_int_carrera(payload["km2000"]),
                agilidad=safe_float(payload["agilidad_seg"]),
                resultado=payload["resultado"],
                porcentaje=payload["porcentaje"]
            )
            print(f"DEBUG DB: Guardado OK.")
        except Exception as e:
            print(f"DEBUG DB ERROR: {e}")
