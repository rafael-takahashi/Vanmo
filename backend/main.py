import datetime
import os
import threading
import time

from fastapi import FastAPI, Depends, HTTPException #, File, UploadFile
# from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List
from contextlib import asynccontextmanager

import database, auth
from classes import classe_aluguel, classe_calendario, classe_endereco, classe_local, classe_usuario, classe_veiculo
from cruds import crud_aluguel, crud_usuario, crud_veiculo, crud_local
from utils import *
from basemodels import *
from testes_main import executar_testes

lista_cidades = []
objeto_cidades = []

def loop_diario():
    """
    Loop diário para atualizar os status dos aluguéis com base na data de hoje

    OBS: Tem que ser executada em uma thread separada para não travar o programa
    """
    while True:
        db = database.conectar_bd()

        database.atualizar_status_alugueis(db)

        time.sleep(24 * 3600)
   

@asynccontextmanager
async def iniciar_app(app: FastAPI):
    """
        Função chamada ao inicializar o sistema
    """
    global objeto_cidades, lista_cidades

    conexao = database.conectar_bd()
    database.criar_tabelas(conexao)

    lista_cidades = carrega_cidades()

    objeto_cidades = retorna_todas_cidades(lista_cidades)

    thread = threading.Thread(target=loop_diario)
    thread.start()

    # await executar_testes()
    yield

app = FastAPI(lifespan=iniciar_app)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquema de autenticação OAuth2 com senha
oauth2_esquema = OAuth2PasswordBearer(tokenUrl="/usuario/login_legacy")

# Métodos de usuário ----------------------------------------

@app.post("/usuario/login")
async def login(dados: UsuarioLogin):
    """
    Realiza o login de um usuário no sistema

    @param form_data: Os dados do formulário contendo email (username) e senha (password)
    @return:
        Caso sucesso, retorna o token de acesso para aquele usuário
        Caso algum dos dados estejam errados, retorna o código 400
    """

    db = database.conectar_bd()
    usuario = auth.autenticar_usuario(db, dados.email, dados.senha)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")

    token_acesso = auth.criar_token_acesso(dados={"sub": usuario.email})
    return {"access_token": token_acesso, "token_type": "bearer"}

@app.post("/usuario/cadastro/empresa")
async def registrar_empresa(dados: CadastroEmpresa):
    global lista_cidades

    db = database.conectar_bd()

    dados.senha = auth.gerar_hash_senha(dados.senha)

    if not valida_uf(dados.uf):
        raise HTTPException(status_code=400, detail="UF inválido, formato necessário: 'PR', 'SP', 'RJ', etc.")

    if not valida_cidade(dados.cidade, lista_cidades):
        raise HTTPException(status_code=400, detail="Nome da cidade inválido")

    endereco: classe_endereco.Endereco = classe_endereco.Endereco(dados.uf, dados.cidade, dados.bairro, dados.cep, 
                                                                  dados.rua, dados.numero)

    latitude, longitude = busca_latitude_longitude_de_cidade(dados.cidade, lista_cidades)

    # OBS: Aqui entraria a validação de cnpj com o formato certinho e os dígitos verificadores
    # mas assim como no CPF, nós decidimos não deixar isso em efeito para a demonstração inicial

    # valida_cnpj(dados.cnpj)

    local: classe_local.Local = classe_local.Local(latitude, longitude, dados.nome_fantasia)

    empresa: classe_usuario.Empresa = classe_usuario.Empresa(0, email=dados.email, senha_hashed=dados.senha, tipo_conta="empresa", foto="",
                                                             nome_fantasia=dados.nome_fantasia, cnpj=dados.cnpj, endereco=endereco, local=local, telefone=dados.telefone)
    
    empresa.id = 0

    crud_usuario.cadastrar_empresa(db, empresa)

    return {"detail": "Cadastro realizado com sucesso"}

@app.post("/usuario/cadastro/cliente")
async def registrar_cliente(dados: CadastroCliente):

    db = database.conectar_bd()

    # OBS: Assim como o CNPJ, optamos por deixar essa implementação inativa pra apresentação por motivos de testagem
    # valida_cpf(dados.cpf)

    dados.senha = auth.gerar_hash_senha(dados.senha)

    cliente: classe_usuario.Cliente = classe_usuario.Cliente(0, dados.email, dados.senha, "cliente", "", dados.nome_completo, dados.cpf, dados.data_nascimento, dados.telefone)

    crud_usuario.cadastrar_cliente(db, cliente)
    
    return {"detail": "Cadastro realizado com sucesso"}

