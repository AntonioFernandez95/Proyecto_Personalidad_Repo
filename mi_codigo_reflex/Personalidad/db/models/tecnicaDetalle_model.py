from sqlalchemy import Column, String, Integer, JSON
from Personalidad.db.models.historialSimplificado_model import Base

class TecnicaDetalle(Base):
    __tablename__ = "tecnicas_data"
    __table_args__ = {'schema': 'tecnicas'}

    id = Column(String, primary_key=True, index=True) # ej: 'flexiones'
    titulo = Column(String, nullable=False)
    posicion_inicial = Column(String)
    # Importador.py los guarda como TEXT (con json.dumps), así que podemos usar String o JSON
    ejecucion = Column(String) 
    normas = Column(String)
    tiempo = Column(String)
    intentos = Column(String)