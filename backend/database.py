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

    # TODO: Esse exemplo eu peguei de outro teste, tenho que trocar a tabela depois

    cursor.execute("CREATE TABLE IF NOT EXISTS Cliente(id, nome, estado_civil, profissao, "
                   "nacionalidade, rg, cpf, sexo, rua, numero_residencia, bairro, cidade, estado, cep, telefone, celular, email, "
                   "data_nascimento)")
    
    conexao.commit()

@dataclass
class QueriesDB:
    query_insercao_usuario = "INSERT ..."
    query_insercao_veiculo = "INSERT ..."
    query_insercao_aluguel = "INSERT ..."
