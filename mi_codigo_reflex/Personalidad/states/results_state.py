import reflex as rx
import uuid

from Personalidad.states.test_state import TestState
from Personalidad.states.base_state import State
from Personalidad.db_service import guardar_resultado_personalidad


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
        # Obtenemos el usuario del estado base correctamente
        base_state = await self.get_state(State)
        user = base_state.user
        
        # 1. RESETEAMOS PUNTUACIONES (para evitar duplicados al recargar)
        self.score_item_1 = 0
        self.score_item_2 = 0
        self.score_item_3 = 0
        self.score_item_4 = 0
        self.score_item_5 = 0
        self.score_item_6 = 0
        self.score_item_7 = 0
        
        item_to_score_attr = {
            1: 'score_item_1',
            2: 'score_item_2',
            3: 'score_item_3',
            4: 'score_item_4',
            5: 'score_item_5',
            6: 'score_item_6',
            7: 'score_item_7',
        }
        
        # 2. CALCULAMOS SOBRE LAS RESPUESTAS
        # Creamos un mapa de ID a pregunta (idx_global como clave si id es None)
        id_a_pregunta = {str(q.get("id") or i): q for i, q in enumerate(test.test_data)}
        
        for q_id, value in test.respuestas_acumuladas.items():
            try:
                current_question = id_a_pregunta.get(q_id)
                if not current_question:
                    continue
                    
                db_key = self.key_converter(value)
                answer_value_raw = current_question.get(db_key, 0)
                
                # Convertimos a entero (la BD devuelve texto)
                try:
                    answer_value = int(float(answer_value_raw)) if answer_value_raw is not None else 0
                except:
                    answer_value = 0
                
                current_item = current_question.get('ITEM')
                # Forzamos que ITEM también sea un número para comparar
                try:
                    current_item_int = int(float(str(current_item)))
                except:
                    current_item_int = 0
                
                if current_item_int in item_to_score_attr:
                    score_attr = item_to_score_attr[current_item_int]
                    setattr(self, score_attr, getattr(self, score_attr) + answer_value)
            except Exception as e:
                print(f"Error procesando pregunta {q_id}: {e}")
                
        self.isOk()
        self.isApto()
        
        # 3. GUARDAMOS EN BASE DE DATOS
        self.persist_results(user)

    def persist_results(self, user: str):
        """Envía los datos calculados a la tabla historial_simplificado.personalidad"""
        if not user:
            print("AVISO: No se puede guardar el resultado porque 'user' es None.")
            return

        data = {
            "id": str(uuid.uuid4()),
            "user_id": user,
            "sinceridad": self.score_item_1,
            "extraversion": self.score_item_2,
            "neuroticismo": (self.score_item_3 + self.score_item_4) // 2,
            "psicoticismo": (self.score_item_5 + self.score_item_6 + self.score_item_7) // 3,
            "es_apto": "APTO" if self.isUserApto else "NO APTO"
        }
        print(f"DEBUG: Intentando guardar resultados para {user}. Data: {data}")
        success = guardar_resultado_personalidad(data)
        if success:
            print(f"ÉXITO: Resultado guardado correctamente en la tabla personalidad para {user}")
        else:
            print(f"ERROR: Falló el guardado en la base de datos para {user}. Revisa los logs de db_service.py")
        
    def key_converter(self, value: str) -> str:
        """Convierte la respuesta del usuario al nombre de columna en la BD."""
        conversion_map = {
            "Si": "SI",
            "Muchas veces": "MUCHAS_VECES",   # con guión bajo, igual que PreguntaModel
            "Alguna vez": "ALGUNA_VEZ",        # con guión bajo
            "Pocas veces": "POCAS_VECES",      # con guión bajo
            "No": "NO"
        }
        return conversion_map.get(value, "NO")

    
    def isApto(self):
        """Determina si el usuario es APTO o NO APTO."""
        scores = [
            self.score_item_1, self.score_item_2, self.score_item_3, 
            self.score_item_4, self.score_item_5, self.score_item_6, 
            self.score_item_7
        ]
        
        sinceridad_extraversion_ok = all(s > 33 for s in scores[:2])
        negativos_ok = all(s < 80 for s in scores[2:])
        
        if sinceridad_extraversion_ok and negativos_ok:
            self.isUserApto = True
        else:
            self.isUserApto = False

    def isOk(self):
        """Marca los checkmarks visuales para cada item."""
        self.is_1_ok = self.score_item_1 > 33
        self.is_2_ok = self.score_item_2 > 33
        self.is_3_ok = self.score_item_3 < 80
        self.is_4_ok = self.score_item_4 < 80
        self.is_5_ok = self.score_item_5 < 80
        self.is_6_ok = self.score_item_6 < 80
        self.is_7_ok = self.score_item_7 < 80
