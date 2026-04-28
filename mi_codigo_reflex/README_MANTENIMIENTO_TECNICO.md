# 📘 Manual de Mantenimiento Técnico - Proyecto Academia

Este documento resume los cambios críticos realizados en la infraestructura del proyecto para estabilizar el sistema, profesionalizar el panel de administración y corregir errores de acceso.

## 1. Cambios en la Base de Datos (PostgreSQL)

### Nueva Estructura de `usuarios_plataformas`
Se ha migrado la tabla para permitir que cada alumno tenga planes independientes. Ya no existe un único vencimiento global.

**Nuevas Columnas Añadidas:**
*   `hasta_personalidad` (TIMESTAMP): Vencimiento del plan de tests.
*   `hasta_fisicas` (TIMESTAMP): Vencimiento del plan de pruebas físicas.
*   `disabled_personalidad` (BOOLEAN): Estado de activación del plan de tests.
*   `disabled_fisicas` (BOOLEAN): Estado de activación del plan de físicas.

> [!IMPORTANT]
> Si añades usuarios manualmente, asegúrate de rellenar estas columnas. El sistema ahora ignora la columna antigua `hasta` para las funciones de administración.

### Limpieza de Usuarios
Se ha ejecutado un script de limpieza profunda que:
1.  **Eliminó duplicados**: Se detectaron múltiples entradas para el mismo email (especialmente correos de prueba).
2.  **Protección de Admins**: Se han preservado únicamente los 26 usuarios oficiales de `@academiametodos.com`.
3.  **Nuevos Estudiantes**: Se ha estandarizado el rol `estudiante` para los nuevos accesos.

---

## 2. El Problema de las Contraseñas ("Contraseña Incorrecta")

Si al intentar loguear con un usuario antiguo da error de contraseña, se debe a la **encriptación**.

**¿Por qué sucede?**
El sistema ahora utiliza `passlib` con el algoritmo **bcrypt** por seguridad. Si en la base de datos la contraseña está en texto plano (ej: "1234"), el sistema intentará compararla como un hash encriptado y fallará.

**Cómo solucionarlo:**
Para resetear la contraseña de un usuario y que vuelva a funcionar, usa este comando desde la terminal (dentro de la carpeta del proyecto):
```bash
docker exec mi_codigo_reflex-backend-1 python -c "from Personalidad.utils.auth import hash_password; from Personalidad.db.client import db_client; pwd = hash_password('NUEVA_CLAVE'); db_client.update_one('usuarios_plataformas', 'email', 'USUARIO@EMAIL.COM', {'password': pwd})"
```

---

## 3. Panel de Administración y Rutas

Se han registrado formalmente dos nuevas rutas críticas:
*   `/academia/admin_panel`: Gestión general y búsqueda con filtros por rol.
*   `/academia/admin_plans`: Gestión individual de vencimientos y perfiles.

**Cambios en el Código:**
*   **Reactividad**: Se ha eliminado el decorador `@rx.background` de las cargas iniciales para evitar el error "An error occurred". Las actualizaciones de estado ahora usan copias del diccionario (`.copy()`) para asegurar que la UI se refresque al instante.
*   **Flexibilidad**: El diseño ha pasado de ser estático a usar `rx.flex` para adaptarse a cualquier resolución.

---

## 4. Guía de Despliegue con Docker

Si al hacer `docker-compose up` te da errores extraños:
1.  **Limpiar Volúmenes**: A veces los cambios en la base de datos no se reflejan por la persistencia.
    ```bash
    docker-compose down -v
    ```
2.  **Reconstrucción Limpia**: Fuerza la compilación del frontend (donde suelen estar los errores de Webpack).
    ```bash
    docker-compose up -d --build
    ```

---

## 5. Conexión con Historial
Los resultados de los tests se guardan en el esquema `historial_simplificado`. La conexión se realiza mediante el campo `user_id` que debe coincidir con el ID del usuario en `usuarios_plataformas`.

---
*Manual generado para el equipo de desarrollo de Academia Métodos.*
