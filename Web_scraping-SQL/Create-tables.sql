--------------------------------------------
-- TABLA DE ID, JUGADOR, EQUIPO, POSICION --
--------------------------------------------

USE BeyondStats;

-- Eliminar la tabla si existe
IF OBJECT_ID('ID_player_team', 'U') IS NOT NULL
    DROP TABLE ID_player_team;

-- Crear la tabla
CREATE TABLE ID_player_team (
    ID NVARCHAR(100) PRIMARY KEY,
    Jugador NVARCHAR(100),
    Equipo NVARCHAR(100),
    Posicion NVARCHAR(100)
);

-- Insertar datos en la tabla desde un archivo de texto
BULK INSERT ID_player_team
FROM 'C:\SQLData\BeyondStats\index_equipo_posicion.txt'
WITH
(
    DATAFILETYPE = 'widechar', -- Tipo de archivo de datos (UTF-16)
    CODEPAGE = '65001', -- Codificación UTF-8
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2 -- Si el archivo tiene encabezados, indica a qué fila comienzan los datos
);


--------------------------
-- TABLA STATS CLÁSICAS --
--------------------------
USE BeyondStats;

-- Eliminar la tabla si existe
IF OBJECT_ID('clasic_stats', 'U') IS NOT NULL
    DROP TABLE clasic_stats;

-- Crear la tabla
CREATE TABLE clasic_stats (
    ID NVARCHAR(100) PRIMARY KEY,
    Jugador NVARCHAR(100),
    [Minutos jugados] INT,
    [Partidos jugados] INT,
    [% Partidos jugados] DECIMAL(10, 2),
    [Partidos completos] INT,
    [% Partidos completos] DECIMAL(10, 2),
    [Partidos como titular] INT,
    [% Partidos como titular] DECIMAL(10, 2),
    [Partidos sustituido] INT,
    [% Partidos sustituido] DECIMAL(10, 2),
    [Tarjetas amarillas] INT,
    [Tarjetas rojas] INT,
    [Segundas amarillas] INT,
    [Goles] INT,
    [Penaltis recibidos] INT,
    [Goles en propia puerta] INT,
    [Goles en contra] INT
);

-- Insertar datos en la tabla desde un archivo de texto
BULK INSERT clasic_stats
FROM 'C:\SQLData\BeyondStats\clasic_stats.txt'
WITH
(
    DATAFILETYPE = 'char', -- Corregir tipo de archivo de datos
    CODEPAGE = '65001', -- Codificación UTF-8
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2 -- Si el archivo tiene encabezados, indica a qué fila comienzan los datos
);




---------------------------
-- TABLA STATS EFICIENCIA -
---------------------------
USE BeyondStats;

-- Eliminar la tabla si existe
IF OBJECT_ID('eficiencia_stats', 'U') IS NOT NULL
    DROP TABLE eficiencia_stats;

-- Crear la tabla
CREATE TABLE eficiencia_stats (
    ID NVARCHAR(100) PRIMARY KEY,
    Jugador NVARCHAR(100),
    [Córners lanzados] INT,
    [Entradas] INT,
    [Duelos] INT,
    [Duelos cuerpo a cuerpo] INT,
    [Duelos aéreos] INT,
    [Pases] INT,
    [Pases cortos] INT,
    [Pases largos] INT,
    [Pases al hueco] INT,
    [Goles por tiro] DECIMAL(10,2),
    [Goles por tiro fuera del área] DECIMAL(10,2),
    [Goles por tiro dentro del área] DECIMAL(10,2),
    [Goles con la pierna izquierda] DECIMAL(10,2),
    [Goles con la pierna derecha] DECIMAL(10,2),
    [Goles de cabeza] DECIMAL(10,2),
    [Goles a balón parado] DECIMAL(10,2)
);

-- Insertar datos en la tabla desde un archivo de texto
BULK INSERT eficiencia_stats
FROM 'C:\SQLData\BeyondStats\eficiencia_stats.txt'
WITH
(
    DATAFILETYPE = 'char', -- Corregir tipo de archivo de datos
    CODEPAGE = '65001', -- Codificación UTF-8
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2 -- Si el archivo tiene encabezados, indica a qué fila comienzan los datos
);


