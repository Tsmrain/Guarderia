from entidades.responsable_pago import ResponsablePago
from database import connect_to_db, execute_query
from utils import clear_screen, wait_for_user
from gestion.ninos import obtener_ninos
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

def obtener_responsables_pago(conn, id_nino=None):
    """Obtiene responsables de pago, filtrados por niño (opcional)."""
    query = "EXEC ObtenerResponsablesPago @IdNino=?"
    params = (id_nino,) if id_nino else None
    cursor = execute_query(conn, query, params)
    return [ResponsablePago(*row) for row in cursor]

def agregar_responsable_pago(conn):
    """Agrega un nuevo responsable de pago."""
    clear_screen()
    console.print("[bold blue]--------- Agregar Responsable de Pago ---------[/bold blue]")

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

    # Obtener datos del responsable de pago
    ci = Prompt.ask("[bold green]Ingrese el CI del responsable de pago[/bold green]")
    nombre = Prompt.ask("[bold green]Ingrese el nombre del responsable de pago[/bold green]")
    direccion = Prompt.ask("[bold green]Ingrese la dirección[/bold green]")
    telefono = Prompt.ask("[bold green]Ingrese el teléfono[/bold green]")
    numero_cuenta_corriente = Prompt.ask("[bold green]Ingrese el número de cuenta corriente[/bold green]")

    # Insertar responsable de pago en la base de datos
    query = "EXEC InsertarResponsablePago ?, ?, ?, ?, ?, ?"
    params = (id_nino, ci, nombre, direccion, telefono, numero_cuenta_corriente)
    execute_query(conn, query, params)
    console.print("[bold green]Responsable de pago agregado exitosamente.[/bold green]")
    wait_for_user()

def actualizar_responsable_pago(conn):
    """Actualiza los datos de un responsable de pago existente."""
    clear_screen()
    console.print("[bold blue]--------- Actualizar Responsable de Pago ---------[/bold blue]")

    # Obtener responsable de pago a actualizar
    responsables_pago = obtener_responsables_pago(conn)
    if not responsables_pago:
        console.print("[bold red]No hay responsables de pago registrados.[/bold red]")
        wait_for_user()
        return

    for i, responsable in enumerate(responsables_pago):
        console.print(f"{i+1}. {responsable.nombre} (CI: {responsable.ci})")

    while True:
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione el responsable de pago a actualizar[/bold green]")) - 1
            responsable_a_actualizar = responsables_pago[opcion]
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    # Obtener nuevos datos del responsable de pago
    nombre = Prompt.ask(f"[bold green]Ingrese el nuevo nombre (o presione Enter para mantener '{responsable_a_actualizar.nombre}')[/bold green]") or responsable_a_actualizar.nombre
    direccion = Prompt.ask(f"[bold green]Ingrese la nueva dirección (o presione Enter para mantener '{responsable_a_actualizar.direccion}')[/bold green]") or responsable_a_actualizar.direccion
    telefono = Prompt.ask(f"[bold green]Ingrese el nuevo teléfono (o presione Enter para mantener '{responsable_a_actualizar.telefono}')[/bold green]") or responsable_a_actualizar.telefono
    numero_cuenta_corriente = Prompt.ask(f"[bold green]Ingrese el nuevo número de cuenta corriente (o presione Enter para mantener '{responsable_a_actualizar.numero_cuenta_corriente}')[/bold green]") or responsable_a_actualizar.numero_cuenta_corriente

    # Actualizar responsable de pago en la base de datos
    query = "EXEC ActualizarResponsablePago ?, ?, ?, ?, ?, ?"
    params = (responsable_a_actualizar.id, responsable_a_actualizar.id_nino, responsable_a_actualizar.ci, nombre, direccion, telefono, numero_cuenta_corriente)
    execute_query(conn, query, params)
    console.print("[bold green]Responsable de pago actualizado exitosamente.[/bold green]")
    wait_for_user()

def eliminar_responsable_pago(conn):
    """Elimina un responsable de pago existente."""
    clear_screen()
    console.print("[bold blue]--------- Eliminar Responsable de Pago ---------[/bold blue]")

    # Obtener responsable de pago a eliminar
    responsables_pago = obtener_responsables_pago(conn)
    if not responsables_pago:
        console.print("[bold red]No hay responsables de pago registrados.[/bold red]")
        wait_for_user()
        return

    for i, responsable in enumerate(responsables_pago):
        console.print(f"{i+1}. {responsable.nombre} (CI: {responsable.ci})")

    while True:
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione el responsable de pago a eliminar[/bold green]")) - 1
            responsable_a_eliminar = responsables_pago[opcion]
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    # Confirmar eliminación
    if not Confirm.ask(f"[bold yellow]¿Estás seguro de que quieres eliminar a {responsable_a_eliminar.nombre} (CI: {responsable_a_eliminar.ci})?[/bold yellow]"):
        return

    query = "EXEC EliminarResponsablePago ?"
    params = (responsable_a_eliminar.id,)
    execute_query(conn, query, params)
    console.print("[bold green]Responsable de pago eliminado exitosamente.[/bold green]")
    wait_for_user()
