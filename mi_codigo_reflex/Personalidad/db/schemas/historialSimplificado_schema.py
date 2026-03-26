from pydantic import BaseModel, validator
from typing import Optional, Any

class HistorialSimplificadoCreate(BaseModel):
    """
    Schema para crear un registro en el historial con todos los campos detallados.
    """
    id: Optional[str] = None
    user_id: str
    simulacro_code: str
    resultado: str
    
    # Nuevos campos individuales
    gender: Optional[str] = None
    flexiones: Optional[str] = None
    plancha_seg: Optional[str] = None
    km2000: Optional[str] = None
    agilidad_seg: Optional[str] = None
    porcentaje: Optional[str] = None

class Response(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
