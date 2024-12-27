import datetime

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from contextlib import asynccontextmanager

import database, auth
from classes import classe_aluguel, classe_calendario, classe_endereco, classe_local, classe_usuario, classe_veiculo
from cruds import crud_aluguel, crud_usuario, crud_veiculo

@asynccontextmanager
async def iniciar_app(app: FastAPI):
    """
        Função chamada ao inicializar o sistema
    """

    # Criar tabelas no banco de dados caso elas não existam
    conexao = database.conectar_bd()
    database.criar_tabelas(conexao)
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
oauth2_esquema = OAuth2PasswordBearer(tokenUrl="/login")

# Métodos de usuário ----------------------------------------

@app.post("/usuario/registrar")
async def registrar_novo_usuario(email: str, senha: str, tipo_conta: str, foto: UploadFile | str = ""):
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

    # A fazer: checar se o tamanho e o tipo de arquivo da foto são permitidos
    # Caso não for, decidir entre retornar um código de erro ou prosseguir sem a foto

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


@app.post("/usuario/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Realiza o login de um usuário no sistema

    @param form_data: Os dados do formulário contendo email (username) e senha (password)
    @return:
        Caso sucesso, retorna o token de acesso para aquele usuário
        Caso algum dos dados estejam errados, retorna o código 400
    """
    db = database.conectar_bd()
    usuario = auth.autenticar_usuario(db, form_data.username, form_data.password)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")

    token_acesso = auth.criar_token_acesso(dados={"sub": usuario.email})
    return {"access_token": token_acesso, "token_type": "bearer"}


@app.delete("/usuario/apagar_conta")
async def apagar_usuario(token: str = Depends(oauth2_esquema)):
    """
    Apaga a conta de um usuário, só pode ser chamado pelo próprio usuário

    @param token: O token de acesso do usuário
    """

    # Buscar o usuário pelo token e validar ele

    # Apagar conta

    # Revogar token
    pass

@app.put("/usuario/alterar_dados")
async def editar_dados_cadastrais(email: str | None = None, senha: str | None = None,
                            foto: UploadFile | None = None, token: str = Depends(oauth2_esquema)):
    """
    Altera os dados cadastrais de um usuário.

    @param email: O email novo daquele usuário, ou None caso não haja alteração
    @param senha: A senha nova daquele usuário, ou None caso não haja alteração
    @param foto: A nova foto daquele usuário, ou None caso não haja alteração
    @param token: O token de acesso daquele usuário
    """

    # Buscar usuário pelo token e validar ele

    # Caso o email seja alterado, ver se não há outro usuário com o mesmo email

    # Alterar os dados
    pass


@app.get("/usuario/buscar_dados_cadastrais")
async def buscar_dados_cadastrais(token: str = Depends(oauth2_esquema)):
    """
    Busca os dados cadastrais de um usuário. Usado para mostrar os dados do perfil do usuário

    @param token: O token de acesso do usuário
    """

    # Busca o usuário a partir do token e retorna os seus dados
    pass

# Métodos de propostas ----------------------------------------

@app.post("/propostas/aceitar_ou_rejetar_proposta")
async def aceitar_ou_rejeitar_proposta(id_proposta: int, opcao: bool, token: str = Depends(oauth2_esquema)):
    """
    Aceita ou rejeita uma proposta feita para uma empresa

    @param id_proposta: O ID da proposta a ser alterada
    @param opcao: True caso ela seja aceita, False caso ela seja rejeitada
    @param token: O token de acesso do usuário
    """

    # Obter o usuário a partir do token

    # Ver se o usuário é uma empresa

    # Ver se a proposta está vinculada aquela empresa em específico

    # Caso a proposta seja rejeitada, alterar o status para rejeitada, caso contrário, passe para ativa

    pass

@app.get("/propostas/buscar_propostas")
async def buscar_todas_propostas_usuario(token: str = Depends(oauth2_esquema)):
    """
    Busca todas as propostas de um usuário

    @param token: O token de acesso do usuário
    """

    # Obter o usuário a partir do token

    # Buscar as propostas desse usuário e retornar
    pass

@app.get("/propostas/dados_proposta")
async def buscar_dados_proposta(id_proposta: int, token: str = Depends(oauth2_esquema)):
    """
    Busca os dados específicos de uma proposta única

    @param id_proposta: O ID da proposta a ser buscada
    @param token: O token de acesso daquele usuário
    """

    # Buscar o usuário a partir do token

    # Ver se o usuário está envolvido com a proposta específica

    # Se sim, retornar os dados dela, caso contrário, retornar erro de autenticação
    pass

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

    # Obter o usuário a partir do token

    # Ver se o usuário é um cliente

    # Obter a empresa a partir do ID

    # Obter o veículo a partir do ID

    # Validar que o veículo é de fato da empresa e está disponível entre as datas necessárias

    # Montar a classe Aluguel necessária, calcular os valores de custo e distância total

    # Armazenar a classe no banco de dados

    pass

@app.put("/propostas/cancelar_proposta/")
async def cancelar_proposta(id_proposta: int, token: str = Depends(oauth2_esquema)):
    """
    Cancela uma proposta de um cliente

    @param id_proposta: O ID da proposta a ser cancelada
    @param token: O token de acesso do usuário
    """

    # Obter o usuário a partir do token

    # Verificar se a proposta é de fato dele e se ela não foi aceitada ou rejeitada ainda

    # Apagar a proposta
    pass

# Métodos de veículos ----------------------------------------

@app.post("/veiculos/cadastrar_veiculo/")
async def cadastrar_veiculo(nome_veiculo: str, placa_veiculo: str, custo_por_km: float, custo_base: float,
                      foto: UploadFile, cor: str, ano_fabricacao: datetime.date, token: str = Depends(oauth2_esquema)):
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

    # Obter o usuário a partir do token

    # Verificar se é de fato uma empresa

    # Validar dados da foto enviada

    # Armazenar a foto na pasta de imagens/veiculos/

    # OBS: No BD se armazena apenas o path da imagem
    # Montar a classe Veiculo correspondente e armazenar no banco de dados
    pass

@app.put("/veiculos/editar_veiculo")
async def editar_veiculo(id_veiculo: int, nome_veiculo: str | None = None, placa_veiculo: str | None = None,
                   custo_por_km: float | None = None, custo_base: float | None = None, foto: UploadFile | None = None,
                   cor: str | None = None, ano_fabricacao: datetime.date | None = None,
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
    # Obter o usuário a partir do token

    # Verificar se é de fato uma empresa e se o veículo pertence a ela

    # Copiar o veículo atualmente armazenado

    # Alterar os campos alterados (!= None)

    # Caso haja alteração na foto, validar seus dados também e atualizá-la na pasta de imagens

    # Alterar o veículo no banco de dados
    pass


@app.get("/veiculos/buscar_veiculos_empresa")
async def buscar_todos_veiculos_empresa(id_empresa: int, token: str = Depends(oauth2_esquema)):
    """
    Busca todos os veículos de uma empresa

    @param id_empresa: O ID da empresa a qual se quer se buscar os veículos
    @param token: O token de acesso do usuário
    """

    # Buscar o usuário pelo token de acesso

    # Ver se é um cliente ou empresa válido

    # Buscar os dados da empresa no banco de dados e retorná-los
    pass

@app.get("/veiculos/buscar_dados_veiculo")
async def buscar_dados_veiculo(id_veiculo: int, token: str = Depends(oauth2_esquema)):
    """
    Busca os dados de um veículo

    @param id_veiculo: O ID do veículo a se buscar os dados
    @param token: O token de acesso do usuário
    """

    # Buscar o usuário a partir do token e validá-lo

    # Buscar os dados do veículo no banco de dados
    pass

@app.delete("/veiculos/apagar_veiculo")
async def apagar_veiculo(id_veiculo: int, token: str = Depends(oauth2_esquema)):
    """
    Apaga um veículo do sistema

    @param id_veiculo: O ID do veículo a ser apagado
    @param token: O token de acesso do usuário
    """

    # Buscar o usuário a partir do token de acesso

    # Validar se o usuário é uma empresa e o veículo pertence a ela

    # Verificar se não há nenhum aluguel ativo com aquele veículo

    # Caso não, apagar o veículo no banco de dados
    pass

# Métodos extras cliente/empresa ----------------------------------------

@app.get("/empresa/buscar_dados_empresa")
async def buscar_dados_empresa(id_empresa: int, token: str = Depends(oauth2_esquema)):
    """
    Busca os dados de uma empresa específica

    @param id_empresa: O ID da empresa a qual se quer buscar os dados
    @param token: O token de acesso do usuário
    """

    # Obter o usuário a partir do token
    pass

@app.put("/empresa/avaliar_empresa")
async def avaliar_empresa(id_empresa: int, avaliacao: float, token: str = Depends(oauth2_esquema)):
    """
    Adiciona uma avaliação a uma empresa

    @param id_empresa: O ID da empresa a ser avaliada
    @param avaliacao: A nota (um valor entre 0 e 5)
    @param token: O token de acesso do usuário
    """

    # Obter o usuário a partir do token

    # Validar se ele não já avaliou a empresa antes (e uma empresa não pode avaliar a si mesma)

    # Buscar os dados da empresa e alterar a soma e a quantidade de avaliações
    pass



@app.get("/busca/buscar_empresas/nome")
async def buscar_empresas_nome(nome_busca: str, token: str = Depends(oauth2_esquema)):
    """
    Busca as empresas a partir do nome

    @param nome_busca: O nome de empresa a ser buscada
    @param token: O token de acesso do usuário
    """

    # Obter o usuário a partir do token

    # Buscar as empresas cujo nome inicia com a string passada
    # OBS: Aqui daria pra usar alguma outra coisa mas adicionaria complexidade desnecessária
    pass

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


# TODO: Converter esses exemplos aqui para sqlite3 e formato com pastas

# @app.post("/tarefas", response_model=schemas.Tarefa)
# def criar_nova_tarefa(tarefa: schemas.TarefaBase, token: str = Depends(oauth2_esquema), db: Session = Depends(get_db)):
#     """Rota para criar uma nova tarefa."""
#     usuario_atual = auth.obter_usuario_atual(db, token)
#     return crud.criar_tarefa(db, tarefa, usuario_id=usuario_atual.id)

# @app.get("/tarefas", response_model=List[schemas.Tarefa])
# def ler_tarefas(token: str = Depends(oauth2_esquema), db: Session = Depends(get_db)):
#     """Rota para obter todas as tarefas do usuário autenticado."""
#     usuario_atual = auth.obter_usuario_atual(db, token)
#     return crud.obter_tarefas(db, usuario_id=usuario_atual.id)

# @app.delete("/tarefas/{tarefa_id}")
# def deletar_tarefa(tarefa_id: int, token: str = Depends(oauth2_esquema), db: Session = Depends(get_db)):
#     """Rota para deletar uma tarefa específica."""
#     usuario_atual = auth.obter_usuario_atual(db, token)
#     tarefa_deletada = crud.deletar_tarefa(db, tarefa_id, usuario_id=usuario_atual.id)
#     if tarefa_deletada is None:
#         raise HTTPException(status_code=404, detail="Tarefa não encontrada")
#     return {"detail": "Tarefa removida com sucesso"}

# @app.delete("/tarefas")
# def deletar_todas_tarefas(token: str = Depends(oauth2_esquema), db: Session = Depends(get_db)):
#     """Rota para deletar todas as tarefas do usuário."""
#     usuario_atual = auth.obter_usuario_atual(db, token)
#     crud.deletar_todas_tarefas(db, usuario_id=usuario_atual.id)
#     return {"detail": "Todas as tarefas foram removidas"}

# @app.put("/tarefas/{tarefa_id}", response_model=schemas.Tarefa)
# def atualizar_tarefa(tarefa_id: int, tarefa: schemas.TarefaBase, token: str = Depends(oauth2_esquema), db: Session = Depends(get_db)):
#     """Rota para atualizar uma tarefa existente."""
#     usuario_atual = auth.obter_usuario_atual(db, token)
#     tarefa_atualizada = crud.atualizar_tarefa(db, tarefa_id, usuario_id=usuario_atual.id, descricao=tarefa.descricao)
#     if tarefa_atualizada is None:
#         raise HTTPException(status_code=404, detail="Tarefa não encontrada")
#     return tarefa_atualizada
