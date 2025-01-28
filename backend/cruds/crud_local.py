import sys
sys.path.append("..")

from decimal import *
from classes.classe_local import Local
from database import *
import sqlite3

def criar_local(db: sqlite3.Connection, local: Local):
    cursor = db.cursor()
    if not local.nome:
        local.nome = ""
    dados = (local.latitude, local.longitude, local.nome)

    cursor.execute(QueriesDB.query_inserir_local_novo, dados)
    id_local: int = cursor.lastrowid
    
    # Como o local é parte do aluguel, o commit só pode ser dado após as demais operações
    # dele serem feitas

    # if db.in_transaction:
    #     db.rollback()

    # db.commit()
    return id_local

def buscar_local_por_id (db: sqlite3.Connection, id_local: int) -> Local:
    cursor = db.cursor()
    dados = (id_local,)

    resultado = cursor.execute(QueriesDB.query_buscar_local_por_id, dados).fetchone()

    if not resultado:
        return None
        
    return Local(resultado[1], resultado[2], resultado[3], resultado[0])