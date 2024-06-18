CREATE PROCEDURE ObtenerServiciosAdicionales
AS
BEGIN
    SELECT * FROM ServiciosAdicionales;
END;

CREATE PROCEDURE InsertarServicioAdicional
    @Nombre NVARCHAR(100),
    @Costo DECIMAL(10,2)
AS
BEGIN
    INSERT INTO ServiciosAdicionales (Nombre, Costo)
    VALUES (@Nombre, @Costo);
END;

CREATE PROCEDURE ActualizarServicioAdicional
    @IdServicioAdicional INT,
    @Nombre NVARCHAR(100),
    @Costo DECIMAL(10,2)
AS
BEGIN
    UPDATE ServiciosAdicionales
    SET Nombre = @Nombre,
        Costo = @Costo
    WHERE IdServicioAdicional = @IdServicioAdicional;
END;

CREATE PROCEDURE EliminarServicioAdicional
    @IdServicioAdicional INT
AS
BEGIN
    DELETE FROM ServiciosAdicionales WHERE IdServicioAdicional = @IdServicioAdicional;
END;
