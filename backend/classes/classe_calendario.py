from typing import List
from datetime import date, timedelta

class Calendario():
    def __init__(self, datas_indisponiveis: List[date]):
        # TODO: Usar set ao invés de list
        self.datas_indisponiveis = datas_indisponiveis
    
    def adicionar_datas_indisponiveis(self, data_inicio: date, data_fim: date):
        incremento_dia = timedelta(days=1)
        while (data_inicio <= data_fim):
            self.datas_indisponiveis.append(data_inicio)
            data_inicio += incremento_dia

    def remover_datas_indisponiveis(self, data_inicio, data_fim):
        incremento_dia = timedelta(days=1)
        while (data_inicio <= data_fim):
            self.datas_indisponiveis.remove(data_inicio)
            data_inicio += incremento_dia