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
    cursor.execute("CREATE TABLE IF NOT EXISTS Veiculo(id_veiculo integer primary key, id_empresa, nome_veiculo, placa_veiculo, capacidade, custo_por_km, custo_base, path_foto, cor, ano_de_fabricacao)")
    cursor.execute("CREATE TABLE IF NOT EXISTS RegistrosLocacao(id_registro integer primary key, nome_cliente, cpf_cliente, nome_fantasia_empresa, cnpj_empresa, nome_veiculo, placa_veiculo, custo_total, data_inicio, data_fim)")

    conexao.commit()


@dataclass
class QueriesDB:
    """
        Classe utilizada para agrupar todas as queries puras em SQL
    """
    # query_buscar_todos_usuarios = "SELECT * FROM Usuario"
    query_inserir_usuario_novo = "INSERT INTO Usuario (email, senha_hashed, tipo_conta, path_foto) VALUES (?, ?, ?, ?)"
    query_buscar_usuario_por_email = "SELECT * FROM Usuario WHERE email = ?"
    query_buscar_usuario_por_id = "SELECT * FROM Usuario WHERE id_usuario = ?"
    query_remover_usuario = "DELETE FROM Usuario WHERE id_usuario = ?"
    
    query_inserir_cliente_novo = "INSERT INTO Cliente (id_usuario, nome_completo, cpf) VALUES (?, ?, ?)"
    query_remover_cliente = "DELETE FROM Cliente WHERE id_usuario = ?"
    query_buscar_cliente = "SELECT * FROM Cliente WHERE id_usuario = ?"

    query_inserir_empresa_nova = "INSERT INTO Empresa (id_usuario, cnpj, nome_fantasia, id_endereco, id_local, num_avaliacoes, soma_avaliacoes) VALUES (?, ?, ?, ?, ?, ?, ?)"
    query_remover_empresa = "DELETE FROM Empresa WHERE id_usuario = ?"
    query_buscar_empresa = "SELECT * FROM Empresa WHERE id_usuario = ?"

    query_inserir_local_novo = "INSERT INTO Local (latitude, longitude, nome) VALUES (?, ?, ?) RETURNING id_local"
    query_buscar_local_por_id = "SELECT * FROM Local WHERE id_local = ?"
    query_remover_local = "DELETE FROM Local WHERE id_local = ?"

    query_inserir_endereco_novo = "INSERT INTO Endereco (cep, rua, numero, bairro, cidade, estado) VALUES (?, ?, ?, ?, ?, ?) RETURNING id_endereco"
    query_buscar_endereco_por_id = "SELECT * FROM Endereco WHERE id_endereco = ?"
    query_remover_endereco = "DELETE FROM Endereco WHERE id_endereco = ?"

    query_buscar_veiculos_empresa = "SELECT * FROM Veiculo WHERE id_empresa = ?"
    query_remover_veiculo = "DELETE FROM Veiculo WHERE id_veiculo = ?"

    query_inserir_aluguel_novo = "INSERT INTO Aluguel (id_aluguel, id_empresa, id_cliente, id_veiculo, valor_total, estado_aluguel, data_inicio, data_fim, distancia_trajeto, distancia_extra, id_local_partida, id_local_chegada) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    query_buscar_alugueis_empresa = "SELECT * FROM Aluguel WHERE id_empresa = ?"
    query_buscar_alugueis_cliente = "SELECT * FROM Aluguel WHERE id_cliente = ?"
    query_remover_aluguel = "DELETE FROM Aluguel WHERE id_aluguel = ?"

    query_remover_calendario = "DELETE FROM Calendario WHERE id_veiculo = ?"
