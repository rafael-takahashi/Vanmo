from pydantic import BaseModel

class Endereco(BaseModel):
    def __init__(self, uf: str, cidade: str, bairro: str, cep: str, rua: str, numero: int):
        self.uf: str = uf
        self.cidade: str = cidade
        self.bairro: str = bairro
        self.cep: str = cep
        self.rua: str = rua
        self.numero: int = numero