import sys
sys.path.append("..")

from decimal import *
from classes.classe_local import Local
from database import *
import sqlite3

def criar_local():
    pass

def remover_local():
    pass

def atualizar_local():
    pass

def buscar_local_por_id (db: sqlite3.Connection, id_local: int) -> Local:
    cursor = db.cursor()
    dados = (id_local,)

    resultado = cursor.execute(QueriesDB.query_buscar_local_por_id, dados)

    return Local(resultado[0], resultado[1], resultado[2], resultado[3])