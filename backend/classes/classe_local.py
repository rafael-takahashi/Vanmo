from decimal import *

class Local():
    def __init__(self, lat: float, lon: float, nome: str | None = None, id_local: int | None = None):
        self.id_local: int | None = id_local
        self.latitude: float = lat
        self.longitude: float = lon
        self.nome: str | None = nome