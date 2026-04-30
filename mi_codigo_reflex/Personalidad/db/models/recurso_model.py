from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from Personalidad.db.models.historialSimplificado_model import Base

class Recurso(Base):
    __tablename__ = "recursos"
    __table_args__ = {'schema': 'tecnicas'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False) # 'video' o 'pdf'
    url = Column(String, nullable=False) # URL o ruta al archivo
    categoria = Column(String, nullable=False) # ej: 'flexiones', 'agilidad', etc.
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
