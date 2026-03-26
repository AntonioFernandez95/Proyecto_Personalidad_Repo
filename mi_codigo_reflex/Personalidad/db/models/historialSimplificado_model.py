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
    resultado = Column(String, nullable=False)       # 'APTO' o 'NO APTO' (para compatibilidad)
    
    # Nuevas Columnas Estructuradas
    gender = Column(String, nullable=True)
    flexiones = Column(String, nullable=True)
    plancha_seg = Column(String, nullable=True)
    km2000 = Column(String, nullable=True)
    agilidad_seg = Column(String, nullable=True)
    porcentaje = Column(String, nullable=True)
    
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
