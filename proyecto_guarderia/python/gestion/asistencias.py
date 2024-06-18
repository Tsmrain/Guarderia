import datetime
from database import connect_to_db, execute_query
from utils import clear_screen, wait_for_user, validar_fecha
from gestion.ninos import obtener_ninos
from gestion.menus_alergias import obtener_menus
from rich.console import Console
from rich.prompt import Prompt, Confirm
from entidades.asistencia import Asistencia

console = Console()

def obtener_asistencias(conn, id_nino=None, fecha=None):
    """Obtiene asistencias, filtradas por niño y/o fecha."""
    query = "EXEC ObtenerAsistencias @IdNino=?, @Fecha=?"
    params = (id_nino, fecha) if id_nino or fecha else None
    cursor = execute_query(conn, query, params)
    return [Asistencia(*row) for row in cursor]

def agregar_asistencia(conn):
    """Registra una nueva asistencia."""
    clear_screen()
    console.print("[bold blue]--------- Registrar Asistencia ---------[/bold blue]")

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

    # Obtener menú
    while True:
        menus = obtener_menus(conn)
        if not menus:
            console.print("[bold red]No hay menús registrados. Registre un menú primero.[/bold red]")
            wait_for_user()
            return
        for i, menu in enumerate(menus):
            console.print(f"{i+1}. {menu.nombre} ({menu.fecha})")
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione el menú[/bold green]")) - 1
            id_menu = menus[opcion].id
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    # Obtener fecha (opcional, por defecto hoy)
    while True:
        fecha_str = Prompt.ask("[bold green]Ingrese la fecha (YYYY-MM-DD, deje en blanco para hoy)[/bold green]")
        if not fecha_str:
            fecha = datetime.date.today()
            break
        elif validar_fecha(fecha_str):
            fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
            break
        else:
            console.print("[bold red]Fecha inválida. Use el formato YYYY-MM-DD.[/bold red]")

    query = "EXEC InsertarAsistencia ?, ?, ?"
    params = (id_nino, fecha, id_menu)
    execute_query(conn, query, params)
    console.print("[bold green]Asistencia registrada exitosamente.[/bold green]")
    wait_for_user()

def actualizar_asistencia(conn):
    """Actualiza una asistencia existente."""
    clear_screen()
    console.print("[bold blue]--------- Actualizar Asistencia ---------[/bold blue]")
    asistencias = obtener_asistencias(conn)
    if not asistencias:
        console.print("[bold red]No hay asistencias registradas.[/bold red]")
        wait_for_user()
        return

    for i, asistencia in enumerate(asistencias):
        console.print(f"{i+1}. Niño: {asistencia.id_nino}, Fecha: {asistencia.fecha}, Menú: {asistencia.id_menu}")

    while True:
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione la asistencia a actualizar[/bold green]")) - 1
            asistencia_a_actualizar = asistencias[opcion]
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    # Obtener nuevo menú (opcional)
    while True:
        actualizar_menu = Prompt.ask("[bold green]¿Desea actualizar el menú? (s/n)[/bold green]").lower()
        if actualizar_menu in ['s', 'n']:
            break
        else:
            console.print("[bold red]Opción inválida. Ingrese 's' o 'n'.[/bold red]")

    if actualizar_menu == 's':
        # ... (Lógica similar a agregar_asistencia para obtener el nuevo menú)
        while True:
            menus = obtener_menus(conn)
            if not menus:
                console.print("[bold red]No hay menús registrados. Registre un menú primero.[/bold red]")
                wait_for_user()
                return
            for i, menu in enumerate(menus):
                console.print(f"{i+1}. {menu.nombre} ({menu.fecha})")
            try:
                opcion = int(Prompt.ask("[bold green]Seleccione el menú[/bold green]")) - 1
                id_menu = menus[opcion].id
                break
            except (ValueError, IndexError):
                console.print("[bold red]Opción inválida.[/bold red]")
    else:
        id_menu = None  # No actualizar el menú

    query = "EXEC ActualizarAsistencia ?, ?, ?"
    params = (asistencia_a_actualizar.id, id_menu)
    execute_query(conn, query, params)
    console.print("[bold green]Asistencia actualizada exitosamente.[/bold green]")
    wait_for_user()

def eliminar_asistencia(conn):
    """Elimina una asistencia existente."""
    clear_screen()
    console.print("[bold blue]--------- Eliminar Asistencia ---------[/bold blue]")

    asistencias = obtener_asistencias(conn)
    if not asistencias:
        console.print("[bold red]No hay asistencias registradas.[/bold red]")
        wait_for_user()
        return

    for i, asistencia in enumerate(asistencias):
        console.print(f"{i+1}. Niño: {asistencia.id_nino}, Fecha: {asistencia.fecha}, Menú: {asistencia.id_menu}")

    while True:
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione la asistencia a eliminar[/bold green]")) - 1
            asistencia_a_eliminar = asistencias[opcion]
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    if not Confirm.ask(f"[bold yellow]¿Estás seguro de que quieres eliminar esta asistencia?[/bold yellow]"):
        return

    query = "EXEC EliminarAsistencia ?"
    params = (asistencia_a_eliminar.id,)
    execute_query(conn, query, params)
    console.print("[bold green]Asistencia eliminada exitosamente.[/bold green]")
    wait_for_user()
