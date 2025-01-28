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
    with open('latitude-longitude-cidades.csv', mode='r', encoding='utf-8') as tabela:
        leitor = csv.reader(tabela,  delimiter=';')
        next(leitor)

        for linha in leitor:
            cidade: Cidade = Cidade(linha[1], linha[2], linha[3], linha[4])
            lista_cidades.append(cidade)
    
    return lista_cidades

import unicodedata

def remove_acentos(texto: str) -> str:
    """
    Remove acentuação e caracteres especiais de uma string.
    
    @param texto: Texto a ser normalizado
    @return: Texto sem acentuação
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'
    )

def busca_latitude_longitude_de_cidade(nome_cidade: str, lista_cidades: list[Cidade], uf: str | None = None) -> tuple[float, float]:
    """
    Busca as coordenadas (latitude e longitude) de uma cidade a partir do nome, ignorando acentuação e cê-cedilha.
    
    @param nome_cidade: Nome da cidade a buscar
    @param lista_cidades: Lista de objetos Cidade
    @return: Tupla com latitude e longitude da cidade
    """
    nome_cidade_normalizado = remove_acentos(nome_cidade.lower())

    uf_normalizado = None
    if uf:
        uf_normalizado = remove_acentos(uf.lower()).replace(" ", "")

    for cidade in lista_cidades:
        if remove_acentos(cidade.nome.lower()) == nome_cidade_normalizado:
            if uf:
                if remove_acentos(cidade.uf.lower()) == uf_normalizado:
                    return float(cidade.latitude), float(cidade.longitude)
            else:
                return float(cidade.latitude), float(cidade.longitude)
    raise ValueError("Cidade não encontrada na lista")

def valida_cpf(cpf: str) -> bool:
    """
    Valida um CPF, considerando seus dígitos verificadores.
    https://www.macoratti.net/alg_cpf.htm
    
    @param cpf: CPF a ser validado
    @return: True se válido, False caso contrário
    """
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    def calcula_digito(cpf, peso):
        soma = sum(int(cpf[i]) * (peso - i) for i in range(peso - 1))
        digito = 11 - soma % 11
        return digito if digito < 10 else 0
    
    digito1 = calcula_digito(cpf, 10)
    digito2 = calcula_digito(cpf, 11)
    return cpf[-2:] == f"{digito1}{digito2}"

def valida_cnpj(cnpj: str) -> bool:
    """
    Valida um CNPJ, considerando seus dígitos verificadores.
    https://www.macoratti.net/alg_cnpj.htm
    
    @param cnpj: CNPJ a ser validado
    @return: True se válido, False caso contrário
    """
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    def calcula_digito(cnpj, pesos):
        soma = sum(int(cnpj[i]) * pesos[i] for i in range(len(pesos)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1
    digito1 = calcula_digito(cnpj[:12], pesos1)
    digito2 = calcula_digito(cnpj[:13], pesos2)
    return cnpj[-2:] == f"{digito1}{digito2}"

def valida_email(email: str) -> bool:
    """
    Valida se um email está no formato correto.
    
    @param email: Email a ser validado
    @return: True se válido, False caso contrário
    """
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.fullmatch(regex, email))

def valida_cidade(cidade: str, lista_cidades: list[Cidade]) -> bool:
    """
    Valida se uma cidade tem um nome válido (somente letras e espaços) e se ela está na lista de cidades
    
    @param cidade: Nome da cidade
    @return: True se válido, False caso contrário
    """
    nome_cidade = remove_acentos(cidade.lower())
    nome_valido = bool(re.fullmatch(r"^[a-zA-ZÀ-ÿ\s]+$", nome_cidade))

    if not nome_valido:
        raise HTTPException(status_code=400, detail="Nome da cidade pode conter apenas letras e números")
    
    for cidade in lista_cidades:
        if remove_acentos(cidade.nome.lower()) == nome_cidade:
            return True
    
    return False

def valida_uf(uf: str) -> bool:
    """
    Valida se uma UF é válida (dois caracteres de siglas brasileiras).
    
    @param uf: Sigla da UF
    @return: True se válido, False caso contrário
    """
    estados_validos = {
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    }
    return uf.upper() in estados_validos

def valida_foto(arquivo: UploadFile, tamanho_maximo: int = 25 * 1024 * 1024) -> bool:
    """
    Valida se um arquivo é uma imagem válida no formato PNG e dentro do tamanho permitido.
    
    @param arquivo: Arquivo a ser validado
    @param tamanho_maximo: Tamanho máximo permitido (em bytes). Padrão: 25 MB
    @return: True se válido, levanta uma exceção caso contrário
    """
    extensao_permitida = "image/png"
    if arquivo.content_type != extensao_permitida:
        # OBS: Aqui a gente levanta uma exceção pra indicar melhor a mensagem de erro com o que tá errado
        raise HTTPException(status_code=400, detail="Arquivo inválido. Apenas imagens PNG são permitidas.")

    arquivo.file.seek(0, os.SEEK_END)
    tamanho_arquivo = arquivo.file.tell()
    arquivo.file.seek(0)

    if tamanho_arquivo > tamanho_maximo:
        raise HTTPException(status_code=400, detail=f"Arquivo muito grande. O tamanho máximo permitido é {tamanho_maximo // (1024 * 1024)} MB.")

    return True

def retorna_todas_cidades(lista_cidades: list[Cidade]) -> str:
    """
    Retorna uma lista formatada com os nomes e estados de todas as cidades fornecidas.

    @param lista_cidades: Lista de objetos da classe "Cidade".
    @return: Lista de strings formatadas no estilo "Nome da Cidade, UF".
    """
    return [f'"{cidade.nome}, {cidade.uf}"' for cidade in lista_cidades]

def carrega_foto_base64(path_foto, veiculo=False) -> str:
    """
    Carrega uma imagem de um arquivo e a converte para base64. 
    Caso o arquivo não seja encontrado, retorna uma imagem padrão.

    @param path_foto: Caminho do arquivo da imagem a ser carregada.
    @param veiculo: Indica se a imagem padrão é de um veículo (True) ou perfil (False).
    @return: String representando a imagem codificada em base64.
    """
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
    """
    Salva um arquivo de imagem no caminho especificado, substituindo o arquivo existente, se houver.

    @param path_foto: Caminho onde a imagem será salva.
    @param arquivo: Arquivo de imagem enviado pelo usuário.
    @return: Apenas levanta uma exceção em caso de falha.
    """
    try:
        if path_foto is None or path_foto == "":
            return

        if (os.path.isfile(path_foto)):
            os.remove(path_foto)

        with open(path_foto, "wb+") as arquivo:
            arquivo.write(arquivo.file.read())
    except Exception:
        raise HTTPException(status_code=400, detail="Falha ao salvar a foto")
