import reflex as rx
from Personalidad.api.test_api import obtener_preguntas_test
from Personalidad.db.models.pregunta_model import PreguntaModel
from typing import Dict

class TestState(rx.State):
    test_data: list = []
    pag_actual: int = 0
    num_preguntas: int = 10
    total_preguntas: int = 133
    selections: Dict[str, str] = {}

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
    
    def next_page(self):
        if (self.pag_actual + 1) * self.num_preguntas < len(self.test_data):
            self.pag_actual += 1
            
    def previous_page(self):
        if self.pag_actual > 0:
            self.pag_actual -= 1
    
    @rx.var
    def total_pages(self) -> int:
        return (len(self.test_data) + self.num_preguntas - 1) // self.num_preguntas

    @rx.var
    def current_progress(self) -> int:
        count = len(self.test_data)
        if count == 0: return 0
        return int((len(self.selections) / count) * 100)

    @rx.var
    def current_data(self) -> list[dict]:
        start = self.pag_actual * self.num_preguntas
        end = start + self.num_preguntas
        return self.test_data[start:end]

    def set_selection(self, index: int, value: str):
        self.selections[str(index)] = value

    def finalizar_test(self):
        """Redirige a resultados."""
        return rx.redirect("/results")

    def reset_test(self):
        self.test_data = []
        self.pag_actual = 0
        self.selections = {}