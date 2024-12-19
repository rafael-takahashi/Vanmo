from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import List

import database, auth
from classes import classe_aluguel, classe_calendario, classe_endereco, classe_local, classe_usuario, classe_veiculo
from cruds import crud_aluguel, crud_usuario, crud_veiculo

app = FastAPI()

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

# @app.post("/registrar", response_model=classe_usuario.Usuario)
# def registrar_novo_usuario(usuario: classe_usuario.Usuario = Depends()):
#     db = database.conectar_bd()
#     if crud_usuario.obter_usuario_por_nome(db, usuario.email):
#         raise HTTPException(status_code=400, detail="Usuario já existe")
    
#     senha_hashed = auth.gerar_hash_senha(usuario.senha)
#     crud_usuario.criar_usuario(db, usuario, senha_hashed)
#     token_acesso = auth.criar_token_acesso(dados={"sub": usuario.username})
#     return {"access_token": token_acesso, "token_type": "bearer"}


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
