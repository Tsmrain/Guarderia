CREATE PROCEDURE ObtenerConsumosTienda
    @IdNino INT = NULL,
    @Fecha DATE = NULL
AS
BEGIN
    SELECT * FROM ConsumosTienda
    WHERE (@IdNino IS NULL OR IdNino = @IdNino)
      AND (@Fecha IS NULL OR Fecha = @Fecha);
END;

CREATE PROCEDURE InsertarConsumoTienda
    @IdNino INT,
    @Fecha DATE,
    @IdProducto INT,
    @Cantidad INT
AS
BEGIN
    INSERT INTO ConsumosTienda (IdNino, Fecha, IdProducto, Cantidad)
    VALUES (@IdNino, @Fecha, @IdProducto, @Cantidad);
END;

CREATE PROCEDURE ActualizarConsumoTienda
    @IdConsumoTienda INT,
    @IdNino INT,
    @Fecha DATE,
    @IdProducto INT,
    @Cantidad INT
AS
BEGIN
    UPDATE ConsumosTienda
    SET IdNino = @IdNino,
        Fecha = @Fecha,
        IdProducto = @IdProducto,
        Cantidad = @Cantidad
    WHERE IdConsumoTienda = @IdConsumoTienda;
END;

CREATE PROCEDURE EliminarConsumoTienda
    @IdConsumoTienda INT
AS
BEGIN
    DELETE FROM ConsumosTienda
    WHERE IdConsumoTienda = @IdConsumoTienda;
END;
