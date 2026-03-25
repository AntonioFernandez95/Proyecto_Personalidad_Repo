from fastapi import APIRouter, HTTPException
from .motor import calcular_resultado_test
# Importamos el CRUD y el Schema de tus compañeros
from Personalidad.db.crud import guardar_historial_ligero
from Personalidad.db.schemas.historial_schema import HistorialSimplificadoCreate
import uuid

router = APIRouter()

@router.post("/api/calcular_fisicas")
async def api_calcular_fisicas(
    gender: str, 
    flexiones: str, 
    plancha_seg: str, 
    km2000: str, 
    agilidad_seg: str, 
    user_id: str = "anónimo"
):
    # 1. Ejecutamos tu Motor de Cálculo (Punto 1B)
    resultado_motor = calcular_resultado_test(gender, flexiones, plancha_seg, km2000, agilidad_seg)
    
    if not resultado_motor["success"]:
        raise HTTPException(status_code=400, detail=f"Error en el cálculo: {resultado_motor.get('error')}")

    try:
        # 2. Preparamos los datos para el "Portero de Discoteca" (Schema de tus compañeros)
        # Generamos un ID único y usamos el resultado que nos dio el motor
        datos_para_db = HistorialSimplificadoCreate(
            id=str(uuid.uuid4()),
            user_id=user_id,
            simulacro_code="FISC-01",  # Código por defecto para físicas
            resultado=resultado_motor["resultado"],
            porcentaje=f"{resultado_motor['porcentaje']}%"
        )

        # 3. Llamamos al Ejecutor (CRUD de tus compañeros - Punto 2C)
        guardar_historial_ligero(datos_para_db)
        
        # Devolvemos el resultado al frontend para que lo pinten de verde o rojo
        return resultado_motor

    except Exception as e:
        print(f"Error en la conexión API-DB: {e}")
        raise HTTPException(status_code=500, detail="Cálculo hecho, pero error al guardar en historial")