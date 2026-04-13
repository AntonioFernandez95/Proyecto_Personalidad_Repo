import reflex as rx
from Personalidad.api.test_api import obtener_preguntas_test
from Personalidad.db.models.pregunta_model import PreguntaModel
from typing import Dict


class TestState(rx.State):
    test_data: list[PreguntaModel] = []
    pag_actual: int = 0
    num_preguntas: int = 1
    total_preguntas: int = 133
    num_pregunta_actual: int = 0
    selections: Dict[int, str] = {}

    #*GET 133 preguntas, 19 por item*#
    async def crear_test(self): 
        self.reset_test()
        try:
            preguntas_dict_list = await obtener_preguntas_test()
            self.test_data = [PreguntaModel(**pregunta).dict() for pregunta in preguntas_dict_list]
        except Exception as e:
                print('Error al procesar la solicitud:', e)
    
    #*Cambios de página*#
    def next_page(self):
        if (self.pag_actual + 1) * self.num_preguntas < len(self.test_data):
            self.pag_actual += 1
            
    def previous_page(self):
        if self.pag_actual > 0:
            self.pag_actual -= 1
    
    #*Calculo porcentaje de test avanzado*#
    @rx.cached_var
    def total_pages(self) -> int:
        return (self.total_preguntas + self.num_preguntas - 1) // self.num_preguntas

    @rx.cached_var
    def current_progress(self) -> int:
        return (self.pag_actual + 1) / self.total_pages * 100

    #*GET rango de la lista de preguntas (paginación)*#
    @rx.cached_var
    def current_data(self) -> list[dict]:
        start = self.pag_actual * self.num_preguntas
        end = start + self.num_preguntas
        return self.test_data[start:end]

    #*SET respuesta seleccionada, guardamos la selección del usuario*#
    def set_selection(self, index: int, value: str):
        self.selections[index] = value
        print(self.selections)

    #*Resetea todos los valores en caso de refresh de página*#
    def reset_test(self):
        self.test_data: list[PreguntaModel] = []
        self.pag_actual: int = 0
        self.num_preguntas: int = 1
        self.total_preguntas: int = 133
        self.num_pregunta_actual: int = 0
        self.selections: Dict[int, str] = {}