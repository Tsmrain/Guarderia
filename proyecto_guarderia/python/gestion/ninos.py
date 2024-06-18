import datetime
from entidades.nino import Nino
from database import connect_to_db, execute_query
from utils import clear_screen, wait_for_user, validar_fecha
from gestion.asistencias import obtener_asistencias
from gestion.servicios_adicionales import obtener_servicios_adicionales_por_nino
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

def obtener_ninos(conn, numero_matricula=None):
    """Obtiene la lista de niños, opcionalmente filtrada por número de matrícula."""
    query = "EXEC ObtenerNinos @NumeroMatricula=?"
    params = (numero_matricula,) if numero_matricula else None
    cursor = execute_query(conn, query, params)
    return [Nino(*row) for row in cursor]

def agregar_nino(conn):
    """Agrega un nuevo niño a la base de datos."""
    # ... (Código para obtener datos del niño, similar al proporcionado anteriormente) ...

def actualizar_nino(conn):
    """Actualiza los datos de un niño existente."""
    clear_screen()
    console.print("[bold blue]--------- Actualizar Niño ---------[/bold blue]")

    while True:
        numero_matricula = Prompt.ask("[bold green]Ingrese el número de matrícula del niño a actualizar[/bold green]")
        if not numero_matricula.isdigit():
            console.print("[bold red]El número de matrícula debe ser un número entero.[/bold red]")
            continue

        nino = obtener_ninos(conn, numero_matricula)
        if not nino:
            console.print("[bold red]No se encontró ningún niño con ese número de matrícula.[/bold red]")
            continue

        break

    nino = nino[0]  # Asumiendo que el número de matrícula es único
    # ... (Código para obtener nuevos datos del niño, similar al proporcionado anteriormente) ...

def eliminar_nino(conn):
    """Elimina un niño de la base de datos."""
    clear_screen()
    console.print("[bold blue]--------- Eliminar Niño ---------[/bold blue]")

    while True:
        numero_matricula = Prompt.ask("[bold green]Ingrese el número de matrícula del niño a eliminar[/bold green]")
        if not numero_matricula.isdigit():
            console.print("[bold red]El número de matrícula debe ser un número entero.[/bold red]")
            continue

        nino = obtener_ninos(conn, numero_matricula)
        if not nino:
            console.print("[bold red]No se encontró ningún niño con ese número de matrícula.[/bold red]")
            continue

        break

    nino = nino[0]  # Asumiendo que el número de matrícula es único

    if not Confirm.ask(f"[bold yellow]¿Estás seguro de que quieres eliminar al niño {nino.nombre} (ID: {nino.id})?[/bold yellow]"):
        return

    query = "EXEC EliminarNino ?"
    params = (nino.id,)
    execute_query(conn, query, params)
    console.print("[bold green]Niño eliminado exitosamente.[/bold green]")
    wait_for_user()

def calcular_costo_mensual(conn, id_nino, fecha_inicio, fecha_fin):
    """Calcula el costo mensual de un niño."""
    nino = obtener_ninos(conn, id_nino)[0]  # Obtener datos del niño

    # Obtener costo de matrícula
    query_matricula = "SELECT CostoMensual FROM Matriculas WHERE IdNino = ? AND FechaMatricula <= ? AND (FechaBaja IS NULL OR FechaBaja >= ?)"
    params_matricula = (id_nino, fecha_fin, fecha_inicio)
    cursor_matricula = execute_query(conn, query_matricula, params_matricula)
    costo_matricula = cursor_matricula.fetchone()[0] if cursor_matricula.fetchone() else 0

    # Obtener costo de asistencias (considerando el menú de cada día)
    asistencias = obtener_asistencias(conn, id_nino)
    asistencias_en_periodo = [a for a in asistencias if fecha_inicio <= a.fecha <= fecha_fin]
    costo_asistencias = sum(asistencia.costo_menu for asistencia in asistencias_en_periodo)

    # Obtener costo de servicios adicionales
    servicios_adicionales = obtener_servicios_adicionales_por_nino(conn, id_nino, fecha_inicio, fecha_fin)
    costo_servicios_adicionales = sum(servicio.costo for servicio in servicios_adicionales)

    costo_total = costo_matricula + costo_asistencias + costo_servicios_adicionales
    return costo_total
