import os
import psycopg2
import bcrypt
from datetime import datetime, timedelta

# Leer configuración centralizada de entorno
DB_NAME = os.getenv("DB_NAME", "db_personalidad_proyecto")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Prefor2026!")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

def crear_usuario():
    email = "alejandragarzon.24@campuscamara.es"
    nombre = "Alejandra"
    apellidos = "Garzón"
    password_plano = "Alejandra2026!"
    
    # Encriptar contraseña con bcrypt
    hashed_password = bcrypt.hashpw(password_plano.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Fechas de inicio y vencimiento (1 año de acceso)
    ahora = datetime.now()
    un_ano = ahora + timedelta(days=365)
    
    print(f"--- CREANDO USUARIO MANUAL: {email} ---")
    
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        
        # Eliminar si ya existe para evitar duplicidad
        cur.execute("DELETE FROM usuarios_metodos.usuarios_plataformas WHERE email = %s", (email,))
        
        # Insertar nuevo usuario
        cur.execute("""
            INSERT INTO usuarios_metodos.usuarios_plataformas 
            (email, password, nombre, apellidos, dni, rol, desde, hasta, hasta_personalidad, hasta_fisicas, disabled_personalidad, disabled_fisicas, are_terms_accepted, is_optional_checked, disabled, count_login)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            email,
            hashed_password,
            nombre,
            apellidos,
            "12345678X",
            "admin",
            ahora,
            un_ano,
            un_ano,
            un_ano,
            False,
            False,
            True,
            True,
            False,
            0
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"\n[ÉXITO] Usuario {email} creado correctamente.")
        print(f"-> Contraseña asignada: {password_plano}")
        print(f"-> Acceso activo hasta: {un_ano.strftime('%Y-%m-%d')}")
        
    except Exception as e:
        print(f"\n[ERROR] No se pudo crear el usuario: {e}")

if __name__ == "__main__":
    crear_usuario()
