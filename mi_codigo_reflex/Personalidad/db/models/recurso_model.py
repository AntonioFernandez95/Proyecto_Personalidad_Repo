from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Video(Base):
    """Modelo para la tabla de vídeos en el esquema recursos."""
    __tablename__ = "videos"
    __table_args__ = {"schema": "recursos"}
   
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    url = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)

class PDF(Base):
    """Modelo para la tabla de PDFs en el esquema recursos."""
    __tablename__ = "pdfs"
    __table_args__ = {"schema": "recursos"}
   
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    url = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
