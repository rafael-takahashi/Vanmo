import sys
sys.path.append("..")

from decimal import *
from classes.classe_usuario import *
from database import *
import sqlite3
import datetime

def criar_veiculo():
    pass

def remover_veiculo():
    pass

# Apenas um específico
def buscar_veiculo():
    pass

# Todos os veículos da empresa
def listar_veiculos():
    pass

def atualizar_veiculo():
    pass

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