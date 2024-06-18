from database import connect_to_db, execute_query
from gestion.ninos import calcular_costo_mensual ,obtener_ninos

def generar_reporte_cobros(conn, fecha_inicio, fecha_fin):
    """Genera un reporte de cobros mensuales."""
    
    # Obtener todos los niños
    ninos = obtener_ninos(conn)

    # Calcular el costo mensual para cada niño
    for nino in ninos:
        costo_mensual = calcular_costo_mensual(conn, nino.id, fecha_inicio, fecha_fin)
        
        # Imprimir o guardar el reporte (puedes usar una librería como pandas o openpyxl para generar un archivo Excel)
        print(f"Niño: {nino.nombre}, Costo Mensual: {costo_mensual}")
