-- ============================================================================
-- MIGRACIÓN: Sistema de Auto-Altas Automáticas
-- Ejecutar sobre la BD: db_personalidad_proyecto
-- Esquema destino: usuarios_metodos
-- ============================================================================

-- 1. Asegurar que el esquema existe (por si acaso)
CREATE SCHEMA IF NOT EXISTS usuarios_metodos;

-- 2. Crear tabla de control de altas procesadas
--    La UNIQUE KEY es fundamental: evita dobles altas aunque el cron se ejecute dos veces
CREATE TABLE IF NOT EXISTS usuarios_metodos.auto_altas_procesadas (
    id            BIGSERIAL PRIMARY KEY,
    pedido_id     VARCHAR(100) NOT NULL,
    linea_id      VARCHAR(100) NOT NULL,
    producto_id   VARCHAR(50)  NOT NULL,
    email         VARCHAR(255) NOT NULL,
    estado        VARCHAR(20)  NOT NULL DEFAULT 'processing'
                      CHECK (estado IN ('processing', 'processed', 'failed')),
    intentos      INT          NOT NULL DEFAULT 0,
    error         TEXT         NULL,
    usuario_id    VARCHAR(255) NULL,     -- email del alumno una vez creado/actualizado
    fecha_inicio      TIMESTAMP NULL,
    fecha_vencimiento TIMESTAMP NULL,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_pedido_linea_producto UNIQUE (pedido_id, linea_id, producto_id)
);

-- 3. Índices de rendimiento
CREATE INDEX IF NOT EXISTS idx_auto_altas_estado
    ON usuarios_metodos.auto_altas_procesadas (estado);

CREATE INDEX IF NOT EXISTS idx_auto_altas_email
    ON usuarios_metodos.auto_altas_procesadas (email);

-- 4. Asegurar que usuarios_plataformas tiene las columnas de vencimiento por módulo
--    (puede que ya existan de migracion_v2.sql, el IF NOT EXISTS lo protege)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'usuarios_metodos'
          AND table_name   = 'usuarios_plataformas'
          AND column_name  = 'hasta_personalidad'
    ) THEN
        ALTER TABLE usuarios_metodos.usuarios_plataformas
            ADD COLUMN hasta_personalidad TIMESTAMP;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'usuarios_metodos'
          AND table_name   = 'usuarios_plataformas'
          AND column_name  = 'hasta_fisicas'
    ) THEN
        ALTER TABLE usuarios_metodos.usuarios_plataformas
            ADD COLUMN hasta_fisicas TIMESTAMP;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'usuarios_metodos'
          AND table_name   = 'usuarios_plataformas'
          AND column_name  = 'disabled_personalidad'
    ) THEN
        ALTER TABLE usuarios_metodos.usuarios_plataformas
            ADD COLUMN disabled_personalidad BOOLEAN DEFAULT TRUE;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'usuarios_metodos'
          AND table_name   = 'usuarios_plataformas'
          AND column_name  = 'disabled_fisicas'
    ) THEN
        ALTER TABLE usuarios_metodos.usuarios_plataformas
            ADD COLUMN disabled_fisicas BOOLEAN DEFAULT TRUE;
    END IF;
END $$;

-- 5. Verificación final: mostrar la tabla creada
SELECT
    column_name,
    data_type,
    column_default,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'usuarios_metodos'
  AND table_name   = 'auto_altas_procesadas'
ORDER BY ordinal_position;
