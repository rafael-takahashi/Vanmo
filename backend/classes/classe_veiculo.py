import sys
sys.path.append("..")

from pydantic import BaseModel
from classes.classe_calendario import Calendario
from decimal import *
from datetime import date
from PIL import Image

class Veiculo(BaseModel):
    def __init__(self, id_veiculo: int, id_empresa: int, nome_veiculo: str, placa_veiculo: str):
        self.id_veiculo = id_veiculo
        self.id_empresa = id_empresa
        self.nome_veiculo = nome_veiculo
        self.placa_veiculo = placa_veiculo
        self.calendario_disponibilidade = Calendario([])

    def adicionar_custos(self, custo_por_km, custo_base):
        self.custo_por_km = custo_por_km
        self.custo_base = custo_base

    def adicionar_dados(self, foto: Image.Image, cor: str, ano_fabricacao: date):
        self.foto = foto
        self.cor = cor
        self.ano_fabricacao = ano_fabricacao
    