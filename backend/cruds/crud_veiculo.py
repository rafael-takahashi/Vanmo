import sys
sys.path.append("..")

from fastapi import HTTPException
from decimal import *
from classes.classe_usuario import *
from database import *
from copy import deepcopy
from classes import classe_veiculo, classe_calendario
import utils
from psycopg2.extensions import connection
import datetime
import os
import base64

def criar_veiculo(db: connection, veiculo: classe_veiculo.Veiculo) -> int:
    cur = db.cursor()
    dados = (veiculo.id_empresa, veiculo.nome_veiculo, veiculo.placa_veiculo, veiculo.capacidade, veiculo.custo_por_km, veiculo.custo_base, veiculo.caminho_foto, veiculo.cor, veiculo.ano_fabricacao)

    cur.execute(QueriesDB.query_inserir_veiculo_novo, dados)
    id_veiculo: int = cur.fetchone()[0]
    db.commit()

    if veiculo.caminho_foto is not None:
        path_foto = f"imagens/veiculos/{veiculo.id_empresa}-{id_veiculo}.png"
        utils.salva_foto(path_foto, veiculo.caminho_foto)

    cur.close()
    return id_veiculo

def remover_veiculo(db: connection, id_veiculo: int):
    cur = db.cursor()
    dados = (id_veiculo,)
    
    obj = buscar_veiculo(db, id_veiculo)

    if obj.caminho_foto is not None and os.path.exists(obj.caminho_foto):
        os.remove(obj.caminho_foto)

    cur.execute(QueriesDB.query_remover_veiculo, dados)
    
    db.commit()
    cur.close()

# Apenas um específico
def buscar_veiculo(db: connection, id_veiculo: int) -> classe_veiculo.Veiculo: 
    cur = db.cursor()
    dados = (id_veiculo,)

    cur.execute(QueriesDB.query_buscar_veiculo, dados)
    resultado = cur.fetchone()

    if resultado is None:
        cur.close()
        return None
    
    veiculo = classe_veiculo.Veiculo(id_veiculo, resultado[1], resultado[2], resultado[3])
    veiculo.adicionar_custos(resultado[5], resultado[6])
    veiculo.adicionar_dados(resultado[7], resultado[8], resultado[9], resultado[4])

    veiculo.calendario_disponibilidade = classe_calendario.Calendario([])

    cur.execute(QueriesDB.query_buscar_calendario_veiculo, (id_veiculo,))
    datas_indisponiveis = cur.fetchall()

    for data in datas_indisponiveis:
        veiculo.calendario_disponibilidade.datas_indisponiveis.append(data[1])  # data_indisponivel está na coluna 1

    # veiculo.caminho_foto = utils.carrega_foto_base64(veiculo.caminho_foto, True)

    cur.close()
    return veiculo

# Todos os veículos da empresa
def listar_veiculos(db: connection, id_empresa: int) -> list[classe_veiculo.Veiculo]:
    cur = db.cursor()
    dados = (id_empresa,)

    cur.execute(QueriesDB.query_buscar_veiculos_empresa, dados)
    lista_resultados = cur.fetchall()

    veiculos = []

    for resultado in lista_resultados:
        # veiculo = classe_veiculo.Veiculo(resultado[0], resultado[1], resultado[2], resultado[3])
        # veiculo.adicionar_custos(resultado[5], resultado[6])
        # veiculo.adicionar_dados(resultado[7], resultado[8], resultado[9], resultado[4])

        veiculo = buscar_veiculo(db, resultado[0])
        
        veiculos.append(deepcopy(veiculo))

    cur.close()
    return veiculos

def atualizar_veiculo(db: connection, veiculo: classe_veiculo.Veiculo):
    cur = db.cursor()
    dados = (veiculo.id_empresa, veiculo.nome_veiculo, veiculo.placa_veiculo, veiculo.capacidade, veiculo.custo_por_km, veiculo.custo_base, veiculo.caminho_foto, veiculo.cor, veiculo.ano_fabricacao, veiculo.id_veiculo)

    if veiculo.caminho_foto is not None:
        utils.salva_foto(f"imagens/veiculos/{veiculo.id_empresa}-{veiculo.id_veiculo}.png", veiculo.caminho_foto)

    cur.execute(QueriesDB.query_atualizar_veiculo, dados)

    db.commit()
    cur.close()

def verificar_alugueis_veiculo(db: connection, id_veiculo: int) -> bool:
    cur = db.cursor()
    dados = (id_veiculo,)

    cur.execute(QueriesDB.query_buscar_alugueis_veiculo, dados)
    resultados = cur.fetchall()

    for resultado in resultados:
        if resultado[5] == "ativo":  # status aluguel
            cur.close()
            return True
    
    cur.close()
    return False

def verificar_veiculo_empresa(db: connection, id_veiculo: int, id_empresa: int) -> bool:
    cur = db.cursor()
    dados = (id_veiculo, id_empresa)

    cur.execute(QueriesDB.query_verificar_veiculo_empresa, dados)
    resultado = cur.fetchone()
    
    cur.close()
    return resultado is not None

def verificar_disponibilidade_veiculo(db: connection, id_veiculo: int, data_inicio: datetime.date, data_fim: datetime.date) -> bool:
    cur = db.cursor()
    dados = (id_veiculo, data_inicio, data_fim)

    cur.execute(QueriesDB.query_verificar_disponibilidade_veiculo, dados)
    resultado = cur.fetchone()

    cur.close()
    return resultado is None

def atualizar_calendario(db: connection, id_veiculo: int, calendario: classe_calendario.Calendario):
    # TODO: talvez refazer o método, implementação provisória
    # OBS: assume-se que o objeto calendario já foi validado previamente
    cur = db.cursor()

    try:
        cur.execute(QueriesDB.query_remover_calendario, (id_veiculo,))

        # cria uma lista com todos os valores a serem inseridos
        dados = [(id_veiculo, data.strftime('%Y-%m-%d')) for data in calendario.datas_indisponiveis]
        cur.executemany(QueriesDB.query_inserir_calendario, dados)
        
        db.commit()
        cur.close()
    
    except Exception as e:
        db.rollback()
        cur.close()
        raise e