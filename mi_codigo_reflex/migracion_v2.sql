-- SCRIPT DE MIGRACIÓN V2 - PROYECTO PERSONALIDAD
-- Ejecutar este script para sincronizar la base de datos con los últimos cambios

-- 1. Asegurar que existen los esquemas necesarios
CREATE SCHEMA IF NOT EXISTS personalidad;
CREATE SCHEMA IF NOT EXISTS recursos;
CREATE SCHEMA IF NOT EXISTS usuarios_metodos;

-- 2. Actualizar tabla de usuarios con campos de caducidad
DO $$ 
BEGIN 
    -- Columnas de fechas
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema='usuarios_metodos' AND table_name='usuarios_plataformas' AND column_name='hasta_fisicas') THEN
        ALTER TABLE usuarios_metodos.usuarios_plataformas ADD COLUMN hasta_fisicas TIMESTAMP;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema='usuarios_metodos' AND table_name='usuarios_plataformas' AND column_name='hasta_personalidad') THEN
        ALTER TABLE usuarios_metodos.usuarios_plataformas ADD COLUMN hasta_personalidad TIMESTAMP;
    END IF;

    -- Columnas de bloqueo (flags)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema='usuarios_metodos' AND table_name='usuarios_plataformas' AND column_name='disabled_fisicas') THEN
        ALTER TABLE usuarios_metodos.usuarios_plataformas ADD COLUMN disabled_fisicas BOOLEAN DEFAULT FALSE;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema='usuarios_metodos' AND table_name='usuarios_plataformas' AND column_name='disabled_personalidad') THEN
        ALTER TABLE usuarios_metodos.usuarios_plataformas ADD COLUMN disabled_personalidad BOOLEAN DEFAULT FALSE;
    END IF;
END $$;

-- 3. Crear tabla de Aptitudes (Historial Personalidad)
CREATE TABLE IF NOT EXISTS personalidad.aptitudes (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR,
    sinceridad INTEGER,
    extraversion INTEGER,
    depresion INTEGER,
    neuroticismo INTEGER,
    psicoticismo INTEGER,
    paranoidismo INTEGER,
    desviacion_psicopatica INTEGER,
    es_apto VARCHAR,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_aptitudes_user_id ON personalidad.aptitudes(user_id);

-- 4. Crear tablas de Recursos (Panel Admin)
CREATE TABLE IF NOT EXISTS recursos.videos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    url TEXT,
    categoria VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recursos.pdfs (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    url TEXT,
    categoria VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Limpieza: Eliminar tabla obsoleta
DROP TABLE IF EXISTS tecnicas.recursos CASCADE;

-- FIN DEL SCRIPT
