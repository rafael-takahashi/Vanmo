from dataclasses import dataclass
import sqlite3
import datetime

def conectar_bd() -> sqlite3.Connection:
    """
    Cria uma conexão com o banco de dados SQLite

    :return: Uma instância de Connection
    """
    return sqlite3.connect("app.db", check_same_thread=False)


def criar_tabelas(conexao: sqlite3.Connection):
    """
    Cria as tabelas do banco de dados caso elas não existam

    :param conexao: A conexão com o banco de dados local
    """

    cursor: sqlite3.Cursor = conexao.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS Usuario(id_usuario integer primary key, email, senha_hashed, tipo_conta, path_foto, telefone)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Cliente(id_usuario, nome_completo, cpf, data_nascimento)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Empresa(id_usuario, cnpj, nome_fantasia, id_endereco, id_local, num_avaliacoes, soma_avaliacoes)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Endereco(id_endereco integer primary key, cep, rua, numero, bairro, cidade, estado)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Local(id_local integer primary key, latitude, longitude, nome)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Aluguel(id_aluguel integer primary key, id_empresa, id_cliente, id_veiculo, valor_total, estado_aluguel, data_inicio, data_fim, distancia_trajeto, distancia_extra, id_local_partida, id_local_chegada)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Calendario(id_veiculo, data_indisponivel)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Veiculo(id_veiculo integer primary key, id_empresa, nome_veiculo, placa_veiculo, capacidade, custo_por_km, custo_base, path_foto, cor, ano_de_fabricacao)")
    
    # OBS: Registros de locação são criados quando um aluguel deixa de ser ativo e passa a ser histórico
    cursor.execute("CREATE TABLE IF NOT EXISTS RegistrosLocacao(id_registro integer primary key, nome_cliente, cpf_cliente, nome_fantasia_empresa, cnpj_empresa, nome_veiculo, placa_veiculo, custo_total, data_inicio, data_fim)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Avaliacao(id_cliente, id_empresa, nota)")

    conexao.commit()


