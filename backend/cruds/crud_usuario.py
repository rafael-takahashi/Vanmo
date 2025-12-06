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
from psycopg2.extensions import connection
import utils
import datetime


# Usada no auth.py
def obter_usuario_por_nome(db: connection, nome: str) -> Usuario:

    cur = db.cursor()

    cur.execute(QueriesDB.query_buscar_usuario_por_email, (nome,))
    resultados = cur.fetchone()

    if not resultados:
        cur.close()
        return None

    (id_usuario, email_usuario, senha_usuario, tipo_conta, path_foto, telefone) = resultados

    cur.close()
    return Usuario(email_usuario, senha_usuario, tipo_conta, path_foto, id_usuario=id_usuario, telefone=telefone)

def criar_usuario(db: connection, usuario: Usuario) -> int:

    path_foto = ""
    
    if usuario.foto is not None:
        path_foto = f"imagens/perfis/{usuario.id_usuario}.png"

        utils.salva_foto(path_foto, usuario.foto)

    cur = db.cursor()

    dados = (usuario.email, usuario.senha_hashed, usuario.tipo_conta, path_foto, usuario.telefone)
    cur.execute(QueriesDB.query_inserir_usuario_novo, dados)
    id_usuario = cur.fetchone()[0]
    cur.close()
    return id_usuario

def __remover_empresa(db: connection, usuario: Usuario):
    cur = db.cursor()

    empresa: Empresa = buscar_dados_empresa(db, usuario)

    dados = (empresa.id_usuario,)

    cur.execute(QueriesDB.query_buscar_alugueis_empresa, dados)
    alugueis: list[tuple] = cur.fetchall()

    for aluguel in alugueis:
        if aluguel[5] == "ativo":
            cur.close()
            raise HTTPException(status_code=400, detail="Empresa possui aluguel ativo, não pode ser excluída")
    
    for aluguel in alugueis:
        id_aluguel = aluguel[0]

        dados = (id_aluguel,)

        cur.execute(QueriesDB.query_remover_aluguel, dados)

    cur.execute(QueriesDB.query_buscar_veiculos_empresa, (empresa.id_usuario,))
    lista_veiculos: list[tuple] = cur.fetchall()
    
    for veiculo in lista_veiculos:
        id_veiculo = veiculo[0]

        dados = (id_veiculo,)

        obj = buscar_veiculo(db, id_veiculo)

        if os.path.exists(obj.caminho_foto):
            os.remove(obj.caminho_foto)

        cur.execute(QueriesDB.query_remover_calendario, dados)
        cur.execute(QueriesDB.query_remover_veiculo, dados)

    cur.execute(QueriesDB.query_remover_endereco, (empresa.endereco.id_endereco,))
    cur.execute(QueriesDB.query_remover_local, (empresa.local.id_local,))
    cur.execute(QueriesDB.query_remover_empresa, (usuario.id_usuario,))

    db.commit()
    cur.close()

def __remover_cliente(db: connection, usuario: Usuario):
    cur = db.cursor()

    cliente: Cliente = buscar_dados_cliente(db, usuario)

    dados = (cliente.id_usuario,)

    cur.execute(QueriesDB.query_buscar_alugueis_cliente, dados)
    alugueis: list[tuple] = cur.fetchall()

    for aluguel in alugueis:
        if aluguel[5] == "ativo":
            cur.close()
            raise HTTPException(status_code=400, detail="Cliente possui aluguel ativo, não pode ser excluído")
    
    for aluguel in alugueis:
        id_aluguel = aluguel[0]

        dados = (id_aluguel,)

        cur.execute(QueriesDB.query_remover_aluguel, dados)

    cur.execute(QueriesDB.query_remover_cliente, (usuario.id_usuario,))

    db.commit()
    cur.close()

def remover_usuario(db: connection, usuario: Usuario):

    dados = (usuario.id_usuario,)
    cur = db.cursor()
    
    if usuario.tipo_conta == "empresa":
        __remover_empresa(db, usuario)
    
    if usuario.tipo_conta == "cliente":
        __remover_cliente(db, usuario)

    cur.execute(QueriesDB.query_remover_usuario, dados)

    if usuario.foto != "":
        if os.path.exists(usuario.foto):
            os.remove(usuario.foto)

    db.commit()
    cur.close()

