from pydantic import BaseModel, validator
from typing import Optional, Any

class HistorialSimplificadoCreate(BaseModel):
    """
    El 'Portero de Discoteca':
    Filtra los datos antes de guardarlos. Si el frontend intenta enviar un ID falso
    o un resultado que no sea texto, este archivo lo bloquea y lanza un error.
    """
    id: Optional[str] = None  # <-- CAMBIO REALIZADO AQUÍ: Ahora es opcional
    user_id: str
    simulacro_code: str
    resultado: str

    @validator('resultado')
    def validar_resultado(cls, v):
        if not isinstance(v, str):
            raise ValueError("El resultado debe ser de tipo texto")
        v_upper = v.upper()
        if v_upper not in ['APTO', 'NO APTO']:
            raise ValueError("El resultado debe ser exactamente 'APTO' o 'NO APTO'")
        return v_upper

class Response(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

db/models

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
import uuid
Base = declarative_base()
class HistorialSimplificado(Base):
    """
    Funcionamiento: Le dice a SQL que cree una tabla aislada con 4 columnas exactas:
    id, user_id, simulacro_code, resultado y fecha (automática).
    """
    __tablename__ = "historial_simplificado"
   
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    simulacro_code = Column(String, nullable=False)  # ej: 'FISC-01'
    resultado = Column(String, nullable=False)       # 'APTO' o 'NO APTO'
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
