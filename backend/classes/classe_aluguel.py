import sys
sys.path.append("..")

from pydantic import BaseModel
from classes.classe_local import Local
from decimal import *
from datetime import date

class Aluguel(BaseModel):
    def __init__(self, id_aluguel: int, id_cliente: int, id_empresa: int, id_veiculo: int):
        self.id_aluguel = id_aluguel
        self.id_cliente = id_cliente
        self.id_empresa = id_empresa
        self.id_veiculo = id_veiculo
        self.distancia_trajeto: Decimal = Decimal(0)
        self.estado_alugues = "proposta"
        self.valor_total: Decimal = Decimal(0)
    
    def adicionar_locais(self, local_partida: Local, local_chegada: Local):
        self.local_partida = local_partida
        self.local_chegada = local_chegada
        self.distancia_trajeto = self.calcular_distancia_trajeto()
    
    def adicionar_datas(self, data_inicio: date, data_fim: date):
        self.data_inicio = data_inicio
        self.data_fim = data_fim
    
    def adicionar_distancia_extra(self, distancia_extra: Decimal):
        self.distancia_extra = distancia_extra
    
    def calcular_distancia_trajeto() -> Decimal:
        return 3
    
