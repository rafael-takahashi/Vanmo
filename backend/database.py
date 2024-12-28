from dataclasses import dataclass
import sqlite3


def conectar_bd() -> sqlite3.Connection:
    """
    Cria uma conexão com o banco de dados SQLite

    :return: Uma instância de Connection
    """
    return sqlite3.connect("app.db")


def criar_tabelas(conexao: sqlite3.Connection):
    """
    Cria as tabelas do banco de dados caso elas não existam

    :param conexao: A conexão com o banco de dados local
    """

    cursor: sqlite3.Cursor = conexao.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS Usuario(id_usuario integer primary key, email, senha_hashed, tipo_conta, path_foto)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Cliente(id_usuario, nome_completo, cpf)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Empresa(id_usuario, cnpj, nome_fantasia, id_endereco, id_local, num_avaliacoes, soma_avaliacoes)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Endereco(id_endereco integer primary key, cep, rua, numero, bairro, cidade, estado)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Local(id_local integer primary key, latitude, longitude, nome)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Aluguel(id_aluguel integer primary key, id_empresa, id_cliente, id_veiculo, valor_total, estado_aluguel, data_inicio, data_fim, distancia_trajeto, distancia_extra, id_local_partida, id_local_chegada)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Calendario(id_veiculo, data_indisponivel)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Veiculo(id_veiculo integer primary key, nome_veiculo, placa_veiculo, capacidade, custo_por_km, custo_base, path_foto, cor, ano_de_fabricacao)")

    conexao.commit()


@dataclass
class QueriesDB:
    """
        Classe utilizada para agrupar todas as queries puras em SQL
    """
    # query_buscar_todos_usuarios = "SELECT * FROM Usuario"
    query_inserir_usuario_novo = "INSERT INTO Usuario (email, senha_hashed, tipo_conta, path_foto) VALUES (?, ?, ?, ?)"
    query_buscar_usuario_por_email = "SELECT * FROM Usuario WHERE email = ?"
    query_remover_usuario = "DELETE FROM Usuario WHERE id_usuario = ?"
    
    query_inserir_cliente_novo = "INSERT INTO Cliente (id_usuario, nome_completo, cpf) VALUES (?, ?, ?)"
    query_inserir_empresa_nova = "INSERT INTO Empresa (id_usuario, cnpj, nome_fantasia, id_endereco, id_local, num_avaliacoes, soma_avaliacoes) VALUES (?, ?, ?, ?, ?, ?, ?)"

    query_inserir_local_novo = "INSERT INTO Local (latitude, longitude, nome) VALUES (?, ?, ?) RETURNING id_local"
    query_inserir_endereco_novo = "INSERT INTO Endereco (cep, rua, numero, bairro, cidade, estado) VALUES (?, ?, ?, ?, ?, ?) RETURNING id_endereco"
