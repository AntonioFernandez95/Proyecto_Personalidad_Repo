from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
import json
from Personalidad.db.models.historialSimplificado_model import HistorialFisicas, HistorialPersonalidad, Base


# Configuración de conexión
DB_NAME = os.getenv("DB_NAME", "db_personalidad_proyecto")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Prefor2026!")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Inicialización de esquemas
try:
    from sqlalchemy import text
    from Personalidad.db.models.recurso_model import Video, PDF
    from Personalidad.db.models.aptitud_model import AptitudModel
    from Personalidad.db.models.tecnicaDetalle_model import TecnicaDetalle
    from Personalidad.db.models.simulacro_model import Simulacro
   
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS historial_simplificado"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS recursos"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS tecnicas"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS personalidad"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS usuarios_metodos"))
        conn.commit()
   
    # Esta llamada creará todas las tablas de los modelos importados si no existen
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error inicializando esquemas: {e}")
    pass


# --- HISTORIAL ---
def guardar_historial_fisico(user_id: str, gender: str, flexiones: int, plancha: int, km2000: int, agilidad: float, resultado: str, porcentaje: str):
    with Session(engine) as session:
        try:
            nuevo = HistorialFisicas(
                propietario_id=user_id,
                gender=gender,
                flexiones=flexiones,
                plancha_seg=plancha,
                km2000=km2000,
                agilidad_seg=agilidad,
                resultado=resultado,
                porcentaje=porcentaje
            )
            session.add(nuevo)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error guardando historial físico: {e}")
            return False


def guardar_historial_personalidad(user_id: str, sinceridad: int, extraversion: int, neuroticismo: int, psicoticismo: int, es_apto: str):
    with Session(engine) as session:
        try:
            nuevo = HistorialPersonalidad(
                user_id=user_id,
                sinceridad=sinceridad,
                extraversion=extraversion,
                neuroticismo=neuroticismo,
                psicoticismo=psicoticismo,
                es_apto=es_apto
            )
            session.add(nuevo)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error guardando historial personalidad: {e}")
            return False


def consultar_historial_completo(user_id: str):
    with Session(engine) as session:
        try:
            # Forzamos una limpieza de sesión para ver datos frescos
            session.expire_all()
           
            fisicas = session.query(HistorialFisicas).filter(HistorialFisicas.propietario_id == user_id).all()
           
            from Personalidad.db.models.aptitud_model import AptitudModel
            aptitudes = session.query(AptitudModel).filter(AptitudModel.user_id == user_id).all()
           
            historial = []
            # Mapeo de Físicas
            for f in fisicas:
                carrera_str = "-"
                if f.km2000:
                    mins = f.km2000 // 60
                    secs = f.km2000 % 60
                    carrera_str = f"{mins:02d}:{secs:02d}"


                # Lógica de baremo para colores individuales
                g = f.gender.lower() if f.gender else "male"
                if g == "female":
                    t_flex, t_plan, t_agil, t_carr = 12, 40, 27.0, 780
                else:
                    t_flex, t_plan, t_agil, t_carr = 17, 60, 25.0, 660


                historial.append({
                    "fecha": f.fecha.strftime("%Y-%m-%d %H:%M"),
                    "tipo": "FÍSICAS",
                    "gender": f.gender,
                    "flexiones": str(f.flexiones),
                    "plancha": str(f.plancha_seg),
                    "km2000": carrera_str,
                    "agilidad": str(f.agilidad_seg),
                    "resultado": f.resultado,
                    "porcentaje": f.porcentaje,
                    "flex_ok": (f.flexiones if f.flexiones else 0) >= t_flex,
                    "plan_ok": (f.plancha_seg if f.plancha_seg else 0) >= t_plan,
                    "agil_ok": (f.agilidad_seg if f.agilidad_seg else 999) <= t_agil,
                    "carr_ok": (f.km2000 if f.km2000 else 9999) <= t_carr
                })
           
            # Mapeo de Aptitudes (Personalidad Detallada)
            for a in aptitudes:
                historial.append({
                    "fecha": a.fecha.strftime("%Y-%m-%d %H:%M"),
                    "tipo": "PERSONALIDAD",
                    "sinceridad": a.sinceridad,
                    "extraversion": a.extraversion,
                    "depresion": a.depresion,
                    "neuroticismo": a.neuroticismo,
                    "psicoticismo": a.psicoticismo,
                    "paranoidismo": a.paranoidismo,
                    "desviacion_psicopatica": a.desviacion_psicopatica,
                    "resultado": a.es_apto,
                    "color": "#e53e3e" if a.es_apto == "NO APTO" else "#28a745",
                    "flex_ok": True, "plan_ok": True, "agil_ok": True, "carr_ok": True # Visuales para la tabla unificada
                })
               
            historial.sort(key=lambda x: x["fecha"], reverse=True)
            return historial
        except Exception as e:
            print(f"Error consultando historial: {e}")
            return []


# --- TÉCNICAS (Textos descriptivos) ---
def obtener_tecnica_por_id(prueba_id: str):
    from Personalidad.db.models.tecnicaDetalle_model import TecnicaDetalle
    with Session(engine) as session:
        return session.query(TecnicaDetalle).filter(TecnicaDetalle.id == prueba_id).first()


def guardar_video(nombre: str, url: str, categoria: str):
    from Personalidad.db.models.recurso_model import Video
    with Session(engine) as session:
        nuevo = Video(nombre=nombre, url=url, categoria=categoria)
        session.add(nuevo)
        session.commit()


