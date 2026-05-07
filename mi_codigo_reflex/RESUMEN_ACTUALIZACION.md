# Sistema de Caducidad de Usuarios

Este documento detalla la implementación del control de acceso basado en la caducidad de la suscripción de los usuarios en la plataforma.

## 1. Lógica de Bloqueo (`auth_service.py`)
Se ha implementado una validación estricta durante el proceso de inicio de sesión (función `login`) que comprueba el estado de la suscripción del usuario justo después de validar su contraseña:

*   **Excepción para Administradores:** Los usuarios con el rol `admin` siempre tienen acceso permitido, independientemente de sus fechas de suscripción.
*   **Validación de Estudiantes:** Para los usuarios con rol `estudiante`, el sistema comprueba tres fechas clave en la base de datos:
    *   `hasta_personalidad` (Nueva columna de planes independientes)
    *   `hasta_fisicas` (Nueva columna de planes independientes)
    *   `hasta` (Columna heredada del sistema antiguo)
*   **Condición de Acceso:** Si el usuario es un estudiante, **al menos una** de esas fechas debe ser posterior al momento actual (`datetime.now()`). Si todas las fechas están vacías (`NULL`) o ya han pasado, el acceso es **denegado** a nivel de backend.
*   **Comportamiento en la Interfaz:** Actualmente, cuando el backend rechaza el acceso por caducidad (devolviendo `False`), el frontend (interfaz de usuario) lo interpreta genéricamente y muestra el mensaje predeterminado de "Contraseña incorrecta". *Se recomienda en una futura actualización diferenciar el mensaje de error en la UI.*

## 2. Soporte de Formatos de Fecha
Se ha añadido la dependencia `python-dateutil` al archivo `requirements.txt`. Esta librería permite al sistema procesar e interpretar de forma segura las fechas de caducidad provenientes de la base de datos, sin importar si llegan como objetos `datetime` o como cadenas de texto (`strings`) en diferentes formatos.

## 3. Estructura de la Base de Datos
Para dar soporte a esta nueva lógica, se han añadido y configurado las siguientes columnas en la tabla `usuarios_metodos.usuarios_plataformas` (y en sus respectivos modelos de Python `user_model.py` y `user_schema.py`):
*   `hasta_personalidad` (TIMESTAMP)
*   `hasta_fisicas` (TIMESTAMP)
*   `disabled_personalidad` (BOOLEAN)
*   `disabled_fisicas` (BOOLEAN)

## 4. Pruebas y Verificación
Para confirmar el correcto funcionamiento de este bloqueo, se generó un script de prueba (`crear_alumno_test.py`) que inyectó un usuario (`alumno.test@academiametodos.com`) con una fecha de caducidad pasada (Año 2023). Se verificó que el sistema le impide correctamente iniciar sesión, confirmando que la lógica de caducidad está activa y funcionando.
