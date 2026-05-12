# Archivo: Personalidad/states/detallesTecnicas_state.py

import reflex as rx
from Personalidad.states.base_state import State
from Personalidad.api.detallesTecnicas_api import DetallesTecnicasAPI


class DetallesTecnicasState(State):
    """Estado dinámico para la pantalla de detalle de las técnicas"""

    # Variables que se muestran en la pantalla
    titulo: str = "Cargando..."
    posicion_inicial: str = ""
    ejecucion: list[str] = []
    normas: list[str] = []
    tiempo: str = ""
    intentos: str = ""
    
    # Recursos dinámicos
    videos: list[dict] = []
    pdfs: list[dict] = []

    @rx.var
    def prueba_id(self) -> str:
        """Lee el segmento dinámico [prueba_id] de la URL."""
        return self.router.page.params.get("prueba_id", "")

    def cargar_datos_prueba(self):
        """Llama a la API cuando la página carga para rellenar los datos."""
        # 1. Intentamos obtener el ID del parámetro dinámico [prueba_id]
        id_a_buscar = self.router.page.params.get("prueba_id", "")
        
        # 2. Si no hay parámetro (página estática), lo extraemos del final de la URL
        if not id_a_buscar:
            # Quitamos los "?" de la URL si los hay y cogemos el último segmento
            raw_path = self.router.page.raw_path.split("?")[0]
            id_a_buscar = raw_path.strip("/").split("/")[-1]
            print(f"ID extraído de la ruta: '{id_a_buscar}'")

        print(f"ON_LOAD TRIGGERED. id_a_buscar: '{id_a_buscar}'")

        if not id_a_buscar:
            self.titulo = "ERROR"
            self.posicion_inicial = "No se pudo leer el ID de la prueba desde la URL."
            return

        try:
            # 3. Cargar Recursos adicionales (Vídeos y PDFs) - Siempre intentamos cargarlos si hay ID
            from Personalidad.db.crud import obtener_recursos_por_categoria
            from Personalidad.db.schemas.recurso_schema import recurso_schema
            
            raw_recursos = obtener_recursos_por_categoria(id_a_buscar)
            self.videos = [recurso_schema(r) for r in raw_recursos if r.tipo == "video"]
            self.pdfs = [recurso_schema(r) for r in raw_recursos if r.tipo == "pdf"]

            # 3.1 Fallback/Sincronización con JSON (si en la BD no hay nada o para asegurar conexión)
            import json
            import os
            try:
                # Cargar Vídeos desde JSON
                video_json_path = os.path.join("data", "recursos_videos.json")
                if os.path.exists(video_json_path):
                    with open(video_json_path, "r", encoding="utf-8") as f:
                        videos_data = json.load(f)
                        for v in videos_data:
                            # Si coincide la categoría y no está ya en la lista (por URL)
                            if v.get("categoria") == id_a_buscar:
                                if not any(existing["url"] == v["url"] for existing in self.videos):
                                    self.videos.append(v)
                
                # Cargar PDFs desde JSON
                pdf_json_path = os.path.join("data", "recursos_pdfs.json")
                if os.path.exists(pdf_json_path):
                    with open(pdf_json_path, "r", encoding="utf-8") as f:
                        pdfs_data = json.load(f)
                        for p in pdfs_data:
                            if p.get("categoria") == id_a_buscar:
                                if not any(existing["url"] == p["url"] for existing in self.pdfs):
                                    self.pdfs.append(p)
            except Exception as json_err:
                print(f"Error cargando fallback JSON: {json_err}")

            # 4. Cargar Info técnica
            datos = DetallesTecnicasAPI.obtener_info_prueba(id_a_buscar)
            if datos:
                self.titulo = datos.get("titulo", "")
                self.posicion_inicial = datos.get("posicion_inicial", "")
                self.ejecucion = datos.get("ejecucion", [])
                self.normas = datos.get("normas", [])
                self.tiempo = datos.get("tiempo", "")
                self.intentos = datos.get("intentos", "")
            else:
                self.titulo = id_a_buscar.upper()
                self.posicion_inicial = f"Información técnica pendiente de actualización."
                self.ejecucion = []
                self.normas = []
                self.tiempo = "--"
                self.intentos = "--"
        except Exception as e:
            print(f"Error en cargar_datos_prueba: {e}")
            self.titulo = "ERROR INTERNO"
            self.posicion_inicial = f"Fallo al leer la base de datos: {e}"
            self.ejecucion = []
            self.normas = []
            self.tiempo = "--"
            self.intentos = "--"