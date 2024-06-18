import os
import datetime

def clear_screen():
    """Limpia la pantalla de la terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_for_user():
    """Espera a que el usuario presione Enter."""
    input("Presione Enter para continuar...")

def validar_fecha(fecha_str):
    """Valida si una cadena tiene el formato de fecha YYYY-MM-DD."""
    try:
        datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
