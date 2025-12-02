import sys
sys.path.append("..")

from decimal import *
from classes.classe_endereco import Endereco
from database import *
from psycopg2.extensions import connection

def buscar_endereco_por_id (db: connection, id_endereco: int) -> Endereco:
    cur = db.cursor()
    dados = (id_endereco,)

    cur.execute(QueriesDB.query_buscar_endereco_por_id, dados)
    resultado = cur.fetchone()
    # (id_endereco, cep, rua, numero, bairro, cidade, estado)

    cur.close()
    return Endereco(resultado[6], resultado[5], resultado[4], resultado[1], resultado[2], resultado[3], resultado[0])
    
    # return Endereco(resultado[0], resultado[6], resultado[5], resultado[4], resultado[1], resultado[2], resultado[3])