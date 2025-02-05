# Esse arquivo contém os BaseModels utilizados na main.py para comunicar com o frontend pelo FastAPI

# OBS: Apesar de utilizarem a estrutura de classes, essas não representam as classes do sistema

# from fastapi import str
from pydantic import BaseModel
import datetime

class CadastroUsuario(BaseModel):
    email: str
    senha: str
    tipo_conta: str
    telefone: str

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class CadastroCliente(BaseModel):
    email: str
    senha: str
    nome_completo: str
    cpf: str
    data_nascimento: str
    telefone: str

class CadastroEmpresa(BaseModel):
    email: str
    senha: str
    nome_fantasia: str
    telefone: str
    cnpj: str
    uf: str
    cidade: str
    bairro: str
    cep: str
    rua: str
    numero: str

class AlterarDadosCliente(BaseModel):
    email: str | None = None
    senha: str | None = None
    foto: str | None = None
    nome_completo: str | None = None
    cpf: str | None = None
    data_nascimento: str | None = None
    telefone: str | None = None

class AlterarDadosEmpresa(BaseModel):
    email: str | None = None
    senha: str | None = None
    foto: str | None = None
    nome_fantasia: str | None = None
    cnpj: str | None = None
    uf: str | None = None
    cidade: str | None = None
    bairro: str | None = None
    cep: str | None = None
    rua: str | None = None
    numero: str | None = None
    telefone: str | None = None

class DadosAcaoProposta(BaseModel):
    id_proposta: int
    opcao: bool

class IdProposta(BaseModel):
    id_proposta: int

class IdVeiculo(BaseModel):
    id_veiculo: int

class RespostaVeiculo(BaseModel):
    id_veiculo: int
    nome_veiculo: str
    placa_veiculo: str

    datas_indisponiveis: list[datetime.date]
    
    custo_por_km: float
    custo_base: float
    
    foto: str
    cor: str
    ano_fabricacao: int
    capacidade: int

class IdEmpresa(BaseModel):
    id_empresa: int

class EditarVeiculo(BaseModel):
    id_veiculo: int
    nome_veiculo: str | None = None,
    placa_veiculo: str | None = None,
    custo_por_km: float | None = None,
    custo_base: float | None = None,
    foto: str | None = None,
    cor: str | None = None,
    ano_fabricacao: int | None = None

class CadastrarVeiculo(BaseModel):
    nome_veiculo: str
    placa_veiculo: str
    custo_por_km: float
    custo_base: float
    cor: str
    ano_fabricacao: int
    capacidade: int
    foto: str | None = None

class RespostaEmpresa(BaseModel):
    foto: str
    nome_fantasia: str
    cnpj: str
    endereco: str
    avaliacao: float
    telefone: str

class AvaliacaoEmpresa(BaseModel):
    id_empresa: int
    avaliacao: int

class BuscaEmpresaNome(BaseModel):
    nome_busca: str
    pagina: int

class CriarProposta(BaseModel):
    id_empresa: int
    id_veiculo: int
    local_saida: str
    local_chegada: str
    distancia_extra_km: float
    data_saida: datetime.date
    data_chegada: datetime.date