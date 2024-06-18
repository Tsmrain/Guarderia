import datetime
from entidades.matricula import Matricula
from database import connect_to_db, execute_query
from python.gestion.asistencias import obtener_asistencias
from utils import clear_screen, wait_for_user, validar_fecha
from gestion.ninos import obtener_ninos
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

def obtener_matriculas(conn, id_nino=None):
    """Obtiene matrículas, filtradas por niño (opcional)."""
    query = "EXEC ObtenerMatriculas @IdNino=?"
    params = (id_nino,) if id_nino else None
    cursor = execute_query(conn, query, params)
    return [Matricula(*row) for row in cursor]

def agregar_matricula(conn):
    """Registra una nueva matrícula."""
    clear_screen()
    console.print("[bold blue]--------- Registrar Matrícula ---------[/bold blue]")

    # Obtener niño
    while True:
        ninos = obtener_ninos(conn)
        if not ninos:
            console.print("[bold red]No hay niños registrados. Registre un niño primero.[/bold red]")
            wait_for_user()
            return
        for i, nino in enumerate(ninos):
            console.print(f"{i+1}. {nino.nombre} (ID: {nino.id})")
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione el niño[/bold green]")) - 1
            id_nino = ninos[opcion].id
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    # Verificar si el niño ya tiene una matrícula activa
    matriculas_existentes = obtener_matriculas(conn, id_nino)
    for matricula in matriculas_existentes:
        if matricula.fecha_baja is None:
            console.print(f"[bold red]El niño {ninos[opcion].nombre} ya tiene una matrícula activa.[/bold red]")
            wait_for_user()
            return

    # Obtener fecha de matrícula (opcional, por defecto hoy)
    while True:
        fecha_matricula_str = Prompt.ask("[bold green]Ingrese la fecha de matrícula (YYYY-MM-DD, deje en blanco para hoy)[/bold green]")
        if not fecha_matricula_str:
            fecha_matricula = datetime.date.today()
            break
        elif validar_fecha(fecha_matricula_str):
            fecha_matricula = datetime.datetime.strptime(fecha_matricula_str, '%Y-%m-%d').date()
            break
        else:
            console.print("[bold red]Fecha inválida. Use el formato YYYY-MM-DD.[/bold red]")

    # Obtener costo mensual
    while True:
        try:
            costo_mensual = float(Prompt.ask("[bold green]Ingrese el costo mensual[/bold green]"))
            if costo_mensual <= 0:
                raise ValueError
            break
        except ValueError:
            console.print("[bold red]Costo inválido. Ingrese un número mayor a cero.[/bold red]")

    query = "EXEC InsertarMatricula ?, ?, ?"
    params = (id_nino, fecha_matricula, costo_mensual)
    execute_query(conn, query, params)
    console.print("[bold green]Matrícula registrada exitosamente.[/bold green]")
    wait_for_user()

def actualizar_matricula(conn):
    """Actualiza una matrícula existente."""
    clear_screen()
    console.print("[bold blue]--------- Actualizar Matrícula ---------[/bold blue]")

    # Obtener matrícula a actualizar
    matriculas = obtener_matriculas(conn)
    if not matriculas:
        console.print("[bold red]No hay matrículas registradas.[/bold red]")
        wait_for_user()
        return
    for i, matricula in enumerate(matriculas):
        console.print(f"{i+1}. Niño: {matricula.id_nino}, Fecha: {matricula.fecha_matricula}, Costo: {matricula.costo_mensual}")
    while True:
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione la matrícula a actualizar[/bold green]")) - 1
            matricula_a_actualizar = matriculas[opcion]
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    # Obtener nuevos datos de la matrícula
    while True:
        fecha_matricula_str = Prompt.ask(
            f"[bold green]Ingrese la nueva fecha de matrícula (YYYY-MM-DD, actual: {matricula_a_actualizar.fecha_matricula})[/bold green]")
        if not fecha_matricula_str:
            fecha_matricula = matricula_a_actualizar.fecha_matricula
            break
        elif validar_fecha(fecha_matricula_str):
            fecha_matricula = datetime.datetime.strptime(fecha_matricula_str, '%Y-%m-%d').date()
            break
        else:
            console.print("[bold red]Fecha inválida. Use el formato YYYY-MM-DD.[/bold red]")

    while True:
        try:
            costo_mensual_str = Prompt.ask(
                f"[bold green]Ingrese el nuevo costo mensual (actual: {matricula_a_actualizar.costo_mensual})[/bold green]")
            if not costo_mensual_str:
                costo_mensual = matricula_a_actualizar.costo_mensual
                break
            costo_mensual = float(costo_mensual_str)
            if costo_mensual <= 0:
                raise ValueError
            break
        except ValueError:
            console.print("[bold red]Costo inválido. Ingrese un número mayor a cero.[/bold red]")

    while True:
        fecha_baja_str = Prompt.ask(
            f"[bold green]Ingrese la nueva fecha de baja (YYYY-MM-DD, actual: {matricula_a_actualizar.fecha_baja})[/bold green]")
        if not fecha_baja_str:
            fecha_baja = matricula_a_actualizar.fecha_baja
            break
        elif validar_fecha(fecha_baja_str):
            fecha_baja = datetime.datetime.strptime(fecha_baja_str, '%Y-%m-%d').date()
            break
        else:
            console.print("[bold red]Fecha inválida. Use el formato YYYY-MM-DD.[/bold red]")

    query = "EXEC ActualizarMatricula ?, ?, ?, ?"
    params = (matricula_a_actualizar.id, fecha_matricula, costo_mensual, fecha_baja)
    execute_query(conn, query, params)
    console.print("[bold green]Matrícula actualizada exitosamente.[/bold green]")
    wait_for_user()


def eliminar_matricula(conn):
    """Elimina una matrícula existente."""
    clear_screen()
    console.print("[bold blue]--------- Eliminar Matrícula ---------[/bold blue]")

    # Obtener matrícula a eliminar
    matriculas = obtener_matriculas(conn)
    if not matriculas:
        console.print("[bold red]No hay matrículas registradas.[/bold red]")
        wait_for_user()
        return

    for i, matricula in enumerate(matriculas):
        console.print(f"{i+1}. Niño: {matricula.id_nino}, Fecha: {matricula.fecha_matricula}, Costo: {matricula.costo_mensual}")

    while True:
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione la matrícula a eliminar[/bold green]")) - 1
            matricula_a_eliminar = matriculas[opcion]
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    # Confirmar eliminación
    if not Confirm.ask(f"[bold yellow]¿Estás seguro de que quieres eliminar la matrícula del niño {matricula_a_eliminar.id_nino}?[/bold yellow]"):
        return

    # Verificar si hay asistencias asociadas a la matrícula
    asistencias = obtener_asistencias(conn, matricula_a_eliminar.id_nino)
    if asistencias:
        if not Confirm.ask(f"[bold yellow]La matrícula tiene asistencias asociadas. ¿Desea eliminarlas también? (s/n)[/bold yellow]"):
            return

        # Eliminar asistencias asociadas a la matrícula
        for asistencia in asistencias:
            query_eliminar_asistencia = "EXEC EliminarAsistencia ?"
            execute_query(conn, query_eliminar_asistencia, (asistencia.id,))

    # Eliminar la matrícula
    query = "EXEC EliminarMatricula ?"
    params = (matricula_a_eliminar.id,)
    execute_query(conn, query, params)
    console.print("[bold green]Matrícula eliminada exitosamente.[/bold green]")
    wait_for_user()
