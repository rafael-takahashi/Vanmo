import re
import csv

class Cidade:
    def __init__(self, uf: str, nome: str, latitude: float, longitude: float):
        self.uf : str = uf
        self.nome : str = nome 
        self.latitude: float = latitude
        self.longitude: float = longitude

def valida_coordendas(latitude: float, longitude: float) -> bool:
    """
    Valida se duas coordenadas possuem valores válidos

    @param latitude: A latitude a verificar
    @param longitude: A longitude a verificar
    @return: True caso elas sejam válidas, False caso contrário
    """
    latitude, longitude = abs(latitude), abs(longitude)
    validacao_lat = (0 <= latitude <= 90)
    validacao_long = (0 <= longitude <= 180)

    return validacao_lat and validacao_long

def valida_placa(placa: str) -> bool:
    """
    Valida se uma placa está no formato correto AAA9999 ou AAA9A99

    @param placa: A placa a ser verificada
    @return: True caso ela seja válida, False caso contrário
    """
    # formato ABC1234
    placa_antiga = r"^[A-Z]{3}\d{4}$"
    # formato ABC1D23

    # Curiosidade: A letra onde seria o segundo dígito k é a (k-1)-ésima letra do alfabeto
    # A: 0, 9: J
    # https://pt.wikipedia.org/wiki/Placas_de_identifica%C3%A7%C3%A3o_de_ve%C3%ADculos_no_Mercosul

    placa_mercosul = r"^[A-Z]{3}\d{1}[A-J]{1}\d{2}$"

    return bool((re.fullmatch(placa_antiga, placa)) or (re.fullmatch(placa_mercosul, placa)))

def carrega_cidades() -> list[Cidade]:
    lista_cidades = []
    with open('latitude-longitude-cidades.csv', mode='r') as tabela:
        leitor = csv.reader(tabela,  delimiter=';')
        next(leitor)

        for linha in leitor:
            cidade: Cidade = Cidade(linha[1], linha[2], linha[3], linha[4])
            lista_cidades.append(cidade)
    
    return lista_cidades