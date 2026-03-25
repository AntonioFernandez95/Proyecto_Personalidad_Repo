# Personalidad/api/motor.py

def calcular_resultado_test(gender: str, flexiones: str, plancha_seg: str, km2000: str, agilidad_seg: str) -> dict:
    """
    Motor de Cálculo (Punto 1B).
    Realiza la lógica de evaluación proporcional para obtener porcentajes exactos (ex: 53%).
    """
    try:
        # Objetivos y límites para el 0% (estimados para proporcionalidad)
        if gender == "male":
            t_flex, t_plan, t_agil, t_carr = 17, 60, 25.0, 660
            w_agil, w_carr = 35.0, 900 # 35s agilidad y 15min carrera = 0%
        else:
            t_flex, t_plan, t_agil, t_carr = 12, 40, 27.0, 780
            w_agil, w_carr = 37.0, 1020 # 37s agilidad y 17min carrera = 0%

        val_flex = int(flexiones) if flexiones else 0
        val_plan = int(plancha_seg) if plancha_seg else 0
        val_agil = float(agilidad_seg) if agilidad_seg else w_agil
        
        # Procesar carrera
        val_carr = w_carr
        if km2000 and ":" in km2000:
            parts = km2000.split(":")
            if len(parts) == 2:
                val_carr = int(parts[0]) * 60 + int(parts[1])

        # Cálculo de puntos proporcionales (0.0 a 1.0 por prueba)
        p_flex = min(val_flex / t_flex, 1.2) if t_flex > 0 else 0 # Capamos en 1.2 por si sobrepasan mucho
        p_plan = min(val_plan / t_plan, 1.2) if t_plan > 0 else 0
        
        # Agilidad y Carrera (Menos es mejor)
        p_agil = max(0, min(1.2, (w_agil - val_agil) / (w_agil - t_agil)))
        p_carr = max(0, min(1.2, (w_carr - val_carr) / (w_carr - t_carr)))

        # Puntos totales (sobre 4.0)
        puntos_totales = p_flex + p_plan + p_agil + p_carr
        
        # Porcentaje exacto (sobre 100)
        porcentaje_exacto = int((puntos_totales / 4) * 100)
        
        # El APTO se sigue rigiendo por cumplir los mínimos en al menos 3 pruebas
        puntos_apto = 0
        if val_flex >= t_flex: puntos_apto += 1
        if val_plan >= t_plan: puntos_apto += 1
        if val_agil <= t_agil: puntos_apto += 1
        if val_carr <= t_carr: puntos_apto += 1
        
        resultado = "APTO" if puntos_apto >= 3 else "NO APTO"
        
        return {
            "resultado": resultado,
            "porcentaje": porcentaje_exacto,
            "puntos": round(puntos_totales, 2),
            "success": True
        }
    except Exception as e:
        return {
            "resultado": "ERROR",
            "porcentaje": 0,
            "success": False,
            "error": str(e)
        }
