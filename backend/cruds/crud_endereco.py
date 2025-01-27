import sys
sys.path.append("..")

from decimal import *
from classes.classe_endereco import Endereco
from database import *
import sqlite3

def buscar_endereco_por_id (db: sqlite3.Connection, id_endereco: int) -> Endereco:
    cursor = db.cursor()
    dados = (id_endereco,)

    resultado = cursor.execute(QueriesDB.query_buscar_endereco_por_id, dados).fetchone()
    # (id_endereco, cep, rua, numero, bairro, cidade, estado)

    return Endereco(resultado[6], resultado[5], resultado[4], resultado[1], resultado[2], resultado[3], resultado[0])
    
    # return Endereco(resultado[0], resultado[6], resultado[5], resultado[4], resultado[1], resultado[2], resultado[3])