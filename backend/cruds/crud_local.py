import sys
sys.path.append("..")

from decimal import *
from classes.classe_local import Local
from database import *
from psycopg2.extensions import connection

def criar_local(db: connection, local: Local):
    cur = db.cursor()
    if not local.nome:
        local.nome = ""
    dados = (local.latitude, local.longitude, local.nome)

    cur.execute(QueriesDB.query_inserir_local_novo, dados)
    id_local: int = cur.fetchone()[0]
    
    # Como o local é parte do aluguel, o commit só pode ser dado após as demais operações
    # dele serem feitas

    # if db.in_transaction:
    #     db.rollback()

    # db.commit()
    cur.close()
    return id_local

def buscar_local_por_id (db: connection, id_local: int) -> Local:
    cur = db.cursor()
    dados = (id_local,)

    cur.execute(QueriesDB.query_buscar_local_por_id, dados)
    resultado = cur.fetchone()

    cur.close()
    if not resultado:
        return None
        
    return Local(resultado[1], resultado[2], resultado[3], resultado[0])