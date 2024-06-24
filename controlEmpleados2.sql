use master 

drop database ControlEmpleados2; 

create database ControlEmpleados2;

use ControlEmpleados2;

-- ------------------------------------------------ --
-- # Creacion de tablas 
-- ------------------------------------------------ --
drop table registro_empleados
-- Registro de empleados
-- Registro de empleados con estado de despedidos
CREATE TABLE registro_empleados (
    id_registro_personal INT IDENTITY(1,1) PRIMARY KEY,
    nombre_empleado VARCHAR(100) NOT NULL,
    apellidos_empleado VARCHAR(100) NOT NULL,
    dni_empleado CHAR(8) NOT NULL,
    sexo CHAR(1) NOT NULL,
    telefono CHAR(9) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    email VARCHAR(100),
    direccion VARCHAR(120),
    fecha_contrato DATE,
    estado VARCHAR(20) DEFAULT 'activo' -- Nuevo campo para el estado del empleado
);


-- Insertando registros de ejemplo en registro_empleados
INSERT INTO registro_empleados (nombre_empleado, apellidos_empleado, dni_empleado, sexo, telefono, fecha_nacimiento, email, direccion, fecha_contrato)
VALUES 
    ('Juan', 'Perez', '12345678', 'M', '123456789', '1990-05-15', 'juan@example.com', 'Calle 123', '2023-01-01'),
    ('Maria', 'Gonzalez', '87654321', 'F', '987654321', '1995-09-20', 'maria@example.com', 'Avenida 456', '2023-01-15'),
    ('Pedro', 'Lopez', '23456789', 'M', '123456789', '1992-08-25', 'pedro@example.com', 'Calle 789', '2023-02-01'),
    ('Ana', 'Martinez', '98765432', 'F', '987654321', '1997-11-10', 'ana@example.com', 'Avenida 1011', '2023-02-15');
select nombre_empleado, id_registro_personal from registro_empleados
-- Empleado
drop table empleado
CREATE TABLE empleado (
    id_empleado INT IDENTITY(1,1) PRIMARY KEY,
    id_registro_personal INT NOT NULL,
    CONSTRAINT unique_employee UNIQUE (id_registro_personal), 
    FOREIGN KEY (id_registro_personal) REFERENCES registro_empleados(id_registro_personal)
);

-- Insertando registros de ejemplo en empleado
INSERT INTO empleado (id_registro_personal)
VALUES 
    (1),
    (2),
    (3),
    (4);

CREATE TABLE fecha_carga (
    id_fecha_carga DATE PRIMARY KEY,
    hora_inicio TIME(0),
    hora_corte TIME(0)
);

INSERT INTO fecha_carga (id_fecha_carga, hora_inicio, hora_corte)
VALUES 
       ('2024-03-20', '08:00:00', '17:00:00'),
       ('2024-03-21', '09:00:00', '18:00:00'),
       ('2024-03-22', '07:30:00', '16:30:00'),
       ('2024-03-23', '10:30:00', '19:30:00'),
       ('2024-03-24', '08:15:00', '17:15:00'),
       ('2024-03-25', '09:45:00', '18:45:00'),
       ('2024-03-26', '07:00:00', '16:00:00'),
       ('2024-03-27', '11:00:00', '20:00:00'),
       ('2024-03-28', '08:30:00', '17:30:00'),
       ('2024-03-29', '09:30:00', '18:30:00'),
       ('2024-03-30', '07:45:00', '16:45:00'),
       ('2024-03-31', '10:45:00', '19:45:00'),
       ('2024-04-01', '08:00:00', '17:00:00'),
       ('2024-04-02', '09:00:00', '18:00:00'),
       ('2024-04-03', '07:30:00', '16:30:00'),
       ('2024-04-04', '10:30:00', '19:30:00'),
       ('2024-04-05', '08:15:00', '17:15:00'),
       ('2024-04-06', '09:45:00', '18:45:00'),
       ('2024-04-07', '07:00:00', '16:00:00'),
       ('2024-04-08', '11:00:00', '20:00:00');

-- Sistema de cargas
CREATE TABLE cargas (
    id_cargas int  IDENTITY(1,1) PRIMARY KEY , 
	hora_entrega TIME(0),
    peso_carga DECIMAL(4,2),
    id_empleado INT,
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
	id_fecha_carga date,
	foreign key (id_fecha_carga) references fecha_carga (id_fecha_carga)
);

