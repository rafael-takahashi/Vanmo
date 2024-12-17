import sys
sys.path.append("..")

from pydantic import BaseModel
from classes.classe_endereco import Endereco
from PIL import Image

class Usuario(BaseModel):
    def __init__(self, id: int, email: str, senha_hashed: bytes, tipo_conta: str, foto: Image.Image | None = None):
        self.id: str = id
        self.email: str = email
        self.senha_hashed: bytes = senha_hashed
        self.tipo_conta: str = tipo_conta
        self.foto: Image.Image | None = foto

class Cliente(Usuario):
    def __init__(self, id, email, senha_hashed, tipo_conta, foto, nome_completo: str, cpf: str):
        super().__init__(id, email, senha_hashed, tipo_conta, foto)
        self.nome_completo: str = nome_completo
        self.cpf: str = cpf

class Empresa(Usuario):
    def __init__(self, id, email, senha_hashed, tipo_conta, foto, nome_fantasia: str, cnpj: str, endereco: Endereco):
        super().__init__(id, email, senha_hashed, tipo_conta, foto)
        self.nome_fantasia: str = nome_fantasia
        self.cnpj: str = cnpj
        self.endereco: Endereco = endereco
        self.num_avaliacoes = 0
        self.soma_avaliacos = 0