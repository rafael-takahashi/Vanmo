import sys
sys.path.append("..")

from decimal import *
from classes.classe_aluguel import Aluguel
from classes.classe_usuario import Usuario
from database import *
import sqlite3

def criar_aluguel(db: sqlite3.Connection, aluguel: Aluguel): #... outros argumentos vêm aqui ):
    cursor: sqlite3.Cursor = db.cursor()

    dados = (aluguel.id_empresa, aluguel.id_cliente, aluguel.id_veiculo, float(aluguel.valor_total), aluguel.estado_aluguel,
             aluguel.data_inicio.strftime('%Y-%m-%d'), aluguel.data_fim.strftime('%Y-%m-%d'), float(aluguel.distancia_trajeto), float(aluguel.distancia_extra), aluguel.local_partida.id, aluguel.local_chegada.id)
    
    print(dados)
    cursor.execute(QueriesDB.query_inserir_aluguel_novo, dados)
    # cursor.execute(QueriesDB.query_inserir_aluguel_novo, (2, 1, 1, 150.3, 'ativo', '2024-01-01', '2024-01-05', 200.3, 10.1, 1, 2))
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

def remover_aluguel():
    pass

def atualizar_aluguel():
    pass

def listar_alugueis():
    pass
