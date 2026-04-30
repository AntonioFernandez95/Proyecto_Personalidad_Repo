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

    # --- GESTIÓN DE RECURSOS ---
    recursos: List[dict] = []
    selected_categoria: str = "flexiones"
    categorias_disponibles: List[str] = ["flexiones", "plancha", "agilidad", "carrera", "planificacion"]
    
    def fetch_recursos(self):
        """Obtiene todos los recursos de la base de datos."""
        from Personalidad.db.crud import obtener_todos_los_recursos
        from Personalidad.db.schemas.recurso_schema import recurso_schema
        try:
            raw = obtener_todos_los_recursos()
            self.recursos = [recurso_schema(r) for r in raw]
        except Exception as e:
            print(f"Error cargando recursos: {e}")
            self.recursos = []

    async def handle_upload(self, files: List[rx.UploadFile]):
        """Sube archivos a assets/uploads y los registra en la BD."""
        import os
        from Personalidad.db.crud import guardar_recurso
        
        upload_dir = os.path.join("assets", "uploads")
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        for file in files:
            upload_data = await file.read()
            outfile = os.path.join(upload_dir, file.filename)
            with open(outfile, "wb") as f:
                f.write(upload_data)
            
            # Detectar tipo
            tipo = "pdf" if file.filename.lower().endswith(".pdf") else "video"
            
            # Guardar en BD
            guardar_recurso(
                nombre=file.filename,
                tipo=tipo,
                url=f"/uploads/{file.filename}",
                categoria=self.selected_categoria
            )
        
        self.fetch_recursos()
        return rx.toast(f"Subidos {len(files)} archivos a {self.selected_categoria}.")

    def borrar_recurso(self, recurso: dict):
        """Elimina un recurso de la BD y el archivo físico."""
        import os
        from Personalidad.db.crud import eliminar_recurso
        
        try:
            if eliminar_recurso(recurso["id"]):
                # Eliminar archivo físico
                path_relativo = recurso["url"].lstrip("/") # uploads/file.ext
                filepath = os.path.join("assets", path_relativo)
                if os.path.exists(filepath):
                    os.remove(filepath)
                
                self.fetch_recursos()
                return rx.toast("Recurso eliminado.")
        except Exception as e:
            return rx.window_alert(f"Error al borrar: {e}")

    def fetch_users(self):
        self.is_loading = True
        try:
            raw_users = db_client.find_all("usuarios_plataformas")
            sorted_users = sorted(raw_users, key=lambda x: x.get("email", ""))
            self.users = users_schema(sorted_users)
        except Exception as e:
            print(f"Error cargando usuarios: {e}")
            self.users = []
        finally:
            self.is_loading = False

    def select_user(self, user: dict):
        self.selected_user = user
        self.new_name = user.get("full_name", "")
        self.new_email = user.get("email", "")
        self.days_to_add = "30"
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
            
            raw_user = db_client.find_one("usuarios_plataformas", "email", email)
            fecha_actual = raw_user.get(col_fecha)
            if not fecha_actual or not isinstance(fecha_actual, datetime):
                fecha_actual = datetime.now()

            nueva_fecha = fecha_actual + timedelta(days=days)
            
            success = db_client.update_one(
                "usuarios_plataformas", "email", email, {col_fecha: nueva_fecha}
            )

            if success:
                new_selected = self.selected_user.copy()
                new_selected[col_fecha] = nueva_fecha.strftime("%Y-%m-%d")
                self.selected_user = new_selected
                self.fetch_users()
                return rx.toast(f"Plan {tipo_plan} extendido.")
            
        except Exception as e:
            return rx.window_alert(f"Error: {str(e)}")

    def toggle_baja_plan(self, tipo_plan: str):
        if not self.selected_user or not self.selected_user.get("email"):
            return rx.window_alert("No hay usuario seleccionado.")

        email = self.selected_user["email"]
        col_disabled = f"disabled_{tipo_plan}"
        nuevo_estado = not self.selected_user.get(col_disabled, False)
        
        success = db_client.update_one(
            "usuarios_plataformas", "email", email, {col_disabled: nuevo_estado}
        )

        if success:
            new_selected = self.selected_user.copy()
            new_selected[col_disabled] = nuevo_estado
            self.selected_user = new_selected
            self.fetch_users()
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

    def on_load(self):
        if self.user_role != "admin":
            return rx.redirect("/academia")
        self.fetch_users()
        self.fetch_recursos()
