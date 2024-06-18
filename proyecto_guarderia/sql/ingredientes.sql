CREATE PROCEDURE ObtenerIngredientes
AS
BEGIN
    SELECT * FROM Ingredientes;
END;

CREATE PROCEDURE InsertarIngrediente
    @Nombre NVARCHAR(100)
AS
BEGIN
    INSERT INTO Ingredientes (Nombre)
    VALUES (@Nombre);
END;

CREATE PROCEDURE ActualizarIngrediente
    @IdIngrediente INT,
    @Nombre NVARCHAR(100)
AS
BEGIN
    UPDATE Ingredientes
    SET Nombre = @Nombre
    WHERE IdIngrediente = @IdIngrediente;
END;

CREATE PROCEDURE EliminarIngrediente
    @IdIngrediente INT
AS
BEGIN
    DELETE FROM Ingredientes WHERE IdIngrediente = @IdIngrediente;
END;
