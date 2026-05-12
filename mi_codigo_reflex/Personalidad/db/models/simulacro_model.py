from sqlalchemy import Column, String, Integer, DateTime
import datetime
from Personalidad.db.models.historialSimplificado_model import Base

class Simulacro(Base):
    """Modelo para la tabla de simulacros presenciales."""
    __tablename__ = "simulacros"
    __table_args__ = {"schema": "recursos"}
   
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False, default="PRÓXIMA CONVOCATORIA")
    fecha = Column(String, nullable=False) # Guardamos como string para flexibilidad (ej: "25 de Abril, 2026")
    ubicacion = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)
