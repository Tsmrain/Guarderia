import datetime
from entidades.menu import Menu
from entidades.plato import Plato
from entidades.ingrediente import Ingrediente
from database import connect_to_db, execute_query
from utils import clear_screen, wait_for_user, validar_fecha
from gestion.ninos import obtener_ninos
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

def obtener_menus(conn, fecha=None):
    """Obtiene menús, filtrados por fecha (opcional)."""
    query = "EXEC ObtenerMenus @Fecha=?"
    params = (fecha,) if fecha else None
    cursor = execute_query(conn, query, params)

    menus = []
    for row in cursor:
        menu_id, nombre, fecha = row
        menu = Menu(id=menu_id, nombre=nombre, fecha=fecha)

        # Obtener platos del menú
        query_platos = "SELECT p.IdPlato, p.Nombre FROM Platos p " \
                       "INNER JOIN Menus_Platos mp ON p.IdPlato = mp.IdPlato " \
                       "WHERE mp.IdMenu = ?"
        cursor_platos = execute_query(conn, query_platos, (menu_id,))
        menu.platos = [Plato(*row) for row in cursor_platos]

        # Obtener ingredientes de cada plato
        for plato in menu.platos:
            query_ingredientes = "SELECT i.IdIngrediente, i.Nombre FROM Ingredientes i " \
                                 "INNER JOIN Platos_Ingredientes pi ON i.IdIngrediente = pi.IdIngrediente " \
                                 "WHERE pi.IdPlato = ?"
            cursor_ingredientes = execute_query(conn, query_ingredientes, (plato.id,))
            plato.ingredientes = [Ingrediente(*row) for row in cursor_ingredientes]

        menus.append(menu)
    return menus

def agregar_menu(conn):
    """Agrega un nuevo menú con sus platos e ingredientes."""
    clear_screen()
    console.print("[bold blue]--------- Crear Menú ---------[/bold blue]")

    nombre = Prompt.ask("[bold green]Ingrese el nombre del menú[/bold green]")
    while True:
        fecha_str = Prompt.ask("[bold green]Ingrese la fecha del menú (YYYY-MM-DD)[/bold green]")
        if validar_fecha(fecha_str):
            fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
            break
        else:
            console.print("[bold red]Fecha inválida. Use el formato YYYY-MM-DD.[/bold red]")

    # Insertar el menú en la base de datos
    query = "EXEC InsertarMenu ?, ?"
    params = (nombre, fecha)
    cursor = execute_query(conn, query, params)
    menu_id = cursor.fetchone()[0]  # Obtener el ID del menú recién insertado

    while True:
        agregar_plato = Prompt.ask("[bold green]¿Desea agregar un plato al menú? (s/n)[/bold green]").lower()
        if agregar_plato not in ['s', 'n']:
            console.print("[bold red]Opción inválida. Ingrese 's' o 'n'.[/bold red]")
            continue
        
        if agregar_plato == 'n':
            break

        nombre_plato = Prompt.ask("[bold green]Ingrese el nombre del plato[/bold green]")

        # Insertar el plato en la base de datos
        query_plato = "EXEC InsertarPlato ?"
        params_plato = (nombre_plato,)
        cursor_plato = execute_query(conn, query_plato, params_plato)
        plato_id = cursor_plato.fetchone()[0]

        # Asociar el plato al menú
        query_menu_plato = "INSERT INTO Menus_Platos (IdMenu, IdPlato) VALUES (?, ?)"
        params_menu_plato = (menu_id, plato_id)
        execute_query(conn, query_menu_plato, params_menu_plato)

        while True:
            agregar_ingrediente = Prompt.ask("[bold green]¿Desea agregar un ingrediente al plato? (s/n)[/bold green]").lower()
            if agregar_ingrediente not in ['s', 'n']:
                console.print("[bold red]Opción inválida. Ingrese 's' o 'n'.[/bold red]")
                continue

            if agregar_ingrediente == 'n':
                break

            nombre_ingrediente = Prompt.ask("[bold green]Ingrese el nombre del ingrediente[/bold green]")

            # Verificar si el ingrediente ya existe
            query_ingrediente_existente = "SELECT IdIngrediente FROM Ingredientes WHERE Nombre = ?"
            cursor_ingrediente_existente = execute_query(conn, query_ingrediente_existente, (nombre_ingrediente,))
            ingrediente_existente = cursor_ingrediente_existente.fetchone()

            if ingrediente_existente:
                ingrediente_id = ingrediente_existente[0]
            else:
                # Insertar el ingrediente en la base de datos
                query_ingrediente = "EXEC InsertarIngrediente ?"
                params_ingrediente = (nombre_ingrediente,)
                cursor_ingrediente = execute_query(conn, query_ingrediente, params_ingrediente)
                ingrediente_id = cursor_ingrediente.fetchone()[0]

            # Asociar el ingrediente al plato
            query_plato_ingrediente = "INSERT INTO Platos_Ingredientes (IdPlato, IdIngrediente) VALUES (?, ?)"
            params_plato_ingrediente = (plato_id, ingrediente_id)
            execute_query(conn, query_plato_ingrediente, params_plato_ingrediente)

    console.print("[bold green]Menú registrado exitosamente.[/bold green]")
    wait_for_user()


