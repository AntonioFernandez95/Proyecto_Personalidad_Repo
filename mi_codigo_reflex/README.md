# 🧠 Proyecto Personalidad - Guía de Operación y Cambios

Este documento detalla la estructura del proyecto, los cambios recientes y las instrucciones críticas para operar el sistema en el nuevo entorno basado en **PostgreSQL** y **Docker**.

## 🚀 Cambios Principales

### 1. Migración a PostgreSQL
Se ha migrado la base de datos de MongoDB a **PostgreSQL (v15)** para mejorar la integridad de datos.
- **Esquema `personalidad`**: Todas las tablas de usuarios y datos del test residen en este esquema.
- **Tipo de dato TEXT/JSON**: Las tablas se han normalizado para aceptar los datos originales de los archivos JSON.
- **Cliente DB**: Ubicado en `Personalidad/db/client.py`, centraliza todas las conexiones.

### 2. Contenerización con Docker
El proyecto ahora corre completamente en Docker con tres servicios principales:
- **`db`**: Base de datos PostgreSQL.
- **`backend`**: Servidor Reflex (Python 3.12).
- **`frontend`**: Servidor estático (Nginx).

### 3. Automatización de Importación
Se ha mejorado `importador.py` para que sea flexible y funcione tanto en local como dentro de Docker.

---

## 🛠️ Instrucciones de Inicialización (Base de Datos)

Si acabas de levantar el proyecto con `docker compose up --build` y la base de datos está vacía, sigue estos pasos para cargar los datos:

### Opción Recomendada (Dentro de Docker)
Para asegurar que los datos se carguen en la base de datos del contenedor y no en una instancia local:

1. Asegúrate de que los contenedores estén corriendo.
2. Ejecuta el siguiente comando en tu terminal:
   ```powershell
   docker exec -e DB_HOST=db mi_codigo_reflex-backend-1 python importador.py
   ```

### Opción Alternativa (Desde el Host)
Si tienes las dependencias instaladas en tu máquina:
```powershell
py importador.py
```
*Nota: Asegúrate de que no haya otro servicio de PostgreSQL ocupando el puerto 5432 en tu máquina Windows.*

---

## 📝 Explicación Técnica de los Cambios (Paso a Paso)

Para resolver el error `relation "personalidad.users" does not exist`, se siguieron estos pasos:

### Paso 1: Diagnóstico de la Estructura de Datos
Se identificó que el código en `login_api.py` realizaba consultas explícitas al esquema `personalidad` (ej. `personalidad.users`). Sin embargo, en PostgreSQL, las tablas se crean por defecto en el esquema `public`. Por lo tanto, era necesario crear el esquema `personalidad` antes de importar los datos.

### Paso 2: Refactorización del Importador
Se modificó `importador.py` para:
- **Creación de Esquemas**: Asegurar que se ejecute `CREATE SCHEMA IF NOT EXISTS` para cada esquema definido en el JSON.
- **Rutas Relativas**: Cambiar rutas absolutas (fijas) por rutas dinámicas usando `os.path.dirname(__file__)`, permitiendo que el script encuentre la carpeta `data/` en cualquier ordenador.
- **Variables de Entorno**: Permitir que el host de la base de datos se configure externamente (localhost o db).

### Paso 3: Resolución del Conflicto de Puertos (Host vs Docker)
Se detectó que al ejecutar el importador desde Windows, éste se conectaba a una instancia de Postgres local (fuera de Docker) en el puerto 5432. Esto hacía que pareciera que los datos estaban cargados, pero el backend de Docker no podía verlos porque apuntaba a su propio contenedor `db-1`.
- **Solución**: Se forzó la ejecución del importador **dentro** del contenedor `backend` para que la conexión fuera directa a la base de datos de Docker mediante la red interna.

### Paso 4: Ajuste de DockerIgnore
Se identificó que el archivo `.dockerignore` estaba excluyendo la carpeta `data/` y el script `importador.py`. Se corrigió esto para permitir que el backend tenga acceso a los archivos fuente necesarios para la población inicial.

---

## 📂 Archivos y Directorios Clave
- **[importador.py](file:///c:/Users/Usuario/Desktop/Personalidad%20Repo/Personalidad%20Repo/mi_codigo_reflex/importador.py)**: Script para poblar la base de datos.
- **[client.py](file:///c:/Users/Usuario/Desktop/Personalidad%20Repo/Personalidad%20Repo/mi_codigo_reflex/Personalidad/db/client.py)**: Configuración de conexión del backend.
- **[login_api.py](file:///c:/Users/Usuario/Desktop/Personalidad%20Repo/Personalidad%20Repo/mi_codigo_reflex/Personalidad/api/login_api.py)**: Lógica de autenticación.

## 🔍 Verificación del Estado
Para comprobar si la tabla de usuarios tiene datos, puedes ejecutar:
```powershell
docker exec mi_codigo_reflex-db-1 psql -U postgres -d db_personalidad_proyecto -c "SELECT count(*) FROM personalidad.users;"
```

---
*Documentación detallada generada para el equipo de desarrollo el 18 de Marzo de 2026.*
