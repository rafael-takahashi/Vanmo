import os
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
def obter_usuario_por_nome(db: sqlite3.Connection, nome: str) -> Usuario:

    cursor: sqlite3.Cursor = db.cursor()

    # usuario = Usuario()

    resultados = cursor.execute(QueriesDB.query_buscar_usuario_por_email, (nome,)).fetchone()

    if not resultados:
        return None

    (id_usuario, email_usuario, senha_usuario, tipo_conta, path_foto) = resultados

    return Usuario(email_usuario, senha_usuario, tipo_conta, path_foto, id=id_usuario)

def criar_usuario(db: sqlite3.Connection, usuario: Usuario):

    path_foto = ""
    
    if usuario.foto is not None:
        path_foto = f"imagens/{usuario.email}.png"

        with open(path_foto, "wb+") as arquivo:
            arquivo.write(usuario.foto.file.read())

    cursor: sqlite3.Cursor = db.cursor()

    dados = (usuario.email, usuario.senha_hashed, usuario.tipo_conta, path_foto)
    cursor.execute(QueriesDB.query_inserir_usuario_novo, dados)
    
    db.commit()

def remover_usuario(db: sqlite3.Connection, usuario: Usuario):

    if usuario.foto != "":
        if os.path.exists(usuario.foto):
            os.remove(usuario.foto)

    dados = (usuario.id,)

    cursor: sqlite3.Cursor = db.cursor()

    cursor.execute(QueriesDB.query_remover_usuario, dados)

    db.commit()

def cadastrar_cliente(db: sqlite3.Connection, cliente: Cliente):
    cursor: sqlite3.Cursor = db.cursor()

    dados = (cliente.id, cliente.nome_completo, cliente.cpf)
    cursor.execute(QueriesDB.query_inserir_cliente_novo, dados)
    
    db.commit()

def cadastrar_empresa(db: sqlite3.Connection, empresa: Empresa):
    cursor: sqlite3.Cursor = db.cursor()

    dados_local = (empresa.local.latitude, empresa.local.longitude, "sede")

    id_local = cursor.execute(QueriesDB.query_inserir_local_novo, dados_local).fetchone()
    id_local = id_local[0]

    # cep, rua, numero, bairro, cidade, estado
    dados_endereco = (empresa.endereco.cep, empresa.endereco.rua, empresa.endereco.numero, 
                      empresa.endereco.bairro, empresa.endereco.cidade, empresa.endereco.uf)
    
    id_endereco = cursor.execute(QueriesDB.query_inserir_endereco_novo, dados_endereco).fetchone()
    id_endereco = id_endereco[0]

    dados = (empresa.id, empresa.cnpj, empresa.nome_fantasia, id_endereco, id_local, 0, 0)

    cursor.execute(QueriesDB.query_inserir_empresa_nova, dados)
    
    db.commit()

def buscar_usuario():
    pass

def atualizar_usuario():
    pass
