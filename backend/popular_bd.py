import sqlite3
from main import registrar_novo_usuario
import database
import asyncio

# import sys
# sys.path.append("..")

async def inserir_dados(db: sqlite3.Connection):
    cursor = db.cursor()

    
    # Inserir dados na tabela Usuario
    # cursor.executemany("""
    #     INSERT INTO Usuario (id_usuario, email, senha_hashed, tipo_conta, path_foto)
    #     VALUES (?, ?, ?, ?, ?)
    # """, [
    await registrar_novo_usuario("usuario1", "senha", "cliente", "")
    await registrar_novo_usuario("usuario2", "senha", "empresa", "")
    await registrar_novo_usuario("usuario3", "senha", "cliente", "")
    await registrar_novo_usuario("usuario4", "senha", "empresa", "")
    await registrar_novo_usuario("usuario5", "senha", "cliente", "")
    #     (1, 'usuario1@email.com', 'senha1hash', 'cliente', 'foto1.jpg'),
    #     (2, 'usuario2@email.com', 'senha2hash', 'empresa', 'foto2.jpg'),
    #     (3, 'usuario3@email.com', 'senha3hash', 'cliente', 'foto3.jpg'),
    #     (4, 'usuario4@email.com', 'senha4hash', 'empresa', 'foto4.jpg'),
    #     (5, 'usuario5@email.com', 'senha5hash', 'cliente', 'foto5.jpg')
    # ])

    # Inserir dados na tabela Cliente
    cursor.executemany("""
        INSERT INTO Cliente (id_usuario, nome_completo, cpf)
        VALUES (?, ?, ?)
    """, [
        (1, 'João Silva', '12345678901'),
        (3, 'Maria Souza', '98765432100'),
        (5, 'Carlos Oliveira', '45612378901'),
        (2, 'Ana Costa', '32165498700'),
        (4, 'Paula Almeida', '65498712300')
    ])

    # Inserir dados na tabela Endereco
    cursor.executemany("""
        INSERT INTO Endereco (cep, rua, numero, bairro, cidade, estado)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ('12345-678', 'Rua A', 100, 'Centro', 'São Paulo', 'SP'),
        ('23456-789', 'Rua B', 200, 'Jardim', 'Rio de Janeiro', 'RJ'),
        ('34567-890', 'Rua C', 300, 'Vila Nova', 'Belo Horizonte', 'MG'),
        ('45678-901', 'Rua D', 400, 'Bairro Alto', 'Curitiba', 'PR'),
        ('56789-012', 'Rua E', 500, 'Vila Progresso', 'Porto Alegre', 'RS')
    ])

    # Inserir dados na tabela Local
    cursor.executemany("""
        INSERT INTO Local (latitude, longitude, nome)
        VALUES (?, ?, ?)
    """, [
        (23.5505, -46.6333, 'Local A'),
        (22.9068, -43.1729, 'Local B'),
        (19.8170, -43.9413, 'Local C'),
        (25.4284, -49.2733, 'Local D'),
        (30.0346, -51.2177, 'Local E')
    ])

    # Inserir dados na tabela Empresa
    cursor.executemany("""
        INSERT INTO Empresa (id_usuario, cnpj, nome_fantasia, id_endereco, id_local, num_avaliacoes, soma_avaliacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        (2, '12345678000123', 'Loja A', 1, 1, 10, 45),
        (4, '23456789000145', 'Loja B', 2, 2, 20, 95),
        (5, '34567890000167', 'Loja C', 3, 3, 15, 70),
        (1, '45678901234567', 'Loja D', 4, 4, 30, 150),
        (3, '56789012345678', 'Loja E', 5, 5, 5, 20)
    ])

    # Inserir dados na tabela Veiculo
    cursor.executemany("""
        INSERT INTO Veiculo (id_veiculo, id_empresa, nome_veiculo, placa_veiculo, capacidade, custo_por_km, custo_base, path_foto, cor, ano_de_fabricacao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (1, 2, 'Fusca', 'ABC1234', 4, 0.5, 50, 'car1.jpg', 'azul', 1980),
        (2, 4, 'Civic', 'XYZ5678', 5, 1.0, 100, 'car2.jpg', 'preto', 2020),
        (3, 4, 'Gol', 'DEF2345', 5, 0.8, 70, 'car3.jpg', 'branco', 2015),
        (4, 2, 'Onix', 'GHI6789', 5, 0.6, 60, 'car4.jpg', 'vermelho', 2018),
        (5, 2, 'HB20', 'JKL3456', 5, 0.7, 65, 'car5.jpg', 'prata', 2019)
    ])

    # Inserir dados na tabela Aluguel
    cursor.executemany("""
        INSERT INTO Aluguel (id_aluguel, id_empresa, id_cliente, id_veiculo, valor_total, estado_aluguel, data_inicio, data_fim, distancia_trajeto, distancia_extra, id_local_partida, id_local_chegada)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (1, 2, 1, 1, 150, 'ativo', '2024-01-01', '2024-01-05', 200, 10, 1, 2),
        (2, 4, 3, 2, 500, 'finalizado', '2024-02-01', '2024-02-10', 500, 20, 2, 3),
        (3, 5, 4, 3, 350, 'ativo', '2024-03-01', '2024-03-05', 300, 15, 3, 4),
        (4, 1, 2, 4, 250, 'finalizado', '2024-04-01', '2024-04-03', 150, 5, 4, 5),
        (5, 3, 5, 5, 400, 'ativo', '2024-05-01', '2024-05-07', 400, 25, 5, 1)
    ])

    # Inserir dados na tabela Calendario
    cursor.executemany("""
        INSERT INTO Calendario (id_veiculo, data_indisponivel)
        VALUES (?, ?)
    """, [
        (1, '2024-01-10'),
        (2, '2024-02-15'),
        (3, '2024-03-12'),
        (4, '2024-04-20'),
        (5, '2024-05-05')
    ])

    # Inserir dados na tabela RegistrosLocacao
    cursor.executemany("""
        INSERT INTO RegistrosLocacao (id_registro, nome_cliente, cpf_cliente, nome_fantasia_empresa, cnpj_empresa, nome_veiculo, placa_veiculo, custo_total, data_inicio, data_fim)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (1, 'João Silva', '12345678901', 'Loja A', '12345678000123', 'Fusca', 'ABC1234', 150, '2024-01-01', '2024-01-05'),
        (2, 'Maria Souza', '98765432100', 'Loja B', '23456789000145', 'Civic', 'XYZ5678', 500, '2024-02-01', '2024-02-10'),
        (3, 'Carlos Oliveira', '45612378901', 'Loja C', '34567890000167', 'Gol', 'DEF2345', 350, '2024-03-01', '2024-03-05'),
        (4, 'Ana Costa', '32165498700', 'Loja D', '45678901234567', 'Onix', 'GHI6789', 250, '2024-04-01', '2024-04-03'),
        (5, 'Paula Almeida', '65498712300', 'Loja E', '56789012345678', 'HB20', 'JKL3456', 400, '2024-05-01', '2024-05-07')
    ])

    # Confirmar transações
    conexao.commit()

    # Fechar a conexão
    conexao.close()

    print("Dados inseridos com sucesso!")

if __name__ == "__main__":
    conexao = sqlite3.connect("app.db")
    asyncio.run(inserir_dados(conexao))
