import os
import sys
sys.path.append("..")

from PIL import Image
from decimal import *
from classes.classe_usuario import *
from classes.classe_endereco import Endereco
from classes.classe_local import Local
from cruds.crud_local import *
from cruds.crud_endereco import *
from cruds.crud_veiculo import buscar_veiculo
from database import *
from fastapi import HTTPException
import base64
import sqlite3
import utils
import datetime


# Usada no auth.py
def obter_usuario_por_nome(db: sqlite3.Connection, nome: str) -> Usuario:

    cursor: sqlite3.Cursor = db.cursor()

    resultados = cursor.execute(QueriesDB.query_buscar_usuario_por_email, (nome,)).fetchone()

    if not resultados:
        return None

    (id_usuario, email_usuario, senha_usuario, tipo_conta, path_foto, telefone) = resultados

    cursor.close()
    return Usuario(email_usuario, senha_usuario, tipo_conta, path_foto, id_usuario=id_usuario, telefone=telefone)

def criar_usuario(db: sqlite3.Connection, usuario: Usuario) -> int:

    path_foto = ""
    
    if usuario.foto is not None:
        path_foto = f"imagens/perfis/{usuario.id}.png"

        utils.salva_foto(path_foto, usuario.foto)

    cursor: sqlite3.Cursor = db.cursor()

    dados = (usuario.email, usuario.senha_hashed, usuario.tipo_conta, path_foto, usuario.telefone)
    cursor.execute(QueriesDB.query_inserir_usuario_novo, dados)
    id_usuario = cursor.lastrowid
    return id_usuario

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

        obj = buscar_veiculo(db, id_veiculo)

        if os.path.exists(obj.caminho_foto):
            os.remove(obj.caminho_foto)

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

def verificar_se_dados_ja_cadastrados(db: sqlite3.Connection, email: str) -> bool:
    cursor: sqlite3.Cursor = db.cursor()

    dados = (email,)
    query = QueriesDB.query_buscar_usuario_por_email

    resultado = cursor.execute(query, dados).fetchone()

    if resultado is None:
        return False
    return True

def cadastrar_cliente(db: sqlite3.Connection, cliente: Cliente):
    
    cliente.foto = None
    id_usr = criar_usuario(db, cliente)
    
    cursor: sqlite3.Cursor = db.cursor()

    dados_cliente = (id_usr, cliente.nome_completo, cliente.cpf, cliente.data_nascimento)
    cursor.execute(QueriesDB.query_inserir_cliente_novo, dados_cliente)
    
    db.commit()

def cadastrar_empresa(db: sqlite3.Connection, empresa: Empresa):
    
    empresa.foto = None
    id_usr = criar_usuario(db, empresa)
    
    cursor: sqlite3.Cursor = db.cursor()

    dados_local = (empresa.local.latitude, empresa.local.longitude, "sede")

    id_local = cursor.execute(QueriesDB.query_inserir_local_novo, dados_local).fetchone()
    id_local = id_local[0]

    dados_endereco = (empresa.endereco.cep, empresa.endereco.rua, empresa.endereco.numero, 
                      empresa.endereco.bairro, empresa.endereco.cidade, empresa.endereco.uf)
    
    id_endereco = cursor.execute(QueriesDB.query_inserir_endereco_novo, dados_endereco).fetchone()
    id_endereco = id_endereco[0]

    dados = (id_usr, empresa.cnpj, empresa.nome_fantasia, id_endereco, id_local, 0, 0)

    cursor.execute(QueriesDB.query_inserir_empresa_nova, dados)

    db.commit()

def buscar_dados_cliente(db: sqlite3.Connection, usuario: Usuario) -> Cliente:
    cursor: sqlite3.Cursor = db.cursor()

    dados = (usuario.id,)
    resultados = cursor.execute(QueriesDB.query_buscar_cliente, dados).fetchone()

    return Cliente(usuario.id, usuario.email, usuario.senha_hashed, usuario.tipo_conta, utils.carrega_foto_base64(usuario.foto), resultados[1], resultados[2], resultados[3], usuario.telefone)

def buscar_dados_empresa(db: sqlite3.Connection, usuario: Usuario) -> Empresa:
    cursor: sqlite3.Cursor = db.cursor()

    dados = (usuario.id,)
    resultados = cursor.execute(QueriesDB.query_buscar_empresa, dados).fetchone()

    local : Local =  buscar_local_por_id(db, resultados[4])
    endereco : Endereco = buscar_endereco_por_id(db, resultados[3])

    empresa = Empresa(id=usuario.id, email=usuario.email, senha_hashed=usuario.senha_hashed, 
                      tipo_conta=usuario.tipo_conta, foto=utils.carrega_foto_base64(usuario.foto), 
                      nome_fantasia=resultados[2], cnpj=resultados[1], endereco=endereco, local=local, telefone=usuario.telefone)

    empresa.num_avaliacoes = resultados[5]
    empresa.soma_avaliacoes = resultados[6]

    return empresa

