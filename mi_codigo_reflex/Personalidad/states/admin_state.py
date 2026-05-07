import reflex as rx
from typing import List, Dict, Any
from datetime import datetime, timedelta
from Personalidad.states.base_state import State
from Personalidad.db.client import db_client
from Personalidad.db.schemas.user_schema import users_schema, user_schema

class AdminState(State):
    """Estado para la gestión del panel de administración."""
    
    users: List[dict] = []
    selected_user: dict = {}
    search_query: str = ""
    filter_role: str = "todos"
    is_loading: bool = False
    
    new_name: str = ""
    new_email: str = ""
    days_to_add: str = "30"

    # --- CAMPOS PARA CREACIÓN DE USUARIOS ---
    create_name: str = ""
    create_email: str = ""
    create_role: str = "estudiante"
    create_has_personality: bool = True
    create_has_physical: bool = True

    # --- GESTIÓN DE RECURSOS ---
    recursos: List[dict] = []
    selected_categoria: str = "flexiones"
    categorias_disponibles: List[str] = ["flexiones", "plancha", "agilidad", "carrera", "planificacion"]
    system_status: Dict[str, bool] = {}
    
    def check_system_health(self):
        """Verifica la integridad de las tablas y esquemas."""
        from sqlalchemy import text
        from Personalidad.db.crud import engine
        
        tablas_a_verificar = [
            ("usuarios_metodos.usuarios_plataformas", "Usuarios"),
            ("historial_simplificado.fisicas", "Historial Físicas"),
            ("historial_simplificado.personalidad", "Historial Personalidad"),
            ("personalidad.aptitudes", "Aptitudes Detalladas"),
            ("recursos.videos", "Vídeos"),
            ("recursos.pdfs", "PDFs"),
            ("tecnicas.tecnicas_data", "Datos de Técnicas")
        ]
        
        status = {}
        with engine.connect() as conn:
            for tabla_full, nombre_amigable in tablas_a_verificar:
                try:
                    conn.execute(text(f"SELECT 1 FROM {tabla_full} LIMIT 1"))
                    status[nombre_amigable] = True
                except Exception:
                    status[nombre_amigable] = False
        
        self.system_status = status

    def fetch_recursos(self):
        """Obtiene todos los recursos combinados (vídeos y PDFs)."""
        from Personalidad.db.crud import obtener_recursos_combinados
        try:
            # Ahora la función unificada ya nos da el formato correcto
            self.recursos = obtener_recursos_combinados()
        except Exception as e:
            print(f"Error cargando recursos: {e}")
            self.recursos = []

    def sync_recursos_to_json(self):
        """Exporta la lista actual de recursos de la BD a archivos JSON locales (separados)."""
        import json
        import os
        try:
            video_path = os.path.join("data", "recursos_videos.json")
            pdf_path = os.path.join("data", "recursos_pdfs.json")
            
            videos_json = []
            pdfs_json = []
            
            for r in self.recursos:
                item = r.copy()
                val_fecha = item.get("fecha")
                if val_fecha and isinstance(val_fecha, datetime):
                    item["fecha"] = val_fecha.isoformat()
                
                if item.get("tipo") == "video":
                    videos_json.append(item)
                elif item.get("tipo") == "pdf":
                    pdfs_json.append(item)
                
            with open(video_path, "w", encoding="utf-8") as f:
                json.dump(videos_json, f, indent=2, ensure_ascii=False)
            with open(pdf_path, "w", encoding="utf-8") as f:
                json.dump(pdfs_json, f, indent=2, ensure_ascii=False)
                
            print(f"Sincronizados recursos a JSON (videos y pdfs).")
        except Exception as e:
            print(f"Error sincronizando recursos a JSON: {e}")

    def sync_users_to_json(self):
        """Exporta la lista completa de usuarios de la BD al archivo JSON local para persistencia en Docker."""
        import json
        import os
        from datetime import datetime
        try:
            json_path = os.path.join("data", "usuarios_metodos.usuarios_plataformas.json")
            
            # Obtenemos todos los usuarios directamente de la base de datos para asegurar fidelidad
            raw_users = db_client.find_all("usuarios_plataformas")
            
            json_ready_users = []
            for user in raw_users:
                item = user.copy()
                # Convertimos campos de fecha a formato ISO string
                for date_field in ["desde", "hasta", "hasta_personalidad", "hasta_fisicas"]:
                    val = item.get(date_field)
                    if val and isinstance(val, datetime):
                        item[date_field] = val.isoformat()
                
                # Eliminar campos internos de Postgres si existen
                item.pop("id", None)
                json_ready_users.append(item)
                
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_ready_users, f, indent=2, ensure_ascii=False)
            
            print(f"Sincronizados {len(json_ready_users)} usuarios a JSON correctamente.")
        except Exception as e:
            print(f"Error sincronizando usuarios a JSON: {e}")

    async def handle_upload(self, files: List[rx.UploadFile]):
        """Sube archivos a assets/uploads y los registra en la BD correspondiente."""
        import os
        from Personalidad.db.crud import guardar_video, guardar_pdf
        
        upload_dir = os.path.join("assets", "uploads")
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        for file in files:
            upload_data = await file.read()
            outfile = os.path.join(upload_dir, file.filename)
            with open(outfile, "wb") as f:
                f.write(upload_data)
            
            # Detectar tipo por extensión
            nombre_archivo = file.filename
            url_archivo = f"/uploads/{file.filename}"
            
            if nombre_archivo.lower().endswith(".pdf"):
                guardar_pdf(nombre=nombre_archivo, url=url_archivo, categoria=self.selected_categoria)
            else:
                # Todo lo que no sea PDF lo tratamos como vídeo por ahora
                guardar_video(nombre=nombre_archivo, url=url_archivo, categoria=self.selected_categoria)
        
        self.fetch_recursos()
        self.sync_recursos_to_json() # <--- Sincronizar con JSON local
        return rx.toast(f"Subidos {len(files)} archivos a {self.selected_categoria}.")

    def borrar_recurso(self, recurso: dict):
        """Elimina un recurso de su tabla y borra el archivo físico."""
        import os
        from Personalidad.db.crud import eliminar_recurso_por_tipo
        
        try:
            recurso_id = recurso.get("id")
            tipo = recurso.get("tipo") # "video" o "pdf"
            
            if eliminar_recurso_por_tipo(recurso_id, tipo):
                # Eliminar archivo físico
                path_relativo = recurso["url"].lstrip("/") # uploads/file.ext
                filepath = os.path.join("assets", path_relativo)
                if os.path.exists(filepath):
                    os.remove(filepath)
                
                self.fetch_recursos()
                self.sync_recursos_to_json() # <--- Sincronizar con JSON local
                return rx.toast("Recurso eliminado correctamente.")
        except Exception as e:
            return rx.window_alert(f"Error al borrar: {e}")

    def fetch_users(self):
        self.is_loading = True
        try:
            raw_users = db_client.find_all("usuarios_plataformas")
            # Ordenamos por email
            sorted_users = sorted(raw_users, key=lambda x: x.get("email", ""))
            # Mapeamos al schema
            all_users = users_schema(sorted_users)
            
            # FILTRO ESTRICTO: Solo mostramos estudiantes
            self.users = [u for u in all_users if u.get("rol") == "estudiante"]
                
        except Exception as e:
            print(f"Error cargando usuarios: {e}")
            self.users = []
        finally:
            self.is_loading = False

    def select_user(self, user: dict):
        from Personalidad.services.auth_service import search_user
        email = user.get("email")
        
        # 1. Sincronizamos caducidad (esto limpia flags en la BD)
        search_user("email", email)
        
        # 2. Leemos el usuario directamente de la base de datos (SIN usar la lista local que puede estar desactualizada)
        raw_user = db_client.find_one("usuarios_plataformas", "email", email)
        if not raw_user:
            return rx.window_alert("Error: No se ha encontrado el usuario en la base de datos.")
            
        # 3. Aplicamos el schema para tener los campos listos para la UI
        from Personalidad.db.schemas.user_schema import user_schema
        updated_user = user_schema(raw_user)
        
        # 4. Actualizamos el estado
        self.selected_user = updated_user
        self.new_name = updated_user.get("full_name", "")
        self.new_email = updated_user.get("email", "")
        self.days_to_add = "30"
        
        # Refrescamos la lista general también
        self.fetch_users()
        
        return rx.redirect("/academia/admin_plans")

    def guardar_perfil(self):
        """Actualiza el nombre y el email del usuario en la base de datos."""
        if not self.selected_user or not self.selected_user.get("email"):
            return rx.window_alert("No hay usuario seleccionado.")

        original_email = self.selected_user["email"]
        
        # Validaciones básicas
        if not self.new_name or not self.new_email:
            return rx.window_alert("El nombre y el email no pueden estar vacíos.")

        try:
            # Separamos nombre y apellidos (suponiendo primer espacio)
            partes = self.new_name.split(" ", 1)
            nombre = partes[0]
            apellidos = partes[1] if len(partes) > 1 else ""

            update_data = {
                "nombre": nombre,
                "apellidos": apellidos,
                "email": self.new_email
            }

            # Usamos el email original para encontrarlo y le aplicamos los cambios
            success = db_client.update_one(
                "usuarios_plataformas", "email", original_email, update_data
            )

            if success:
                # Actualizamos estado local
                new_selected = self.selected_user.copy()
                new_selected["full_name"] = self.new_name
                new_selected["email"] = self.new_email
                self.selected_user = new_selected
                self.fetch_users()
                self.sync_users_to_json() # <--- Persistir en JSON
                return rx.toast("Perfil actualizado correctamente.")
            else:
                return rx.window_alert("Error al actualizar la base de datos.")

        except Exception as e:
            return rx.window_alert(f"Error: {str(e)}")

    def alargar_vencimiento_plan(self, tipo_plan: str):
        if not self.selected_user or not self.selected_user.get("email"):
            return rx.window_alert("No hay usuario seleccionado.")

        try:
            days = int(self.days_to_add)
            email = self.selected_user["email"]
            col_fecha = f"hasta_{tipo_plan}"
            col_disabled = f"disabled_{tipo_plan}"
            
            raw_user = db_client.find_one("usuarios_plataformas", "email", email)
            # Buscamos la fecha actual (específica o genérica)
            fecha_actual = raw_user.get(col_fecha) or raw_user.get("hasta")
            if not fecha_actual or not isinstance(fecha_actual, datetime):
                fecha_actual = datetime.now()

            nueva_fecha = fecha_actual + timedelta(days=days)
            
            # Intentamos detectar si usamos columnas separadas o unificadas
            # IMPORTANTE: Ponemos 'disabled' en False también para evitar conflictos
            updates = {col_fecha: nueva_fecha, col_disabled: False, "disabled": False}
            success = db_client.update_one("usuarios_plataformas", "email", email, updates)
            
            if not success:
                # Reintento con columnas unificadas
                updates = {"hasta": nueva_fecha, "disabled": False}
                success = db_client.update_one("usuarios_plataformas", "email", email, updates)

            if success:
                new_selected = self.selected_user.copy()
                new_selected[col_fecha] = nueva_fecha.strftime("%Y-%m-%d")
                new_selected[col_disabled] = False # Reflejamos el alta inmediata
                self.selected_user = new_selected
                self.fetch_users()
                self.sync_users_to_json() # <--- Persistir en JSON
                return rx.toast(f"Plan {tipo_plan} extendido y activado.")
            
        except Exception as e:
            return rx.window_alert(f"Error: {str(e)}")

    def crear_usuario_manual(self):
        """Crea un nuevo usuario con contraseña aleatoria."""
        from Personalidad.services.auth_service import generate_random_password
        import bcrypt
        
        if not self.create_name or not self.create_email:
            return rx.window_alert("Nombre y Email son obligatorios.")
            
        # 1. Generar contraseña aleatoria
        temp_pass = generate_random_password(8)
        hashed_pass = bcrypt.hashpw(temp_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # 2. Preparar datos
        partes = self.create_name.split(" ", 1)
        nombre = partes[0]
        apellidos = partes[1] if len(partes) > 1 else ""
        
        try:
            # Comprobamos si ya existe
            existente = db_client.find_one("usuarios_plataformas", "email", self.create_email.lower().strip())
            if existente:
                return rx.window_alert("Este email ya está registrado.")

            # Inserción manual via SQL para asegurar todos los campos por defecto
            import psycopg2
            from Personalidad.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            cur = conn.cursor()
            
            sql = """
                INSERT INTO usuarios_metodos.usuarios_plataformas 
                (nombre, apellidos, email, password, rol, desde, hasta, 
                 count_login, are_terms_accepted, is_optional_checked, 
                 disabled_personalidad, disabled_fisicas) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                nombre, apellidos, self.create_email.lower().strip(), hashed_pass, self.create_role,
                datetime.now(), datetime.now() + timedelta(days=30),
                0, True, True, 
                not self.create_has_personality, not self.create_has_physical
            )
            
            cur.execute(sql, valores)
            conn.commit()
            conn.close()
            
            # 3. Enviar Email con credenciales
            from Personalidad.services.email_service import send_credentials_email
            email_enviado = send_credentials_email(self.create_email.lower().strip(), temp_pass)

            # Limpiar campos y refrescar
            self.create_name = ""
            self.create_email = ""
            self.fetch_users()
            self.sync_users_to_json() # <--- Sincronizar todo al JSON (incluyendo el nuevo usuario)
            
            if email_enviado:
                return rx.toast("¡Usuario creado y credenciales enviadas por email!")
            else:
                return rx.window_alert(f"Usuario creado, pero hubo un error al enviar el email.\n\nContraseña generada: {temp_pass}")

        except Exception as e:
            return rx.window_alert(f"Error al crear usuario: {str(e)}")

    def toggle_baja_plan(self, tipo_plan: str):
        if not self.selected_user or not self.selected_user.get("email"):
            return rx.window_alert("No hay usuario seleccionado.")

        email = self.selected_user["email"]
        col_disabled = f"disabled_{tipo_plan}"
        nuevo_estado = not self.selected_user.get(col_disabled, False)
        
        # Al activar (nuevo_estado = False), aseguramos que la columna general 'disabled' también sea False
        updates = {col_disabled: nuevo_estado}
        if not nuevo_estado:
            updates["disabled"] = False

        success = db_client.update_one(
            "usuarios_plataformas", "email", email, updates
        )

        if not success:
            # Reintento con columna unificada
            success = db_client.update_one(
                "usuarios_plataformas", "email", email, {"disabled": nuevo_estado}
            )

        if success:
            new_selected = self.selected_user.copy()
            new_selected[col_disabled] = nuevo_estado
            self.selected_user = new_selected
            self.fetch_users()
            self.sync_users_to_json() # <--- Persistir en JSON
            return rx.toast("Estado del plan actualizado.")

    @rx.var
    def filtered_users(self) -> List[dict]:
        filtered = self.users
        if self.filter_role != "todos":
            filtered = [u for u in filtered if u["rol"] == self.filter_role]
        if self.search_query:
            q = self.search_query.lower()
            filtered = [u for u in filtered if q in u["email"].lower() or q in u["full_name"].lower()]
        return filtered

    def set_search_query(self, query: str):
        self.search_query = query

    def set_filter_role(self, role: str):
        self.filter_role = role

    def set_selected_categoria(self, cat: str):
        self.selected_categoria = cat

    def on_load(self):
        if self.user_role != "admin":
            return rx.redirect("/academia")
        self.fetch_users()
        self.fetch_recursos()
        self.check_system_health()