import datetime
from entidades.menu import Menu
from entidades.plato import Plato
from entidades.ingrediente import Ingrediente
from database import connect_to_db, execute_query
from utils import clear_screen, wait_for_user, validar_fecha
from gestion.ninos import obtener_ninos
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

# ... (Funciones obtener_menus y agregar_menu ya proporcionadas anteriormente) ...

def actualizar_menu(conn):
    """Actualiza un menú existente."""
    clear_screen()
    console.print("[bold blue]--------- Actualizar Menú ---------[/bold blue]")

    menus = obtener_menus(conn)
    if not menus:
        console.print("[bold red]No hay menús registrados.[/bold red]")
        wait_for_user()
        return

    for i, menu in enumerate(menus):
        console.print(f"{i+1}. {menu.nombre} ({menu.fecha})")
    
    while True:
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione el menú a actualizar[/bold green]")) - 1
            menu_a_actualizar = menus[opcion]
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    nuevo_nombre = Prompt.ask("[bold green]Ingrese el nuevo nombre del menú[/bold green]")
    while True:
        nueva_fecha_str = Prompt.ask("[bold green]Ingrese la nueva fecha del menú (YYYY-MM-DD)[/bold green]")
        if validar_fecha(nueva_fecha_str):
            nueva_fecha = datetime.datetime.strptime(nueva_fecha_str, '%Y-%m-%d').date()
            break
        else:
            console.print("[bold red]Fecha inválida. Use el formato YYYY-MM-DD.[/bold red]")

    query = "EXEC ActualizarMenu?,?,?"
    params = (menu_a_actualizar.id, nuevo_nombre, nueva_fecha)
    execute_query(conn, query, params)
    console.print("[bold green]Menú actualizado exitosamente.[/bold green]")
    wait_for_user()

def eliminar_menu(conn):
    """Elimina un menú existente."""
    clear_screen()
    console.print("[bold blue]--------- Eliminar Menú ---------[/bold blue]")

    menus = obtener_menus(conn)
    if not menus:
        console.print("[bold red]No hay menús registrados.[/bold red]")
        wait_for_user()
        return

    for i, menu in enumerate(menus):
        console.print(f"{i+1}. {menu.nombre} ({menu.fecha})")

    while True:
        try:
            opcion = int(Prompt.ask("[bold green]Seleccione el menú a eliminar[/bold green]")) - 1
            menu_a_eliminar = menus[opcion]
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    if not Confirm.ask(f"[bold yellow]¿Estás seguro de que quieres eliminar el menú '{menu_a_eliminar.nombre}'?[/bold yellow]"):
        return

    query = "EXEC EliminarMenu ?"  # Asumiendo que tienes un procedimiento EliminarMenu
    params = (menu_a_eliminar.id,)
    execute_query(conn, query, params)
    console.print("[bold green]Menú eliminado exitosamente.[/bold green]")
    wait_for_user()

