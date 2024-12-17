from pydantic import BaseModel
from decimal import *

class Local(BaseModel):
    def __init__(self, latitude: float, longitude: float, nome: str | None = None):
        self.latitude = latitude
        self.longitude = longitude
        self.nome = nome