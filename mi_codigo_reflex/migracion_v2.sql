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

-- 3. Insertar usuarios base si no existen (Claudia y Alejandra)
-- Nota: Usamos una subconsulta para evitar errores si ya existen
INSERT INTO usuarios_metodos.usuarios_plataformas (email, nombre, apellidos, rol, password, hasta_fisicas, hasta_personalidad, disabled_fisicas, disabled_personalidad)
SELECT 'claudia@academiametodos.com', 'Claudia', 'Mendoza Antequera', 'admin', '$2b$12$yUNv.e9.gfvEv2HQZOp09uSWOKEoL358q.S4MoUt3jkvNkBWfN9ga', '2026-10-25', '2026-09-29', false, false
WHERE NOT EXISTS (SELECT 1 FROM usuarios_metodos.usuarios_plataformas WHERE email = 'claudia@academiametodos.com');

INSERT INTO usuarios_metodos.usuarios_plataformas (email, nombre, apellidos, rol, password, hasta_fisicas, hasta_personalidad, disabled_fisicas, disabled_personalidad)
SELECT 'alejandragarzon.24@campuscamara.es', 'Alejandra', '', 'estudiante', '$2b$12$AbQPoUdyqBhSNnLidhCkH.j/n.RqkSFe5eePj6rD7LkQpefRGJ3QS', '2026-10-25', '2020-01-01', false, false
WHERE NOT EXISTS (SELECT 1 FROM usuarios_metodos.usuarios_plataformas WHERE email = 'alejandragarzon.24@campuscamara.es');

-- 4. Crear tabla de Aptitudes (Historial Personalidad)
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

-- 5. Crear tablas de Recursos (Panel Admin)
CREATE TABLE IF NOT EXISTS recursos.videos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    url TEXT,
    categoria VARCHAR(100),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recursos.pdfs (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    url TEXT,
    categoria VARCHAR(100),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Limpieza: Eliminar tabla obsoleta
DROP TABLE IF EXISTS tecnicas.recursos CASCADE;

-- FIN DEL SCRIPT