def buscar_empresa_por_data(db: sqlite3.Connection, data_partida: datetime.date) -> list[Empresa]:
    cursor: sqlite3.Cursor = db.cursor()
    dados = (data_partida.strftime('%Y-%m-%d'),)

    resultados = cursor.execute(QueriesDB.query_buscar_empresa_por_data, dados).fetchall()

    if not resultados:
        return []
    
    else:
        empresas = []
        for resultado in resultados:
            resultado_usuario = cursor.execute(QueriesDB.query_buscar_usuario_por_id, (resultado[0],)).fetchone()

            email = resultado_usuario[1]
            senha = resultado_usuario[2]
            tipo = resultado_usuario[3]
            foto = resultado_usuario[4]
            telefone = resultado_usuario[5]

            local : Local =  buscar_local_por_id(db, resultado[4])
            endereco : Endereco = buscar_endereco_por_id(db, resultado[3])
            
            empresa = Empresa(None, None, None, None, None, None, None, None, None, None)
            
            empresa.id = resultado[0]
            empresa.email = email
            empresa.senha_hashed = senha
            empresa.tipo_conta = tipo
            empresa.foto = foto
            empresa.cnpj = resultado[1]
            empresa.nome_fantasia = resultado[2]
            empresa.endereco = endereco
            empresa.local = local
            empresa.num_avaliacoes = resultado[5]
            empresa.soma_avaliacoes = resultado[6]
            empresa.telefone = telefone

            empresa.foto = utils.carrega_foto_base64(empresa.foto)

            empresas.append(empresa)
    
    return empresas

def buscar_empresa_por_passageiros(db: sqlite3.Connection, num_passageiros: int) -> list[Empresa]:
    cursor: sqlite3.Cursor = db.cursor()
    dados = (num_passageiros,)

    resultados = cursor.execute(QueriesDB.query_buscar_empresa_por_passageiros, dados).fetchall()  

    if not resultados:
        return []
    
    else:
        empresas = []
        for resultado in resultados:
            resultado_usuario = cursor.execute(QueriesDB.query_buscar_usuario_por_id, (resultado[0],)).fetchone()

            email = resultado_usuario[1]
            senha = resultado_usuario[2]
            tipo = resultado_usuario[3]
            foto = resultado_usuario[4]
            telefone = resultado_usuario[5]

            local : Local =  buscar_local_por_id(db, resultado[4])
            endereco : Endereco = buscar_endereco_por_id(db, resultado[3])
            
            empresa = Empresa(None, None, None, None, None, None, None, None, None, None)
            
            empresa.id = resultado[0]
            empresa.email = email
            empresa.senha_hashed = senha
            empresa.tipo_conta = tipo
            empresa.foto = foto
            empresa.cnpj = resultado[1]
            empresa.nome_fantasia = resultado[2]
            empresa.endereco = endereco
            empresa.local = local
            empresa.num_avaliacoes = resultado[5]
            empresa.soma_avaliacoes = resultado[6]
            empresa.telefone = telefone

            empresa.foto = utils.carrega_foto_base64(empresa.foto)

            empresas.append(empresa)
    
    return empresas

def buscar_empresas_por_local (db: sqlite3.Connection, latitude: float, longitude:float) -> list[Empresa]:
    cursor: sqlite3.Cursor = db.cursor()
    dados = (latitude, longitude)

    resultados = cursor.execute(QueriesDB.query_buscar_empresa_por_local, dados).fetchall()  

    if not resultados:
        return []
    
    else:
        empresas = []
        for resultado in resultados:
            resultado_usuario = cursor.execute(QueriesDB.query_buscar_usuario_por_id, (resultado[0],)).fetchone()

            email = resultado_usuario[1]
            senha = resultado_usuario[2]
            tipo = resultado_usuario[3]
            foto = resultado_usuario[4]
            telefone = resultado_usuario[5]

            local : Local =  buscar_local_por_id(db, resultado[4])
            endereco : Endereco = buscar_endereco_por_id(db, resultado[3])
            
            empresa = Empresa(None, None, None, None, None, None, None, None, None, None)
            
            empresa.id = resultado[0]
            empresa.email = email
            empresa.senha_hashed = senha
            empresa.tipo_conta = tipo
            empresa.foto = foto
            empresa.cnpj = resultado[1]
            empresa.nome_fantasia = resultado[2]
            empresa.endereco = endereco
            empresa.local = local
            empresa.num_avaliacoes = resultado[5]
            empresa.soma_avaliacoes = resultado[6]
            empresa.telefone = telefone

            empresa.foto = utils.carrega_foto_base64(empresa.foto)

            empresas.append(empresa)
    
    return empresas

