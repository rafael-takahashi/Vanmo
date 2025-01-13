import sys
sys.path.append("..")

from classes.classe_calendario import Calendario
from decimal import *
from datetime import date

class Veiculo():
    def __init__(self, id_veiculo: int | None, id_empresa: int, nome_veiculo: str, placa_veiculo: str):
        self.id_veiculo: int | None = id_veiculo
        self.id_empresa: int = id_empresa
        self.nome_veiculo: str = nome_veiculo
        self.placa_veiculo: str = placa_veiculo
        self.calendario_disponibilidade = Calendario([])
        
    def adicionar_custos(self, custo_por_km, custo_base):
        self.custo_por_km: float = custo_por_km
        self.custo_base: float = custo_base

    def adicionar_dados(self, caminho_foto: str | None, cor: str, ano_fabricacao: int, capacidade: int):
        self.caminho_foto: str | None = caminho_foto
        self.cor: str = cor
        self.ano_fabricacao: int = ano_fabricacao
        self.capacidade: int = capacidade
    