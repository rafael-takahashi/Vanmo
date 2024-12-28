from decimal import *

class Local():
    def __init__(self, lat: float, lon: float, nome: str | None = None):
        self.latitude = lat
        self.longitude = lon
        self.nome = nome