import sys
sys.path.append("..")

from pydantic import BaseModel
from classes.classe_endereco import Endereco

class Usuario():
    def __init__(self, email: str, senha_hashed: str, tipo_conta: str, foto: bytes | None = None, id: int | None = None):
        self.id: int | None = id
        self.email: str = email
        self.senha_hashed: str = senha_hashed
        self.tipo_conta: str = tipo_conta
        self.foto: bytes | None = foto

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