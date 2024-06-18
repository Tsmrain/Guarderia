class Menu:
    def __init__(self, id=None, nombre=None, fecha=None, platos=None):
        self.id = id
        self.nombre = nombre
        self.fecha = fecha
        self.platos = platos or []  # Lista de objetos Plato
