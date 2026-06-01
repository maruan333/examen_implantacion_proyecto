CREATE DATABASE IF NOT EXISTS examen;
USE examen;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARBINARY(255) NOT NULL,
    es_admin BOOLEAN NOT NULL DEFAULT FALSE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(120) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(120) NOT NULL,
    fecha_nacimiento DATE NULL,
    titulacion VARCHAR(120) NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS asignaturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    codigo VARCHAR(60) UNIQUE NOT NULL,
    creditos INT NOT NULL,
    departamento VARCHAR(120) NULL,
    cuatrimestre VARCHAR(30) NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS matriculas (
    estudiante_id INT NOT NULL,
    asignatura_id INT NOT NULL,
    anio_academico VARCHAR(20) NULL,
    nota_final DECIMAL(4,2) NULL,
    fecha_matricula DATE DEFAULT (CURRENT_DATE),
    PRIMARY KEY (estudiante_id, asignatura_id),
    CONSTRAINT fk_matricula_estudiante FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_matricula_asignatura FOREIGN KEY (asignatura_id) REFERENCES asignaturas(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;
