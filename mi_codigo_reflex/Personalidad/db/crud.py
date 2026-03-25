from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from .models.historial_model import HistorialSimplificado, Base
from .schemas.historial_schema import HistorialSimplificadoCreate


# Configuramos SQLAlchemy para conectarse a Postgres (usando las credenciales actuales)
DB_NAME = os.getenv("DB_NAME", "db_personalidad_proyecto")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Prefor2026!")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")


# String de conexión a postgres (requiere psycopg2-binary o psycopg2 ya instalado)
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def guardar_historial_ligero(data_validada: HistorialSimplificadoCreate):
    """
    Capa de Datos (Punto 2C).
    Ejecuta el INSERT real en la base de datos a través de SQLAlchemy.
    """
    # Creamos la tabla si no existe (al ser llamado en ejecución, ya habrá conexión)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        nuevo_historial = HistorialSimplificado(
            id=data_validada.id,
            user_id=data_validada.user_id,
            simulacro_code=data_validada.simulacro_code,
            resultado=data_validada.resultado,
            porcentaje=data_validada.porcentaje
            # "fecha" se autocompleta por el modelo
        )
        db.add(nuevo_historial)
        db.commit()
        db.refresh(nuevo_historial)
        return nuevo_historial
    except Exception as e:
        db.rollback()
        print(f"Error al guardar historial ligero: {e}")
        raise e
    finally:
        db.close()


def consultar_historial_usuario(user_id: str):
    """
    Capa de Datos.
    Consulta todos los tickets del historial para un usuario específico.
    """
    db = SessionLocal()
    try:
        # Consultamos ordenando por fecha descendente (más nuevos primero)
        registros = db.query(HistorialSimplificado).filter(
            HistorialSimplificado.user_id == user_id
        ).order_by(HistorialSimplificado.fecha.desc()).all()
        return registros
    except Exception as e:
        print(f"Error al consultar historial: {e}")
        return []
    finally:
        db.close()