def verificar_se_dados_ja_cadastrados(db: connection, email: str) -> bool:
    cur = db.cursor()

    dados = (email,)
    query = QueriesDB.query_buscar_usuario_por_email

    cur.execute(query, dados)
    resultado = cur.fetchone()

    cur.close()
    if resultado is None:
        return False
    return True

def cadastrar_cliente(db: connection, cliente: Cliente):
    
    cliente.foto = None
    id_usr = criar_usuario(db, cliente)
    
    cur = db.cursor()

    dados_cliente = (id_usr, cliente.nome_completo, cliente.cpf, cliente.data_nascimento, cliente.foto_url)
    cur.execute(QueriesDB.query_inserir_cliente_novo, dados_cliente)
    
    db.commit()
    cur.close()

def cadastrar_empresa(db: connection, empresa: Empresa):
    
    empresa.foto = None
    id_usr = criar_usuario(db, empresa)
    
    cur = db.cursor()

    dados_local = (empresa.local.latitude, empresa.local.longitude, "sede")

    cur.execute(QueriesDB.query_inserir_local_novo, dados_local)
    id_local = cur.fetchone()[0]

    dados_endereco = (empresa.endereco.cep, empresa.endereco.rua, empresa.endereco.numero, 
                      empresa.endereco.bairro, empresa.endereco.cidade, empresa.endereco.uf)
    
    cur.execute(QueriesDB.query_inserir_endereco_novo, dados_endereco)
    id_endereco = cur.fetchone()[0]

    dados = (id_usr, empresa.cnpj, empresa.nome_fantasia, id_endereco, id_local, 0, 0, empresa.foto_url)

    cur.execute(QueriesDB.query_inserir_empresa_nova, dados)

    db.commit()
    cur.close()

def buscar_usuario_por_id(db: connection, id_usuario: int) -> Usuario:
    cur = db.cursor()

    dados = (id_usuario,)
    cur.execute(QueriesDB.query_buscar_usuario_por_id, dados)
    resultados = cur.fetchone()

    cur.close()
    return Usuario(resultados[1], resultados[2], resultados[3], resultados[4], resultados[5], resultados[0])
    
def buscar_dados_cliente(db: connection, usuario: Usuario) -> Cliente:
    cur = db.cursor()

    dados = (usuario.id_usuario,)
    cur.execute(QueriesDB.query_buscar_cliente, dados)
    resultados = cur.fetchone()

    cur.close()
    foto_url = resultados[4] if len(resultados) > 4 else None
    return Cliente(usuario.id_usuario, usuario.email, usuario.senha_hashed, usuario.tipo_conta, utils.carrega_foto_base64(usuario.foto), resultados[1], resultados[2], resultados[3], usuario.telefone, foto_url)

def buscar_dados_empresa(db: connection, usuario: Usuario) -> Empresa:
    cur = db.cursor()

    dados = (usuario.id_usuario,)
    cur.execute(QueriesDB.query_buscar_empresa, dados)
    resultados = cur.fetchone()

    local : Local =  buscar_local_por_id(db, resultados[4])
    endereco : Endereco = buscar_endereco_por_id(db, resultados[3])
    
    foto_url = resultados[7] if len(resultados) > 7 else None

    empresa = Empresa(id_usuario=usuario.id_usuario, email=usuario.email, senha_hashed=usuario.senha_hashed, 
                      tipo_conta=usuario.tipo_conta, foto=utils.carrega_foto_base64(usuario.foto), 
                      nome_fantasia=resultados[2], cnpj=resultados[1], endereco=endereco, local=local, telefone=usuario.telefone, foto_url=foto_url)

    empresa.num_avaliacoes = resultados[5]
    empresa.soma_avaliacoes = resultados[6]

    cur.close()
    return empresa

def buscar_empresa_por_data(db: connection, data_partida: datetime.date) -> list[int]:
    cur = db.cursor()
    dados = (data_partida.strftime('%Y-%m-%d'),)

    cur.execute(QueriesDB.query_buscar_empresa_por_data, dados)
    resultados = cur.fetchall()
    
    cur.close()
    return resultados

