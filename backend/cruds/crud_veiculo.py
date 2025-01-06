import sys
sys.path.append("..")

from fastapi import HTTPException
from decimal import *
from classes.classe_usuario import *
from database import *
from copy import deepcopy
from classes import classe_veiculo, classe_calendario
import sqlite3
import datetime

def criar_veiculo(db: sqlite3.Connection, veiculo: classe_veiculo.Veiculo) -> int:
    cursor = db.cursor()
    dados = (veiculo.id_empresa, veiculo.nome_veiculo, veiculo.placa_veiculo, veiculo.capacidade, veiculo.custo_por_km, veiculo.custo_base, veiculo.caminho_foto, veiculo.cor, veiculo.ano_fabricacao)

    cursor.execute(QueriesDB.query_inserir_veiculo_novo, dados)

    id_veiculo: int = cursor.lastrowid
    db.commit()

    return id_veiculo

def remover_veiculo(db: sqlite3.Connection, id_veiculo: int):
    cursor = db.cursor()
    dados = (id_veiculo,)

    cursor.execute(QueriesDB.query_remover_veiculo, id_veiculo)

# Apenas um específico
def buscar_veiculo(db: sqlite3.Connection, id_veiculo: int) -> classe_veiculo.Veiculo | None: 
    cursor = db.cursor()
    dados = (id_veiculo,)

    resultado = cursor.execute(QueriesDB.query_buscar_veiculo, dados).fetchone()

    if resultado is None:
        return None
    
    veiculo = classe_veiculo.Veiculo(id_veiculo, resultado[1], resultado[2], resultado[3])
    veiculo.adicionar_custos(resultado[5], resultado[6])
    veiculo.adicionar_dados(resultado[7], resultado[8], resultado[9], resultado[4])

    return veiculo

# Todos os veículos da empresa
def listar_veiculos(db: sqlite3.Connection, id_empresa: int) -> list[classe_veiculo.Veiculo]:
    cursor = db.cursor()
    dados = (id_empresa,)

    lista_resultados = cursor.execute(QueriesDB.query_buscar_veiculos_empresa, dados).fetchall()

    print(f"Resultados: {lista_resultados}")

    veiculos = []

    for resultado in lista_resultados:
        veiculo = classe_veiculo.Veiculo(resultado[0], resultado[1], resultado[2], resultado[3])
        veiculo.adicionar_custos(resultado[5], resultado[6])
        veiculo.adicionar_dados(resultado[7], resultado[8], resultado[9], resultado[4])

        veiculos.append(deepcopy(veiculo))

    return veiculos

def atualizar_veiculo():
    pass

def verificar_alugueis_veiculo(db: sqlite3.Connection, id_veiculo: int) -> bool:
    cursor = db.cursor()
    dados = (id_veiculo,)

    resultados = cursor.execute(QueriesDB.query_buscar_alugueis_veiculo, dados).fetchall()

    for resultado in resultados:
        if resultado[5] == "ativo":  # status aluguel
            return True
    
    return False

def verificar_veiculo_empresa(db: sqlite3.Connection, id_veiculo: int, id_empresa: int) -> bool:
    cursor = db.cursor()
    dados = (id_veiculo, id_empresa)

    resultado = cursor.execute(QueriesDB.query_verificar_veiculo_empresa, dados).fetchone()
    
    return resultado is not None

def verificar_disponibilidade_veiculo(db: sqlite3.Connection, id_veiculo: int, data_inicio: datetime.date, data_fim: datetime.date) -> bool:
    cursor = db.cursor()
    dados = (id_veiculo, data_inicio, data_fim)

    resultado = cursor.execute(QueriesDB.query_verificar_disponibilidade_veiculo, dados).fetchone()

    return resultado is None

def atualizar_calendario(db: sqlite3.Connection, id_veiculo: int, calendario: classe_calendario.Calendario):
    # TODO: talvez refazer o método, implementação provisória
    # OBS: assume-se que o objeto calendario já foi validado previamente
    cursor = db.cursor()

    try:
        cursor.execute(QueriesDB.query_remover_calendario, (id_veiculo,))

        # cria uma lista com todos os valores a serem inseridos
        dados = [(id_veiculo, data.strftime('%Y-%m-%d')) for data in calendario.datas_indisponiveis]
        cursor.executemany(QueriesDB.query_inserir_calendario, dados)
        
        db.commit()
    
    except Exception as e:
        db.rollback()
        raise e