def gestionar_alergias(conn):
    """Gestiona las alergias de los niños."""
    clear_screen()
    console.print("[bold blue]--------- Gestionar Alergias ---------[/bold blue]")

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
            nino_seleccionado = ninos[opcion]
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    # Mostrar alergias actuales del niño (si las hay)
    console.print(f"\nAlergias actuales de {nino_seleccionado.nombre}: {nino_seleccionado.alergias}")

    # Opciones para agregar, eliminar o modificar alergias
    # ... (Lógica para interactuar con el usuario y actualizar las alergias en la base de datos)
    # ... (resto del código del archivo menus_alergias.py)

def gestionar_alergias(conn):
    """Gestiona las alergias de los niños."""
    clear_screen()
    console.print("[bold blue]--------- Gestionar Alergias ---------[/bold blue]")

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
            nino_seleccionado = ninos[opcion]
            break
        except (ValueError, IndexError):
            console.print("[bold red]Opción inválida.[/bold red]")

    # Mostrar alergias actuales del niño (si las hay)
    alergias_actuales = nino_seleccionado.alergias.split(',') if nino_seleccionado.alergias else []
    if alergias_actuales:
        console.print(f"\nAlergias actuales de {nino_seleccionado.nombre}: {', '.join(alergias_actuales)}")
    else:
        console.print(f"\n{nino_seleccionado.nombre} no tiene alergias registradas.")

    while True:
        console.print("\n[bold green]Opciones:[/bold green]")
        console.print("1. Agregar alergia")
        console.print("2. Eliminar alergia")
        console.print("3. Modificar alergias (reescribir todas)")
        console.print("4. Volver")

        opcion = Prompt.ask("[bold green]Seleccione una opción[/bold green]")

        if opcion == '1':
            nueva_alergia = Prompt.ask("[bold green]Ingrese la nueva alergia[/bold green]")
            if nueva_alergia not in alergias_actuales:
                alergias_actuales.append(nueva_alergia)
            else:
                console.print("[bold yellow]El niño ya tiene esa alergia registrada.[/bold yellow]")
        elif opcion == '2':
            if not alergias_actuales:
                console.print("[bold yellow]El niño no tiene alergias registradas.[/bold yellow]")
            else:
                for i, alergia in enumerate(alergias_actuales):
                    console.print(f"{i+1}. {alergia}")
                try:
                    opcion_eliminar = int(Prompt.ask("[bold green]Seleccione la alergia a eliminar[/bold green]")) - 1
                    del alergias_actuales[opcion_eliminar]
                except (ValueError, IndexError):
                    console.print("[bold red]Opción inválida.[/bold red]")
        elif opcion == '3':
            nuevas_alergias_str = Prompt.ask("[bold green]Ingrese todas las alergias separadas por comas (o deje en blanco si no tiene)[/bold green]")
            alergias_actuales = nuevas_alergias_str.split(',') if nuevas_alergias_str else []
        elif opcion == '4':
            break
        else:
            console.print("[bold red]Opción inválida.[/bold red]")

        # Actualizar las alergias en la base de datos
        alergias_str = ",".join(alergias_actuales)
        query = "EXEC ActualizarNino ?, ?, ?, ?, ?, ?"
        params = (nino_seleccionado.id, nino_seleccionado.numero_matricula, nino_seleccionado.nombre, nino_seleccionado.fecha_nacimiento, nino_seleccionado.fecha_ingreso, alergias_str)
        execute_query(conn, query, params)
        console.print("[bold green]Alergias actualizadas exitosamente.[/bold green]")
