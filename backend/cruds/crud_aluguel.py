import sys
sys.path.append("..")

from decimal import *
from classes.classe_aluguel import Aluguel
from classes.classe_usuario import Cliente
from database import *
import sqlite3

def criar_aluguel(db: sqlite3.Cursor, aluguel: Aluguel): #... outros argumentos vêm aqui ):
    query = QueriesDB.query_insercao_aluguel
    # Formatar query, etc ...
    pass

def buscar_alugueis_cliente(db: sqlite3.Cursor, cliente: Cliente) -> list[Aluguel]:
    cursor: sqlite3.Cursor = db.cursor()
    query = QueriesDB.query_buscar_alugueis_cliente
    
    alugueis = cursor.execute(query, (cliente.id,)).fetchall()

    if not alugueis:
        return alugueis
    else:
        resultado_busca = []
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
