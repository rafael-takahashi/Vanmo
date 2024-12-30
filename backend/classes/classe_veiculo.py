import sys
sys.path.append("..")

from classes.classe_calendario import Calendario
from decimal import *
from datetime import date

class Veiculo():
    def __init__(self, id_veiculo: int, id_empresa: int, nome_veiculo: str, placa_veiculo: str):
        self.id_veiculo = id_veiculo
        self.id_empresa = id_empresa
        self.nome_veiculo = nome_veiculo
        self.placa_veiculo = placa_veiculo
        self.calendario_disponibilidade = Calendario([])

    def adicionar_custos(self, custo_por_km, custo_base):
        self.custo_por_km = custo_por_km
        self.custo_base = custo_base

    def adicionar_dados(self, foto: bytes, cor: str, ano_fabricacao: date, capacidade: int):
        self.foto = foto
        self.cor = cor
        self.ano_fabricacao = ano_fabricacao
        self.capacidade = capacidade
    