@app.delete("/usuario/apagar_conta")
async def apagar_usuario(token: str = Depends(oauth2_esquema)):
    """
    Apaga a conta de um usuário, só pode ser chamado pelo próprio usuário

    @param token: O token de acesso do usuário
    """

    db = database.conectar_bd()

    usuario_atual = auth.obter_usuario_atual(db, token)

    crud_usuario.remover_usuario(db, usuario_atual)

    return {"detail": "Usuario removido com sucesso"}

@app.put("/usuario/alterar_dados/cliente")
async def editar_dados_cliente(dados: AlterarDadosCliente, token: str = Depends(oauth2_esquema)):
    
    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    cliente = crud_usuario.buscar_dados_cliente(db, usuario)

    if dados.email:
        if crud_usuario.verificar_se_dados_ja_cadastrados(db, dados.email):
            raise HTTPException(status_code=400, detail="O email já está cadastrado no sistema")
        cliente.email = dados.email

    if dados.senha:
        cliente.senha = auth.gerar_hash_senha(dados.senha)

    if dados.foto:
        
        valida_foto(dados.foto)

        path_foto = f"imagens/usuarios/{usuario.id}.png"
        salva_foto(path_foto, dados.foto)

    if dados.nome_completo: 
        cliente.nome_completo = dados.nome_completo

    if dados.cpf:
        cliente.cpf = dados.cpf

    if dados.data_nascimento:
        cliente.data_nascimento = dados.data_nascimento
    
    if dados.telefone:
        cliente.telefone = dados.telefone

    crud_usuario.atualizar_cliente(db, cliente)    

@app.put("/usuario/alterar_dados/empresa")
async def editar_dados_empresa(dados: AlterarDadosEmpresa, token: str = Depends(oauth2_esquema)):
    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    empresa: classe_usuario.Empresa = crud_usuario.buscar_dados_empresa(db, usuario)

    if dados.email:
        if crud_usuario.verificar_se_dados_ja_cadastrados(db, dados.email):
            raise HTTPException(status_code=400, detail="O email já está cadastrado no sistema")
        empresa.email = dados.email

    if dados.senha:
        empresa.senha = auth.gerar_hash_senha(dados.senha)

    if dados.foto:
        
        valida_foto(dados.foto)

        path_foto = f"imagens/usuarios/{usuario.id}.png"
        salva_foto(path_foto, dados.foto)
    
    if dados.telefone:
        empresa.telefone = dados.telefone

    if dados.nome_fantasia:
        empresa.nome_fantasia = dados.nome_fantasia

    if dados.cnpj:
        empresa.cnpj = dados.cnpj

    if dados.uf:
        empresa.endereco.uf = dados.uf

    if dados.cidade:
        if not valida_cidade(dados.cidade):
            raise HTTPException(status_code=400, detail="Cidade inválida")
        
        empresa.endereco.cidade = dados.cidade

    if dados.bairro:
        empresa.endereco.bairro = dados.bairro

    if dados.cep:
        empresa.endereco.cep = dados.cep

    if dados.rua:
        empresa.endereco.rua = dados.rua

    if dados.numero:
        empresa.endereco.numero = dados.numero

    crud_usuario.atualizar_empresa(db, empresa)

@app.get("/usuario/buscar_dados_cadastrais/cliente")
async def buscar_dados_cadastrais_cliente(token: str = Depends(oauth2_esquema)):

    db = database.conectar_bd()
    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    cliente: classe_usuario.Cliente = crud_usuario.buscar_dados_cliente(db, usuario)
    cliente.senha_hashed = ""

    return cliente

@app.get("/usuario/buscar_dados_cadastrais/empresa")
async def buscar_dados_cadastrais_empresa(token: str = Depends(oauth2_esquema)):
    db = database.conectar_bd()
    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    empresa: classe_usuario.Empresa = crud_usuario.buscar_dados_empresa(db, usuario)
    empresa.senha_hashed = ""

    return empresa

# Métodos de propostas ----------------------------------------

