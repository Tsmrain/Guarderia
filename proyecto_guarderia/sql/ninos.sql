CREATE PROCEDURE ObtenerNinos
    @NumeroMatricula INT = NULL  
AS
BEGIN
    SELECT * FROM Ninos
    WHERE (@NumeroMatricula IS NULL OR NumeroMatricula = @NumeroMatricula);
END;

CREATE PROCEDURE InsertarNino
    @NumeroMatricula INT,
    @Nombre NVARCHAR(100),
    @FechaNacimiento DATE,
    @FechaIngreso DATE,
    @Alergias NVARCHAR(255) = NULL
AS
BEGIN
    INSERT INTO Ninos (NumeroMatricula, Nombre, FechaNacimiento, FechaIngreso, Alergias)
    VALUES (@NumeroMatricula, @Nombre, @FechaNacimiento, @FechaIngreso, @Alergias);
END;

CREATE PROCEDURE ActualizarNino
    @IdNino INT,
    @NumeroMatricula INT,
    @Nombre NVARCHAR(100),
    @FechaNacimiento DATE,
    @FechaIngreso DATE,
    @FechaBaja DATE = NULL,
    @Alergias NVARCHAR(255) = NULL
AS
BEGIN
    UPDATE Ninos
    SET NumeroMatricula = @NumeroMatricula,
        Nombre = @Nombre,
        FechaNacimiento = @FechaNacimiento,
        FechaIngreso = @FechaIngreso,
        FechaBaja = @FechaBaja,
        Alergias = @Alergias
    WHERE IdNino = @IdNino;
END;

CREATE PROCEDURE EliminarNino
    @IdNino INT
AS
BEGIN
    DELETE FROM Ninos WHERE IdNino = @IdNino;
END;
