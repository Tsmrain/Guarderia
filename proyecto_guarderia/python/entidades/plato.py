class Plato:
    def __init__(self, id=None, nombre=None, ingredientes=None):
        self.id = id
        self.nombre = nombre
        self.ingredientes = ingredientes or []  # Lista de objetos Ingrediente
