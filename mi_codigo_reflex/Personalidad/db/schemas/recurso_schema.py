from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RecursoBase(BaseModel):
    nombre: str
    tipo: str
    url: str
    categoria: str

class RecursoCreate(RecursoBase):
    pass

class RecursoRead(RecursoBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True

def recurso_schema(recurso) -> dict:
    if not recurso: return {}
    return {
        "id": recurso.id,
        "nombre": recurso.nombre,
        "tipo": recurso.tipo,
        "url": recurso.url,
        "categoria": recurso.categoria,
        "fecha": recurso.fecha.isoformat() if recurso.fecha else None
    }
