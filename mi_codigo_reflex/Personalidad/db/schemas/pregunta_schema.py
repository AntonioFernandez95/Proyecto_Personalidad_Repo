
#*Devuelve una pregunta como diccionario*#
def pregunta_schema(pregunta) -> dict:
    return {
        "id": str(pregunta.get("id", pregunta.get("_id", ""))),
        "ITEM": int(pregunta.get("ITEM", 0)),
        "PREGUNTA": str(pregunta.get("PREGUNTA", "").replace('\xa0', ' ')),
        "SI": int(pregunta.get("SI", 0)),
        "MUCHAS_VECES": int(pregunta.get("MUCHAS VECES", 0)),
        "ALGUNA_VEZ": int(pregunta.get("ALGUNA VEZ", 0)),
        "POCAS_VECES": int(pregunta.get("POCAS VECES", 0)),
        "NO": int(pregunta.get("NO", 0)),
    }


#*Devuelve el listado de diccionario de preguntas*#
def listado_preguntas_schema(preguntas) -> list:
    return [pregunta_schema(pregunta) for pregunta in preguntas]