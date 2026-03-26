import reflex as rx
from datetime import datetime
from Personalidad.states.base_state import State
from Personalidad.db.crud import guardar_historial_ligero

class CalculadoraState(State):
    """Estado de la Calculadora: Hace las matemáticas y le pasa el dato al CRUD"""
   
    # Variables del formulario conectadas al frontend
    gender: str = "male"  # male/female
    flexiones: str = ""
    plancha_seg: str = ""
    km2000: str = ""
    agilidad_seg: str = ""
    resultado: str = ""
    porcentaje: int = 0
   
    # Variable de respuesta
    resultado_final: str = ""
   
    async def procesar_calculo(self):
        """
        CAPA DE CONEXIÓN: Realiza el cálculo y delega el guardado a la API.
        Usa yield para asegurar que la UI se actualice en cada paso.
        """
        # 1. Indicamos inicio de procesamiento
        self.resultado = "Procesando..."
        yield
        
        try:
            # 2. Realizamos el cálculo directamente (es síncrono y rápido)
            res, porc = self.motor_de_calculo(
                self.gender, 
                self.flexiones, 
                self.plancha_seg, 
                self.km2000, 
                self.agilidad_seg
            )
            
            # 3. Actualizamos valores y 'yield' para que el usuario los vea YA
            self.resultado = res
            self.porcentaje = porc
            yield
            
            # 4. Guardado en DB (Delegado a la API)
            from Personalidad.api.calculadora_api import CalculadoraAPI
            await CalculadoraAPI.ejecutar_flujo_calculo(self)
            
            # 5. Refrescar el historial de la otra pestaña/componente dinámicamente
            from Personalidad.states.historial_state import HistorialSimplificado_State
            hist_state = await self.get_state(HistorialSimplificado_State)
            hist_state.cargar_historial()
            
        except Exception as e:
            print(f"ERROR en procesar_calculo: {e}")
            self.resultado = "ERROR"
            yield
            yield rx.window_alert(f"Error en el cálculo: {str(e)}")
            return

    def calcular_resultado(self):
        """Método antiguo - Mantenido por compatibilidad si se usa internamente."""
        pass

    def _enviar_datos_al_crud(self):
        """Prepara el paquete de datos y llama a la función de base de datos de tu compañero"""
        usuario_identificador = self.user if self.user else "anonimo@test.com"
       
        # 1. Empaquetamos los datos exactamente como los va a pedir el Schema de tu amigo
        datos_para_guardar = {
            "user_id": usuario_identificador,
            "simulacro_code": "FISICAS-CALC",
            "resultado": self.resultado_final,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
       
        # 2. Se lo enviamos a su función
        try:
            # 👇 Cuando tu amigo termine, descomenta esta línea para que se guarde de verdad
            # guardar_historial_ligero(datos_para_guardar)
           
            # Mientras tu amigo termina, dejamos este print para que veas que tu parte funciona
            print(f"✅ ¡Cálculo terminado! Esperando al CRUD de tu amigo para guardar esto: {datos_para_guardar}")
           
        except Exception as e:
            print(f"❌ Error al conectar con el CRUD: {e}")

    def motor_de_calculo(self, genero: str, flexiones: str, plancha: str, km2000: str, agilidad: str) -> tuple:
        """
        Motor de Cálculo.
        Recibe los datos y devuelve "APTO" o "NO APTO" y el porcentaje.
        """
        try:
            # Baremo simplificado
            if genero == "male":
                t_flex, t_plan, t_agil, t_carr = 17, 60, 25.0, 660 # 11:00 min
            else:
                t_flex, t_plan, t_agil, t_carr = 12, 40, 27.0, 780 # 13:00 min

            # Conversión segura
            def to_int(v, default=0):
                try: return int(float(v)) if v else default
                except: return default
            
            def to_float(v, default=0.0):
                try: return float(v) if v else default
                except: return default

            val_flex = to_int(flexiones)
            val_plan = to_int(plancha)
            val_agil = to_float(agilidad, 999.0)
            
            # Procesar carrera 2000m (mm:ss o segundos)
            val_carr = 9999
            if km2000:
                if ":" in km2000:
                    parts = km2000.split(":")
                    if len(parts) == 2:
                        val_carr = to_int(parts[0]) * 60 + to_int(parts[1])
                else:
                    val_carr = to_int(km2000, 9999)

            print(f"MOTOR DEBUG: Genero={genero}, Flex={val_flex}(>={t_flex}), Plan={val_plan}(>={t_plan}), Agil={val_agil}(<={t_agil}), Carr={val_carr}(<={t_carr})")

            puntos_apto = 0
            # Ratios de progreso (0.0 a 1.0)
            r_flex = min(1.0, val_flex / t_flex) if t_flex > 0 else 0
            r_plan = min(1.0, val_plan / t_plan) if t_plan > 0 else 0
            # Para agilidad y carrera, menor es mejor. Ratio = objetivo / actual
            r_agil = min(1.0, t_agil / val_agil) if val_agil > 0 else 0
            r_carr = min(1.0, t_carr / val_carr) if val_carr > 0 else 0

            if val_flex >= t_flex: puntos_apto += 1
            if val_plan >= t_plan: puntos_apto += 1
            if val_agil <= t_agil: puntos_apto += 1
            if val_carr <= t_carr: puntos_apto += 1
            
            # El porcentaje es la media de los progresos individuales
            porcentaje = int(((r_flex + r_plan + r_agil + r_carr) / 4) * 100)
            
            # Nuevo criterio: APTO a partir del 70% de progreso medio
            resultado = "APTO" if porcentaje >= 70 else "NO APTO"
            
            print(f"MOTOR DEBUG: Ratios -> Flex:{r_flex:.2f}, Plan:{r_plan:.2f}, Agil:{r_agil:.2f}, Carr:{r_carr:.2f} -> Total:{porcentaje}% RESULTADO:{resultado}")

            return resultado, porcentaje
        except Exception as e:
            print(f"Error en motor de cálculo: {e}")
            return "ERROR", 0
