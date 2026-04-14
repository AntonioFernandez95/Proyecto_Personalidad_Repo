import random
from Personalidad.db.schemas.pregunta_schema import pregunta_schema, listado_preguntas_schema
from Personalidad.db.models.pregunta_model import PreguntaModel
from Personalidad.db.client import db_client  # CAMBIO: Usamos db_client que apunta al esquema 'personalidad'
from typing import List 
from collections import defaultdict

#*GET listado todas las preguntas BD*#
async def preguntas(): 
    # CAMBIO: Usamos db_client en lugar de personalidad_db_client
    return listado_preguntas_schema(db_client.find_all("personalidad.db_personalidad"))

#*GET PREGUNTAS BY ITEM, FILTRO (PONER INT ITEM)*#
async def buscar_preguntas_item(item:int):
    try: 
        item_int= int(item)
        preguntas_list= await preguntas()
        preguntas_por_item = list(filter(lambda pregunta:pregunta['ITEM']==item_int, preguntas_list))
        if preguntas_por_item:
                return preguntas_por_item
        else: 
            return "No hay preguntas con ese item"
    except ValueError:
        return "Mete un número chiquillo"

#*GET PREGUNTA POR ID, METES EL ID Y T LO DEVUELVE*#
async def pregunta_id(id: str):
    try:
        pregunta = buscar_pregunta_id("id", id) 
        return pregunta
    except Exception as e:
        return {"error": str(e)}

def buscar_pregunta_id(field: str, key):
    try:
        # CAMBIO: Usamos db_client
        pregunta = db_client.find_one("personalidad.db_personalidad", field, key)
        if pregunta:
            return PreguntaModel(**pregunta_schema(pregunta))
        else: 
            return {"error": "Te estás inventando el id chati"}
    except Exception as e:
        return {"error": str(e)}

#*GET las 133 preguntas del test, 19 por cada item*#
async def obtener_preguntas_test():
    try:
        preguntas_list = await preguntas()
        preguntas_validas=[PreguntaModel(**pregunta).dict() for pregunta in preguntas_list]
        test = await seleccionar_preguntas_por_item(preguntas_validas)
        return test
    except Exception as e:
        return {"error": str(e)}

#*Función para seleccionar 19 preguntas de cada ítem*#
async def seleccionar_preguntas_por_item(preguntas_list: List[PreguntaModel]) -> List[PreguntaModel]:
    preguntas_por_item = {}
    
    # Preguntas por item
    for pregunta in preguntas_list:
        item = pregunta['ITEM']
        if item not in preguntas_por_item:
            preguntas_por_item[item] = []
        preguntas_por_item[item].append(pregunta)
        
    test = []
    
    # Seleccionamos las 19 preguntas de cada ítem
    for item, preguntas in preguntas_por_item.items():
        if len(preguntas) >= 19:
            preguntas_seleccionadas = random.sample(preguntas, 19)
        else:
            preguntas_seleccionadas = preguntas
        
        test.extend(preguntas_seleccionadas)

    random.shuffle(test)
    
    return test