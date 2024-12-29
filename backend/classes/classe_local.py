from decimal import *

class Local():
    def __init__(self, id: int, lat: float, lon: float, nome: str | None = None):
        self.id = id
        self.latitude = lat
        self.longitude = lon
        self.nome = nome