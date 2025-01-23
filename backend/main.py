import datetime
import os

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from contextlib import asynccontextmanager

import database, auth
from classes import classe_aluguel, classe_calendario, classe_endereco, classe_local, classe_usuario, classe_veiculo
from cruds import crud_aluguel, crud_usuario, crud_veiculo, crud_local
from utils import *

@asynccontextmanager
async def iniciar_app(app: FastAPI):
    """
        Função chamada ao inicializar o sistema
    """

    # Criar tabelas no banco de dados caso elas não existam
    conexao = database.conectar_bd()
    database.criar_tabelas(conexao)

    # TODO: Função que roda na inicialização do sistema e uma vez ao dia atualizando os status dos aluguéis
    # que já passaram das datas de vencimento

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
class UsuarioRegistro(BaseModel):
    email: str
    senha: str
    tipo_conta: str

@app.post("/usuario/registrar")
async def registrar_novo_usuario(dados: UsuarioRegistro):
    """
    Registra um novo usuário no sistema

    @param email: O email do usuário a ser cadastrado
    @param senha: A senha do usuário a ser cadastrado (preferencialmente em hash já)
    @param tipo_conta: O tipo de conta ("Cliente", "Empresa")
    @param foto: (Opcional) O arquivo de foto que o usuário enviou para seu perfil
    @return:
        Caso sucesso, retorna o token de acesso para aquele usuário
        Caso haja um usuário cadastrado com o mesmo email, retorna o código 400
    """

    # TODO: Validar email

    email = dados.email
    senha = dados.senha
    tipo_conta = dados.tipo_conta

    usuario = classe_usuario.Usuario(email, senha, tipo_conta)
    db = database.conectar_bd()

    if crud_usuario.obter_usuario_por_nome(db, usuario.email):
        raise HTTPException(status_code=400, detail="Usuario já existe")
    
    usuario.senha_hashed = auth.gerar_hash_senha(usuario.senha_hashed)
    crud_usuario.criar_usuario(db, usuario)
    token_acesso = auth.criar_token_acesso(dados={"sub": usuario.email})
    return {"access_token": token_acesso, "token_type": "bearer"}

@app.post("/usuario/registrar_legacy")
async def registrar_novo_usuario(email: str, senha: str, tipo_conta: str, foto: UploadFile | str):
    """
    Método legado para testar com o /docs do FastAPI
    """

    usuario = classe_usuario.Usuario(email, senha, tipo_conta, foto)
    db = database.conectar_bd()

    if usuario.foto == "":
        usuario.foto = None

    if crud_usuario.obter_usuario_por_nome(db, usuario.email):
        raise HTTPException(status_code=400, detail="Usuario já existe")
    
    usuario.senha_hashed = auth.gerar_hash_senha(usuario.senha_hashed)
    crud_usuario.criar_usuario(db, usuario)
    token_acesso = auth.criar_token_acesso(dados={"sub": usuario.email})
    return {"access_token": token_acesso, "token_type": "bearer"}


class UsuarioLogin(BaseModel):
    email: str
    senha: str

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

