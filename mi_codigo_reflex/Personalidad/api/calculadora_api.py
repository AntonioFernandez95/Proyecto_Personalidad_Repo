# Personalidad/api/calculadora_api.py
import reflex as rx
import uuid
from Personalidad.db.crud import guardar_historial_ligero
from Personalidad.db.schemas.historialSimplificado_schema import HistorialSimplificadoCreate

class CalculadoraAPI:
    """
    Capa de Conexión.
    Puente exclusivo entre el cálculo y la base de datos.
    """

    @staticmethod
    async def ejecutar_flujo_calculo(state):
        """
        Orquesta el flujo: Motor -> Captura -> CRUD -> Historial.
        """
        from Personalidad.states.calculadora_state import CalculadoraState
        from Personalidad.states.historial_state import HistorialSimplificado_State
        
        # 1. Recepción y Llamada al Motor (Delegación)
        # Obtenemos el motor de cálculo
        calc_engine = await state.get_state(CalculadoraState)
        
        # Ejecutamos el motor pasando los datos del estado
        resultado_apto = calc_engine.motor_de_calculo(
            state.gender,
            state.flexiones,
            state.plancha_seg,
            state.km2000,
            state.agilidad_seg
        )

        # 2. Captura de Resultados
        state.resultado = resultado_apto
        user_id = state.user if state.user else "anónimo"

        # 3. Guardado (Llamada al CRUD)
        # Preparamos el schema para el CRUD (Caja Negra)
        try:
            datos_ticket = HistorialSimplificadoCreate(
                id=str(uuid.uuid4()),
                user_id=user_id,
                simulacro_code="CALC-API",
                resultado=state.resultado
            )
            guardar_historial_ligero(datos_ticket)
        except Exception as e:
            print(f"Error al guardar en el CRUD: {e}")
