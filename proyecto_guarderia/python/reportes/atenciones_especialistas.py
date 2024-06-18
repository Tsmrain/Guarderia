import datetime
from python.utils import *
from database import connect_to_db, execute_query
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def generar_reporte_atenciones_especialistas(conn, fecha_inicio, fecha_fin):
    """Genera un reporte de atenciones por especialistas en un período dado."""

    # Obtener todas las atenciones en el período
    query = "EXEC ObtenerAtencionesEspecialistas @FechaInicio=?, @FechaFin=?"
    params = (fecha_inicio, fecha_fin)
    cursor = execute_query(conn, query, params)
    atenciones = cursor.fetchall()

    # Obtener nombres de niños y especialistas (asumiendo que existen las tablas Ninos y Especialistas)
    ninos = {row[0]: row[1] for row in execute_query(conn, "SELECT IdNino, Nombre FROM Ninos").fetchall()}
    especialistas = {row[0]: row[1] for row in execute_query(conn, "SELECT IdEspecialista, Nombre FROM Especialistas").fetchall()}

    # Crear tabla para el reporte
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Niño", style="dim")
    table.add_column("Fecha", style="dim")
    table.add_column("Especialista")
    table.add_column("Observaciones")

    # Procesar las atenciones y agregarlas a la tabla
    for atencion in atenciones:
        id_nino, fecha, id_especialista, observaciones = atencion
        table.add_row(ninos.get(id_nino, "Desconocido"), fecha.strftime("%Y-%m-%d"), especialistas.get(id_especialista, "Desconocido"), observaciones)

    # Mostrar el reporte
    clear_screen()
    console.print("[bold blue]Reporte de Atenciones por Especialistas[/bold blue]\n")
    console.print(table)

def main():
    """Función principal para la gestión de reportes de atenciones de especialistas."""
    with connect_to_db() as conn:
        while True:
            clear_screen()
            console.print("[bold blue]Menú de Reportes de Atenciones de Especialistas[/bold blue]")
            console.print("1. Generar Reporte")
            console.print("2. Salir")

            opcion = Prompt.ask("[bold green]Seleccione una opción[/bold green]")

            if opcion == '1':
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
                        break
                    else:
                        console.print("[bold red]Fecha inválida. Use el formato YYYY-MM-DD.[/bold red]")

                generar_reporte_atenciones_especialistas(conn, fecha_inicio, fecha_fin)
                wait_for_user()
            elif opcion == '2':
                break
            else:
                console.print("[bold red]Opción inválida.[/bold red]")

if __name__ == "__main__":
    main()