@app.post("/usuario/login_legacy")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login legado para teste com o /docs do FastAPI
    """
    db = database.conectar_bd()
    usuario = auth.autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    token_acesso = auth.criar_token_acesso(dados={"sub": usuario.email})
    return {"access_token": token_acesso, "token_type": "bearer"}

class EmpresaCadastro(BaseModel):
    nome_fantasia: str
    cnpj: str
    uf: str
    cidade: str
    bairro: str
    cep: str
    rua: str
    numero: int
    latitude: float
    longitude: float

@app.post("/usuario/cadastrar_dados_empresa")
async def cadastrar_dados_empresa(empresa: EmpresaCadastro, token: str = Depends(oauth2_esquema)):
    """
    Continuação do cadastro para os dados da empresa
    """
    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    if usuario.tipo_conta != "empresa":
        raise HTTPException(status_code=400, detail="Tipo de usuário não é empresa")

    if crud_usuario.verificar_se_dados_ja_cadastrados(db, usuario.email):
        raise HTTPException(status_code=400, detail="Empresa já possui cadastro")

    empresa.latitude = float(empresa.latitude)
    empresa.longitude = float(empresa.longitude)
    
    # TODO: Validar latitude e longitude

    endereco: classe_endereco.Endereco = classe_endereco.Endereco(empresa.uf, empresa.cidade, empresa.bairro, empresa.cep, empresa.rua, empresa.numero)
    
    # TODO: Validar UF e outros dados do endereço

    local: classe_local.Local = classe_local.Local(0,0)
    local.latitude = empresa.latitude
    local.longitude = empresa.longitude

    # TODO: Validar CNPJ

    empresa: classe_usuario.Empresa = classe_usuario.Empresa(id=usuario.id, email=usuario.email, senha_hashed=usuario.senha_hashed, 
                                                             tipo_conta="empresa", foto=usuario.foto, nome_fantasia=empresa.nome_fantasia, cnpj=empresa.cnpj, 
                                                             endereco=endereco, local=local)
    
    empresa.id = usuario.id

    crud_usuario.cadastrar_empresa(db, empresa)

    return {"detail": "Cadastro realizado com sucesso"}

@app.post("/usuario/cadastrar_dados_cliente")
async def cadastrar_dados_cliente(nome_completo: str, cpf: str, token: str = Depends(oauth2_esquema)):
    """
    Continuação do cadastro para os dados do cliente
    """

    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    if usuario.tipo_conta != "cliente":
        raise HTTPException(status_code=400, detail="Tipo de usuário não é cliente")
    
    if crud_usuario.verificar_se_dados_ja_cadastrados(db, usuario.email):
        raise HTTPException(status_code=400, detail="Cliente já possui cadastro")
    
    # TODO: Validar CPF

    cliente: classe_usuario.Cliente = classe_usuario.Cliente(usuario.id, usuario.email, usuario.senha_hashed,
                                                             "cliente", usuario.foto, nome_completo, cpf)
    
    cliente.id = usuario.id

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

class UsuarioEditar(BaseModel):
    email: str | None = None,
    senha: str | None = None,
    foto: UploadFile | None = None
    token: str = Depends(oauth2_esquema)

@app.put("/usuario/alterar_dados")
async def editar_dados_cadastrais(dados: UsuarioEditar):
    """
    Altera os dados cadastrais de um usuário.

    @param email: O email novo daquele usuário, ou None caso não haja alteração
    @param senha: A senha nova daquele usuário, ou None caso não haja alteração
    @param foto: A nova foto daquele usuário, ou None caso não haja alteração
    @param token: O token de acesso daquele usuário
    """

    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, dados.token)

    if dados.email:
        if crud_usuario.obter_usuario_por_nome(db, dados.email):
            raise HTTPException(status_code=400, detail="E-mail já cadastrado")
        else:
            usuario.email = dados.email
    
    if dados.senha:
        usuario.senha_hashed = auth.gerar_hash_senha(dados.senha)
    
    if dados.foto:
        if (os.path.isfile(usuario.foto)):
            # remover a foto antiga e salvar a nova
            try:
                os.remove(usuario.foto)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Erro ao deletar foto antiga: {e}")
        
        try:
            caminho_da_nova_foto = f"imagens/usuarios/{dados.foto.filename}"
            with open(caminho_da_nova_foto, "wb") as arquivo_foto:
                arquivo_foto.write(dados.foto.file.read())
                usuario.foto = caminho_da_nova_foto
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Falha ao salvar a foto do usuário: {e.args}")

    crud_usuario.atualizar_usuario(db, usuario)
    
    return {"detail": "Dados alterados com sucesso"}

@app.get("/usuario/buscar_dados_cadastrais")
async def buscar_dados_cadastrais(token: str = Depends(oauth2_esquema)):
    """
    Busca os dados cadastrais de um usuário. Usado para mostrar os dados do perfil do usuário

    @param token: O token de acesso do usuário
    """

    db = database.conectar_bd()
    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    return usuario

@app.get("/usuario/buscar_foto_perfil")
async def buscar_foto_perfil(token: str = Depends(oauth2_esquema)):
    """
    Busca a foto de perfil de um usuário

    @param token: O token de acesso do usuário
    """
    
    db = database.conectar_bd()
    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    if usuario.foto == "" or usuario.foto is None:
        return FileResponse("imagens/imagem_perfil_padrao.png")
    
    if os.path.isfile(usuario.foto):
        return FileResponse(usuario.foto)
    
    return FileResponse("imagens/imagem_perfil_padrao.png")

# Métodos de propostas ----------------------------------------

@app.post("/propostas/aceitar_ou_rejetar_proposta")
async def aceitar_ou_rejeitar_proposta(id_proposta: int, opcao: bool, token: str = Depends(oauth2_esquema)):
    """
    Aceita ou rejeita uma proposta feita para uma empresa

    @param id_proposta: O ID da proposta a ser alterada
    @param opcao: True caso ela seja aceita, False caso ela seja rejeitada
    @param token: O token de acesso do usuário
    """

    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    if usuario.tipo_conta != "empresa":
        raise HTTPException(status_code=400, detail="Apenas empresas podem aceitar ou rejeitar propostas")

    aluguel = crud_aluguel.buscar_aluguel(db, id_proposta)

    if aluguel is None:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")
    
    if aluguel.id_empresa != usuario.id:
        raise HTTPException(status_code=400, detail="Proposta não pertence ao usuário")
    
    if aluguel.estado_aluguel != "proposto":
        raise HTTPException(status_code=400, detail="Status do aluguel não é 'proposta'")
    
    novo_status = "rejeitado"
    if opcao:
        novo_status = "ativo"

    crud_aluguel.alterar_status_aluguel(db, id_proposta, novo_status)

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
async def buscar_dados_proposta(id_proposta: int, token: str = Depends(oauth2_esquema)):
    """
    Busca os dados específicos de uma proposta única

    @param id_proposta: O ID da proposta a ser buscada
    @param token: O token de acesso daquele usuário
    """

    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    aluguel = crud_aluguel.buscar_aluguel(db, id_proposta)

    if aluguel is None:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")
    
    if aluguel.id_empresa != usuario.id and aluguel.id_cliente != usuario.id:
        raise HTTPException(status_code=400, detail="Proposta não pertence ao usuário")
    
    return aluguel

@app.post("/propostas/criar_proposta/")
async def criar_proposta(id_empresa: int, id_veiculo: int, latitude_partida: float, longitude_partida: float,
                   latitude_chegada: float, longitude_chegada: float, distancia_extra_km: float,
                   data_saida: datetime.date, data_chegada: datetime.date,
                   token: str = Depends(oauth2_esquema)):
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

    if usuario.tipo_conta != "cliente":
        raise HTTPException(status_code=400, detail="Tipo de usuário não é cliente")
    
    if not crud_veiculo.verificar_veiculo_empresa(db, id_veiculo, id_empresa):
        raise HTTPException(status_code=400, detail="Veículo não pertence a empresa")
    
    if not crud_veiculo.verificar_disponibilidade_veiculo(db, id_veiculo, data_saida, data_chegada):
        raise HTTPException(status_code=400, detail="Veículo não disponível para o período escolhido")

    if (not valida_coordendas(latitude_partida, longitude_partida)) or (not valida_coordendas(latitude_chegada, longitude_chegada)):
        raise HTTPException(status_code=400, detail="Coordenadas inválidas")
    
    if (data_chegada > data_saida):
        raise HTTPException(status_code=400, detail="Datas inválidas: data de chegada anterior a data de saída")

    veiculo: classe_veiculo.Veiculo = crud_veiculo.buscar_veiculo(db, id_veiculo)
    if not veiculo:
        raise HTTPException(status_code=400, detail="Veículo não encontrado")

    aluguel: classe_aluguel.Aluguel = classe_aluguel.Aluguel(None, usuario.id, id_empresa, id_veiculo)
    aluguel.adicionar_datas(data_saida, data_chegada)

    # TODO: verficar se o local já existe
    # TODO: pensar numa forma para adicionar o nome no local
    # TODO: verificar se veículo tem valor por km

    local_partida: classe_local.Local = classe_local.Local(latitude_partida, longitude_partida)
    local_partida.id = crud_local.criar_local(db, local_partida)
    local_chegada: classe_local.Local = classe_local.Local(latitude_chegada, longitude_chegada)
    local_chegada.id = crud_local.criar_local(db, local_chegada)

    aluguel.adicionar_locais(local_partida, local_chegada)
    aluguel.adicionar_distancia_extra(distancia_extra_km)
    aluguel.calcular_valor_total(veiculo.custo_por_km, veiculo.custo_base)

    aluguel.estado_aluguel = "proposto"

    crud_aluguel.criar_aluguel(db, aluguel)

    return {"detail": "Proposta criada com sucesso"}

@app.put("/propostas/cancelar_proposta/")
async def cancelar_proposta(id_proposta: int, token: str = Depends(oauth2_esquema)):
    """
    Cancela uma proposta de um cliente

    @param id_proposta: O ID da proposta a ser cancelada
    @param token: O token de acesso do usuário
    """

    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(token)

    if usuario.tipo_conta != "cliente":
        raise HTTPException(status_code=400, detail="Apenas clientes podem cancelar propostas")

    aluguel = crud_aluguel.buscar_aluguel(db, id_proposta)

    if aluguel is None:
        raise HTTPException(status_code=404, detail="Proposta não encontrada")
    
    if aluguel.id_cliente != usuario.id:
        raise HTTPException(status_code=400, detail="Proposta não pertence ao cliente")
    
    if aluguel.estado_aluguel != "proposto":
        raise HTTPException(status_code=400, detail="Status do aluguel não é 'proposto'")

    crud_aluguel.remover_aluguel(db, id_proposta)

    return {"detail": "Proposta cancelada com sucesso!"}    
    
# Métodos de veículos ----------------------------------------

@app.post("/veiculos/cadastrar_veiculo/")
async def cadastrar_veiculo(nome_veiculo: str, placa_veiculo: str, custo_por_km: float, custo_base: float, cor: str, 
                            ano_fabricacao: int, capacidade: int, foto: UploadFile, token: str = Depends(oauth2_esquema)):
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
    
    if foto == "":
        raise HTTPException(status_code=400, detail="Foto inválida")
    
    if (custo_por_km <= 0) or (custo_base <= 0):
        raise HTTPException(status_code=400, detail="Valores de custo negativos")
    
    if capacidade < 1:
        raise HTTPException(status_code=400, detail="Capacidade do veículo inválida")
    
    if (ano_fabricacao < 1990) or (ano_fabricacao > datetime.date.today().year):
        raise HTTPException(status_code=400, detail="Ano de fabricação inválido")
    
    placa_veiculo = placa_veiculo.upper()
    if not valida_placa(placa_veiculo):
        raise HTTPException(status_code=400, detail="Placa do veículo inválida")

    try:
        caminho_da_foto = f"imagens/veiculos/{foto.filename}"
        with open(caminho_da_foto, "wb") as arquivo_foto:
            arquivo_foto.write(foto.file.read())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Falha ao salvar a foto do veículo: {e.args}")

    veiculo: classe_veiculo.Veiculo = classe_veiculo.Veiculo(None, usuario.id, nome_veiculo, placa_veiculo)
    veiculo.adicionar_custos(custo_por_km, custo_base)
    veiculo.adicionar_dados(caminho_da_foto, cor, ano_fabricacao, capacidade)

    crud_veiculo.criar_veiculo(db, veiculo)

    return {"detail": "Veículo cadastrado com sucesso!"}

@app.put("/veiculos/editar_veiculo")
async def editar_veiculo(id_veiculo: int, nome_veiculo: str | None = None, placa_veiculo: str | None = None,
                   custo_por_km: float | None = None, custo_base: float | None = None, foto: UploadFile | None = None,
                   cor: str | None = None, ano_fabricacao: int | None = None,
                   token: str = Depends(oauth2_esquema)):
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

    if not crud_veiculo.verificar_veiculo_empresa(db, id_veiculo, usuario.id):
        raise HTTPException(status_code=400, detail="O veículo não pertence à empresa")

    veiculo: classe_veiculo.Veiculo = crud_veiculo.buscar_veiculo(db, id_veiculo)

    # tentando fugir de criar vários if's
    novos_valores: dict[str, any | None] = {
        "nome_veiculo": nome_veiculo,
        "placa_veiculo": placa_veiculo,
        "custo_por_km": custo_por_km,
        "custo_base": custo_base,
        "cor": cor,
        "ano_fabricacao": ano_fabricacao
    }

    for atributo, valor in novos_valores.items():
        if valor is not None:
            setattr(veiculo, atributo, valor)

    if foto:
        if (os.path.isfile(veiculo.caminho_foto)):
            # remover a foto antiga e salvar a nova
            try:
                os.remove(veiculo.caminho_foto)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Erro ao deletar foto antiga: {e}")
        
        try:
            caminho_da_nova_foto = f"imagens/veiculos/{foto.filename}"
            with open(caminho_da_nova_foto, "wb") as arquivo_foto:
                arquivo_foto.write(foto.file.read())
                veiculo.caminho_foto = caminho_da_nova_foto
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Falha ao salvar a foto do veículo: {e.args}")

    crud_veiculo.atualizar_veiculo(db, veiculo)

    return {"detail": "Veículo editado com sucesso!"}

@app.get("/veiculos/buscar_veiculos_empresa")
async def buscar_todos_veiculos_empresa(id_empresa: int, token: str = Depends(oauth2_esquema)):
    """
    Busca todos os veículos de uma empresa

    @param id_empresa: O ID da empresa a qual se quer se buscar os veículos
    @param token: O token de acesso do usuário
    """

    db = database.conectar_bd()

    auth.obter_usuario_atual(db, token)

    return crud_veiculo.listar_veiculos(db, id_empresa)

@app.get("/veiculos/buscar_dados_veiculo")
async def buscar_dados_veiculo(id_veiculo: int, token: str = Depends(oauth2_esquema)):
    """
    Busca os dados de um veículo

    @param id_veiculo: O ID do veículo a se buscar os dados
    @param token: O token de acesso do usuário
    """
    db = database.conectar_bd()

    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    # Buscar os dados do veículo no banco de dados
    return crud_veiculo.buscar_veiculo(db, id_veiculo)

@app.delete("/veiculos/apagar_veiculo")
async def apagar_veiculo(id_veiculo: int, token: str = Depends(oauth2_esquema)):
    """
    Apaga um veículo do sistema

    @param id_veiculo: O ID do veículo a ser apagado
    @param token: O token de acesso do usuário
    """

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

@app.get("/veiculos/buscar_foto_veiculo")
async def buscar_foto_veiculo(id_veiculo: int, token: str = Depends(oauth2_esquema)):
    """
    Busca a foto de um veículo

    @param token: O token de acesso do usuário
    """
    db = database.conectar_bd()
    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    veiculo = crud_veiculo.buscar_veiculo(db, id_veiculo)

    if veiculo.caminho_foto == "" or veiculo.caminho_foto is None:
        return FileResponse("imagens/imagem_veiculo_padrao.png")
    
    if os.path.isfile(veiculo.caminho_foto):
        return FileResponse(veiculo.caminho_foto)
    
    return FileResponse("imagens/imagem_veiculo_padrao.png")

# Métodos extras cliente/empresa ----------------------------------------

@app.get("/empresa/buscar_dados_empresa")
async def buscar_dados_empresa(id_empresa: int, token: str = Depends(oauth2_esquema)):
    """
    Busca os dados de uma empresa específica

    @param id_empresa: O ID da empresa a qual se quer buscar os dados
    @param token: O token de acesso do usuário
    """

    db = database.conectar_bd()
    usuario_atual = auth.obter_usuario_atual(db, token)

    return crud_usuario.buscar_empresa_por_id(db, id_empresa)

@app.put("/empresa/avaliar_empresa")
async def avaliar_empresa(id_empresa: int, avaliacao: float, token: str = Depends(oauth2_esquema)):
    """
    Adiciona uma avaliação a uma empresa

    @param id_empresa: O ID da empresa a ser avaliada
    @param avaliacao: A nota (um valor entre 0 e 5)
    @param token: O token de acesso do usuário
    """

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
async def buscar_empresas_nome(nome_busca: str, token: str = Depends(oauth2_esquema)):
    """
    Busca as empresas a partir do nome

    @param nome_busca: O nome de empresa a ser buscada
    @param token: O token de acesso do usuário
    """

    # Obter o usuário a partir do token

    db = database.conectar_bd()

    # Validação apenas
    usuario: classe_usuario.Usuario = auth.obter_usuario_atual(db, token)

    nome_busca = nome_busca + "%"

    # TODO: Ver formato necessário para retornar para o frontend

    return crud_usuario.buscador_empresas_nome(db, nome_busca)

@app.get("/busca/buscar_empresas/criterio")
async def buscar_empresas_criterio(criterio: str, token: str = Depends(oauth2_esquema)):
    """
    Busca as empresas a partir de outros critérios

    @param criterio:
    @param token: O token de acesso do usuário
    """

    # Obter o usuário a partir do token

    # TODO: Pensar em mais critérios aqui...

    pass
