CREATE PROCEDURE ObtenerResponsablesPago
    @IdNino INT = NULL
AS
BEGIN
    SELECT * FROM ResponsablesPago
    WHERE (@IdNino IS NULL OR IdNino = @IdNino);
END;

CREATE PROCEDURE InsertarResponsablePago
    @IdNino INT,
    @CI VARCHAR(20),
    @Nombre NVARCHAR(100),
    @Direccion NVARCHAR(255),
    @Telefono VARCHAR(20),
    @NumeroCuentaCorriente VARCHAR(50)
AS
BEGIN
    INSERT INTO ResponsablesPago (IdNino, CI, Nombre, Direccion, Telefono, NumeroCuentaCorriente)
    VALUES (@IdNino, @CI, @Nombre, @Direccion, @Telefono, @NumeroCuentaCorriente);
END;

CREATE PROCEDURE ActualizarResponsablePago
    @IdResponsablePago INT,
    @IdNino INT,
    @CI VARCHAR(20),
    @Nombre NVARCHAR(100),
    @Direccion NVARCHAR(255),
    @Telefono VARCHAR(20),
    @NumeroCuentaCorriente VARCHAR(50)
AS
BEGIN
    UPDATE ResponsablesPago
    SET IdNino = @IdNino,
        CI = @CI,
        Nombre = @Nombre,
        Direccion = @Direccion,
        Telefono = @Telefono,
        NumeroCuentaCorriente = @NumeroCuentaCorriente
    WHERE IdResponsablePago = @IdResponsablePago;
END;

CREATE PROCEDURE EliminarResponsablePago
    @IdResponsablePago INT
AS
BEGIN
    DELETE FROM ResponsablesPago WHERE IdResponsablePago = @IdResponsablePago;
END;
