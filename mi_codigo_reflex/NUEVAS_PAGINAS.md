# 🎓 Documentación: Nuevas Páginas y Arquitectura de Academia Online

Este documento explica todos los cambios realizados para transformar la plataforma en una aplicación multi-página robusta, segura y profesional.

---

## 🚀 Resumen de Cambios Principales

1.  **Arquitectura Multi-Página**: Se ha eliminado el archivo único gigante (`academia.py`) y se ha dividido en una estructura modular de **9 rutas independientes**.
2.  **Seguridad (Login Check)**: Todas las páginas de la academia están protegidas. Si un usuario no está logueado, es redirigido automáticamente al inicio.
3.  **Redirección Inteligente**:
    *   Al hacer login correctamente, el usuario va **directamente al Dashboard**.
    *   Si un usuario logueado visita la página principal (`/`), el sistema lo lleva al Dashboard sin pedirle login de nuevo.
4.  **Personalización**: El Dashboard muestra ahora el nombre del usuario (email).
5.  **Gestión de Sesión**: Se ha añadido un botón de **Cerrar Sesión** funcional en la barra de navegación.

---

## 📂 Archivos Creados y Modificados

### 1. Directorio de Academia (`Personalidad/pages/academia/`)
Este es el nuevo núcleo de la plataforma.

*   [NEW] `index.py`: El **Dashboard** principal con la bienvenida personalizada.
*   [NEW] `layout.py`: Define el diseño común (Navbar verde oliva, fondo de bosque, estructura de contenedores). **Aquí está el botón de Cerrar Sesión.**
*   [NEW] `state.py`: Estado compartido para la academia (hereda de `State` para tener acceso al usuario y sesiones).
*   [NEW] `fisicas.py`: Página de Pruebas Físicas.
*   [NEW] `curso.py`: Página del curso.
*   [NEW] `tecnica.py`: Menú de técnicas.
*   [NEW] `detalle.py`: Detalle de ejercicios (Flexiones).
*   [NEW] `planificacion.py`: Planes de entrenamiento.
*   [NEW] `calculadora.py`: Calculadora de marcas.
*   [NEW] `historial.py`: Historial de simulacros.
*   [NEW] `simulacro.py`: Información de simulacros presenciales.

### 2. Archivos de Sistema Modificados
*   [MODIFY] `Personalidad/pages/login.py`: Se cambió el comportamiento al cargar para chequear si el usuario ya está autenticado (`check_authenticated`).
*   [MODIFY] `Personalidad/states/login_state.py`:
    *   Se añadió la lógica para redirigir a `/academia` tras un login exitoso.
    *   Se añadió la función `check_authenticated` para el auto-redireccionamiento.
*   [DELETE] `Personalidad/pages/academia.py`: Eliminado el archivo antiguo para evitar conflictos y redundancia.

---

## 🛠️ Cómo Funciona la Seguridad (`on_load`)

Cada página nueva utiliza un decorador de Reflex para verificar la sesión antes de mostrar el contenido:

```python
@rx.page(route="/academia/...", on_load=AcademiaState.check_login)
def mi_pagina():
    ...
```

Esto asegura que nadie pueda "saltarse" el login introduciendo la URL manualmente.

## 🧭 Navegación
*   **Logo / ACADEMIA ONLINE**: Te devuelve siempre al Dashboard.
*   **Botón Volver**: Configurado dinámicamente en cada página para que la navegación sea fluida (ej. de Detalle de Técnica vuelve a Técnicas, de Técnicas vuelve a Físicas).
*   **Cerrar Sesión**: Limpia el estado y devuelve al login.

---

> [!TIP]
> Para aplicar cualquier cambio futuro en el diseño visual, edita directamente `Personalidad/pages/academia/layout.py`. Todos los contenedores y estilos globales se centralizan allí.
