CREATE PROCEDURE ObtenerAtencionesEspecialistas
    @IdNino INT = NULL,
    @Fecha DATE = NULL
AS
BEGIN
    SELECT * FROM AtencionesEspecialistas
    WHERE (@IdNino IS NULL OR IdNino = @IdNino)
      AND (@Fecha IS NULL OR Fecha = @Fecha);
END;

CREATE PROCEDURE InsertarAtencionEspecialista
    @IdNino INT,
    @Fecha DATE,
    @IdEspecialista INT,
    @Observaciones NVARCHAR(255)
AS
BEGIN
    INSERT INTO AtencionesEspecialistas (IdNino, Fecha, IdEspecialista, Observaciones)
    VALUES (@IdNino, @Fecha, @IdEspecialista, @Observaciones);
END;

CREATE PROCEDURE ActualizarAtencionEspecialista
    @IdAtencion INT,
    @IdNino INT,
    @Fecha DATE,
    @IdEspecialista INT,
    @Observaciones NVARCHAR(255)
AS
BEGIN
    UPDATE AtencionesEspecialistas
    SET IdNino = @IdNino,
        Fecha = @Fecha,
        IdEspecialista = @IdEspecialista,
        Observaciones = @Observaciones
    WHERE IdAtencion = @IdAtencion;
END;

CREATE PROCEDURE EliminarAtencionEspecialista
    @IdAtencion INT
AS
BEGIN
    DELETE FROM AtencionesEspecialistas WHERE IdAtencion = @IdAtencion;
END;