def guardar_aptitudes(user_id: str, sinceridad: int, extraversion: int, depresion: int,
                      neuroticismo: int, psicoticismo: int, paranoidismo: int,
                      desviacion_psicopatica: int, es_apto: str):
    from Personalidad.db.models.aptitud_model import AptitudModel
    import uuid
    with Session(engine) as session:
        nueva_entrada = AptitudModel(
            id=str(uuid.uuid4()),
            user_id=user_id,
            sinceridad=sinceridad,
            extraversion=extraversion,
            depresion=depresion,
            neuroticismo=neuroticismo,
            psicoticismo=psicoticismo,
            paranoidismo=paranoidismo,
            desviacion_psicopatica=desviacion_psicopatica,
            es_apto=es_apto
        )
        session.add(nueva_entrada)
        session.commit()


def guardar_pdf(nombre: str, url: str, categoria: str):
    from Personalidad.db.models.recurso_model import PDF
    with Session(engine) as session:
        nuevo = PDF(nombre=nombre, url=url, categoria=categoria)
        session.add(nuevo)
        session.commit()


def obtener_recursos_combinados():
    from Personalidad.db.models.recurso_model import Video, PDF
    with Session(engine) as session:
        videos = session.query(Video).all()
        pdfs = session.query(PDF).all()
       
        resultado = []
        for v in videos:
            resultado.append({"id": v.id, "nombre": v.nombre, "url": v.url, "categoria": v.categoria, "tipo": "video", "fecha": v.fecha})
        for p in pdfs:
            resultado.append({"id": p.id, "nombre": p.nombre, "url": p.url, "categoria": p.categoria, "tipo": "pdf", "fecha": p.fecha})
        return resultado


def eliminar_recurso_por_tipo(recurso_id: int, tipo: str):
    from Personalidad.db.models.recurso_model import Video, PDF
    with Session(engine) as session:
        if tipo == "video":
            item = session.query(Video).filter(Video.id == recurso_id).first()
        else:
            item = session.query(PDF).filter(PDF.id == recurso_id).first()
           
        if item:
            session.delete(item)
            session.commit()
            return True
    return False


def obtener_recursos_por_categoria_y_tipo(categoria: str, tipo: str):
    from Personalidad.db.models.recurso_model import Video, PDF
    with Session(engine) as session:
        if tipo == "video":
            return session.query(Video).filter(Video.categoria == categoria).all()
        else:
            return session.query(PDF).filter(PDF.categoria == categoria).all()


def obtener_recursos_por_categoria(categoria: str):
    from Personalidad.db.models.recurso_model import Video, PDF
    with Session(engine) as session:
        videos = session.query(Video).filter(Video.categoria == categoria).all()
        pdfs = session.query(PDF).filter(PDF.categoria == categoria).all()
        return videos + pdfs


# --- SIMULACROS ---
def obtener_simulacros():
    from Personalidad.db.models.simulacro_model import Simulacro
    with Session(engine) as session:
        return session.query(Simulacro).order_by(Simulacro.fecha_creacion.desc()).all()


def obtener_simulacro_por_id(id: int):
    from Personalidad.db.models.simulacro_model import Simulacro
    with Session(engine) as session:
        return session.query(Simulacro).filter(Simulacro.id == id).first()


def guardar_simulacro(fecha: str, ubicacion: str, descripcion: str, titulo: str = "PRÓXIMA CONVOCATORIA"):
    from Personalidad.db.models.simulacro_model import Simulacro
    with Session(engine) as session:
        nuevo = Simulacro(titulo=titulo, fecha=fecha, ubicacion=ubicacion, descripcion=descripcion)
        session.add(nuevo)
        session.commit()
        return nuevo.id


def actualizar_simulacro(id: int, fecha: str, ubicacion: str, descripcion: str, titulo: str):
    from Personalidad.db.models.simulacro_model import Simulacro
    with Session(engine) as session:
        item = session.query(Simulacro).filter(Simulacro.id == id).first()
        if item:
            item.fecha = fecha
            item.ubicacion = ubicacion
            item.descripcion = descripcion
            item.titulo = titulo
            session.commit()
            return True
    return False


def eliminar_simulacro(id: int):
    from Personalidad.db.models.simulacro_model import Simulacro
    with Session(engine) as session:
        item = session.query(Simulacro).filter(Simulacro.id == id).first()
        if item:
            session.delete(item)
            session.commit()
            return True
    return False

def upsert_simulacro(id: int = None, titulo: str = "", fecha: str = "", ubicacion: str = "", descripcion: str = "", url_reserva: str = ""):
    from Personalidad.db.models.simulacro_model import Simulacro
    with Session(engine) as session:
        if id:
            item = session.query(Simulacro).filter(Simulacro.id == id).first()
            if item:
                item.titulo = titulo
                item.fecha = fecha
                item.ubicacion = ubicacion
                item.descripcion = descripcion
                item.url_reserva = url_reserva
                session.commit()
                return item.id
        
        # Si no hay ID o no se encontró, creamos uno nuevo
        nuevo = Simulacro(titulo=titulo, fecha=fecha, ubicacion=ubicacion, descripcion=descripcion, url_reserva=url_reserva)
        session.add(nuevo)
        session.commit()
        return nuevo.id
