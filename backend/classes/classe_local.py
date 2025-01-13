from decimal import *

class Local():
    def __init__(self, lat: float, lon: float, nome: str | None = None, id: int | None = None):
        self.id: int | None = id
        self.latitude: float = lat
        self.longitude: float = lon
        self.nome: str | None = nome