import re
import csv
import base64
import os
from fastapi import UploadFile, HTTPException

class Cidade:
    def __init__(self, uf: str, nome: str, latitude: float, longitude: float):
        self.uf : str = uf
        self.nome : str = nome 
        self.latitude: float = latitude
        self.longitude: float = longitude

CONST_NUM_RESULTADOS_POR_PAGINA = 10

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

def busca_latitude_longitude_de_cidade(nome_cidade: str, lista_cidades: list[Cidade]) -> tuple[int, int]:
    pass

def valida_cpf(cpf: str) -> bool:
    pass

def valida_cnpj(cnpj: str) -> bool:
    pass

def valida_email(email: str) -> bool:
    pass

def valida_cidade(cidade: str) -> bool:
    pass

def valida_uf(uf: str) -> bool:
    pass

def valida_foto(arquivo: UploadFile) -> bool:
    pass

def carrega_foto_base64(path_foto, veiculo=False) -> str:
    try:
        with open(path_foto, "rb") as file:
            photo_bytes = file.read()
            photo_base64 = base64.b64encode(photo_bytes).decode("utf-8")
            return photo_base64
    except FileNotFoundError:
        path_padrao = "imagens/imagem_perfil_padrao.png"
        if veiculo:
            path_padrao = "imagens/imagem_veiculo_padrao.png"
        
        with open(path_padrao, "rb") as file:
            photo_bytes = file.read()
            photo_base64 = base64.b64encode(photo_bytes).decode("utf-8")
            return photo_base64

def salva_foto(path_foto, arquivo: UploadFile):

    try:
        if path_foto is None or path_foto == "":
            return

        if (os.path.isfile(path_foto)):
            os.remove(path_foto)

        with open(path_foto, "wb+") as arquivo:
            arquivo.write(arquivo.file.read())
    except Exception:
        raise HTTPException(status_code=400, detail="Falha ao salvar a foto")
