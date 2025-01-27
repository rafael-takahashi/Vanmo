import sys
sys.path.append("..")

from decimal import *
from classes.classe_aluguel import Aluguel
from classes.classe_usuario import Usuario
from classes.classe_local import Local
from database import *
from cruds.crud_local import buscar_local_por_id
import sqlite3

def criar_aluguel(db: sqlite3.Connection, aluguel: Aluguel):
    cursor: sqlite3.Cursor = db.cursor()

    dados = (aluguel.id_empresa, aluguel.id_cliente, aluguel.id_veiculo, aluguel.valor_total, aluguel.estado_aluguel, 
             aluguel.data_inicio.strftime('%Y-%m-%d'), aluguel.data_fim.strftime('%Y-%m-%d'), aluguel.distancia_trajeto, aluguel.distancia_extra, aluguel.local_partida.id_local, aluguel.local_chegada.id_local)
    
    cursor.execute(QueriesDB.query_inserir_aluguel_novo, dados)
    db.commit()

def buscar_alugueis_usuario_id(db: sqlite3.Connection, id_usuario: int) -> list[Aluguel]:
    cursor: sqlite3.Cursor = db.cursor()
    query = QueriesDB.query_buscar_alugueis_cliente
    
    alugueis = cursor.execute(query, (id_usuario,)).fetchall()

    if not alugueis:
        return alugueis
    
    else:
        resultado_busca: list[Aluguel] = []
        for aluguel in alugueis:
            item = Aluguel(aluguel[0], aluguel[2], aluguel[1], aluguel[3])
            item.adicionar_datas(aluguel[6], aluguel[7])
            local_partida: Local = buscar_local_por_id(db, aluguel[10])
            local_chegada: Local = buscar_local_por_id(db, aluguel[11])
            item.adicionar_locais(local_partida, local_chegada)
            item.adicionar_distancia_extra(aluguel[9])
            item.estado_aluguel = aluguel[5]
            resultado_busca.append(item)
        return resultado_busca

def buscar_aluguel(db: sqlite3.Connection, id_aluguel: int) -> Aluguel | None:
    cursor: sqlite3.Cursor = db.cursor()
    query = QueriesDB.query_buscar_aluguel
    
    resultado = cursor.execute(query, (id_aluguel,)).fetchone()

    if resultado is None:
        return None
    
    aluguel = Aluguel(id_aluguel, resultado[2], resultado[1], resultado[3])
    aluguel.adicionar_datas(resultado[6], resultado[7])
    local_partida: Local = buscar_local_por_id(db, resultado[10])
    local_chegada: Local = buscar_local_por_id(db, resultado[11])
    aluguel.adicionar_locais(local_partida, local_chegada)
    aluguel.adicionar_distancia_extra(resultado[9])
    aluguel.estado_aluguel = resultado[5]

    return aluguel

def alterar_status_aluguel(db: sqlite3.Connection, id_aluguel: int, novo_status: str):
    cursor: sqlite3.Cursor = db.cursor()
    query = QueriesDB.query_alterar_status_aluguel

    cursor.execute(query, (novo_status, id_aluguel))

    db.commit()

def remover_aluguel(db: sqlite3.Connection, id_aluguel: int):
    cursor = db.cursor()

    cursor.execute(QueriesDB.query_remover_aluguel, (id_aluguel,))

    db.commit()
