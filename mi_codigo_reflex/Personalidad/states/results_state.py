import reflex as rx

from Personalidad.states.test_state import TestState
from Personalidad.states.base_state import State


class ResultsState(rx.State):
    
    isUserApto: bool = False
    
    score_item_1: int = 0
    score_item_2: int = 0
    score_item_3: int = 0
    score_item_4: int = 0
    score_item_5: int = 0
    score_item_6: int = 0
    score_item_7: int = 0
    
    is_1_ok: bool = False
    is_2_ok: bool = False
    is_3_ok: bool = False
    is_4_ok: bool = False
    is_5_ok: bool = False
    is_6_ok: bool = False
    is_7_ok: bool = False
    
    #*Función que recorre la lista de resultados y calcula la puntuación final en cada item*#
    async def calculate_results(self):
        test = await self.get_state(TestState)
        item_to_score_attr = {
            1: 'score_item_1',
            2: 'score_item_2',
            3: 'score_item_3',
            4: 'score_item_4',
            5: 'score_item_5',
            6: 'score_item_6',
            7: 'score_item_7',
        }
        
        for key, value in test.selections.items():
            current_question = test.test_data[key]
            answer_value = current_question.get(self.key_converter(value))
            current_item = current_question.get('ITEM')
            
            if current_item in item_to_score_attr:
                score_attr = item_to_score_attr[current_item]
                setattr(self, score_attr, getattr(self, score_attr) + answer_value)
                
        self.isOk()
        self.isApto()
        
        
    #*Función que recoge la respuesta del usuario y la convierte al formato de la BBDD*#
    def key_converter(self, value: str) -> str:
        conversion_map = {
            "Si": "SI",
            "Muchas veces": "MUCHAS_VECES",
            "Alguna vez": "ALGUNA_VEZ",
            "Pocas veces": "POCAS_VECES",
            "No": "NO"
        }
        return conversion_map.get(value, "")    
    
    #*Función que revisa las puntuaciones del usuario y devuelve si es apto o no es apto*#
    def isApto(self):
        scores = [
                self.score_item_1,
                self.score_item_2,
                self.score_item_3, 
                self.score_item_4, 
                self.score_item_5, 
                self.score_item_6, 
                self.score_item_7
        ]
            
        if any(score < 34 for score in scores[:2]):
            return print("Sinceridad o extraversión por debajo de la media")
            
        if any(score > 80 for score in scores[2:]):
            return print("Alguno negativo por encima de la media")
            
        if all(33 < score < 81 for score in scores):
            return print("Todos en la media")
            
        self.isUserApto = True
        return print("Todo bien!")
    
    def isOk(self):
        if self.score_item_1 > 33:
            self.is_1_ok = True
            
        if self.score_item_2 > 33:
            self.is_2_ok = True
            
        if self.score_item_3 < 80:
            self.is_3_ok = True
            
        if self.score_item_4 < 80:
            self.is_4_ok = True
            
        if self.score_item_5 < 80:
            self.is_5_ok = True
            
        if self.score_item_6 < 80:
            self.is_6_ok = True
            
        if self.score_item_7 < 80:
            self.is_7_ok = True
        

