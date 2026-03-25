from pydantic import BaseModel
from typing import Optional 

#*Modelo completo de la pregunta (Libre de MongoDB)*#
class PreguntaModel(BaseModel):
    id: Optional[str] = None  # Cambiamos _id y ObjectId por un id estándar de texto/número
    ITEM: int
    PREGUNTA: str
    SI: int
    MUCHAS_VECES: int
    ALGUNA_VEZ: int
    POCAS_VECES: int
    NO: int