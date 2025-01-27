import sys
sys.path.append("..")

from fastapi import UploadFile
from pydantic import BaseModel
from classes.classe_endereco import Endereco
from classes.classe_local import Local

class Usuario():
    def __init__(self, email: str, senha_hashed: str, tipo_conta: str, foto: str | None = None, telefone: str | None = None, id_usuario: int | None = None):
        self.id_usuario: int | None = id_usuario
        self.email: str = email
        self.senha_hashed: str = senha_hashed
        self.tipo_conta: str = tipo_conta
        self.foto: str | None = foto
        self.telefone: str = telefone

class Cliente(Usuario):
    def __init__(self, id_usuario, email, senha_hashed, tipo_conta, foto, nome_completo: str, cpf: str, data_nascimento: str, telefone: str):
        super().__init__(email, senha_hashed, tipo_conta, foto, telefone, id_usuario)
        self.nome_completo: str = nome_completo
        self.cpf: str = cpf
        self.data_nascimento: str = data_nascimento
        
    def __repr__(self):
        return f"[Cliente] Id: {self.id_usuario} email: {self.email} nome: {self.nome_completo} cpf: {self.cpf}"
    
class Empresa(Usuario):
    def __init__(self, id_usuario, email, senha_hashed, tipo_conta, foto, nome_fantasia: str, cnpj: str, endereco: Endereco, local: Local, telefone: str):
        super().__init__(email, senha_hashed, tipo_conta, foto, telefone, id_usuario)
        self.nome_fantasia: str = nome_fantasia
        self.cnpj: str = cnpj
        self.endereco: Endereco = endereco
        self.local: Local = local
        self.num_avaliacoes = 0
        self.soma_avaliacoes = 0

    def __repr__(self):
        return f"[Empresa] Id: {self.id_usuario} email: {self.email} nome fantasia: {self.nome_fantasia} cnpj: {self.cnpj} endereco: {self.endereco} local: {self.local} num avls {self.num_avaliacoes} soma avls {self.soma_avaliacoes}"