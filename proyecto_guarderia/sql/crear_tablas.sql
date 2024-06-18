-- Eliminar tablas si existen
DROP TABLE IF EXISTS AtencionesEspecialistas;
DROP TABLE IF EXISTS ConsumosTienda;
DROP TABLE IF EXISTS Asistencias;
DROP TABLE IF EXISTS ServiciosAdicionales;
DROP TABLE IF EXISTS Platos_Ingredientes;
DROP TABLE IF EXISTS Ingredientes;
DROP TABLE IF EXISTS Platos;
DROP TABLE IF EXISTS Menus;
DROP TABLE IF EXISTS ResponsablesPago;
DROP TABLE IF EXISTS PersonasAutorizadas;
DROP TABLE IF EXISTS Matriculas;
DROP TABLE IF EXISTS Ninos;
DROP TABLE IF EXISTS Especialistas;
DROP TABLE IF EXISTS Productos;

-- Crear tabla Niños
CREATE TABLE Ninos (
    IdNino INT IDENTITY(1,1) PRIMARY KEY,
    NumeroMatricula INT UNIQUE NOT NULL,
    Nombre NVARCHAR(100) NOT NULL,
    FechaNacimiento DATE NOT NULL,
    FechaIngreso DATE NOT NULL,
    FechaBaja DATE NULL,
    Alergias NVARCHAR(255)
);

-- Crear tabla Matrículas
CREATE TABLE Matriculas (
    IdMatricula INT IDENTITY(1,1) PRIMARY KEY,
    IdNino INT NOT NULL FOREIGN KEY REFERENCES Ninos(IdNino),
    FechaMatricula DATE NOT NULL,
    CostoMensual DECIMAL(10,2) NOT NULL
);

-- Crear tabla Personas Autorizadas
CREATE TABLE PersonasAutorizadas (
    IdPersonaAutorizada INT IDENTITY(1,1) PRIMARY KEY,
    IdNino INT NOT NULL FOREIGN KEY REFERENCES Ninos(IdNino),
    CI VARCHAR(20) UNIQUE NOT NULL,
    Nombre NVARCHAR(100) NOT NULL,
    Direccion NVARCHAR(255) NOT NULL,
    Telefono VARCHAR(20) NOT NULL,
    RelacionConNino NVARCHAR(50) NOT NULL
);

-- Crear tabla Responsables de Pago
CREATE TABLE ResponsablesPago (
    IdResponsablePago INT IDENTITY(1,1) PRIMARY KEY,
    IdNino INT NOT NULL FOREIGN KEY REFERENCES Ninos(IdNino),
    CI VARCHAR(20) UNIQUE NOT NULL,
    Nombre NVARCHAR(100) NOT NULL,
    Direccion NVARCHAR(255) NOT NULL,
    Telefono VARCHAR(20) NOT NULL,
    NumeroCuentaCorriente VARCHAR(50) NOT NULL
);

-- Crear tabla Menús
CREATE TABLE Menus (
    IdMenu INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL,
    Fecha DATE NOT NULL
);

-- Crear tabla Platos
CREATE TABLE Platos (
    IdPlato INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL
);

-- Crear tabla Ingredientes
CREATE TABLE Ingredientes (
    IdIngrediente INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL
);

-- Crear tabla Platos_Ingredientes (Relación muchos a muchos entre Platos e Ingredientes)
CREATE TABLE Platos_Ingredientes (
    IdPlato INT NOT NULL FOREIGN KEY REFERENCES Platos(IdPlato),
    IdIngrediente INT NOT NULL FOREIGN KEY REFERENCES Ingredientes(IdIngrediente),
    PRIMARY KEY (IdPlato, IdIngrediente)
);

-- Crear tabla Servicios Adicionales
CREATE TABLE ServiciosAdicionales (
    IdServicioAdicional INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL,
    Costo DECIMAL(10,2) NOT NULL
);

-- Crear tabla Especialistas
CREATE TABLE Especialistas (
    IdEspecialista INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL,
    Especialidad NVARCHAR(100) NOT NULL,
    CostoConsulta DECIMAL(10,2) NOT NULL
);

-- Crear tabla Productos
CREATE TABLE Productos (
    IdProducto INT IDENTITY(1,1) PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL,
    Precio DECIMAL(10,2) NOT NULL,
    StockMinimo INT NOT NULL
);

-- Crear tabla Asistencias
CREATE TABLE Asistencias (
    IdAsistencia INT IDENTITY(1,1) PRIMARY KEY,
    IdNino INT NOT NULL FOREIGN KEY REFERENCES Ninos(IdNino),
    Fecha DATE NOT NULL,
    IdMenu INT NOT NULL FOREIGN KEY REFERENCES Menus(IdMenu)
);

-- Crear tabla Consumos en Tienda
CREATE TABLE ConsumosTienda (
    IdConsumoTienda INT IDENTITY(1,1) PRIMARY KEY,
    IdNino INT NOT NULL FOREIGN KEY REFERENCES Ninos(IdNino),
    Fecha DATE NOT NULL,
    IdProducto INT NOT NULL FOREIGN KEY REFERENCES Productos(IdProducto),
    Cantidad INT NOT NULL
);

-- Crear tabla Atenciones por Especialistas
CREATE TABLE AtencionesEspecialistas (
    IdAtencion INT IDENTITY(1,1) PRIMARY KEY,
    IdNino INT NOT NULL FOREIGN KEY REFERENCES Ninos(IdNino),
    Fecha DATE NOT NULL,
    IdEspecialista INT NOT NULL FOREIGN KEY REFERENCES Especialistas(IdEspecialista),
    Observaciones NVARCHAR(255)
);
