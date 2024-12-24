import sys
sys.path.append("..")

from PIL import Image
from decimal import *
from classes.classe_usuario import *
from database import *
import sqlite3

# def obter_todos_usuarios(db):
#     respota = db.cursor().execute(QueriesDB.query_buscar_todos_usuarios).fetchall()
#     return list(respota)

# Usada no auth.py
def obter_usuario_por_nome(db, nome):

    cursor: sqlite3.Cursor = db.cursor()

    return cursor.execute(QueriesDB.query_buscar_usuario_por_email, (nome,)).fetchone()

def criar_usuario(db, usuario: Usuario):

    path_foto = ""
    
    if usuario.foto is not None:
        path_foto = f"imagens/{usuario.email}.png"

        with open(path_foto, "wb+") as arquivo:
            arquivo.write(usuario.foto.file.read())

    cursor: sqlite3.Cursor = db.cursor()

    dados = (usuario.email, usuario.senha_hashed, usuario.tipo_conta, path_foto)
    cursor.execute(QueriesDB.query_inserir_usuario_novo, dados)
    
    db.commit()

def remover_usuario():
    pass

# Uso interno
def buscar_usuario():
    pass

def atualizar_usuario():
    pass
