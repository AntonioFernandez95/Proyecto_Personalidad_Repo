import reflex as rx
from sqlalchemy import Column, String, Integer, DateTime, func
from Personalidad.db.models.historialSimplificado_model import Base

class AptitudModel(Base):
    __tablename__ = "aptitudes"
    __table_args__ = {'schema': 'personalidad'}

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    sinceridad = Column(Integer)
    extraversion = Column(Integer)
    depresion = Column(Integer)
    neuroticismo = Column(Integer)
    psicoticismo = Column(Integer)
    paranoidismo = Column(Integer)
    desviacion_psicopatica = Column(Integer)
    es_apto = Column(String)
    fecha = Column(DateTime, server_default=func.now())