@dataclass
class QueriesDB:
    """
        Classe utilizada para agrupar todas as queries puras em SQL
    """
    # query_buscar_todos_usuarios = "SELECT * FROM Usuario"
    query_inserir_usuario_novo = "INSERT INTO Usuario (email, senha_hashed, tipo_conta, path_foto, telefone) VALUES (?, ?, ?, ?, ?) RETURNING id_usuario"
    query_buscar_usuario_por_email = "SELECT * FROM Usuario WHERE email = ?"
    query_buscar_usuario_por_id = "SELECT * FROM Usuario WHERE id_usuario = ?"
    query_remover_usuario = "DELETE FROM Usuario WHERE id_usuario = ?"
    query_atualizar_usuario = "UPDATE Usuario SET email=?, senha_hashed=?, path_foto=?, telefone = ? WHERE id_usuario=?"
    
    query_inserir_cliente_novo = "INSERT INTO Cliente (id_usuario, nome_completo, cpf, data_nascimento) VALUES (?, ?, ?, ?)"
    query_remover_cliente = "DELETE FROM Cliente WHERE id_usuario = ?"
    query_buscar_cliente = "SELECT * FROM Cliente WHERE id_usuario = ?"
    query_atualizar_cliente = "UPDATE Cliente SET nome_completo=?, cpf=?, data_nascimento=? WHERE id_usuario = ?"

    query_inserir_empresa_nova = "INSERT INTO Empresa (id_usuario, cnpj, nome_fantasia, id_endereco, id_local, num_avaliacoes, soma_avaliacoes) VALUES (?, ?, ?, ?, ?, ?, ?)"
    query_remover_empresa = "DELETE FROM Empresa WHERE id_usuario = ?"
    query_buscar_empresa = "SELECT * FROM Empresa WHERE id_usuario = ?"
    query_atualizar_avaliacoes_empresa = "UPDATE Empresa SET num_avaliacoes = ?, soma_avaliacoes = ? WHERE id_usuario = ?"
    query_atualizar_empresa = "UPDATE Empresa SET cnpj = ?, nome_fantasia = ? WHERE id_usuario = ?"
    query_buscar_empresa_por_data = "SELECT DISTINCT e.id_usuario FROM Empresa e JOIN Veiculo v ON e.id_usuario = v.id_empresa WHERE v.id_veiculo NOT IN (SELECT c.id_veiculo FROM Calendario c WHERE c.data_indisponivel = ?)"
    query_buscar_empresa_por_passageiros = "SELECT DISTINCT e.id_usuario FROM Empresa e JOIN Veiculo v ON e.id_usuario = v.id_empresa WHERE v.capacidade >= ?"
    query_buscar_empresa_por_local = "SELECT DISTINCT e.id_usuario FROM Empresa e JOIN Local l ON e.id_local = l.id_local WHERE (ABS(l.latitude - ?) <= 0.00001 AND ABS(l.longitude - ?) <= 0.00001)"
    query_buscar_todas_empresas = "SELECT DISTINCT * FROM Empresa"

    query_inserir_local_novo = "INSERT INTO Local (latitude, longitude, nome) VALUES (?, ?, ?) RETURNING id_local"
    query_buscar_local_por_id = "SELECT * FROM Local WHERE id_local = ?"
    query_remover_local = "DELETE FROM Local WHERE id_local = ?"
    query_atualizar_local = "UPDATE Local SET latitude=?, longitude=?, nome=? WHERE id_local = ?"

    query_inserir_endereco_novo = "INSERT INTO Endereco (cep, rua, numero, bairro, cidade, estado) VALUES (?, ?, ?, ?, ?, ?) RETURNING id_endereco"
    query_buscar_endereco_por_id = "SELECT * FROM Endereco WHERE id_endereco = ?"
    query_remover_endereco = "DELETE FROM Endereco WHERE id_endereco = ?"
    query_atualizar_endereco = "UPDATE Endereco SET cep=?, rua=?, numero=?, bairro=?, cidade=?, estado=? WHERE id_endereco=?"

    query_inserir_veiculo_novo = "INSERT INTO Veiculo (id_empresa, nome_veiculo, placa_veiculo, capacidade, custo_por_km, custo_base, path_foto, cor, ano_de_fabricacao) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    query_buscar_veiculo = "SELECT * FROM Veiculo WHERE id_veiculo = ?"
    query_buscar_veiculos_empresa = "SELECT * FROM Veiculo WHERE id_empresa = ?"
    query_buscar_alugueis_veiculo = "SELECT * FROM Aluguel WHERE id_veiculo = ?"
    query_remover_veiculo = "DELETE FROM Veiculo WHERE id_veiculo = ?"
    query_verificar_veiculo_empresa = "SELECT id_veiculo FROM Veiculo WHERE id_veiculo = ? AND id_empresa = ?"
    query_verificar_disponibilidade_veiculo = "SELECT data_indisponivel FROM Calendario WHERE id_veiculo = ? AND (data_indisponivel BETWEEN ? AND ?)"
    query_atualizar_veiculo = "UPDATE Veiculo SET id_empresa=?, nome_veiculo=?, placa_veiculo=?, capacidade=?, custo_por_km=?, custo_base=?, path_foto=?, cor=?, ano_de_fabricacao=? WHERE id_veiculo = ?"

    query_inserir_aluguel_novo = "INSERT INTO Aluguel (id_empresa, id_cliente, id_veiculo, valor_total, estado_aluguel, data_inicio, data_fim, distancia_trajeto, distancia_extra, id_local_partida, id_local_chegada) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    query_buscar_aluguel = "SELECT * FROM Aluguel WHERE id_aluguel = ?"
    query_buscar_alugueis_empresa = "SELECT * FROM Aluguel WHERE id_empresa = ?"
    query_buscar_alugueis_cliente = "SELECT * FROM Aluguel WHERE id_cliente = ?"
    query_remover_aluguel = "DELETE FROM Aluguel WHERE id_aluguel = ?"
    query_alterar_status_aluguel = "UPDATE Aluguel SET estado_aluguel = ? WHERE id_aluguel = ?"
    query_buscar_alugueis_vencidos = "SELECT * FROM Aluguel WHERE data_fim < ?"

    query_inserir_calendario = "INSERT INTO Calendario (id_veiculo, data_indisponivel) VALUES (?, ?)"
    query_buscar_calendario_veiculo = "SELECT * FROM Calendario WHERE id_veiculo = ?"
    query_remover_calendario = "DELETE FROM Calendario WHERE id_veiculo = ?"

    query_buscar_avaliacao = "SELECT * FROM Avaliacao WHERE id_cliente = ? AND id_empresa = ?"
    query_inserir_avaliacao_nova = "INSERT INTO Avaliacao (id_cliente, id_empresa, nota) VALUES (?, ?, ?)"
    query_atualizar_avaliacao = "UPDATE Avaliacao SET nota = ? WHERE id_cliente = ? AND id_empresa = ?"

    query_buscador_por_nome = "SELECT * FROM Empresa WHERE nome_fantasia LIKE ?"

    query_inserir_registro_historico = "INSERT INTO RegistrosLocacao(nome_cliente, cpf_cliente, nome_fantasia_empresa, cnpj_empresa, nome_veiculo, placa_veiculo, custo_total, data_inicio, data_fim) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

def atualizar_status_alugueis(conexao: sqlite3.Connection):
    """
    Atualiza os status dos aluguéis que já passaram da data de vencimento.

    :param conexao: Conexão ativa com o banco de dados.
    """
    cursor = conexao.cursor()

    hoje  = datetime.datetime.now().strftime('%Y-%m-%d')

    alugueis_vencidos = cursor.execute(QueriesDB.query_buscar_alugueis_vencidos, (hoje,)).fetchall()

    for aluguel in alugueis_vencidos:
        id_aluguel, id_empresa, id_cliente, id_veiculo, valor_total, estado_aluguel, \
        data_inicio, data_fim, distancia_trajeto, distancia_extra, id_local_partida, id_local_chegada = aluguel

        cliente = cursor.execute(QueriesDB.query_buscar_cliente, (id_cliente,)).fetchone()
        _, nome_cliente, cpf_cliente, _ = cliente

        empresa = cursor.execute(QueriesDB.query_buscar_empresa, (id_empresa,)).fetchone()
        _, cnpj_empresa, nome_fantasia_empresa, _, _, _, _ = empresa

        veiculo = cursor.execute(QueriesDB.query_buscar_veiculo, (id_veiculo,)).fetchone()
        _, _, nome_veiculo, placa_veiculo, _, _, _, _, _, _ = veiculo

        dados_registro = (nome_cliente, cpf_cliente, nome_fantasia_empresa, cnpj_empresa, nome_veiculo, placa_veiculo, valor_total, data_inicio, data_fim)
        
        cursor.execute(QueriesDB.query_inserir_registro_historico, dados_registro)

        cursor.execute(QueriesDB.query_remover_aluguel, (id_aluguel,))
