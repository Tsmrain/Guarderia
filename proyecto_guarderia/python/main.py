import datetime
from rich.console import Console
from rich.prompt import Prompt, Confirm
from database import connect_to_db
from gestion import (
    ninos, matriculas, personas_autorizadas, 
    responsables_pago, menus_alergias, servicios_adicionales
)
from reportes import cobros, consumos_tienda, atenciones_especialistas
from utils import clear_screen, validar_fecha

console = Console()

def mostrar_menu_principal():
    """Muestra el menú principal de la aplicación."""
    clear_screen()
    console.print("[bold blue]Menú Principal de la Guardería[/bold blue]", justify="center")
    console.print("\n[bold green]Seleccione una opción:[/bold green]")
    console.print("1. Gestión de Niños")
    console.print("2. Gestión de Matrículas")
    console.print("3. Gestión de Personas Autorizadas")
    console.print("4. Gestión de Responsables de Pago")
    console.print("5. Gestión de Menús y Alergias")
    console.print("6. Gestión de Servicios Adicionales")
    console.print("7. Generar Reportes")
    console.print("8. Salir")

def mostrar_menu_reportes():
    """Muestra el submenú de reportes."""
    clear_screen()
    console.print("[bold blue]Menú de Reportes[/bold blue]", justify="center")
    console.print("\n[bold green]Seleccione un reporte:[/bold green]")
    console.print("1. Reporte de Cobros")
    console.print("2. Reporte de Consumos en Tienda")
    console.print("3. Reporte de Atenciones por Especialistas")
    console.print("4. Volver al Menú Principal")

def obtener_fechas_reporte(conn):
    """Obtiene las fechas de inicio y fin para un reporte."""
    while True:
        fecha_inicio_str = Prompt.ask("[bold green]Ingrese la fecha de inicio (YYYY-MM-DD)[/bold green]")
        if validar_fecha(fecha_inicio_str):
            fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            break
        else:
            console.print("[bold red]Fecha inválida. Use el formato YYYY-MM-DD.[/bold red]")

    while True:
        fecha_fin_str = Prompt.ask("[bold green]Ingrese la fecha de fin (YYYY-MM-DD)[/bold green]")
        if validar_fecha(fecha_fin_str):
            fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            if fecha_fin >= fecha_inicio:  # Validar que la fecha de fin sea posterior a la de inicio
                break
            else:
                console.print("[bold red]La fecha de fin debe ser posterior o igual a la fecha de inicio.[/bold red]")
        else:
            console.print("[bold red]Fecha inválida. Use el formato YYYY-MM-DD.[/bold red]")

    return fecha_inicio, fecha_fin

def main():
    """Función principal de la aplicación."""
    with connect_to_db() as conn:
        while True:
            mostrar_menu_principal()
            opcion = Prompt.ask("[bold green]Opción[/bold green]")

            if opcion == '1':
                ninos.menu_ninos(conn)
            elif opcion == '2':
                matriculas.menu_matriculas(conn)
            elif opcion == '3':
                personas_autorizadas.menu_personas_autorizadas(conn)
            elif opcion == '4':
                responsables_pago.menu_responsables_pago(conn)
            elif opcion == '5':
                menus_alergias.menu_menus_alergias(conn)
            elif opcion == '6':
                servicios_adicionales.menu_servicios_adicionales(conn)
            elif opcion == '7':
                while True:
                    mostrar_menu_reportes()
                    opcion_reporte = Prompt.ask("[bold green]Opción[/bold green]")

                    if opcion_reporte == '1':
                        fecha_inicio, fecha_fin = obtener_fechas_reporte(conn)
                        if fecha_inicio and fecha_fin:
                            cobros.generar_reporte_cobros(conn, fecha_inicio, fecha_fin)
                    elif opcion_reporte == '2':
                        fecha_inicio, fecha_fin = obtener_fechas_reporte(conn)
                        if fecha_inicio and fecha_fin:
                            consumos_tienda.generar_reporte_consumos_tienda(conn, fecha_inicio, fecha_fin)
                    elif opcion_reporte == '3':
                        fecha_inicio, fecha_fin = obtener_fechas_reporte(conn)
                        if fecha_inicio and fecha_fin:
                            atenciones_especialistas.generar_reporte_atenciones_especialistas(conn, fecha_inicio, fecha_fin)
                    elif opcion_reporte == '4':
                        break
                    else:
                        console.print("[bold red]Opción inválida.[/bold red]")
            elif opcion == '8':
                if Confirm.ask("[bold yellow]¿Estás seguro de que quieres salir?[/bold yellow]"):
                    break
            else:
                console.print("[bold red]Opción inválida.[/bold red]")

if __name__ == "__main__":
    main()
