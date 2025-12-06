from dataclasses import dataclass
import os
import psycopg2
from psycopg2.extensions import connection, cursor
from typing import Union
import datetime
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

def conectar_bd() -> connection:
    """
    Cria uma conexão com o banco de dados PostgreSQL

    :return: Uma instância de Connection
    """
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "vanmo_db")
    db_user = os.getenv("DB_USER", "vanmo_user")
    db_password = os.getenv("DB_PASSWORD", "vanmo_password")
    
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )


def criar_tabelas(conexao: connection):
    """
    Cria as tabelas do banco de dados caso elas não existam

    :param conexao: A conexão com o banco de dados PostgreSQL
    """

    cur: cursor = conexao.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Usuario(
            id_usuario SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            senha_hashed TEXT NOT NULL,
            tipo_conta VARCHAR(50) NOT NULL,
            path_foto TEXT,
            telefone VARCHAR(20)
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Cliente(
            id_usuario INTEGER REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
            nome_completo VARCHAR(255) NOT NULL,
            cpf VARCHAR(14) NOT NULL,
            data_nascimento DATE,
            foto_url TEXT
        )
    """)
    
    # Adiciona coluna foto_url se não existir (para tabelas já criadas)
    cur.execute("""
        DO $$ 
        BEGIN 
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='cliente' AND column_name='foto_url') THEN
                ALTER TABLE Cliente ADD COLUMN foto_url TEXT;
            END IF;
        END $$;
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Endereco(
            id_endereco SERIAL PRIMARY KEY,
            cep VARCHAR(10),
            rua VARCHAR(255),
            numero VARCHAR(20),
            bairro VARCHAR(255),
            cidade VARCHAR(255),
            estado VARCHAR(2)
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Local(
            id_local SERIAL PRIMARY KEY,
            latitude DECIMAL(10, 8),
            longitude DECIMAL(11, 8),
            nome VARCHAR(255)
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Empresa(
            id_usuario INTEGER REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
            cnpj VARCHAR(18) NOT NULL,
            nome_fantasia VARCHAR(255) NOT NULL,
            id_endereco INTEGER REFERENCES Endereco(id_endereco),
            id_local INTEGER REFERENCES Local(id_local),
            num_avaliacoes INTEGER DEFAULT 0,
            soma_avaliacoes DECIMAL(10, 2) DEFAULT 0,
            foto_url TEXT
        )
    """)
    
    # Adiciona coluna foto_url se não existir (para tabelas já criadas)
    cur.execute("""
        DO $$ 
        BEGIN 
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='empresa' AND column_name='foto_url') THEN
                ALTER TABLE Empresa ADD COLUMN foto_url TEXT;
            END IF;
        END $$;
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Veiculo(
            id_veiculo SERIAL PRIMARY KEY,
            id_empresa INTEGER REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
            nome_veiculo VARCHAR(255) NOT NULL,
            placa_veiculo VARCHAR(10) NOT NULL,
            capacidade INTEGER NOT NULL,
            custo_por_km DECIMAL(10, 2) NOT NULL,
            custo_base DECIMAL(10, 2) NOT NULL,
            path_foto TEXT,
            cor VARCHAR(50),
            ano_de_fabricacao INTEGER,
            foto_url TEXT
        )
    """)
    
    # Adiciona coluna foto_url se não existir (para tabelas já criadas)
    cur.execute("""
        DO $$ 
        BEGIN 
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='veiculo' AND column_name='foto_url') THEN
                ALTER TABLE Veiculo ADD COLUMN foto_url TEXT;
            END IF;
        END $$;
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Aluguel(
            id_aluguel SERIAL PRIMARY KEY,
            id_empresa INTEGER REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
            id_cliente INTEGER REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
            id_veiculo INTEGER REFERENCES Veiculo(id_veiculo) ON DELETE CASCADE,
            valor_total DECIMAL(10, 2),
            estado_aluguel VARCHAR(50),
            data_inicio DATE,
            data_fim DATE,
            distancia_trajeto DECIMAL(10, 2),
            distancia_extra DECIMAL(10, 2),
            id_local_partida INTEGER REFERENCES Local(id_local),
            id_local_chegada INTEGER REFERENCES Local(id_local)
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Calendario(
            id_veiculo INTEGER REFERENCES Veiculo(id_veiculo) ON DELETE CASCADE,
            data_indisponivel DATE,
            PRIMARY KEY (id_veiculo, data_indisponivel)
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS RegistrosLocacao(
            id_registro SERIAL PRIMARY KEY,
            nome_cliente VARCHAR(255),
            cpf_cliente VARCHAR(14),
            nome_fantasia_empresa VARCHAR(255),
            cnpj_empresa VARCHAR(18),
            nome_veiculo VARCHAR(255),
            placa_veiculo VARCHAR(10),
            custo_total DECIMAL(10, 2),
            data_inicio DATE,
            data_fim DATE
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Avaliacao(
            id_cliente INTEGER REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
            id_empresa INTEGER REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
            nota DECIMAL(3, 2) NOT NULL,
            PRIMARY KEY (id_cliente, id_empresa)
        )
    """)

    conexao.commit()
    cur.close()


@dataclass
class QueriesDB:
    """
        Classe utilizada para agrupar todas as queries puras em SQL
    """
    # query_buscar_todos_usuarios = "SELECT * FROM Usuario"
    query_inserir_usuario_novo = "INSERT INTO Usuario (email, senha_hashed, tipo_conta, path_foto, telefone) VALUES (%s, %s, %s, %s, %s) RETURNING id_usuario"
    query_buscar_usuario_por_email = "SELECT * FROM Usuario WHERE email = %s"
    query_buscar_usuario_por_id = "SELECT * FROM Usuario WHERE id_usuario = %s"
    query_remover_usuario = "DELETE FROM Usuario WHERE id_usuario = %s"
    query_atualizar_usuario = "UPDATE Usuario SET email=%s, senha_hashed=%s, path_foto=%s, telefone = %s WHERE id_usuario=%s"
    
    query_inserir_cliente_novo = "INSERT INTO Cliente (id_usuario, nome_completo, cpf, data_nascimento, foto_url) VALUES (%s, %s, %s, %s, %s)"
    query_remover_cliente = "DELETE FROM Cliente WHERE id_usuario = %s"
    query_buscar_cliente = "SELECT * FROM Cliente WHERE id_usuario = %s"
    query_atualizar_cliente = "UPDATE Cliente SET nome_completo=%s, cpf=%s, data_nascimento=%s, foto_url=%s WHERE id_usuario = %s"

    query_inserir_empresa_nova = "INSERT INTO Empresa (id_usuario, cnpj, nome_fantasia, id_endereco, id_local, num_avaliacoes, soma_avaliacoes, foto_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    query_remover_empresa = "DELETE FROM Empresa WHERE id_usuario = %s"
    query_buscar_empresa = "SELECT * FROM Empresa WHERE id_usuario = %s"
    query_atualizar_avaliacoes_empresa = "UPDATE Empresa SET num_avaliacoes = %s, soma_avaliacoes = %s WHERE id_usuario = %s"
    query_atualizar_empresa = "UPDATE Empresa SET cnpj = %s, nome_fantasia = %s, foto_url = %s WHERE id_usuario = %s"
    query_buscar_empresa_por_data = "SELECT DISTINCT e.id_usuario FROM Empresa e JOIN Veiculo v ON e.id_usuario = v.id_empresa WHERE v.id_veiculo NOT IN (SELECT c.id_veiculo FROM Calendario c WHERE c.data_indisponivel = %s)"
    query_buscar_empresa_por_passageiros = "SELECT DISTINCT e.id_usuario FROM Empresa e JOIN Veiculo v ON e.id_usuario = v.id_empresa WHERE v.capacidade >= %s"
    query_buscar_empresa_por_local = "SELECT DISTINCT e.id_usuario FROM Empresa e JOIN Local l ON e.id_local = l.id_local WHERE (ABS(l.latitude - %s) <= 0.00001 AND ABS(l.longitude - %s) <= 0.00001)"
    query_buscar_todas_empresas = "SELECT DISTINCT * FROM Empresa"

    query_inserir_local_novo = "INSERT INTO Local (latitude, longitude, nome) VALUES (%s, %s, %s) RETURNING id_local"
    query_buscar_local_por_id = "SELECT * FROM Local WHERE id_local = %s"
    query_remover_local = "DELETE FROM Local WHERE id_local = %s"
    query_atualizar_local = "UPDATE Local SET latitude=%s, longitude=%s, nome=%s WHERE id_local = %s"

    query_inserir_endereco_novo = "INSERT INTO Endereco (cep, rua, numero, bairro, cidade, estado) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_endereco"
    query_buscar_endereco_por_id = "SELECT * FROM Endereco WHERE id_endereco = %s"
    query_remover_endereco = "DELETE FROM Endereco WHERE id_endereco = %s"
    query_atualizar_endereco = "UPDATE Endereco SET cep=%s, rua=%s, numero=%s, bairro=%s, cidade=%s, estado=%s WHERE id_endereco=%s"

    query_inserir_veiculo_novo = "INSERT INTO Veiculo (id_empresa, nome_veiculo, placa_veiculo, capacidade, custo_por_km, custo_base, path_foto, cor, ano_de_fabricacao, foto_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_veiculo"
    query_buscar_veiculo = "SELECT * FROM Veiculo WHERE id_veiculo = %s"
    query_buscar_veiculos_empresa = "SELECT * FROM Veiculo WHERE id_empresa = %s"
    query_buscar_alugueis_veiculo = "SELECT * FROM Aluguel WHERE id_veiculo = %s"
    query_remover_veiculo = "DELETE FROM Veiculo WHERE id_veiculo = %s"
    query_verificar_veiculo_empresa = "SELECT id_veiculo FROM Veiculo WHERE id_veiculo = %s AND id_empresa = %s"
    query_verificar_disponibilidade_veiculo = "SELECT data_indisponivel FROM Calendario WHERE id_veiculo = %s AND (data_indisponivel BETWEEN %s AND %s)"
    query_atualizar_veiculo = "UPDATE Veiculo SET id_empresa=%s, nome_veiculo=%s, placa_veiculo=%s, capacidade=%s, custo_por_km=%s, custo_base=%s, path_foto=%s, cor=%s, ano_de_fabricacao=%s, foto_url=%s WHERE id_veiculo = %s"

    query_inserir_aluguel_novo = "INSERT INTO Aluguel (id_empresa, id_cliente, id_veiculo, valor_total, estado_aluguel, data_inicio, data_fim, distancia_trajeto, distancia_extra, id_local_partida, id_local_chegada) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    query_buscar_aluguel = "SELECT * FROM Aluguel WHERE id_aluguel = %s"
    query_buscar_alugueis_empresa = "SELECT * FROM Aluguel WHERE id_empresa = %s"
    query_buscar_alugueis_cliente = "SELECT * FROM Aluguel WHERE id_cliente = %s"
    query_remover_aluguel = "DELETE FROM Aluguel WHERE id_aluguel = %s"
    query_alterar_status_aluguel = "UPDATE Aluguel SET estado_aluguel = %s WHERE id_aluguel = %s"
    query_buscar_alugueis_vencidos = "SELECT * FROM Aluguel WHERE data_fim < %s"

    query_inserir_calendario = "INSERT INTO Calendario (id_veiculo, data_indisponivel) VALUES (%s, %s)"
    query_buscar_calendario_veiculo = "SELECT * FROM Calendario WHERE id_veiculo = %s"
    query_remover_calendario = "DELETE FROM Calendario WHERE id_veiculo = %s"

    query_buscar_avaliacao = "SELECT * FROM Avaliacao WHERE id_cliente = %s AND id_empresa = %s"
    query_inserir_avaliacao_nova = "INSERT INTO Avaliacao (id_cliente, id_empresa, nota) VALUES (%s, %s, %s)"
    query_atualizar_avaliacao = "UPDATE Avaliacao SET nota = %s WHERE id_cliente = %s AND id_empresa = %s"

    query_buscador_por_nome = "SELECT * FROM Empresa WHERE nome_fantasia LIKE %s"

    query_inserir_registro_historico = "INSERT INTO RegistrosLocacao(nome_cliente, cpf_cliente, nome_fantasia_empresa, cnpj_empresa, nome_veiculo, placa_veiculo, custo_total, data_inicio, data_fim) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

def atualizar_status_alugueis(conexao: connection):
    """
    Atualiza os status dos aluguéis que já passaram da data de vencimento.

    :param conexao: Conexão ativa com o banco de dados.
    """
    cur = conexao.cursor()

    hoje = datetime.datetime.now().strftime('%Y-%m-%d')

    cur.execute(QueriesDB.query_buscar_alugueis_vencidos, (hoje,))
    alugueis_vencidos = cur.fetchall()

    for aluguel in alugueis_vencidos:
        id_aluguel = aluguel[0]

        dados = ("concluido", id_aluguel)

        cur.execute(QueriesDB.query_alterar_status_aluguel, dados)
        
        # cliente = cur.execute(QueriesDB.query_buscar_cliente, (id_cliente,)).fetchone()
        # _, nome_cliente, cpf_cliente, _ = cliente

        # empresa = cur.execute(QueriesDB.query_buscar_empresa, (id_empresa,)).fetchone()
        # _, cnpj_empresa, nome_fantasia_empresa, _, _, _, _ = empresa

        # veiculo = cur.execute(QueriesDB.query_buscar_veiculo, (id_veiculo,)).fetchone()
        # _, _, nome_veiculo, placa_veiculo, _, _, _, _, _, _ = veiculo

        # dados_registro = (nome_cliente, cpf_cliente, nome_fantasia_empresa, cnpj_empresa, nome_veiculo, placa_veiculo, valor_total, data_inicio, data_fim)
        
        # cur.execute(QueriesDB.query_inserir_registro_historico, dados_registro)

        # cur.execute(QueriesDB.query_remover_aluguel, (id_aluguel,))
    
    conexao.commit()
    cur.close()
