from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from .models.historialSimplificado_model import HistorialSimplificado, Base
from .schemas.historialSimplificado_schema import HistorialSimplificadoCreate
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
# "Le dice a SQL que cree una tabla aislada con 4 columnas exactas"
# Esto crea la tabla en la base de datos si no existe
try:
    Base.metadata.create_all(bind=engine)
except Exception:
    # Ignoramos fallos durante el build; las tablas se crearán al arrancar el contenedor
    pass
def guardar_historial_ligero(data_validada: HistorialSimplificadoCreate):
    """
    Funcionamiento: Recibe los datos validados del schema y ejecuta el INSERT real
    en la base de datos a través de SQLAlchemy.
    """
    db = SessionLocal()
    try:
        nuevo_historial = HistorialSimplificado(
            id=data_validada.id,
            user_id=data_validada.user_id,
            simulacro_code=data_validada.simulacro_code,
            resultado=data_validada.resultado
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
    Funcionamiento: Consulta todos los registros de la tabla historial_simplificado
    para un usuario específico.
    """
    db = SessionLocal()
    try:
        return db.query(HistorialSimplificado).filter(HistorialSimplificado.user_id == user_id).order_by(HistorialSimplificado.fecha.desc()).all()
    except Exception as e:
        print(f"Error al consultar historial: {e}")
        return []
    finally:
        db.close()