---------------------------
-- TABLA STATS DISCIPLINA -
---------------------------
USE BeyondStats;

-- Eliminar la tabla si existe
IF OBJECT_ID('disciplina_stats', 'U') IS NOT NULL
    DROP TABLE disciplina_stats;

-- Crear la tabla
CREATE TABLE disciplina_stats (
    ID NVARCHAR(100) PRIMARY KEY,
    Jugador NVARCHAR(100),
    [Tarjetas amarillas] INT,
    [Tarjetas rojas] INT,
    [Segundas amarillas] INT,
    [Fueras de juego] INT,
    [Faltas recibidas] INT,
    [Faltas cometidas] INT,
    [Penaltis recibidos] INT,
    [Penaltis en contra] INT,
    [Manos] INT,
    [Faltas por tarjeta] DECIMAL(10,2)
);

-- Insertar datos en la tabla desde un archivo de texto
BULK INSERT disciplina_stats
FROM 'C:\SQLData\BeyondStats\disciplina_stats.txt'
WITH
(
    DATAFILETYPE = 'char', -- Corregir tipo de archivo de datos
    CODEPAGE = '65001', -- Codificación UTF-8
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2 -- Si el archivo tiene encabezados, indica a qué fila comienzan los datos
);




---------------------------
-- TABLA STATS ATAQUES ----
---------------------------
USE BeyondStats;

-- Eliminar la tabla si existe
IF OBJECT_ID('ataques_stats', 'U') IS NOT NULL
    DROP TABLE ataques_stats;

-- Crear la tabla
CREATE TABLE ataques_stats (
    ID NVARCHAR(100) PRIMARY KEY,
    Jugador NVARCHAR(100),
    [Disparos] INT,
    [Disparos a puerta] INT,
    [Asistencias] INT,
    [Regates con éxito] INT,
    [Regates fallidos] INT,
    [Goles] INT,
    [Goles desde dentro del área] INT,
    [Goles desde fuera del área] INT,
    [Goles con la pierna izquierda] DECIMAL(10,2),
    [Goles con la pierna derecha] DECIMAL(10,2),
    [Goles de penalti] INT,
    [Goles de cabeza] DECIMAL(10,2),
    [Goles a balón parado] INT,
    [Goles en propia puerta] INT
);

-- Insertar datos en la tabla desde un archivo de texto
BULK INSERT ataques_stats
FROM 'C:\SQLData\BeyondStats\ataques_stats.txt'
WITH
(
    DATAFILETYPE = 'char', -- Corregir tipo de archivo de datos
    CODEPAGE = '65001', -- Codificación UTF-8
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2 -- Si el archivo tiene encabezados, indica a qué fila comienzan los datos
);




---------------------------
-- TABLA STATS DEFENSIVAS -
---------------------------
USE BeyondStats;

-- Eliminar la tabla si existe
IF OBJECT_ID('defensivas_stats', 'U') IS NOT NULL
    DROP TABLE defensivas_stats;

-- Crear la tabla
CREATE TABLE defensivas_stats (
    ID NVARCHAR(100) PRIMARY KEY,
    Jugador NVARCHAR(100),
    [Bloqueos] INT,
    [Intercepciones] INT,
    [Recuperaciones] INT,
    [Despejes] INT,
    [Entradas con éxito] INT,
    [Entradas fallidas] INT,
    [Jugadas como último hombre] INT,
    [Duelos con éxito] INT,
    [Duelos fallidos] INT,
    [Duelos aéreos con éxito] INT,
    [Duelos aéreos fallidos] INT
);

-- Insertar datos en la tabla desde un archivo de texto
BULK INSERT defensivas_stats
FROM 'C:\SQLData\BeyondStats\defensivas_stats.txt'
WITH
(
    DATAFILETYPE = 'char', -- Corregir tipo de archivo de datos
    CODEPAGE = '65001', -- Codificación UTF-8
    FIELDTERMINATOR = ';',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2 -- Si el archivo tiene encabezados, indica a qué fila comienzan los datos
);