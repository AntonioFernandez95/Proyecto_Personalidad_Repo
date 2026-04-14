# Registro de Modificaciones Frontend

Este documento resume los cambios realizados en el proyecto Reflex para actualizar el diseño, contenido y funcionalidad de la sección de academia y pruebas físicas.

## 🛠️ Correcciones Técnicas
- **[base_state.py](file:///c:/Users/antoniofernandez/Desktop/Proyecto_Personalidad_Repo/mi_codigo_reflex/Personalidad/states/base_state.py)**: Eliminación de un carácter no válido (`鼓`) al final del archivo que bloqueaba la compilación en Docker.

## 🖼️ Estética y Diseño Global
- **[styles.py](file:///c:/Users/antoniofernandez/Desktop/Proyecto_Personalidad_Repo/mi_codigo_reflex/Personalidad/styles/styles.py)**: Definición del fondo global con la imagen de soldados (`fondo-soldados (1).png`) en modo `cover` y `fixed`.
- **[layout.py](file:///c:/Users/antoniofernandez/Desktop/Proyecto_Personalidad_Repo/mi_codigo_reflex/Personalidad/pages/academia/layout.py)**: Sustitución del fondo de montañas por el de soldados en el layout de la academia. Actualización del componente `plan_row` para soportar enlaces externos.
- **[login.py](file:///c:/Users/antoniofernandez/Desktop/Proyecto_Personalidad_Repo/mi_codigo_reflex/Personalidad/pages/login.py)**: Cambio de la imagen de fondo de la pantalla de acceso para unificar el estilo con el resto de la web.

## 📱 Comunidad y Contacto
- **[curso.py](file:///c:/Users/antoniofernandez/Desktop/Proyecto_Personalidad_Repo/mi_codigo_reflex/Personalidad/pages/academia/curso.py)**:
    - **WhatsApp**: Incorporación del número `(676917128)` en el botón de tutorías.
    - **Telegram**: Actualización del enlace al canal de físicas (`https://t.me/+1ftMK4D17I1iYzg0`) y cambio de nombre a "Grupo Pruebas Físicas".

## 📋 Planificación de Entrenamiento
- **[planificacion.py](file:///c:/Users/antoniofernandez/Desktop/Proyecto_Personalidad_Repo/mi_codigo_reflex/Personalidad/pages/academia/planificacion.py)**:
    - Actualización de los nombres de los planes actuales.
    - Inserción de un nuevo plan específico de **Carrera**.
    - Vinculación de todos los planes a sus respectivos archivos PDF almacenados en `assets/`.
- **Assets**: Renombramiento físico de los archivos PDF en la carpeta del proyecto para usar nombres de archivo limpios (ej: `curso_fisicas_2026.pdf`).

## 🏃‍♂️ Técnicas de Pruebas Físicas
Se ha creado una estructura modular para que cada técnica tenga su propia página con imágenes ilustrativas reales:
- **[flexiones.py](file:///c:/Users/antoniofernandez/Desktop/Proyecto_Personalidad_Repo/mi_codigo_reflex/Personalidad/pages/academia/tecnica/flexiones.py)**: Muestra `EJERCICIO_METODOS_PLANCHA.webp`.
- **[planchas.py](file:///c:/Users/antoniofernandez/Desktop/Proyecto_Personalidad_Repo/mi_codigo_reflex/Personalidad/pages/academia/tecnica/planchas.py)**: Muestra `EJERCICIO_METODOS_FLEXIONES.webp`.
- **[agilidad.py](file:///c:/Users/antoniofernandez/Desktop/Proyecto_Personalidad_Repo/mi_codigo_reflex/Personalidad/pages/academia/tecnica/agilidad.py)**: Muestra el esquema del circuito de agilidad.
- **[carrera.py](file:///c:/Users/antoniofernandez/Desktop/Proyecto_Personalidad_Repo/mi_codigo_reflex/Personalidad/pages/academia/tecnica/carrera.py)**: Muestra el esquema de carrera.
- **[__init__.py (Academia)](file:///c:/Users/antoniofernandez/Desktop/Proyecto_Personalidad_Repo/mi_codigo_reflex/Personalidad/pages/academia/__init__.py)**: Registro de las nuevas rutas de navegación.
