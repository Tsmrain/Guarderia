CREATE PROCEDURE ObtenerMatriculas
    @IdNino INT = NULL
AS
BEGIN
    SELECT * FROM Matriculas
    WHERE (@IdNino IS NULL OR IdNino = @IdNino);
END;

CREATE PROCEDURE InsertarMatricula
    @IdNino INT,
    @FechaMatricula DATE,
    @CostoMensual DECIMAL(10,2)
AS
BEGIN
    INSERT INTO Matriculas (IdNino, FechaMatricula, CostoMensual)
    VALUES (@IdNino, @FechaMatricula, @CostoMensual);
END;

CREATE PROCEDURE ActualizarMatricula
    @IdMatricula INT,
    @IdNino INT,
    @FechaMatricula DATE,
    @CostoMensual DECIMAL(10,2)
AS
BEGIN
    UPDATE Matriculas
    SET IdNino = @IdNino,
        FechaMatricula = @FechaMatricula,
        CostoMensual = @CostoMensual
    WHERE IdMatricula = @IdMatricula;
END;

CREATE PROCEDURE EliminarMatricula
    @IdMatricula INT
AS
BEGIN
    DELETE FROM Matriculas WHERE IdMatricula = @IdMatricula;
END;
