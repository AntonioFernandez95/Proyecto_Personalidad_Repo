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
            datos = DetallesTecnicasAPI.obtener_info_prueba(id_a_buscar)
            if datos:
                self.titulo = datos.get("titulo", "")
                self.posicion_inicial = datos.get("posicion_inicial", "")
                self.ejecucion = datos.get("ejecucion", [])
                self.normas = datos.get("normas", [])
                self.tiempo = datos.get("tiempo", "")
                self.intentos = datos.get("intentos", "")
            else:
                self.titulo = "PRUEBA NO ENCONTRADA"
                self.posicion_inicial = f"No se encontraron datos para: {id_a_buscar}"
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