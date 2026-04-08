from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
import json
# Mantenemos tus imports y añadimos el nuevo modelo
from Personalidad.db.models.historialSimplificado_model import HistorialSimplificado, Base
from Personalidad.db.models.tecnicaDetalle_model import TecnicaDetalle  # <--- NUEVO
from Personalidad.db.schemas.historialSimplificado_schema import HistorialSimplificadoCreate

# Tu configuración de conexión (IDÉNTICA)
DB_NAME = os.getenv("DB_NAME", "db_personalidad_proyecto")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Prefor2026!")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esto ahora creará AMBAS tablas (Historial y Técnicas)
try:
    Base.metadata.create_all(bind=engine)
except Exception:
    pass

# --- TUS FUNCIONES DE SIEMPRE (No tocamos nada) ---
def guardar_historial_ligero(data_validada: HistorialSimplificadoCreate):
    db = SessionLocal()
    try:
        nuevo_historial = HistorialSimplificado(
            id=data_validada.id,
            user_id=data_validada.user_id,
            simulacro_code=data_validada.simulacro_code,
            resultado=data_validada.resultado,
            gender=data_validada.gender,
            flexiones=data_validada.flexiones,
            plancha_seg=data_validada.plancha_seg,
            km2000=data_validada.km2000,
            agilidad_seg=data_validada.agilidad_seg,
            porcentaje=data_validada.porcentaje
        )
        db.add(nuevo_historial)
        db.commit()
        db.refresh(nuevo_historial)
        return nuevo_historial
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def consultar_historial_usuario(user_id: str):
    db = SessionLocal()
    try:
        return db.query(HistorialSimplificado).filter(HistorialSimplificado.user_id == user_id).order_by(HistorialSimplificado.fecha.desc()).all()
    except Exception as e:
        return []
    finally:
        db.close()

# --- NUEVA FUNCIÓN PARA TÉCNICAS (Respetando tu estilo) ---
def obtener_tecnica_por_id(prueba_id: str):
    """Consulta la base de datos para traer los textos de una prueba técnica"""
    db = SessionLocal()
    try:
        return db.query(TecnicaDetalle).filter(TecnicaDetalle.id == prueba_id).first()
    finally:
        db.close()