@app.post("/propostas/aceitar_ou_rejetar_proposta")
async def aceitar_ou_rejeitar_proposta(dados: DadosAcaoProposta, token: str = Depends(oauth2_esquema)):
    """
    Aceita ou rejeita uma proposta feita para uma empresa

    @param id_proposta: O ID da proposta a ser alterada
    @param opcao: True caso ela seja aceita, False caso ela seja rejeitada
    @param token: O token de acesso do usuário
    """
    id_proposta = dados.id_proposta
    opcao = dados.opcao

    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    if usuario.tipo_conta != "empresa":
        raise HTTPException(status_code=400, detail="Apenas empresas podem aceitar ou rejeitar propostas")

    aluguel = crud_aluguel.buscar_aluguel(db, dados.id_proposta)

    if aluguel is None:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")
    
    if aluguel.id_empresa != usuario.id:
        raise HTTPException(status_code=400, detail="Proposta não pertence ao usuário")
    
    if aluguel.estado_aluguel != "proposto":
        raise HTTPException(status_code=400, detail="Status do aluguel não é 'proposta'")
    
    novo_status = "rejeitado"
    if dados.opcao:
        novo_status = "ativo"

    crud_aluguel.alterar_status_aluguel(db, dados.id_proposta, novo_status)

    return {"detail": f"Status alterado para '{novo_status}' com sucesso!"}

@app.get("/propostas/buscar_propostas")
async def buscar_todas_propostas_usuario(token: str = Depends(oauth2_esquema)):
    """
    Busca todas as propostas de um usuário

    @param token: O token de acesso do usuário
    """

    # Obter o usuário a partir do token
    db = database.conectar_bd()
    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    # Buscar as propostas desse usuário e retornar
    alugueis = crud_aluguel.buscar_alugueis_usuario_id(db, usuario.id)

    if alugueis:
        return alugueis
    else:
        return {"detail" : "Nenhuma proposta encontrada para o cliente.",
                "data" : []}

@app.get("/propostas/buscar_dados_proposta")
async def buscar_dados_proposta(dados: IdProposta, token: str = Depends(oauth2_esquema)):
    """
    Busca os dados específicos de uma proposta única

    @param id_proposta: O ID da proposta a ser buscada
    @param token: O token de acesso daquele usuário
    """

    id_proposta = dados.id_proposta

    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    aluguel = crud_aluguel.buscar_aluguel(db, dados.id_proposta)

    if aluguel is None:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")
    
    if aluguel.id_empresa != usuario.id and aluguel.id_cliente != usuario.id:
        raise HTTPException(status_code=400, detail="Proposta não pertence ao usuário")
    
    return aluguel

