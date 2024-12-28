from typing import List
from datetime import date

class Calendario():
    def __init__(self, datas_indisponiveis: List[date]):
        self.datas_indisponiveis = datas_indisponiveis
    
    def adicionar_datas_indisponiveis(self, data_inicio: date, data_fim: date):
        pass

    def remover_datas_indisponiveis(self, data_inicio, data_fim):
        pass