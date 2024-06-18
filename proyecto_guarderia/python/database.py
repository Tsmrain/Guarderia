import pyodbc

def connect_to_db():
    """Conecta a la base de datos SQL Server."""
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=Guarderia;'
            'UID=sa;'
            'PWD=<YourStrong@Passw0rd>;'
            'TrustServerCertificate=yes'
        )
        return conn
    except pyodbc.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def execute_query(conn, query, params=None):
    """Ejecuta una consulta SQL o procedimiento almacenado."""
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    return cursor
