-- =============================================
-- Sistema de Gestion de Tareas Personales
-- Script de creacion de base de datos y tablas
-- =============================================

-- Si la base ya existe la elimina, para poder correr este script
-- las veces que haga falta mientras desarrollamos (empezar de cero).
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'TaskManagerDB')
BEGIN
    ALTER DATABASE TaskManagerDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE TaskManagerDB;
END
GO

CREATE DATABASE TaskManagerDB;
GO

USE TaskManagerDB;
GO

-- ---------------------------------------------
-- Tabla: usuarios
-- ---------------------------------------------
CREATE TABLE usuarios (
    id_usuario      INT IDENTITY(1,1) PRIMARY KEY,
    nombre_usuario  VARCHAR(50)  NOT NULL UNIQUE,
    nombre_completo VARCHAR(100) NOT NULL,
    email           VARCHAR(100) NOT NULL UNIQUE,
    fecha_registro  DATETIME     NOT NULL DEFAULT GETDATE()
);
GO

-- ---------------------------------------------
-- Tabla: categorias
-- ---------------------------------------------
CREATE TABLE categorias (
    id_categoria INT IDENTITY(1,1) PRIMARY KEY,
    nombre       VARCHAR(50) NOT NULL UNIQUE,
    descripcion  VARCHAR(200) NULL
);
GO

-- ---------------------------------------------
-- Tabla: tareas
-- ---------------------------------------------
CREATE TABLE tareas (
    id_tarea      INT IDENTITY(1,1) PRIMARY KEY,
    titulo        VARCHAR(100)  NOT NULL,
    descripcion   VARCHAR(500)  NULL,
    prioridad     VARCHAR(10)   NOT NULL DEFAULT 'Media',
    fecha_limite  DATE          NULL,
    estado        VARCHAR(20)   NOT NULL DEFAULT 'Pendiente',
    fecha_creacion DATETIME     NOT NULL DEFAULT GETDATE(),
    id_usuario    INT           NOT NULL,
    id_categoria  INT           NULL,

    CONSTRAINT FK_tareas_usuarios
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    CONSTRAINT FK_tareas_categorias
        FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),

    CONSTRAINT CK_tareas_prioridad
        CHECK (prioridad IN ('Alta', 'Media', 'Baja')),
    CONSTRAINT CK_tareas_estado
        CHECK (estado IN ('Pendiente', 'En progreso', 'Completada'))
);
GO

-- ---------------------------------------------
-- Datos de ejemplo
-- ---------------------------------------------
INSERT INTO usuarios (nombre_usuario, nombre_completo, email) VALUES
    ('rcanico', 'Raul Canico', 'raccanico03@gmail.com'),
    ('jperez',  'Juan Perez',  'jperez@example.com');
GO

INSERT INTO categorias (nombre, descripcion) VALUES
    ('Estudio',  'Tareas relacionadas con la facultad y cursos'),
    ('Trabajo',  'Tareas laborales y profesionales'),
    ('Personal', 'Tareas de la vida personal y hogar');
GO

INSERT INTO tareas (titulo, descripcion, prioridad, fecha_limite, estado, id_usuario, id_categoria) VALUES
    ('Terminar TP de Bases de Datos', 'Entregar el modelo relacional',        'Alta',  DATEADD(DAY, 3,  GETDATE()), 'En progreso', 1, 1),
    ('Preparar entrevista tecnica',   'Repasar estructuras de datos',        'Alta',  DATEADD(DAY, 1,  GETDATE()), 'Pendiente',   1, 2),
    ('Actualizar CV',                 'Agregar el proyecto Task Manager',    'Media', DATEADD(DAY, 7,  GETDATE()), 'Pendiente',   1, 2),
    ('Pagar servicios',               'Luz, agua e internet',                'Baja',  DATEADD(DAY, -2, GETDATE()), 'Pendiente',   1, 3),
    ('Repasar SQL para la materia',   'Joins, subconsultas y vistas',        'Media', DATEADD(DAY, -1, GETDATE()), 'Completada',  2, 1);
GO