def buscar_empresa_por_passageiros(db: connection, num_passageiros: int) -> list[int]:
    cur = db.cursor()
    dados = (num_passageiros,)

    cur.execute(QueriesDB.query_buscar_empresa_por_passageiros, dados)
    resultados = cur.fetchall()  

    cur.close()
    return resultados

def buscar_empresas_por_local (db: connection, latitude: float, longitude:float) -> list[int]:
    cur = db.cursor()
    dados = (latitude, longitude)

    cur.execute(QueriesDB.query_buscar_empresa_por_local, dados)
    resultados = cur.fetchall()  
    
    cur.close()
    return resultados

def buscar_todas_empresas (db: connection) -> list[Empresa]:
    cur = db.cursor()

    empresas = []
    cur.execute(QueriesDB.query_buscar_todas_empresas)
    resultados = cur.fetchall()

    for resultado in resultados:
        cur.execute(QueriesDB.query_buscar_usuario_por_id, (resultado[0],))
        resultado_usuario = cur.fetchone()

        # email = resultado_usuario[1]
        # senha = resultado_usuario[2]
        tipo = resultado_usuario[3]
        foto = resultado_usuario[4]
        telefone = resultado_usuario[5]

        local : Local =  buscar_local_por_id(db, resultado[4])
        endereco : Endereco = buscar_endereco_por_id(db, resultado[3])
        
        # empresa = Empresa(None, None, None, None, None, None, None, None, None, None)
        empresa = Empresa(resultado[0], "", "", tipo, foto, resultado[2], resultado[1], endereco, local, telefone)            
        # empresa.id_usuario = resultado[0]
        # empresa.email = email
        # empresa.senha_hashed = senha
        # empresa.tipo_conta = tipo
        # empresa.foto = foto
        # empresa.cnpj = resultado[1]
        # empresa.nome_fantasia = resultado[2]
        # empresa.endereco = endereco
        # empresa.local = local
        # empresa.num_avaliacoes = resultado[5]
        # empresa.soma_avaliacoes = resultado[6]
        # empresa.telefone = telefone
        
        foto_url = resultado[7] if len(resultado) > 7 else None
        empresa.foto_url = foto_url

        empresa.foto = utils.carrega_foto_base64(empresa.foto)

        empresas.append(empresa)
    
    cur.close()
    return empresas
    
def buscar_empresa_por_id (db: connection, id_empresa: int) -> Empresa:
    cur = db.cursor()

    dados = (id_empresa,)
    cur.execute(QueriesDB.query_buscar_usuario_por_id, dados)
    resultado_usuario = cur.fetchone()
    cur.execute(QueriesDB.query_buscar_empresa, dados)
    resultado_empresa = cur.fetchone()

    # id_usuario = resultado_usuario[0]
    # email = resultado_usuario[1]
    # senha = resultado_usuario[2]
    tipo = resultado_usuario[3]
    foto = resultado_usuario[4]
    telefone = resultado_usuario[5]


    local : Local =  buscar_local_por_id(db, resultado_empresa[4])
    endereco : Endereco = buscar_endereco_por_id(db, resultado_empresa[3])
    
    # empresa = Empresa(None, None, None, None, None, None, None, None, None)
    empresa = Empresa(resultado_empresa[0], "", "", tipo, foto, resultado_empresa[2], resultado_empresa[1], endereco, local, telefone)    
    # empresa.id_usuario = id_empresa
    # empresa.email = email
    # empresa.senha_hashed = senha
    # empresa.tipo_conta = tipo
    # empresa.foto = foto
    # empresa.cnpj = resultado_empresa[1]
    # empresa.nome_fantasia = resultado_empresa[2]
    # empresa.endereco = endereco
    # empresa.local = local
    # empresa.num_avaliacoes = resultado_empresa[5]
    # empresa.soma_avaliacoes = resultado_empresa[6]
    # empresa.telefone = telefone

    foto_url = resultado_empresa[7] if len(resultado_empresa) > 7 else None
    empresa.foto_url = foto_url
    
    empresa.foto = utils.carrega_foto_base64(empresa.foto)
    
    cur.close()
    return empresa

