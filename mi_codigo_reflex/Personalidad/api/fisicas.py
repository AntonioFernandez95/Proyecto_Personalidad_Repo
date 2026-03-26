from fastapi import APIRouter, HTTPException
import uuid
from Personalidad.api.motor import calcular_resultado_test
from Personalidad.db.crud import guardar_historial_ligero
from Personalidad.db.schemas.historial_schema import HistorialSimplificadoCreate

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
    """
    Punto 3 vía API: Recibe datos externos, calcula y persiste en DB.
    """
    # 1. Ejecutar Motor (1B)
    res = calcular_resultado_test(gender, flexiones, plancha_seg, km2000, agilidad_seg) 
    
    if not res["success"]:
        raise HTTPException(status_code=400, detail=res.get("error"))

    try:
        # 2. Crear ticket y llamar a CRUD (2C)
        ticket = HistorialSimplificadoCreate(
            id=str(uuid.uuid4()),
            user_id=user_id,
            simulacro_code="FISC-API",
            resultado=res["resultado"]
        )
        
        guardar_historial_ligero(ticket) 
        return res
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al guardar el ticket en la base de datos") [cite: 97]