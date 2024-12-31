import sys
sys.path.append("..")

from classes.classe_local import Local
from decimal import *
from datetime import date
import math

class Aluguel():
    def __init__(self, id_aluguel: int, id_cliente: int, id_empresa: int, id_veiculo: int):
        self.id_aluguel = id_aluguel
        self.id_cliente = id_cliente
        self.id_empresa = id_empresa
        self.id_veiculo = id_veiculo
        self.distancia_trajeto: Decimal = Decimal(0)
        self.estado_aluguel = "proposta"
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
    
    def calcular_distancia_trajeto_haversine(self) -> Decimal:
        """
            Método para o cálculo da distância entre dois pontos na Terra baseado na fórmula de Haversine
            https://community.esri.com/t5/coordinate-reference-systems-blog/distance-on-a-sphere-the-haversine-formula/ba-p/902128
        """
        if (not self.local_chegada) or (not self.local_partida):
            return Decimal(-1)
        
        raio_da_terra = 6371
        lat1, lat2 = math.radians(self.local_partida.latitude), math.radians(self.local_chegada.latitude)
        variacao_latitude = math.radians(self.local_chegada.latitude - self.local_partida.latitude)
        variacao_longitude = math.radians(self.local_chegada.longitude - self.local_partida.longitude)

        a = math.sin(variacao_latitude / 2.0)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(variacao_longitude / 2.0)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = round((raio_da_terra * c), 3) # em kilômetros

        return Decimal(distance)
    
