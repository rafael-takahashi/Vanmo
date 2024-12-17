from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
import sqlite3
from cruds.crud_usuario import obter_usuario_por_nome

CHAVE_SECRETA = ""  # Altere para uma chave secreta em produção
ALGORITMO = "HS256"
TEMPO_EXPIRACAO_TOKEN_MINUTOS = 30

pwd_contexto = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_plana, senha_hashed):
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return pwd_contexto.verify(senha_plana, senha_hashed)

def gerar_hash_senha(senha):
    """Gera um hash para a senha fornecida."""
    return pwd_contexto.hash(senha)

def autenticar_usuario(db, username: str, senha: str):
    """Autentica o usuário verificando suas credenciais."""
    usuario = obter_usuario_por_nome(db, username)
    if usuario and verificar_senha(senha, usuario.senha_hashed):
        return usuario
    return None

def criar_token_acesso(dados: dict):
    """Cria um token de acesso JWT para o usuário."""
    dados_a_codificar = dados.copy()
    expira = datetime.now() + timedelta(minutes=TEMPO_EXPIRACAO_TOKEN_MINUTOS)
    dados_a_codificar.update({"exp": expira})
    return jwt.encode(dados_a_codificar, CHAVE_SECRETA, algorithm=ALGORITMO)

def obter_usuario_atual(db, token: str):
    """Obtém o usuário atual a partir do token JWT."""
    from fastapi import HTTPException, status
    try:
        payload = jwt.decode(token, CHAVE_SECRETA, algorithms=[ALGORITMO])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        usuario = obter_usuario_por_nome(db, username=username)
        if usuario is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
