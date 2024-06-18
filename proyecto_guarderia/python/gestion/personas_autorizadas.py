from entidades.persona_autorizada import PersonaAutorizada
from database import connect_to_db, execute_query
from utils import clear_screen, wait_for_user
from gestion.ninos import obtener_ninos
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

def obtener_personas_autorizadas(conn, id_nino=None):
    """Obtiene personas autorizadas, filtradas por niño (opcional)."""
    query = "EXEC ObtenerPersonasAutorizadas @IdNino=?"
    params = (id_nino,) if id_nino else None
    cursor = execute_query(conn, query, params)
    return [PersonaAutorizada(*row) for row in cursor]

def agregar_persona_autorizada(conn):
    """Agrega una nueva persona autorizada."""
    clear_screen()
    console.print("[bold blue]--------- Agregar Persona Autorizada ---------[/bold blue]")

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

    # Obtener datos de la persona autorizada
    ci = Prompt.ask("[bold green]Ingrese el CI de la persona autorizada[/bold green]")
    nombre = Prompt.ask("[bold green]Ingrese el nombre de la persona autorizada[/bold green]")
    direccion = Prompt.ask("[bold green]Ingrese la dirección[/bold green]")
    telefono = Prompt.ask("[bold green]Ingrese el teléfono[/bold green]")
    relacion_con_nino = Prompt.ask("[bold green]Ingrese la relación con el niño[/bold green]")

    # Insertar persona autorizada en la base de datos
    query = "EXEC InsertarPersonaAutorizada ?, ?, ?, ?, ?, ?"
    params = (id_nino, ci, nombre, direccion, telefono, relacion_con_nino)
    execute_query(conn, query, params)
    console.print("[bold green]Persona autorizada agregada exitosamente.[/bold green]")
    wait_for_user()

def actualizar_persona_autorizada(conn):
    """Actualiza los datos de una persona autorizada existente."""
    clear_screen()
    console.print("[bold blue]--------- Actualizar Persona Autorizada ---------[/bold blue]")

    # Obtener persona autorizada a actualizar
    personas_autorizadas = obtener_personas_autorizadas(conn)
    if not personas_autorizadas:
        console.print("[bold red]No hay personas autorizadas registradas.[/bold red]")
        wait_for_user()
        return

    for i, persona in enumerate(personas_autorizadas):
        console.print(f"{i+1}. {persona.nombre} (CI: {persona.ci})")

    while True:
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione la persona autorizada a actualizar[/bold green]")) - 1
            persona_a_actualizar = personas_autorizadas[opcion]
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    # Obtener nuevos datos de la persona autorizada
    nombre = Prompt.ask(f"[bold green]Ingrese el nuevo nombre (o presione Enter para mantener '{persona_a_actualizar.nombre}')[/bold green]") or persona_a_actualizar.nombre
    direccion = Prompt.ask(f"[bold green]Ingrese la nueva dirección (o presione Enter para mantener '{persona_a_actualizar.direccion}')[/bold green]") or persona_a_actualizar.direccion
    telefono = Prompt.ask(f"[bold green]Ingrese el nuevo teléfono (o presione Enter para mantener '{persona_a_actualizar.telefono}')[/bold green]") or persona_a_actualizar.telefono
    relacion_con_nino = Prompt.ask(f"[bold green]Ingrese la nueva relación con el niño (o presione Enter para mantener '{persona_a_actualizar.relacion_con_nino}')[/bold green]") or persona_a_actualizar.relacion_con_nino

    # Actualizar persona autorizada en la base de datos
    query = "EXEC ActualizarPersonaAutorizada ?, ?, ?, ?, ?, ?"
    params = (persona_a_actualizar.id, persona_a_actualizar.id_nino, persona_a_actualizar.ci, nombre, direccion, telefono, relacion_con_nino)
    execute_query(conn, query, params)
    console.print("[bold green]Persona autorizada actualizada exitosamente.[/bold green]")
    wait_for_user()

def eliminar_persona_autorizada(conn):
    """Elimina una persona autorizada existente."""
    clear_screen()
    console.print("[bold blue]--------- Eliminar Persona Autorizada ---------[/bold blue]")

    # Obtener persona autorizada a eliminar
    personas_autorizadas = obtener_personas_autorizadas(conn)
    if not personas_autorizadas:
        console.print("[bold red]No hay personas autorizadas registradas.[/bold red]")
        wait_for_user()
        return

    for i, persona in enumerate(personas_autorizadas):
        console.print(f"{i+1}. {persona.nombre} (CI: {persona.ci})")

    while True:
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione la persona autorizada a eliminar[/bold green]")) - 1
            persona_a_eliminar = personas_autorizadas[opcion]
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    # Confirmar eliminación
    if not Confirm.ask(f"[bold yellow]¿Estás seguro de que quieres eliminar a {persona_a_eliminar.nombre} (CI: {persona_a_eliminar.ci})?[/bold yellow]"):
        return

    query = "EXEC EliminarPersonaAutorizada ?"
    params = (persona_a_eliminar.id,)
    execute_query(conn, query, params)
    console.print("[bold green]Persona autorizada eliminada exitosamente.[/bold green]")
    wait_for_user()
