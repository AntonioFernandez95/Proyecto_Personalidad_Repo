from pydantic import BaseModel, validator
from typing import Optional, Any

class HistorialSimplificadoCreate(BaseModel):
    """
    Schema para crear un registro en el historial con todos los campos detallados.
    """
    token_simulacro: Optional[str] = None
    propietario_id: str
    simulacro_code: str
    resultado: str
    
    # Nuevos campos individuales con tipos corregidos
    gender: Optional[str] = None
    flexiones: Optional[int] = None
    plancha_seg: Optional[int] = None
    km2000: Optional[int] = None  # Segundos totales
    agilidad_seg: Optional[float] = None
    porcentaje: Optional[str] = None

class Response(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
