import json
import os
import psycopg2
import bcrypt

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_PERSONALIDAD_JSON = os.path.join(BASE_DIR, "data", "Personalidad.users.json")
PLATAFORMAS_JSON = os.path.join(BASE_DIR, "data", "usuarios_metodos.usuarios_plataformas.json")

# Configuración DB
DB_CONFIG = {
    "dbname": "db_personalidad_proyecto",
    "user": "postgres",
    "password": "Prefor2026!",
    "host": "localhost",
    "port": "5432"
}

def crear_claudia():
    print("--- INICIANDO CREACIÓN/ACTUALIZACIÓN DE CLAUDIA ---")
    
    # 1. Obtener datos de Claudia desde Personalidad.users.json
    claudia_data = None
    if os.path.exists(USERS_PERSONALIDAD_JSON):
        with open(USERS_PERSONALIDAD_JSON, 'r', encoding='utf-8') as f:
            users = json.load(f)
            for u in users:
                if u.get("email") == "claudia@academiametodos.com":
                    claudia_data = u
                    break
    
    if not claudia_data:
        print("ERROR: No se encontró a Claudia en Personalidad.users.json")
        claudia_data = {
            "email": "claudia@academiametodos.com",
            "password": "ATC4IWR",
            "disabled": False,
            "full_name": "Claudia Antequera",
            "count_login": 0,
            "are_terms_accepted": True,
            "is_optional_checked": True,
            "rol": "admin"
        }
    
    # 2. Encriptar contraseña
    raw_password = claudia_data.get("password", "ATC4IWR")
    hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print(f"Contraseña encriptada para Claudia.")

    # 3. Preparar el objeto para usuarios_plataformas.json
    claudia_final = {
        "email": claudia_data["email"],
        "password": hashed_password,
        "nombre": "Claudia",
        "apellidos": "Antequera",
        "dni": "32132321a",
        "disabled": claudia_data.get("disabled", False),
        "count_login": claudia_data.get("count_login", 0),
        "are_terms_accepted": True,
        "is_optional_checked": True,
        "rol": "admin",
        "hasta_personalidad": "2026-12-31 23:59:59",
        "hasta_fisicas": "2026-12-31 23:59:59",
        "disabled_personalidad": False,
        "disabled_fisicas": False
    }

    # 4. Actualizar JSON
    if os.path.exists(PLATAFORMAS_JSON):
        with open(PLATAFORMAS_JSON, 'r', encoding='utf-8') as f:
            plataformas_users = json.load(f)
            
        found = False
        for i, u in enumerate(plataformas_users):
            if u.get("email") == "claudia@academiametodos.com":
                plataformas_users[i].update(claudia_final)
                found = True
                break
        
        if not found:
            plataformas_users.append(claudia_final)
            
        with open(PLATAFORMAS_JSON, 'w', encoding='utf-8') as f:
            json.dump(plataformas_users, f, indent=2, ensure_ascii=False)
        print("JSON de plataformas actualizado.")

    # 5. Actualizar Base de Datos
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Asegurar columnas (incluyendo las nuevas)
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='usuarios_plataformas' AND column_name='hasta_personalidad'")
        if not cur.fetchone():
            print("Añadiendo nuevas columnas a la BD...")
            cur.execute("ALTER TABLE usuarios_metodos.usuarios_plataformas ADD COLUMN IF NOT EXISTS hasta_personalidad TIMESTAMP;")
            cur.execute("ALTER TABLE usuarios_metodos.usuarios_plataformas ADD COLUMN IF NOT EXISTS hasta_fisicas TIMESTAMP;")
            cur.execute("ALTER TABLE usuarios_metodos.usuarios_plataformas ADD COLUMN IF NOT EXISTS disabled_personalidad BOOLEAN DEFAULT FALSE;")
            cur.execute("ALTER TABLE usuarios_metodos.usuarios_plataformas ADD COLUMN IF NOT EXISTS disabled_fisicas BOOLEAN DEFAULT FALSE;")

        # Actualizar o Insertar (usando email como búsqueda)
        cur.execute("SELECT email FROM usuarios_metodos.usuarios_plataformas WHERE email = %s", (claudia_final["email"],))
        if cur.fetchone():
            print("Actualizando Claudia en la BD...")
            cur.execute("""
                UPDATE usuarios_metodos.usuarios_plataformas 
                SET password = %s, rol = %s, hasta_personalidad = %s, hasta_fisicas = %s, 
                    disabled_personalidad = %s, disabled_fisicas = %s, are_terms_accepted = %s, is_optional_checked = %s,
                    nombre = %s, apellidos = %s, dni = %s, disabled = %s
                WHERE email = %s
            """, (
                claudia_final["password"], claudia_final["rol"], claudia_final["hasta_personalidad"], 
                claudia_final["hasta_fisicas"], claudia_final["disabled_personalidad"], 
                claudia_final["disabled_fisicas"], claudia_final["are_terms_accepted"],
                claudia_final["is_optional_checked"], claudia_final["nombre"], claudia_final["apellidos"],
                claudia_final["dni"], claudia_final["disabled"], claudia_final["email"]
            ))
        else:
            print("Insertando Claudia en la BD...")
            cur.execute("""
                INSERT INTO usuarios_metodos.usuarios_plataformas 
                (email, password, nombre, apellidos, dni, rol, hasta_personalidad, hasta_fisicas, disabled_personalidad, disabled_fisicas, are_terms_accepted, is_optional_checked, disabled)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                claudia_final["email"], claudia_final["password"], claudia_final["nombre"], claudia_final["apellidos"],
                claudia_final["dni"], claudia_final["rol"], claudia_final["hasta_personalidad"], claudia_final["hasta_fisicas"],
                claudia_final["disabled_personalidad"], claudia_final["disabled_fisicas"], 
                claudia_final["are_terms_accepted"], claudia_final["is_optional_checked"], claudia_final["disabled"]
            ))
        
        conn.commit()
        cur.close()
        conn.close()
        print("Base de datos actualizada con éxito.")
    except Exception as e:
        print(f"Error actualizando BD: {e}")

if __name__ == "__main__":
    crear_claudia()
