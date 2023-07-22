-- Crear la base de datos "osiris"
CREATE DATABASE IF NOT EXISTS osiris_web;

-- Usar la base de datos "osiris"
USE osiris_web;

-- Enlazar el archivo "tablas.sql" al final
SOURCE tablas.sql;
