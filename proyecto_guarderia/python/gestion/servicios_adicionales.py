import datetime
from entidades.servicio_adicional import ServicioAdicional
from database import connect_to_db, execute_query
from utils import clear_screen, wait_for_user, validar_fecha
from gestion.ninos import obtener_ninos
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

def obtener_servicios_adicionales(conn):
    """Obtiene todos los servicios adicionales registrados."""
    query = "EXEC ObtenerServiciosAdicionales"
    cursor = execute_query(conn, query)
    return [ServicioAdicional(*row) for row in cursor]

def registrar_consumo_servicio_adicional(conn):
    """Registra el consumo de un servicio adicional por un niño."""
    clear_screen()
    console.print("[bold blue]--------- Registrar Consumo de Servicio Adicional ---------[/bold blue]")

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

    # Obtener servicio adicional
    while True:
        servicios = obtener_servicios_adicionales(conn)
        if not servicios:
            console.print("[bold red]No hay servicios adicionales registrados. Agregue un servicio primero.[/bold red]")
            wait_for_user()
            return
        for i, servicio in enumerate(servicios):
            console.print(f"{i+1}. {servicio.nombre} (Costo: {servicio.costo})")
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione el servicio adicional[/bold green]")) - 1
            id_servicio = servicios[opcion].id
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

    # Insertar consumo en la base de datos (usando la tabla ConsumosTienda)
    query = "EXEC InsertarConsumoTienda ?, ?, ?, ?"
    params = (id_nino, fecha, id_servicio, 1)  # Asumiendo que la cantidad es siempre 1
    execute_query(conn, query, params)
    console.print("[bold green]Consumo de servicio adicional registrado exitosamente.[/bold green]")
    wait_for_user()

# ... (otras importaciones)

def agregar_servicio_adicional(conn):
    """Agrega un nuevo servicio adicional."""
    clear_screen()
    console.print("[bold blue]--------- Agregar Servicio Adicional ---------[/bold blue]")

    nombre = Prompt.ask("[bold green]Ingrese el nombre del servicio adicional[/bold green]")

    while True:
        try:
            costo = float(Prompt.ask("[bold green]Ingrese el costo del servicio[/bold green]"))
            if costo <= 0:
                raise ValueError
            break
        except ValueError:
            console.print("[bold red]Costo inválido. Ingrese un número mayor a cero.[/bold red]")

    query = "EXEC InsertarServicioAdicional ?, ?"
    params = (nombre, costo)
    execute_query(conn, query, params)
    console.print("[bold green]Servicio adicional agregado exitosamente.[/bold green]")
    wait_for_user()

def actualizar_servicio_adicional(conn):
    """Actualiza un servicio adicional existente."""
    clear_screen()
    console.print("[bold blue]--------- Actualizar Servicio Adicional ---------[/bold blue]")

    servicios = obtener_servicios_adicionales(conn)
    if not servicios:
        console.print("[bold red]No hay servicios adicionales registrados.[/bold red]")
        wait_for_user()
        return

    for i, servicio in enumerate(servicios):
        console.print(f"{i+1}. {servicio.nombre} (Costo: {servicio.costo})")

    while True:
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione el servicio adicional a actualizar[/bold green]")) - 1
            servicio_a_actualizar = servicios[opcion]
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    nombre = Prompt.ask(f"[bold green]Ingrese el nuevo nombre (o presione Enter para mantener '{servicio_a_actualizar.nombre}')[/bold green]") or servicio_a_actualizar.nombre

    while True:
        try:
            costo_str = Prompt.ask(f"[bold green]Ingrese el nuevo costo (o presione Enter para mantener '{servicio_a_actualizar.costo}')[/bold green]")
            if not costo_str:
                costo = servicio_a_actualizar.costo
                break
            costo = float(costo_str)
            if costo <= 0:
                raise ValueError
            break
        except ValueError:
            console.print("[bold red]Costo inválido. Ingrese un número mayor a cero.[/bold red]")

    query = "EXEC ActualizarServicioAdicional ?, ?, ?"
    params = (servicio_a_actualizar.id, nombre, costo)
    execute_query(conn, query, params)
    console.print("[bold green]Servicio adicional actualizado exitosamente.[/bold green]")
    wait_for_user()

def eliminar_servicio_adicional(conn):
    """Elimina un servicio adicional existente."""
    clear_screen()
    console.print("[bold blue]--------- Eliminar Servicio Adicional ---------[/bold blue]")

    servicios = obtener_servicios_adicionales(conn)
    if not servicios:
        console.print("[bold red]No hay servicios adicionales registrados.[/bold red]")
        wait_for_user()
        return

    for i, servicio in enumerate(servicios):
        console.print(f"{i+1}. {servicio.nombre} (Costo: {servicio.costo})")

    while True:
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione el servicio adicional a eliminar[/bold green]")) - 1
            servicio_a_eliminar = servicios[opcion]
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    if not Confirm.ask(f"[bold yellow]¿Estás seguro de que quieres eliminar el servicio '{servicio_a_eliminar.nombre}'?[/bold yellow]"):
        return

    query = "EXEC EliminarServicioAdicional ?"
    params = (servicio_a_eliminar.id,)
    execute_query(conn, query, params)
    console.print("[bold green]Servicio adicional eliminado exitosamente.[/bold green]")
    wait_for_user()
