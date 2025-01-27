class Endereco():
    def __init__(self, uf: str, cidade: str, bairro: str, cep: str, rua: str, numero: int, id_endereco: int | None = None):
        self.id_endereco: int | None = id_endereco
        self.uf: str = uf
        self.cidade: str = cidade
        self.bairro: str = bairro
        self.cep: str = cep
        self.rua: str = rua
        self.numero: int = numero

    def __repr__(self):
        return f"{self.uf}, {self.cidade}, {self.cep}, {self.bairro}, {self.rua}, {self.numero}"