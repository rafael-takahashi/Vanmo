import os
import sys
sys.path.append("..")

from PIL import Image
from decimal import *
from classes.classe_usuario import *
from classes.classe_endereco import Endereco
from classes.classe_local import Local
from crud_local import *
from crud_endereco import *
from database import *
from fastapi import HTTPException
import sqlite3

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
        path_foto = f"imagens/perfis/{usuario.id}.png"

        with open(path_foto, "wb+") as arquivo:
            arquivo.write(usuario.foto.file.read())

    cursor: sqlite3.Cursor = db.cursor()

    dados = (usuario.email, usuario.senha_hashed, usuario.tipo_conta, path_foto)
    cursor.execute(QueriesDB.query_inserir_usuario_novo, dados)
    
    db.commit()

def __remover_empresa(db: sqlite3.Connection, usuario: Usuario):
    cursor = db.cursor()

    empresa: Empresa = buscar_dados_empresa(db, usuario)

    dados = (empresa.id,)

    alugueis: list[tuple] = cursor.execute(QueriesDB.query_buscar_alugueis_empresa, dados).fetchall()

    for aluguel in alugueis:
        if aluguel[5] == "ativo":
            raise HTTPException(status_code=400, detail="Empresa possui aluguel ativo, não pode ser excluída")
    
    for aluguel in alugueis:
        id_aluguel = aluguel[0]

        dados = (id_aluguel,)

        cursor.execute(QueriesDB.query_remover_aluguel, dados)

    lista_veiculos: list[tuple] = cursor.execute(QueriesDB.query_buscar_veiculos_empresa, dados).fetchall()
    
    for veiculo in lista_veiculos:
        id_veiculo = veiculo[0]

        dados = (id_veiculo,)

        cursor.execute(QueriesDB.query_remover_calendario, dados)
        cursor.execute(QueriesDB.query_remover_veiculo, dados)

    cursor.execute(QueriesDB.query_remover_endereco, (empresa.endereco,))
    cursor.execute(QueriesDB.query_remover_local, (empresa.local,))
    cursor.execute(QueriesDB.query_remover_empresa, (usuario.id,))

    db.commit()

def __remover_cliente(db: sqlite3.Connection, usuario: Usuario):
    cursor: sqlite3.Cursor = db.cursor()

    cliente: Cliente = buscar_dados_cliente(db, usuario)

    dados = (cliente.id,)

    alugueis: list[tuple] = cursor.execute(QueriesDB.query_buscar_alugueis_cliente, dados).fetchall()

    for aluguel in alugueis:
        if aluguel[5] == "ativo":
            raise HTTPException(status_code=400, detail="Cliente possui aluguel ativo, não pode ser excluído")
    
    for aluguel in alugueis:
        id_aluguel = aluguel[0]

        dados = (id_aluguel,)

        cursor.execute(QueriesDB.query_remover_aluguel, dados)

    cursor.execute(QueriesDB.query_remover_cliente, (usuario.id,))

    db.commit()

def remover_usuario(db: sqlite3.Connection, usuario: Usuario):

    dados = (usuario.id,)
    cursor: sqlite3.Cursor = db.cursor()
    
    if usuario.tipo_conta == "empresa":
        __remover_empresa(db, usuario)
    
    if usuario.tipo_conta == "cliente":
        __remover_cliente(db, usuario)

    cursor.execute(QueriesDB.query_remover_usuario, dados)

    if usuario.foto != "":
        if os.path.exists(usuario.foto):
            os.remove(usuario.foto)

    db.commit()

def verificar_se_dados_ja_cadastrados(db: sqlite3.Connection, email: str, tipo_conta: str) -> bool:
    cursor: sqlite3.Cursor = db.cursor()

    dados = (email,)
    query = QueriesDB.query_buscar_empresa
    if tipo_conta == "cliente":
        query = QueriesDB.query_buscar_cliente

    resultado = cursor.execute(query, dados).fetchone()

    if resultado is None:
        return False
    return True

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

    dados_endereco = (empresa.endereco.cep, empresa.endereco.rua, empresa.endereco.numero, 
                      empresa.endereco.bairro, empresa.endereco.cidade, empresa.endereco.uf)
    
    id_endereco = cursor.execute(QueriesDB.query_inserir_endereco_novo, dados_endereco).fetchone()
    id_endereco = id_endereco[0]

    dados = (empresa.id, empresa.cnpj, empresa.nome_fantasia, id_endereco, id_local, 0, 0)

    cursor.execute(QueriesDB.query_inserir_empresa_nova, dados)
    
    db.commit()

def buscar_dados_cliente(db: sqlite3.Connection, usuario: Usuario) -> Cliente:
    cursor: sqlite3.Cursor = db.cursor()

    dados = (usuario.id,)
    resultados = cursor.execute(QueriesDB.query_buscar_cliente, dados).fetchone()

    return Cliente(usuario.id, usuario.email, usuario.senha_hashed, usuario.tipo_conta, usuario.foto, resultados[1], resultados[2])

def buscar_dados_empresa(db: sqlite3.Connection, usuario: Usuario) -> Empresa:
    cursor: sqlite3.Cursor = db.cursor()

    dados = (usuario.id,)
    resultados = cursor.execute(QueriesDB.query_buscar_empresa, dados).fetchone()

    local : Local =  buscar_local_por_id(db, resultados[4])
    endereco : Endereco = buscar_endereco_por_id(db, resultados[3])

    # TODO: Não esquecer de recuperar as avaliações quando forem implementadas

    empresa = Empresa(usuario.id, usuario.email, usuario.senha_hashed, usuario.tipo_conta, usuario.foto, 
                     resultados[2], resultados[1], endereco, local)

    return empresa

def buscar_empresa_por_id (db: sqlite3.Connection, id_empresa: int) -> Empresa:
    cursor: sqlite3.Cursor = db.cursor()

    dados = (id_empresa,)
    resultado_usuario = cursor.execute(QueriesDB.query_buscar_usuario_por_id, dados).fetchone()
    resultado_empresa = cursor.execute(QueriesDB.query_buscar_empresa, dados).fetchone()

    local : Local =  buscar_local_por_id(db, resultado_empresa[4])
    endereco : Endereco = buscar_endereco_por_id(db, resultado_empresa[3])

    # TODO: Não esquecer de recuperar as avaliações quando forem implementadas
    
    empresa = Empresa(resultado_usuario[0], resultado_usuario[1], resultado_usuario[2], resultado_usuario[3], resultado_usuario[4],
                      resultado_empresa[2], resultado_empresa[1], endereco, local)