@app.post("/propostas/criar_proposta/")
async def criar_proposta(dados: CriarProposta, token: str = Depends(oauth2_esquema)):
    global lista_cidades
    """
    Cria uma proposta de aluguel de um cliente para uma empresa envolvendo um veículo

    @param id_empresa: O ID da empresa que receberá a proposta
    @param id_veiculo: O ID do veículo que se deseja locar
    @param latitude_partida: A coordenada geográfica do ponto de partida
    @param longitude_partida: A coordenada geográfica do ponto de partida
    @param latitude_chegada: A coordenada geográfica do ponto de chegada
    @param longitude_chegada: A coordenada geográfica do ponto de chegada
    @param distancia_extra_km: A distância extra que poderá ser percorrida pelo Cliente
    @param data_saida: A data que o cliente deseja partir com o veículo
    @param data_chegada: A data prevista de retorno do cliente
    @param token: O token de acesso do usuário
    """

    db = database.conectar_bd()
    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    id_empresa = dados.id_empresa
    id_veiculo = dados.id_veiculo

    if not valida_cidade(dados.cidade_saida, lista_cidades):
        raise HTTPException(status_code=400, detail="Cidade de partida inválida")

    if not valida_cidade(dados.cidade_chegada, lista_cidades):
        raise HTTPException(status_code=400, detail="Cidade de chegada inválida")
    
    latitude_partida, longitude_partida = busca_latitude_longitude_de_cidade(dados.cidade_saida)

    latitude_chegada, longitude_chegada = busca_latitude_longitude_de_cidade(dados.cidade_chegada)

    data_saida = data_saida
    data_chegada = data_chegada

    if usuario.tipo_conta != "cliente":
        raise HTTPException(status_code=400, detail="Tipo de usuário não é cliente")
    
    if not crud_veiculo.verificar_veiculo_empresa(db, dados.id_veiculo, dados.id_empresa):
        raise HTTPException(status_code=400, detail="Veículo não pertence a empresa")
    
    if not crud_veiculo.verificar_disponibilidade_veiculo(db, dados.id_veiculo, dados.data_saida, dados.data_chegada):
        raise HTTPException(status_code=400, detail="Veículo não disponível para o período escolhido")

    # OBS: Como as coordenadas são internas da cidade agora, não é mais necessária essa validação

    # if (not valida_coordendas(dados.latitude_partida, dados.longitude_partida)) or (not valida_coordendas(dados.latitude_chegada, dados.longitude_chegada)):
    #     raise HTTPException(status_code=400, detail="Coordenadas inválidas")
    
    if (dados.data_chegada > dados.data_saida):
        raise HTTPException(status_code=400, detail="Datas inválidas: data de chegada anterior a data de saída")

    veiculo: classe_veiculo.Veiculo = crud_veiculo.buscar_veiculo(db, dados.id_veiculo)
    if not veiculo:
        raise HTTPException(status_code=400, detail="Veículo não encontrado")

    aluguel: classe_aluguel.Aluguel = classe_aluguel.Aluguel(None, usuario.id, dados.id_empresa, dados.id_veiculo)
    aluguel.adicionar_datas(dados.data_saida, dados.data_chegada)

    local_partida: classe_local.Local = classe_local.Local(latitude_partida, longitude_partida)
    local_partida.id = crud_local.criar_local(db, local_partida)
    local_chegada: classe_local.Local = classe_local.Local(latitude_chegada, longitude_chegada)
    local_chegada.id = crud_local.criar_local(db, local_chegada)

    aluguel.adicionar_locais(local_partida, local_chegada)
    aluguel.adicionar_distancia_extra(dados.distancia_extra_km)
    aluguel.calcular_valor_total(veiculo.custo_por_km, veiculo.custo_base)

    aluguel.estado_aluguel = "proposto"

    crud_aluguel.criar_aluguel(db, aluguel)

    return {"detail": "Proposta criada com sucesso"}

@app.put("/propostas/cancelar_proposta/")
async def cancelar_proposta(dados: IdProposta, token: str = Depends(oauth2_esquema)):
    """
    Cancela uma proposta de um cliente

    @param id_proposta: O ID da proposta a ser cancelada
    @param token: O token de acesso do usuário
    """

    id_proposta = dados.id_proposta

    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(token)

    if usuario.tipo_conta != "cliente":
        raise HTTPException(status_code=400, detail="Apenas clientes podem cancelar propostas")

    aluguel = crud_aluguel.buscar_aluguel(db, dados.id_proposta)

    if aluguel is None:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")
    
    if aluguel.id_cliente != usuario.id:
        raise HTTPException(status_code=400, detail="Proposta não pertence ao cliente")
    
    if aluguel.estado_aluguel != "proposto":
        raise HTTPException(status_code=400, detail="Status do aluguel não é 'proposto'")

    crud_aluguel.remover_aluguel(db, dados.id_proposta)

    return {"detail": "Proposta cancelada com sucesso!"}    

