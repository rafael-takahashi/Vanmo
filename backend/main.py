from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from contextlib import asynccontextmanager

import database, auth
from classes import classe_aluguel, classe_calendario, classe_endereco, classe_local, classe_usuario, classe_veiculo
from cruds import crud_aluguel, crud_usuario, crud_veiculo

@asynccontextmanager
async def iniciar_app(app: FastAPI):
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

# @app.get("/teste")
# def teste():
#     db = database.conectar_bd()
#     return crud_usuario.obter_todos_usuarios(db)

@app.post("/registrar")
def registrar_novo_usuario(email: str, senha: str, tipo_conta: str, foto: bytes | None = None):
    usuario = classe_usuario.Usuario(email, senha, tipo_conta, foto)
    db = database.conectar_bd()
    if crud_usuario.obter_usuario_por_nome(db, usuario.email):
        raise HTTPException(status_code=400, detail="Usuario já existe")
    
    usuario.senha_hashed = auth.gerar_hash_senha(usuario.senha_hashed)
    crud_usuario.criar_usuario(db, usuario)
    token_acesso = auth.criar_token_acesso(dados={"sub": usuario.email})
    return {"access_token": token_acesso, "token_type": "bearer"}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = database.conectar_bd()
    usuario = auth.autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    token_acesso = auth.criar_token_acesso(dados={"sub": usuario.username})
    return {"access_token": token_acesso, "token_type": "bearer"}


@app.delete("/usuario/{id_usuario}")
def apagar_usuario(id_usuario: int, token: str = Depends(oauth2_esquema)):
    pass

@app.put("/usuario/{id_usuario}")
def editar_dados_cadastrais(email: str, senha: str, tipo_conta: str, 
                            foto: bytes | None = None, token: str = Depends(oauth2_esquema)):
    pass

@app.post("/empresa/propostas/{id_proposta}")
def alterar_proposta(id_proposta: int, opcao: bool, token: str = Depends(oauth2_esquema)):
    pass

@app.get("/propostas_usuario/{id_usuario}")
def buscar_todas_propostas_usuario(id_usuario: int, token: str = Depends(oauth2_esquema)):
    pass

@app.get("/propostas/{id_proposta}")
def buscar_dados_proposta(id_proposta: int, token: str = Depends(oauth2_esquema)):
    pass

@app.post("/propostas/criar_proposta/")
def criar_proposta(dados_para_a_proposta_vem_aqui: str, token: str = Depends(oauth2_esquema)):
    pass

@app.post("/veiculos/")
def cadastrar_veiculo(dados_veiculo_aqui: str, token: str = Depends(oauth2_esquema)):
    pass

@app.put("/veiculos/{id_veiculo}")
def editar_veiculo(id_veiculo: int, dados_veiculo_aqui: str, token: str = Depends(oauth2_esquema)):
    pass

@app.get("/veiculos_empresa/{id_empresa}")
def buscar_todos_veiculos_empresa(id_empresa: int, token: str = Depends(oauth2_esquema)):
    pass

@app.get("/veiculos/{id_veiculo}")
def buscar_dados_veiculo(id_veiculo: int, token: str = Depends(oauth2_esquema)):
    pass

@app.delete("/veiculos/{id_veiculo}")
def apagar_veiculo(id_veiculo: int, token: str = Depends(oauth2_esquema)):
    pass

@app.get("/empresa/{id_empresa}")
def buscar_dados_empresa(id_empresa: int, token: str = Depends(oauth2_esquema)):
    pass

@app.put("/empresa/{id_empresa}/avaliar_empresa")
def avaliar_empresa(id_empresa: int, avaliacao: float, token: str = Depends(oauth2_esquema)):
    pass

@app.put("/cliente/cancelar_proposta/{id_proposta}")
def cancelar_proposta(id_proposta: int, token: str = Depends(oauth2_esquema)):
    pass

@app.get("/busca/buscar_empresas/nome/{nome_empresa}")
def buscar_empresas_nome(token: str = Depends(oauth2_esquema)):
    pass

@app.get("/busca/buscar_empresas/filtros/")
def buscar_empresas_filtros(filtros_vem_aqui: str, token: str = Depends(oauth2_esquema)):
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
