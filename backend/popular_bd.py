import sqlite3
from auth import gerar_hash_senha

# import sys
# sys.path.append("..")

async def inserir_dados(db: sqlite3.Connection):
    cursor = db.cursor()

    cursor.executemany("INSERT INTO Usuario (id_usuario, email, senha_hashed, tipo_conta, path_foto, telefone) VALUES (?, ?, ?, ?, ?, ?)",
                       [
                           (1, 'usuario1@email.com', gerar_hash_senha("senha123"), "cliente", "", "1234-56781"),
                           (2, 'usuario2@email.com', gerar_hash_senha("senha123"), "cliente", "", "1234-56782"),
                           (3, 'usuario3@email.com', gerar_hash_senha("senha123"), "cliente", "", "1234-56783"),
                           (4, 'usuario4@email.com', gerar_hash_senha("senha123"), "cliente", "", "1234-56784"),
                           (5, 'usuario5@email.com', gerar_hash_senha("senha123"), "empresa", "", "1234-56785"),
                           (6, 'usuario6@email.com', gerar_hash_senha("senha123"), "empresa", "", "1234-56786"),
                           (7, 'usuario7@email.com', gerar_hash_senha("senha123"), "empresa", "", "1234-56787"),
                           (8, 'usuario8@email.com', gerar_hash_senha("senha123"), "empresa", "", "1234-56788"),
                           (9, 'usuario9@email.com', gerar_hash_senha("senha123"), "empresa", "", "1234-56789")
                       ])
    
    cursor.executemany("INSERT INTO Cliente (id_usuario, nome_completo, cpf, data_nascimento) VALUES (?, ?, ?, ?)",
                       [
                           (1, "João da silva", "1234567891", "2001-01-01"),
                           (2, "Maria das dores", "1234567892", "2002-02-02"),
                           (3, "Francisco Campos", "1234567893", "2003-03-03"),
                           (4, "Rodrigo Holanda", "1234567894", "2004-04-04")
                       ])
    
    cursor.executemany("INSERT INTO Empresa (id_usuario, cnpj, nome_fantasia, id_endereco, id_local, num_avaliacoes, soma_avaliacoes) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       [
                           (5, "000012300000", "Empresa #5", 1, 1, 0, 0),
                           (6, "000012300001", "Empresa #6", 2, 2, 0, 0),
                           (7, "000012300002", "Empresa #7", 3, 3, 0, 0),
                           (8, "000012300003", "Empresa #8", 4, 4, 0, 0),
                           (9, "000012300004", "Empresa #9", 5, 5, 0, 0)
                       ])

    cursor.executemany("INSERT INTO Endereco (id_endereco, cep, rua, numero, bairro, cidade, estado) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       [
                           (1, "0123456", "Avenida Morangueira", "001", "Zona 7", "Maringá", "PR"),
                           (2, "0123456", "Avenida Paraná", "002", "Zona 7", "Maringá", "PR"),
                           (3, "0123456", "Avenida Herval", "003", "Zona 7", "Maringá", "PR"),
                           (4, "0123456", "Avenida Horacio", "004", "Zona 7", "Maringá", "PR"),
                           (5, "0123456", "Avenida Colombo", "000", "Zona 7", "Maringá", "PR")
                       ])
    
    cursor.executemany("INSERT INTO Local (id_local, latitude, longitude, nome) VALUES (?, ?, ?, ?)", 
                       [
                           (1, -51.933298, -23.420545, "sede"),
                           (2, -51.933298, -23.420545, "sede"),
                           (3, -51.933298, -23.420545, "sede"),
                           (4, -51.933298, -23.420545, "sede"),
                           (5, -51.933298, -23.420545, "sede")
                       ])
    
    cursor.executemany("INSERT INTO Veiculo (id_veiculo, id_empresa, nome_veiculo, placa_veiculo, capacidade, custo_por_km, custo_base, path_foto, cor, ano_de_fabricacao) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       [
                           (1, 5, 'Onibus Marcopolo DD', 'ABC1234', 52, 10, 200, "imagens/imagem_veiculo_padrao.png", "Preto", 2012),
                           (2, 5, 'Onibus Marcopolo SD', 'ABC1235', 32, 10, 100, "imagens/imagem_veiculo_padrao.png", "Branco", 2009),
                           (3, 5, 'Microonibus SD', 'ABC1236', 25, 6, 50, "imagens/imagem_veiculo_padrao.png", "Preto", 2012)
                       ])
    
    db.commit()

    db.close()

    print("Dados inseridos com sucesso!")
