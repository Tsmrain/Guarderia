CREATE PROCEDURE ObtenerMenus
    @Fecha DATE = NULL
AS
BEGIN
    SELECT * FROM Menus
    WHERE (@Fecha IS NULL OR Fecha = @Fecha);
END;

CREATE PROCEDURE InsertarMenu
    @Nombre NVARCHAR(100),
    @Fecha DATE
AS
BEGIN
    INSERT INTO Menus (Nombre, Fecha)
    VALUES (@Nombre, @Fecha);
END;

CREATE PROCEDURE ActualizarMenu
    @IdMenu INT,
    @Nombre NVARCHAR(100),
    @Fecha DATE
AS
BEGIN
    UPDATE Menus
    SET Nombre = @Nombre,
        Fecha = @Fecha
    WHERE IdMenu = @IdMenu;
END;

CREATE PROCEDURE EliminarMenu
    @IdMenu INT
AS
BEGIN
    DELETE FROM Menus WHERE IdMenu = @IdMenu;
END;
