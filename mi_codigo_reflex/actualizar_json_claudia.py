import json
import os
import bcrypt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "data", "usuarios_metodos.usuarios_plataformas.json")

def actualizar():
    print("--- ACTUALIZANDO CONTRASEÑA EN usuarios_metodos.usuarios_plataformas.json ---")
    
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        users = json.load(f)

    updated = False
    for u in users:
        if u.get("email") == "claudia@academiametodos.com":
            # Forzamos la contraseña en texto plano
            raw_password = "ATC4IWR"
            hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            u["password"] = hashed
            print(f"Contraseña encriptada: {hashed}")
            updated = True
            break

    if updated:
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        print("JSON guardado correctamente.")
    else:
        print("No se realizaron cambios.")

if __name__ == "__main__":
    actualizar()
