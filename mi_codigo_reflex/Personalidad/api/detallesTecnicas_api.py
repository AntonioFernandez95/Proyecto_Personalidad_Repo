# Archivo: Personalidad/api/detallesTecnicas_api.py

from Personalidad.db.crud import obtener_tecnica_por_id


import json

class DetallesTecnicasAPI:
    @staticmethod
    def obtener_info_prueba(id_prueba: str):
        try:
            # 1. Intentar obtener de la Base de Datos
            tecnica = obtener_tecnica_por_id(id_prueba)
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
            
            # 2. Fallback: Intentar obtener del archivo JSON si no está en la BD
            import os
            json_path = os.path.join("data", "tecnicas_data.json")
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        if item.get("id") == id_prueba:
                            return {
                                "titulo": item.get("titulo", ""),
                                "posicion_inicial": item.get("posicion_inicial", ""),
                                "ejecucion": item.get("ejecucion", []),
                                "normas": item.get("normas", []),
                                "tiempo": item.get("tiempo", ""),
                                "intentos": item.get("intentos", "")
                            }
            
            return None
        except Exception as e:
            print(f"Error al obtener tecnica: {e}")
            return None
           