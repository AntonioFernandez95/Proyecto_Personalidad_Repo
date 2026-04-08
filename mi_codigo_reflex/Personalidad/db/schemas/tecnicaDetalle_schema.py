from pydantic import BaseModel
from typing import List, Optional

class TecnicaDetalleBase(BaseModel):
    id: str
    titulo: str
    posicion_inicial: str
    ejecucion: List[str]
    normas: List[str]
    tiempo: str
    intentos: str

class TecnicaDetalleRead(TecnicaDetalleBase):
    class Config:
        from_attributes = True