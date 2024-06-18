CREATE PROCEDURE ObtenerAsistencias
    @IdNino INT = NULL,
    @Fecha DATE = NULL
AS
BEGIN
    SELECT * FROM Asistencias
    WHERE (@IdNino IS NULL OR IdNino = @IdNino)
      AND (@Fecha IS NULL OR Fecha = @Fecha);
END;

CREATE PROCEDURE InsertarAsistencia
    @IdNino INT,
    @Fecha DATE,
    @IdMenu INT
AS
BEGIN
    INSERT INTO Asistencias (IdNino, Fecha, IdMenu)
    VALUES (@IdNino, @Fecha, @IdMenu);
END;

CREATE PROCEDURE ActualizarAsistencia
    @IdAsistencia INT,
    @IdNino INT,
    @Fecha DATE,
    @IdMenu INT
AS
BEGIN
    UPDATE Asistencias
    SET IdNino = @IdNino,
        Fecha = @Fecha,
        IdMenu = @IdMenu
    WHERE IdAsistencia = @IdAsistencia;
END;

CREATE PROCEDURE EliminarAsistencia
    @IdAsistencia INT
AS
BEGIN
    DELETE FROM Asistencias WHERE IdAsistencia = @IdAsistencia;
END;
