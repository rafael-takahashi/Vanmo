import sys
sys.path.append("..")

from decimal import *
from classes.classe_local import Local
from database import *
import sqlite3

def criar_local(db: sqlite3.Connection, local: Local):
    cursor = db.curso()
    if not local.nome:
        local.nome = ""
    dados = (local.latitude, local.longitude, local.nome)

    cursor.execute(QueriesDB.query_inserir_local_novo, dados)
    db.commit()

def remover_local():
    pass

def atualizar_local():
    pass

def buscar_local_por_id (db: sqlite3.Connection, id_local: int) -> Local:
    cursor = db.cursor()
    dados = (id_local,)

    resultado = cursor.execute(QueriesDB.query_buscar_local_por_id, dados).fetchone()

    return Local(resultado[0], resultado[1], resultado[2], resultado[3])