@app.post("/propostas/calcular_custo/")
async def verificar_custo_proposta(dados: CriarProposta, token: str = Depends(oauth2_esquema)):
    global lista_cidades
    """
    Calcula o custo de uma proposta de um aluguel para retornar ao cliente

    @param id_empresa: O ID da empresa que receberá a proposta
    @param id_veiculo: O ID do veículo que se deseja locar
    @param latitude_partida: A coordenada geográfica do ponto de partida
    @param longitude_partida: A coordenada geográfica do ponto de partida
    @param latitude_chegada: A coordenada geográfica do ponto de chegada
    @param longitude_chegada: A coordenada geográfica do ponto de chegada
    @param distancia_extra_km: A distância extra que poderá ser percorrida pelo Cliente
    @param data_saida: A data que o cliente deseja partir com o veículo
    @param data_chegada: A data prevista de retorno do cliente
    @param token: O token de acesso do usuário
    """

    db = database.conectar_bd()
    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    if not valida_cidade(dados.cidade_saida, lista_cidades):
        raise HTTPException(status_code=400, detail="Cidade de partida inválida")

    if not valida_cidade(dados.cidade_chegada, lista_cidades):
        raise HTTPException(status_code=400, detail="Cidade de chegada inválida")
    
    latitude_partida, longitude_partida = busca_latitude_longitude_de_cidade(dados.cidade_saida)

    latitude_chegada, longitude_chegada = busca_latitude_longitude_de_cidade(dados.cidade_chegada)

    data_saida = data_saida
    data_chegada = data_chegada

    if usuario.tipo_conta != "cliente":
        raise HTTPException(status_code=400, detail="Tipo de usuário não é cliente")
    
    if not crud_veiculo.verificar_veiculo_empresa(db, dados.id_veiculo, dados.id_empresa):
        raise HTTPException(status_code=400, detail="Veículo não pertence a empresa")
    
    if not crud_veiculo.verificar_disponibilidade_veiculo(db, dados.id_veiculo, dados.data_saida, dados.data_chegada):
        raise HTTPException(status_code=400, detail="Veículo não disponível para o período escolhido")

    if (dados.data_chegada > dados.data_saida):
        raise HTTPException(status_code=400, detail="Datas inválidas: data de chegada anterior a data de saída")

    veiculo: classe_veiculo.Veiculo = crud_veiculo.buscar_veiculo(db, dados.id_veiculo)
    if not veiculo:
        raise HTTPException(status_code=400, detail="Veículo não encontrado")

    aluguel: classe_aluguel.Aluguel = classe_aluguel.Aluguel(None, usuario.id, dados.id_empresa, dados.id_veiculo)
    aluguel.adicionar_datas(dados.data_saida, dados.data_chegada)

    local_partida: classe_local.Local = classe_local.Local(latitude_partida, longitude_partida)
    local_partida.id = crud_local.criar_local(db, local_partida)
    local_chegada: classe_local.Local = classe_local.Local(latitude_chegada, longitude_chegada)
    local_chegada.id = crud_local.criar_local(db, local_chegada)

    aluguel.adicionar_locais(local_partida, local_chegada)
    aluguel.adicionar_distancia_extra(dados.distancia_extra_km)
    aluguel.calcular_valor_total(veiculo.custo_por_km, veiculo.custo_base)

    return aluguel.valor_total

# Métodos de veículos ----------------------------------------

@app.post("/veiculos/cadastrar_veiculo/")
async def cadastrar_veiculo(dados: CadastrarVeiculo, token: str = Depends(oauth2_esquema)):
    """
    Cadastra um veículo para uma empresa

    @param nome_veiculo: O nome do modelo do veículo
    @param placa_veiculo: A placa do veículo
    @param custo_por_km: O custo por km (R$)
    @param custo_base: O custo base do veículo (R$)
    @param foto: A foto do veículo
    @param cor: A cor do veículo
    @param ano_fabricacao: O ano de fabricação do veículo
    @param token: O token de acesso do usuário
    """
    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    if usuario.tipo_conta != "empresa":
        raise HTTPException(status_code=400, detail="Tipo de usuário não é empresa")
    
    if dados.foto == "":
        raise HTTPException(status_code=400, detail="Foto inválida")
    
    if (dados.custo_por_km <= 0) or (dados.custo_base <= 0):
        raise HTTPException(status_code=400, detail="Valores de custo negativos")
    
    if dados.capacidade < 1:
        raise HTTPException(status_code=400, detail="Capacidade do veículo inválida")
    
    if (dados.ano_fabricacao < 1970) or (dados.ano_fabricacao > datetime.date.today().year):
        raise HTTPException(status_code=400, detail="Ano de fabricação inválido")
    
    placa_veiculo = dados.placa_veiculo.upper()
    if not valida_placa(placa_veiculo):
        raise HTTPException(status_code=400, detail="Placa do veículo inválida")

    veiculo: classe_veiculo.Veiculo = classe_veiculo.Veiculo(None, usuario.id, dados.nome_veiculo, placa_veiculo)
    veiculo.adicionar_custos(dados.custo_por_km, dados.custo_base)
    veiculo.adicionar_dados("", dados.cor, dados.ano_fabricacao, dados.capacidade)

    id_veiculo = crud_veiculo.criar_veiculo(db, veiculo)

    caminho_da_foto = f"imagens/veiculos/{usuario.id}-{id_veiculo}.png"
    
    salva_foto(caminho_da_foto, dados.foto)

    return {"detail": "Veículo cadastrado com sucesso!"}

