import sys
import os

# Añadir el directorio actual al path para que pueda encontrar Personalidad
sys.path.append(os.getcwd())

try:
    from Personalidad.states.login_state import LoginState, ButtonClick
    print("Import successful")
    from Personalidad.states.base_state import State
    print("Base state import successful")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
