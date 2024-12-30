import sys
sys.path.append("..")

from fastapi import HTTPException
from decimal import *
from classes.classe_usuario import *
from database import *
from classes import classe_veiculo
import sqlite3
import datetime

def criar_veiculo():
    pass

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
    pass

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

    return resultado is not None