from psycopg2.extensions import connection
from auth import gerar_hash_senha

# import sys
# sys.path.append("..")

async def inserir_dados(db: connection):
    cur = db.cursor()

    # Nota: No PostgreSQL, não podemos especificar id_usuario diretamente se for SERIAL
    # Vamos usar DEFAULT ou omitir o campo para usar a sequência
    cur.executemany("INSERT INTO Usuario (email, senha_hashed, tipo_conta, path_foto, telefone) VALUES (%s, %s, %s, %s, %s)",
                       [
                           ('usuario1@email.com', gerar_hash_senha("senha123"), "cliente", "", "1234-56781"),
                           ('usuario2@email.com', gerar_hash_senha("senha123"), "cliente", "", "1234-56782"),
                           ('usuario3@email.com', gerar_hash_senha("senha123"), "cliente", "", "1234-56783"),
                           ('usuario4@email.com', gerar_hash_senha("senha123"), "cliente", "", "1234-56784"),
                           ('usuario5@email.com', gerar_hash_senha("senha123"), "empresa", "", "1234-56785"),
                           ('usuario6@email.com', gerar_hash_senha("senha123"), "empresa", "", "1234-56786"),
                           ('usuario7@email.com', gerar_hash_senha("senha123"), "empresa", "", "1234-56787"),
                           ('usuario8@email.com', gerar_hash_senha("senha123"), "empresa", "", "1234-56788"),
                           ('usuario9@email.com', gerar_hash_senha("senha123"), "empresa", "", "1234-56789")
                       ])
    
    # Buscar os IDs gerados para os usuários
    cur.execute("SELECT id_usuario FROM Usuario ORDER BY id_usuario")
    usuario_ids = [row[0] for row in cur.fetchall()]
    
    cur.executemany("INSERT INTO Cliente (id_usuario, nome_completo, cpf, data_nascimento) VALUES (%s, %s, %s, %s)",
                       [
                           (usuario_ids[0], "João da silva", "1234567891", "2001-01-01"),
                           (usuario_ids[1], "Maria das dores", "1234567892", "2002-02-02"),
                           (usuario_ids[2], "Francisco Campos", "1234567893", "2003-03-03"),
                           (usuario_ids[3], "Rodrigo Holanda", "1234567894", "2004-04-04")
                       ])
    
    cur.executemany("INSERT INTO Endereco (cep, rua, numero, bairro, cidade, estado) VALUES (%s, %s, %s, %s, %s, %s)",
                       [
                           ("0123456", "Avenida Morangueira", "001", "Zona 7", "Maringá", "PR"),
                           ("0123456", "Avenida Paraná", "002", "Zona 7", "Maringá", "PR"),
                           ("0123456", "Avenida Herval", "003", "Zona 7", "Maringá", "PR"),
                           ("0123456", "Avenida Horacio", "004", "Zona 7", "Maringá", "PR"),
                           ("0123456", "Avenida Colombo", "000", "Zona 7", "Maringá", "PR")
                       ])
    
    # Buscar os IDs gerados para os endereços
    cur.execute("SELECT id_endereco FROM Endereco ORDER BY id_endereco")
    endereco_ids = [row[0] for row in cur.fetchall()]
    
    cur.executemany("INSERT INTO Local (latitude, longitude, nome) VALUES (%s, %s, %s)", 
                       [
                           (-51.933298, -23.420545, "sede"),
                           (-51.933298, -23.420545, "sede"),
                           (-51.933298, -23.420545, "sede"),
                           (-51.933298, -23.420545, "sede"),
                           (-51.933298, -23.420545, "sede")
                       ])
    
    # Buscar os IDs gerados para os locais
    cur.execute("SELECT id_local FROM Local ORDER BY id_local")
    local_ids = [row[0] for row in cur.fetchall()]
    
    cur.executemany("INSERT INTO Empresa (id_usuario, cnpj, nome_fantasia, id_endereco, id_local, num_avaliacoes, soma_avaliacoes) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                       [
                           (usuario_ids[4], "000012300000", "Empresa #5", endereco_ids[0], local_ids[0], 0, 0),
                           (usuario_ids[5], "000012300001", "Empresa #6", endereco_ids[1], local_ids[1], 0, 0),
                           (usuario_ids[6], "000012300002", "Empresa #7", endereco_ids[2], local_ids[2], 0, 0),
                           (usuario_ids[7], "000012300003", "Empresa #8", endereco_ids[3], local_ids[3], 0, 0),
                           (usuario_ids[8], "000012300004", "Empresa #9", endereco_ids[4], local_ids[4], 0, 0)
                       ])
    
    cur.executemany("INSERT INTO Veiculo (id_empresa, nome_veiculo, placa_veiculo, capacidade, custo_por_km, custo_base, path_foto, cor, ano_de_fabricacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       [
                           (usuario_ids[4], 'Onibus Marcopolo DD', 'ABC1234', 52, 10, 2000, "imagens/imagem_veiculo_padrao.png", "Preto", 2012),
                           (usuario_ids[4], 'Onibus Marcopolo SD', 'ABC1235', 32, 10, 1000, "imagens/imagem_veiculo_padrao.png", "Branco", 2009),
                           (usuario_ids[4], 'Microonibus SD', 'ABC1236', 25, 6, 500, "imagens/imagem_veiculo_padrao.png", "Preto", 2011),
                           (usuario_ids[5], 'Ônibus Leito DD', 'ABC1237', 64, 25, 500, "imagens/imagem_veiculo_padrao.png", "Preto", 2013),
                           (usuario_ids[5], 'Ônibus Semileito SD', 'ABC1238', 29, 15, 350, "imagens/imagem_veiculo_padrao.png", "Preto", 2015),
                           (usuario_ids[6], 'Microonibus minivan', 'ABC1239', 12, 8, 50, "imagens/imagem_veiculo_padrao.png", "Preto", 2017),
                       ])
    
    db.commit()

    cur.close()
    db.close()

    print("Dados inseridos com sucesso!")
