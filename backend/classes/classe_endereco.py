class Endereco():
    def __init__(self, id: int, uf: str, cidade: str, bairro: str, cep: str, rua: str, numero: int):
        self.id: int = id
        self.uf: str = uf
        self.cidade: str = cidade
        self.bairro: str = bairro
        self.cep: str = cep
        self.rua: str = rua
        self.numero: int = numero