# Archivo: Personalidad/api/detallesTecnicas_api.py

from Personalidad.db.crud import obtener_tecnica_por_id


import json

class DetallesTecnicasAPI:
    @staticmethod
    def obtener_info_prueba(id: str):
        try:
            tecnica = obtener_tecnica_por_id(id)
            if tecnica:
                # Si vienen como string por el importador, los parseamos
                ejecucion = json.loads(tecnica.ejecucion) if tecnica.ejecucion and isinstance(tecnica.ejecucion, str) and tecnica.ejecucion.startswith('[') else tecnica.ejecucion or []
                normas = json.loads(tecnica.normas) if tecnica.normas and isinstance(tecnica.normas, str) and tecnica.normas.startswith('[') else tecnica.normas or []
                
                return {
                    "titulo": tecnica.titulo,
                    "posicion_inicial": tecnica.posicion_inicial,
                    "ejecucion": ejecucion if isinstance(ejecucion, list) else [ejecucion],
                    "normas": normas if isinstance(normas, list) else [normas],
                    "tiempo": tecnica.tiempo,
                    "intentos": tecnica.intentos
                }
        except Exception as e:
            print(f"Error al obtener tecnica: {e}")
            return None
           