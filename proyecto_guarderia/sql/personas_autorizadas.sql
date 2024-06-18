CREATE PROCEDURE ObtenerPersonasAutorizadas
    @IdNino INT = NULL
AS
BEGIN
    SELECT * FROM PersonasAutorizadas
    WHERE (@IdNino IS NULL OR IdNino = @IdNino);
END;

CREATE PROCEDURE InsertarPersonaAutorizada
    @IdNino INT,
    @CI VARCHAR(20),
    @Nombre NVARCHAR(100),
    @Direccion NVARCHAR(255),
    @Telefono VARCHAR(20),
    @RelacionConNino NVARCHAR(50)
AS
BEGIN
    INSERT INTO PersonasAutorizadas (IdNino, CI, Nombre, Direccion, Telefono, RelacionConNino)
    VALUES (@IdNino, @CI, @Nombre, @Direccion, @Telefono, @RelacionConNino);
END;

CREATE PROCEDURE ActualizarPersonaAutorizada
    @IdPersonaAutorizada INT,
    @IdNino INT,
    @CI VARCHAR(20),
    @Nombre NVARCHAR(100),
    @Direccion NVARCHAR(255),
    @Telefono VARCHAR(20),
    @RelacionConNino NVARCHAR(50)
AS
BEGIN
    UPDATE PersonasAutorizadas
    SET IdNino = @IdNino,
        CI = @CI,
        Nombre = @Nombre,
        Direccion = @Direccion,
        Telefono = @Telefono,
        RelacionConNino = @RelacionConNino
    WHERE IdPersonaAutorizada = @IdPersonaAutorizada;
END;

CREATE PROCEDURE EliminarPersonaAutorizada
    @IdPersonaAutorizada INT
AS
BEGIN
    DELETE FROM PersonasAutorizadas WHERE IdPersonaAutorizada = @IdPersonaAutorizada;
END;
