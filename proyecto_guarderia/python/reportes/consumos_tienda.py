import datetime
from utils import clear_screen, wait_for_user , validar_fecha
from database import connect_to_db, execute_query
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def generar_reporte_consumos_tienda(conn, fecha_inicio, fecha_fin):
    """Genera un reporte de consumos en la tienda y verifica stock."""

    # Obtener todos los consumos en el período
    query_consumos = "EXEC ObtenerConsumosTienda @FechaInicio=?, @FechaFin=?"
    params_consumos = (fecha_inicio, fecha_fin)
    cursor_consumos = execute_query(conn, query_consumos, params_consumos)
    consumos = cursor_consumos.fetchall()

    # Obtener información de productos (asumiendo que existe una tabla Productos)
    query_productos = "SELECT IdProducto, Nombre, StockMinimo FROM Productos"
    cursor_productos = execute_query(conn, query_productos)
    productos = {row[0]: {"Nombre": row[1], "StockMinimo": row[2]} for row in cursor_productos}

    # Crear tabla para el reporte
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Niño", style="dim")
    table.add_column("Fecha", style="dim")
    table.add_column("Producto")
    table.add_column("Cantidad")

    # Procesar los consumos
    productos_bajo_minimo = []
    for consumo in consumos:
        id_nino, fecha, id_producto, cantidad = consumo
        nombre_producto = productos[id_producto]["Nombre"]
        table.add_row(str(id_nino), fecha.strftime("%Y-%m-%d"), nombre_producto, str(cantidad))

        # Verificar stock
        productos[id_producto]["StockMinimo"] -= cantidad
        if productos[id_producto]["StockMinimo"] <= 0:
            productos_bajo_minimo.append(nombre_producto)

    # Mostrar el reporte
    clear_screen()
    console.print("[bold blue]Reporte de Consumos en la Tienda[/bold blue]\n")
    console.print(table)

    # Mostrar alertas de productos bajo mínimo
    if productos_bajo_minimo:
        console.print("\n[bold red]Alerta: Los siguientes productos están por debajo del stock mínimo:[/bold red]")
        for producto in productos_bajo_minimo:
            console.print(f"- {producto}")

def main():
    """Función principal para la gestión de reportes de consumos de la tienda."""
    with connect_to_db() as conn:
        while True:
            clear_screen()
            console.print("[bold blue]Menú de Reportes de Consumos de la Tienda[/bold blue]")
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

                generar_reporte_consumos_tienda(conn, fecha_inicio, fecha_fin)
                wait_for_user()
            elif opcion == '2':
                break
            else:
                console.print("[bold red]Opción inválida.[/bold red]")

if __name__ == "__main__":
    main()
