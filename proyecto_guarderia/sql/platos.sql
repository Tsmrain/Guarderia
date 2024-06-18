CREATE PROCEDURE ObtenerPlatos
AS
BEGIN
    SELECT * FROM Platos;
END;

CREATE PROCEDURE InsertarPlato
    @Nombre NVARCHAR(100)
AS
BEGIN
    INSERT INTO Platos (Nombre)
    VALUES (@Nombre);
END;

CREATE PROCEDURE ActualizarPlato
    @IdPlato INT,
    @Nombre NVARCHAR(100)
AS
BEGIN
    UPDATE Platos
    SET Nombre = @Nombre
    WHERE IdPlato = @IdPlato;
END;

CREATE PROCEDURE EliminarPlato
    @IdPlato INT
AS
BEGIN
    DELETE FROM Platos WHERE IdPlato = @IdPlato;
END;
