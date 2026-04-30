from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
import datetime
import uuid

Base = declarative_base()

class HistorialFisicas(Base):
    """Modelo para la tabla 'fisicas' en el esquema 'historial_simplificado'."""
    __tablename__ = "fisicas"
    __table_args__ = {"schema": "historial_simplificado"}
   
    token_simulacro = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    propietario_id = Column(String, nullable=False)
    simulacro_code = Column(String, nullable=True, default="FISC-01")
    resultado = Column(String, nullable=False)       # 'APTO' o 'NO APTO'
    gender = Column(String, nullable=True)
    flexiones = Column(Integer, nullable=True)
    plancha_seg = Column(Integer, nullable=True)
    km2000 = Column(Integer, nullable=True)
    agilidad_seg = Column(Float, nullable=True)
    porcentaje = Column(String, nullable=True)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)

class HistorialPersonalidad(Base):
    """Modelo para la tabla 'personalidad' en el esquema 'historial_simplificado'."""
    __tablename__ = "personalidad"
    __table_args__ = {"schema": "historial_simplificado"}
   
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    sinceridad = Column(Integer, nullable=True)
    extraversion = Column(Integer, nullable=True)
    neuroticismo = Column(Integer, nullable=True)
    psicoticismo = Column(Integer, nullable=True)
    es_apto = Column(String, nullable=True)          # 'APTO' o 'NO APTO'
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
