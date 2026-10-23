-- Base de datos propia para la actividad conjunta (microservicios + tokens)
CREATE DATABASE IF NOT EXISTS microservicios;
USE microservicios;

CREATE TABLE usuarios_token (
    usuario  VARCHAR(50) PRIMARY KEY,
    password VARCHAR(64) NOT NULL,  -- SHA-256 siempre ocupa 64 caracteres en hexadecimal
    token    VARCHAR(64),
    tiempo   DATETIME
);