@app.put("/veiculos/editar_veiculo")
async def editar_veiculo(dados: EditarVeiculo, token: str = Depends(oauth2_esquema)):
    """
    Altera o veículo de uma empresa

    @param id_veiculo: O ID do veículo a ser alterado
    @param nome_veiculo: O nome do modelo do veículo
    @param placa_veiculo: A placa do veículo
    @param custo_por_km: O custo por km (R$)
    @param custo_base: O custo base do veículo (R$)
    @param foto: A foto do veículo
    @param cor: A cor do veículo
    @param ano_fabricacao: O ano de fabricação do veículo
    @param token: O token de acesso do usuário
    """
    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    if usuario.tipo_conta != "empresa":
        raise HTTPException(status_code=400, detail="Tipo de usuário não é empresa")

    if not crud_veiculo.verificar_veiculo_empresa(db, dados.id_veiculo, usuario.id):
        raise HTTPException(status_code=400, detail="O veículo não pertence à empresa")

    veiculo: classe_veiculo.Veiculo = crud_veiculo.buscar_veiculo(db, dados.id_veiculo)

    # tentando fugir de criar vários if's
    novos_valores: dict[str, any | None] = {
        "nome_veiculo": dados.nome_veiculo,
        "placa_veiculo": dados.placa_veiculo,
        "custo_por_km": dados.custo_por_km,
        "custo_base": dados.custo_base,
        "cor": dados.cor,
        "ano_fabricacao": dados.ano_fabricacao
    }

    for atributo, valor in novos_valores.items():
        if valor is not None:
            setattr(veiculo, atributo, valor)

    if dados.foto:

        valida_foto(dados.foto)

        caminho_da_nova_foto = f"imagens/veiculos/{veiculo.id_empresa}-{veiculo.id_veiculo}.png"
        salva_foto(caminho_da_nova_foto, dados.foto)

    crud_veiculo.atualizar_veiculo(db, veiculo)

    return {"detail": "Veículo editado com sucesso!"}

@app.get("/veiculos/buscar_veiculos_empresa")
async def buscar_todos_veiculos_empresa(dados: IdEmpresa):
    """
    Busca todos os veículos de uma empresa

    @param id_empresa: O ID da empresa a qual se quer se buscar os veículos
    @param token: O token de acesso do usuário
    """

    id_empresa = dados.id_empresa

    db = database.conectar_bd()

    # TODO: organizar resultado por páginas

    # não precisa estar logado para buscar os veículos
    # auth.obter_usuario_atual(db, token)

    return crud_veiculo.listar_veiculos(db, dados.id_empresa)

@app.get("/veiculos/buscar_dados_veiculo", response_model=RespostaVeiculo)
async def buscar_dados_veiculo(dados: IdVeiculo, token: str = Depends(oauth2_esquema)):
    """
    Busca os dados de um veículo

    @param id_veiculo: O ID do veículo a se buscar os dados
    @param token: O token de acesso do usuário
    """

    id_veiculo = dados.id_veiculo

    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    veiculo = crud_veiculo.buscar_veiculo(db, id_veiculo)

    response_data = RespostaVeiculo(id_veiculo=veiculo.id_veiculo, nome_veiculo=veiculo.nome_veiculo, placa_veiculo=veiculo.placa_veiculo,
                                    datas_indisponiveis=veiculo.calendario_disponibilidade.datas_indisponiveis, custo_por_km=veiculo.custo_por_km,
                                    custo_base=veiculo.custo_base, foto=veiculo.caminho_foto, cor=veiculo.cor,
                                    ano_fabricacao=veiculo.ano_fabricacao, capacidade=veiculo.capacidade)

    return RespostaVeiculo

@app.delete("/veiculos/apagar_veiculo")
async def apagar_veiculo(dados: IdVeiculo, token: str = Depends(oauth2_esquema)):
    """
    Apaga um veículo do sistema

    @param id_veiculo: O ID do veículo a ser apagado
    @param token: O token de acesso do usuário
    """

    id_veiculo = dados.id_veiculo

    db = database.conectar_bd()

    usuario_atual = auth.obter_usuario_atual(db, token)

    # Validar se o usuário é uma empresa e o veículo pertence a ela
    if usuario_atual.tipo_conta != "empresa":
        raise HTTPException(status_code=400, detail="Usuário não é uma empresa para apagar veículo")
    
    if not crud_veiculo.verificar_veiculo_empresa(db, id_veiculo, usuario_atual.id):
        raise HTTPException(status_code=400, detail="Veículo pertence a outra empresa")
    
    if crud_veiculo.verificar_alugueis_veiculo(db, id_veiculo):
        raise HTTPException(status_code=400, detail="Veículo possui aluguéis ativos")
    
    if crud_veiculo.buscar_veiculo(db, id_veiculo) is None:
        raise HTTPException(status_code=400, detail="Veículo não encontrado no banco de dados")

    crud_veiculo.remover_veiculo(id_veiculo)

    return {"detail": "Veículo removido com sucesso"}