def verificar_se_avaliacao_ja_feita(db: connection, id_usuario: int, id_empresa: int) -> bool:
    cur = db.cursor()

    dados = (id_usuario, id_empresa)

    cur.execute(QueriesDB.query_buscar_avaliacao, dados)
    resultado = cur.fetchone()

    cur.close()
    if resultado is None:
        return False
    return True

def avaliar_empresa(db: connection, id_usuario: int, id_empresa: int, nota: float):
    cur = db.cursor()

    dados = (id_usuario, id_empresa, nota)

    cur.execute(QueriesDB.query_inserir_avaliacao_nova, dados)
    
    empresa: Empresa = buscar_empresa_por_id(db, id_empresa)

    empresa.num_avaliacoes += 1
    empresa.soma_avaliacoes += nota

    dados = (empresa.num_avaliacoes, empresa.soma_avaliacoes, id_empresa)

    cur.execute(QueriesDB.query_atualizar_avaliacoes_empresa, dados)

    db.commit()
    cur.close()

def atualizar_avaliacao(db: connection, id_usuario: int, id_empresa: int, nota_nova: float):
    cur = db.cursor()

    cur.execute(QueriesDB.query_buscar_avaliacao, (id_usuario, id_empresa))
    nota_antiga = cur.fetchone()

    if nota_antiga is None:
        cur.close()
        avaliar_empresa(db, id_usuario, id_empresa, nota_nova)
        return

    dados = (nota_nova, id_usuario, id_empresa)
    cur.execute(QueriesDB.query_atualizar_avaliacao, dados)
    
    empresa: Empresa = buscar_empresa_por_id(db, id_empresa)

    empresa.soma_avaliacoes -= nota_antiga[2]
    empresa.soma_avaliacoes += nota_nova

    dados = (empresa.num_avaliacoes, empresa.soma_avaliacoes, id_empresa)
    cur.execute(QueriesDB.query_atualizar_avaliacoes_empresa, dados)

    db.commit()
    cur.close()

def buscador_empresas_nome(db: connection, string_busca: str):
    cur = db.cursor()

    cur.execute(QueriesDB.query_buscador_por_nome, (string_busca,))
    resultados = cur.fetchall()

    empresas: list[Empresa] = []

    for resultado in resultados:
        item: Empresa = buscar_empresa_por_id(db, resultado[0])
        item.senha_hashed = ''
        item.email = ''
        empresas.append(item)

    cur.close()
    return empresas

def atualizar_cliente(db: connection, cliente: Cliente):
    cur = db.cursor()

    dados = (cliente.nome_completo, cliente.cpf, cliente.data_nascimento, cliente.foto_url, cliente.id_usuario)

    cur.execute(QueriesDB.query_atualizar_cliente, dados)

    db.commit()
    cur.close()

    atualizar_usuario(db, cliente)

def atualizar_empresa(db: connection, empresa: Empresa):
    cur = db.cursor()
    dados = (empresa.cnpj, empresa.nome_fantasia, empresa.foto_url, empresa.id_usuario)

    cur.execute(QueriesDB.query_atualizar_empresa, dados)

    dados_local = (empresa.local.latitude, empresa.local.longitude, empresa.local.nome, empresa.local.id_local)

    cur.execute(QueriesDB.query_atualizar_local, dados_local)

    dados_endereco = (empresa.endereco.cep, empresa.endereco.rua, empresa.endereco.numero, empresa.endereco.bairro,
                      empresa.endereco.cidade, empresa.endereco.uf, empresa.endereco.id_endereco)
    
    cur.execute(QueriesDB.query_atualizar_endereco, dados_endereco)

    db.commit()
    cur.close()

    atualizar_usuario(db, empresa)

def atualizar_usuario(db: connection, usuario: Usuario):
    cur = db.cursor()
    dados = (usuario.email, usuario.senha_hashed, usuario.foto, usuario.telefone, usuario.id_usuario)

    cur.execute(QueriesDB.query_atualizar_usuario, dados)

    db.commit()
    cur.close()