def buscar_empresa_por_id (db: sqlite3.Connection, id_empresa: int) -> Empresa:
    cursor: sqlite3.Cursor = db.cursor()

    dados = (id_empresa,)
    resultado_usuario = cursor.execute(QueriesDB.query_buscar_usuario_por_id, dados).fetchone()
    resultado_empresa = cursor.execute(QueriesDB.query_buscar_empresa, dados).fetchone()

    # id_usuario = resultado_usuario[0]
    email = resultado_usuario[1]
    senha = resultado_usuario[2]
    tipo = resultado_usuario[3]
    foto = resultado_usuario[4]
    telefone = resultado_usuario[5]


    local : Local =  buscar_local_por_id(db, resultado_empresa[4])
    endereco : Endereco = buscar_endereco_por_id(db, resultado_empresa[3])
    
    empresa = Empresa(None, None, None, None, None, None, None, None, None)
    
    empresa.id = id_empresa
    empresa.email = email
    empresa.senha_hashed = senha
    empresa.tipo_conta = tipo
    empresa.foto = foto
    empresa.cnpj = resultado_empresa[1]
    empresa.nome_fantasia = resultado_empresa[2]
    empresa.endereco = endereco
    empresa.local = local
    empresa.num_avaliacoes = resultado_empresa[5]
    empresa.soma_avaliacoes = resultado_empresa[6]
    empresa.telefone = telefone

    empresa.foto = utils.carrega_foto_base64(empresa.foto)
    
    return empresa

def verificar_se_avaliacao_ja_feita(db: sqlite3.Connection, id_usuario: int, id_empresa: int) -> bool:
    cursor = db.cursor()

    dados = (id_usuario, id_empresa)

    resultado = cursor.execute(QueriesDB.query_buscar_avaliacao, dados).fetchone()

    if resultado is None:
        return False
    return True

def avaliar_empresa(db: sqlite3.Connection, id_usuario: int, id_empresa: int, nota: float):
    cursor = db.cursor()

    dados = (id_usuario, id_empresa, nota)

    cursor.execute(QueriesDB.query_inserir_avaliacao_nova, dados)
    
    empresa: Empresa = buscar_empresa_por_id(db, id_empresa)

    empresa.num_avaliacoes += 1
    empresa.soma_avaliacoes += nota

    dados = (empresa.num_avaliacoes, empresa.soma_avaliacoes, id_empresa)

    cursor.execute(QueriesDB.query_atualizar_avaliacoes_empresa, dados)

    db.commit()

def atualizar_avaliacao(db: sqlite3.Connection, id_usuario: int, id_empresa: int, nota_nova: float):
    cursor = db.cursor()

    nota_antiga = cursor.execute(QueriesDB.query_buscar_avaliacao, (id_usuario, id_empresa)).fetchone()

    if nota_antiga is None:
        avaliar_empresa(db, id_usuario, id_empresa, nota_nova)
        return

    dados = (nota_nova, id_usuario, id_empresa)
    cursor.execute(QueriesDB.query_atualizar_avaliacao, dados)
    
    empresa: Empresa = buscar_empresa_por_id(db, id_empresa)

    empresa.soma_avaliacoes -= nota_antiga[2]
    empresa.soma_avaliacoes += nota_nova

    dados = (empresa.num_avaliacoes, empresa.soma_avaliacoes, id_empresa)
    cursor.execute(QueriesDB.query_atualizar_avaliacoes_empresa, dados)

    db.commit()

def buscador_empresas_nome(db: sqlite3.Connection, string_busca: str, pagina: int = 1):
    cursor = db.cursor()

    resultados = cursor.execute(QueriesDB.query_buscador_por_nome, (string_busca,)).fetchall()

    empresas: list[Empresa] = []

    for resultado in resultados:
        item: Empresa = buscar_empresa_por_id(db, resultado[0])
        item.senha_hashed = ''
        item.email = ''
        empresas.append(item)

    inicio_pag = 10 * (pagina - 1)
    fim_pag = inicio_pag + 9

    return empresas[inicio_pag:fim_pag]

def atualizar_cliente(db: sqlite3.Connection, cliente: Cliente):
    cursor = db.cursor()

    dados = (cliente.nome_completo, cliente.cpf, cliente.data_nascimento, cliente.id)

    cursor.execute(QueriesDB.query_atualizar_cliente, dados)

    db.commit()

    atualizar_usuario(db, cliente)

def atualizar_empresa(db: sqlite3.Connection, empresa: Empresa):
    cursor = db.cursor()
    dados = (empresa.cnpj, empresa.nome_fantasia, empresa.id)

    cursor.execute(QueriesDB.query_atualizar_empresa, dados)

    dados_local = (empresa.local.latitude, empresa.local.longitude, empresa.local.nome, empresa.local.id)

    cursor.execute(QueriesDB.query_atualizar_local, dados_local)

    dados_endereco = (empresa.endereco.cep, empresa.endereco.rua, empresa.endereco.numero, empresa.endereco.bairro,
                      empresa.endereco.cidade, empresa.endereco.uf, empresa.endereco.id)
    
    cursor.execute(QueriesDB.query_atualizar_endereco, dados_endereco)

    db.commit()

    atualizar_usuario(db, empresa)

def atualizar_usuario(db: sqlite3.Connection, usuario: Usuario):
    cursor = db.cursor()
    dados = (usuario.email, usuario.senha_hashed, usuario.foto, usuario.id)

    cursor.execute(QueriesDB.query_atualizar_usuario, dados)

    db.commit()