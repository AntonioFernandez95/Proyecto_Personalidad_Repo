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
            from Personalidad.db.crud import guardar_historial_ligero
            from Personalidad.db.schemas.historialSimplificado_schema import HistorialSimplificadoCreate
            
            datos_ticket = HistorialSimplificadoCreate(
                token_simulacro=str(uuid.uuid4()),
                propietario_id=user_id,
                simulacro_code="CALC-API",
                resultado=payload["resultado"],
                gender=payload["gender"],
                flexiones=payload["flexiones"],
                plancha_seg=payload["plancha_seg"],
                km2000=payload["km2000"],
                agilidad_seg=payload["agilidad_seg"],
                porcentaje=payload["porcentaje"]
            )
            print(f"DEBUG DB: Guardando para {user_id}...")
            guardar_historial_ligero(datos_ticket)
            print(f"DEBUG DB: Guardado OK.")
        except Exception as e:
            print(f"DEBUG DB ERROR: {e}")
