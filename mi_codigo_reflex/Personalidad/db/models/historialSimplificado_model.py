from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
import datetime
import uuid
Base = declarative_base()
class HistorialSimplificado(Base):
    """
    Funcionamiento: Le dice a SQL que cree una tabla aislada dentro del esquema historial_simplificado.
    """
    __tablename__ = "registros_calculadora_fisicas"
    __table_args__ = {"schema": "historial_simplificado"}
   
    token_simulacro = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    propietario_id = Column(String, nullable=False)
    simulacro_code = Column(String, nullable=False)  # ej: 'FISC-01'
    resultado = Column(String, nullable=False)       # 'APTO' o 'NO APTO' (para compatibilidad)
    
    # Nuevas Columnas Estructuradas con tipos numéricos
    gender = Column(String, nullable=True)
    flexiones = Column(Integer, nullable=True)
    plancha_seg = Column(Integer, nullable=True)
    km2000 = Column(Integer, nullable=True)  # Guardado como segundos totales
    agilidad_seg = Column(Float, nullable=True)
    porcentaje = Column(String, nullable=True)
    
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
