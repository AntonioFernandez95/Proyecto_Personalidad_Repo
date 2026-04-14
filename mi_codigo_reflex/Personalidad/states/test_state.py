import reflex as rx
from Personalidad.api.test_api import obtener_preguntas_test
from Personalidad.db.models.pregunta_model import PreguntaModel
from typing import Dict, List

class TestState(rx.State):
    test_data: list = []
    pag_actual: int = 0
    num_preguntas: int = 10
    total_preguntas: int = 133
    # Respuestas guardadas por ID de pregunta (histórico global)
    respuestas_acumuladas: Dict[str, str] = {}
    # Respuestas temporales de la página actual (lista de 10 slots fijos)
    page_answers: List[str] = ["", "", "", "", "", "", "", "", "", ""]

    async def crear_test(self): 
        """Carga las preguntas si no están cargadas."""
        if not self.test_data:
            try:
                result = await obtener_preguntas_test()
                if isinstance(result, list):
                    self.test_data = result
                else:
                    print('Error en API:', result)
            except Exception as e:
                print('Error cargando test:', e)

        # Cargar respuestas si ya existen para la página actual
        self._cargar_respuestas_pagina()

    def _cargar_respuestas_pagina(self):
        """Carga en page_answers las respuestas previas de la página actual."""
        nueva_lista = ["", "", "", "", "", "", "", "", "", ""]
        inicio = self.pag_actual * self.num_preguntas
        for i in range(self.num_preguntas):
            idx_global = inicio + i
            if idx_global < len(self.test_data):
                pregunta = self.test_data[idx_global]
                q_id = str(pregunta.get("id") or idx_global)
                nueva_lista[i] = self.respuestas_acumuladas.get(q_id, "")
        self.page_answers = nueva_lista

    def _guardar_respuestas_pagina(self):
        """Guarda las respuestas de page_answers en el histórico global."""
        inicio = self.pag_actual * self.num_preguntas
        for i in range(self.num_preguntas):
            idx_global = inicio + i
            if idx_global < len(self.test_data):
                pregunta = self.test_data[idx_global]
                q_id = str(pregunta.get("id") or idx_global)
                if self.page_answers[i]:  # solo guardamos si hay respuesta
                    self.respuestas_acumuladas[q_id] = self.page_answers[i]

    def set_page_answer(self, index: int, valor: str):
        """Actualiza solo el slot 'index' de la lista de respuestas actuales."""
        nueva_lista = list(self.page_answers)
        nueva_lista[index] = valor
        self.page_answers = nueva_lista

    def next_page(self):
        # 1. Guardar respuestas actuales en histórico
        self._guardar_respuestas_pagina()
        # 2. Avanzar página
        if (self.pag_actual + 1) * self.num_preguntas < len(self.test_data):
            self.pag_actual += 1
        # 3. Limpiar/cargar respuestas de la nueva página
        self._cargar_respuestas_pagina()

    def previous_page(self):
        if self.pag_actual > 0:
            # 1. Guardar respuestas actuales en histórico
            self._guardar_respuestas_pagina()
            # 2. Retroceder página
            self.pag_actual -= 1
            # 3. Cargar respuestas de la página anterior
            self._cargar_respuestas_pagina()

    @rx.var
    def total_pages(self) -> int:
        return (len(self.test_data) + self.num_preguntas - 1) // self.num_preguntas

    @rx.var
    def current_progress(self) -> int:
        count = len(self.test_data)
        if count == 0: return 0
        return int((len(self.respuestas_acumuladas) / count) * 100)

    @rx.var
    def current_data(self) -> list[dict]:
        start = self.pag_actual * self.num_preguntas
        end = start + self.num_preguntas
        return self.test_data[start:end]

    def finalizar_test(self):
        """Guarda la última página y redirige a resultados."""
        self._guardar_respuestas_pagina()
        return rx.redirect("/results")

    def reset_test(self):
        self.pag_actual = 0
        self.respuestas_acumuladas = {}
        self.page_answers = ["", "", "", "", "", "", "", "", "", ""]