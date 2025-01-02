import sys
sys.path.append("..")

from decimal import *
from classes.classe_aluguel import Aluguel
from classes.classe_usuario import Usuario
from database import *
import sqlite3

def criar_aluguel(db: sqlite3.Connection, aluguel: Aluguel): #... outros argumentos vêm aqui ):
    cursor: sqlite3.Cursor = db.cursor()

    dados = (aluguel.id_empresa, aluguel.id_cliente, aluguel.id_veiculo, aluguel.valor_total, aluguel.estado_aluguel, 
             aluguel.data_inicio.strftime('%Y-%m-%d'), aluguel.data_fim.strftime('%Y-%m-%d'), aluguel.distancia_trajeto, aluguel.distancia_extra, aluguel.local_partida.id, aluguel.local_chegada.id)
    
    print(dados)
    cursor.execute(QueriesDB.query_inserir_aluguel_novo, dados)
    db.commit()

def buscar_alugueis_usuario(db: sqlite3.Connection, usuario: Usuario) -> list[Aluguel]:
    cursor: sqlite3.Cursor = db.cursor()
    query = QueriesDB.query_buscar_alugueis_cliente
    
    alugueis = cursor.execute(query, (usuario.id,)).fetchall()

    if not alugueis:
        return alugueis
    
    else:
        resultado_busca: list[Aluguel] = []
        for aluguel in alugueis:
            item = Aluguel(aluguel[0], aluguel[2], aluguel[1], aluguel[3])
            item.adicionar_datas(aluguel[6], aluguel[7])
            item.adicionar_locais(aluguel[10], aluguel[11])
            item.adicionar_distancia_extra(aluguel[9])
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
    aluguel.adicionar_locais(resultado[10], resultado[11])
    aluguel.adicionar_distancia_extra(resultado[9])

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

def atualizar_aluguel():
    pass

def listar_alugueis():
    pass