-- --------------------------------------------------------------------- --
-- # Insercion de datos # --
-- --------------------------------------------------------------------- --
INSERT INTO cargas (hora_entrega, peso_carga, id_empleado, id_fecha_carga)
VALUES 
    ('08:00:00', 20.50, 1, '2024-03-20'),
    ('09:00:00', 50.75, 2, '2024-03-20'),
    ('10:00:00', 80.25, 3, '2024-03-20'),
    ('11:00:00', 30.00, 4, '2024-03-20'),
    ('12:00:00', 70.00, 2, '2024-03-20'),
    ('13:00:00', 45.50, 3, '2024-03-20'),
    ('14:00:00', 55.25, 4, '2024-03-20'),
    ('15:00:00', 40.75, 1, '2024-03-20'),
    ('16:00:00', 60.50, 3, '2024-03-20'),
    ('17:00:00', 90.25, 1, '2024-03-20'),
    ('18:00:00', 35.00, 4, '2024-03-20'),
    ('19:00:00', 25.75, 2, '2024-03-20'),
    ('20:00:00', 50.00, 4, '2024-03-20'),
    ('21:00:00', 65.25, 2, '2024-03-20'),
    ('22:00:00', 75.50, 1, '2024-03-20'),
    ('23:00:00', 85.25, 3, '2024-03-20'),

    ('08:00:00', 20.50, 1, '2024-03-21'),
    ('09:00:00', 50.75, 2, '2024-03-21'),
    ('10:00:00', 80.25, 3, '2024-03-21'),
    ('11:00:00', 30.00, 4, '2024-03-21'),
    ('12:00:00', 70.00, 2, '2024-03-21'),
    ('13:00:00', 45.50, 3, '2024-03-21'),
    ('14:00:00', 55.25, 4, '2024-03-21'),
    ('15:00:00', 40.75, 1, '2024-03-21'),
    ('16:00:00', 60.50, 3, '2024-03-21'),
    ('17:00:00', 90.25, 1, '2024-03-21'),
    ('18:00:00', 35.00, 4, '2024-03-21'),
    ('19:00:00', 25.75, 2, '2024-03-21'),
    ('20:00:00', 50.00, 4, '2024-03-21'),
    ('21:00:00', 65.25, 2, '2024-03-21'),
    ('22:00:00', 75.50, 1, '2024-03-21'),
    ('23:00:00', 85.25, 3, '2024-03-21'),

    ('08:00:00', 20.50, 1, '2024-03-22'),
    ('09:00:00', 50.75, 2, '2024-03-22'),
    ('10:00:00', 80.25, 3, '2024-03-22'),
    ('11:00:00', 30.00, 4, '2024-03-22'),
    ('12:00:00', 70.00, 2, '2024-03-22'),
    ('13:00:00', 45.50, 3, '2024-03-22'),
    ('14:00:00', 55.25, 4, '2024-03-22'),
    ('15:00:00', 40.75, 1, '2024-03-22'),
    ('16:00:00', 60.50, 3, '2024-03-22'),
    ('17:00:00', 90.25, 1, '2024-03-22'),
    ('18:00:00', 35.00, 4, '2024-03-22'),
    ('19:00:00', 25.75, 2, '2024-03-22'),
    ('20:00:00', 50.00, 4, '2024-03-22'),
    ('21:00:00', 65.25, 2, '2024-03-22');
go


CREATE TABLE Administrador (
    id INT PRIMARY KEY IDENTITY(1,1),
    usuario NVARCHAR(50) NOT NULL UNIQUE,
    contrasenia NVARCHAR(255) NOT NULL
);


CREATE TABLE Usuario (
    id INT PRIMARY KEY IDENTITY(1,1),
    usuario NVARCHAR(50) NOT NULL UNIQUE,
    contrasenia NVARCHAR(255) NOT NULL
);

-- ------------------------------------------- --
-- # LISTAdo de datos ------------------------
-------------------------------------------------

-- CORTE DEL DIA : listado de cargas que hicieron los empleados en un dia de cargas
SELECT e.nombre_empleado, e.apellidos_empleado, e.dni_empleado, c.id_cargas, c.peso_carga, c.id_fecha_carga, fc.hora_inicio, fc.hora_corte, c.hora_entrega
FROM empleado em
INNER JOIN registro_empleados e ON em.id_registro_personal = e.id_registro_personal
INNER JOIN cargas c ON em.id_empleado = c.id_empleado
INNER JOIN fecha_carga fc ON c.id_fecha_carga = fc.id_fecha_carga
WHERE c.id_fecha_carga = '2024-03-22'
ORDER BY c.id_cargas--e.nombre_empleado, e.apellidos_empleado;--
go  

-- PERFILES EMPLEADOS: listado de datos personales de los empleados
select * from registro_empleados order by id_registro_personal
go

-- ADMINISTRACION EMPLEADOS: listado de los empleados registrados
select nombre_empleado, apellidos_empleado, dni_empleado from registro_empleados order by id_registro_personal
go

-- HISTORIAL DE CARGAS
select * from fecha_carga
go

-- SEGUIMIENTO DE CARGA EMPLEADO: lista las cargas realizadas en un dia de un empleado
SELECT e.nombre_empleado, e.apellidos_empleado, e.dni_empleado, c.id_cargas, c.peso_carga, c.id_fecha_carga, fc.hora_inicio, fc.hora_corte, c.hora_entrega
FROM empleado em
INNER JOIN registro_empleados e ON em.id_registro_personal = e.id_registro_personal
INNER JOIN cargas c ON em.id_empleado = c.id_empleado
INNER JOIN fecha_carga fc ON c.id_fecha_carga = fc.id_fecha_carga
WHERE c.id_fecha_carga = '2024-03-22' -- Filtra por la fecha de carga deseada
AND em.id_empleado = 4 -- Filtra por el ID del empleado deseado
ORDER BY c.id_cargas;


-- Esto es lo que pondre en el query sql pero para el historial de empleados que hicieron la carga en una fecha
        SELECT e.nombre_empleado, e.apellidos_empleado, e.dni_empleado, c.peso_carga, c.id_fecha_carga, c.hora_entrega
        FROM empleado em
        INNER JOIN registro_empleados e ON em.id_registro_personal = e.id_registro_personal
        INNER JOIN cargas c ON em.id_empleado = c.id_empleado
        INNER JOIN fecha_carga fc ON c.id_fecha_carga = fc.id_fecha_carga
        WHERE c.id_fecha_carga = '2024-03-20'
        ORDER BY e.nombre_empleado;