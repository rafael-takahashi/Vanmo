import sys
sys.path.append("..")

from decimal import *
from classes.classe_aluguel import Aluguel
from database import *
import sqlite3

def criar_aluguel(db: sqlite3.Cursor, aluguel: Aluguel): #... outros argumentos vêm aqui ):
    query = QueriesDB.query_insercao_aluguel
    # Formatar query, etc ...
    pass

def remover_aluguel():
    pass

def atualizar_aluguel():
    pass

def listar_alugueis():
    pass
