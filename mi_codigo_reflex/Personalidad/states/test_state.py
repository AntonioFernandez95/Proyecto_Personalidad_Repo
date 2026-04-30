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

        self._cargar_respuestas_pagina()


    def _cargar_respuestas_pagina(self):
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
        # Aseguramos mutación de estado correcta en Reflex
        nuevas = self.respuestas_acumuladas.copy()
        inicio = self.pag_actual * self.num_preguntas
        for i in range(self.num_preguntas):
            idx_global = inicio + i
            if idx_global < len(self.test_data):
                pregunta = self.test_data[idx_global]
                q_id = str(pregunta.get("id") or idx_global)
                if i < len(self.page_answers) and self.page_answers[i]:
                    nuevas[q_id] = self.page_answers[i]
        self.respuestas_acumuladas = nuevas


    def set_page_answer(self, index: int, valor: str):
        nueva_lista = list(self.page_answers)
        if index < len(nueva_lista):
            nueva_lista[index] = valor
        self.page_answers = nueva_lista


    def next_page(self):
        self._guardar_respuestas_pagina()
        if (self.pag_actual + 1) * self.num_preguntas < len(self.test_data):
            self.pag_actual += 1
            self._cargar_respuestas_pagina()


    def previous_page(self):
        if self.pag_actual > 0:
            self._guardar_respuestas_pagina()
            self.pag_actual -= 1
            self._cargar_respuestas_pagina()


    @rx.var
    def total_pages(self) -> int:
        count = len(self.test_data)
        if count == 0: return 1
        return (count + self.num_preguntas - 1) // self.num_preguntas


    @rx.var
    def current_progress(self) -> int:
        count = len(self.test_data)
        if count == 0: return 0
        
        # Lógica de progreso por páginas de tu compañero, pero blindada
        total = (count + self.num_preguntas - 1) // self.num_preguntas
        if total <= 1:
            return 100
        
        # Evitamos división por cero y aseguramos que no pase de 100
        progreso = int((self.pag_actual * 100) / (total - 1))
        return min(100, progreso)


    @rx.var
    def current_data(self) -> list[dict]:
        start = self.pag_actual * self.num_preguntas
        end = start + self.num_preguntas
        return self.test_data[start:end]


    def finalizar_test(self):
        self._guardar_respuestas_pagina()
        return rx.redirect("/results")


    def reset_test(self):
        self.pag_actual = 0
        self.respuestas_acumuladas = {}
        self.page_answers = ["", "", "", "", "", "", "", "", "", ""]
