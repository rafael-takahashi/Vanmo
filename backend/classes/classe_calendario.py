from typing import List
from datetime import date, timedelta, datetime

class Calendario():
    def __init__(self, datas_indisponiveis: List[date]):
        # TODO: Usar set ao invés de list
        self.datas_indisponiveis = datas_indisponiveis
    
    def adicionar_datas_indisponiveis(self, data_inicio: str, data_fim: str):
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
        incremento_dia = timedelta(days=1)
        while (data_inicio <= data_fim):
            self.datas_indisponiveis.append(data_inicio)
            data_inicio += incremento_dia

    def remover_datas_indisponiveis(self, data_inicio, data_fim):
        incremento_dia = timedelta(days=1)
        while (data_inicio <= data_fim):
            self.datas_indisponiveis.remove(data_inicio)
            data_inicio += incremento_dia