# Métodos extras cliente/empresa ----------------------------------------

@app.get("/empresa/buscar_dados_empresa", response_model=RespostaEmpresa)
async def buscar_dados_empresa(dados: IdEmpresa, token: str = Depends(oauth2_esquema)):
    """
    Busca os dados de uma empresa específica

    @param id_empresa: O ID da empresa a qual se quer buscar os dados
    @param token: O token de acesso do usuário
    """

    id_empresa: int = dados.id_empresa

    db = database.conectar_bd()
    usuario_atual = auth.obter_usuario_atual(db, token)

    empresa = crud_usuario.buscar_empresa_por_id(db, id_empresa)

    response_data = RespostaEmpresa(foto=empresa.foto, nome_fantasia=empresa.nome_fantasia, cnpj=empresa.cnpj,
                                    endereco=str(empresa.endereco), avaliacao=(empresa.soma_avaliacoes/empresa.num_avaliacoes),
                                    telefone=empresa.telefone)

    return response_data

@app.put("/empresa/avaliar_empresa")
async def avaliar_empresa(dados: AvaliacaoEmpresa, token: str = Depends(oauth2_esquema)):
    """
    Adiciona uma avaliação a uma empresa

    @param id_empresa: O ID da empresa a ser avaliada
    @param avaliacao: A nota (um valor entre 0 e 5)
    @param token: O token de acesso do usuário
    """
    id_empresa = dados.id_empresa
    avaliacao = dados.avaliacao

    db = database.conectar_bd()

    usuario = auth.obter_usuario_atual(db, token)

    if usuario.tipo_conta != "cliente":
        raise HTTPException(status_code=400, detail="Apenas clientes podem avaliar empresas")
    
    if avaliacao <= 0 or avaliacao >= 5:
        raise HTTPException(status_code=400, detail="Nota deve estar entre 0 e 5")

    if crud_usuario.verificar_se_avaliacao_ja_feita(db, usuario.id, id_empresa):
        crud_usuario.atualizar_avaliacao(db, usuario.id, id_empresa, avaliacao)
        return {"detail": "Avaliação atualizada com sucesso"}

    crud_usuario.avaliar_empresa(db, usuario.id, id_empresa, avaliacao)

    return {"detail": "Avaliação feita com sucesso"}
    
@app.get("/busca/buscar_empresas/nome")
async def buscar_empresas_nome(dados: BuscaEmpresaNome, token: str = Depends(oauth2_esquema)):
    """
    Busca as empresas a partir do nome

    @param nome_busca: O nome de empresa a ser buscada
    @param token: O token de acesso do usuário
    """

    nome_busca = dados.nome_busca
    pagina = dados.pagina

    db = database.conectar_bd()

    # usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    nome_busca = nome_busca + "%"

    return crud_usuario.buscador_empresas_nome(db, nome_busca, pagina)

@app.get("/busca/buscar_empresas/criterio")
async def buscar_empresas_criterio(dados: CriteriosBuscaEmpresa, token: str = Depends(oauth2_esquema)):
    """
    Busca as empresas a partir de outros critérios

    @param criterio:
    @param token: O token de acesso do usuário
    """
    empresas = set()

    if dados.data_de_partida:
        resultados = crud_usuario.buscar_empresa_por_data(dados.data_de_partida)
        for resultado in resultados:
            empresas.add(resultado)

    if dados.qtd_passageiros:
        resultados = crud_usuario.buscar_empresa_por_passageiros(dados.qtd_passageiros)
        for resultado in resultados:
            empresas.add(resultado) 

    if dados.latitude_partida and dados.longitude_partida:
        pass
    
    # TODO: paginação
    # TODO: lógica de combinação dos critérios

    pass

@app.get("/cidades/lista_de_cidades")
async def busca_lista_cidades():
    global objeto_cidades
    return objeto_cidades
