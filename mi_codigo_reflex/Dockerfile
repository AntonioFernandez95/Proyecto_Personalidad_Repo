# 1. Base de Python 3.12
FROM python:3.12-slim

# 2.dependencias del sistema y Node.js 
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

WORKDIR /app

# 3. Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar proyecto e inicializar Reflex
COPY . .
RUN reflex init

# 5. Exponer puertos (8000 para backend, 3000 interno para frontend)
EXPOSE 8000 3000

# 6. Comando para ejecutar en modo producción
CMD ["reflex", "run", "--env", "prod"]