from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import sqlite3
from cruds.crud_usuario import obter_usuario_por_nome

CHAVE_SECRETA = ""  # Alterar para uma chave secreta na hora da implementar o embiente
ALGORITMO = "HS256"
TEMPO_EXPIRACAO_TOKEN_MINUTOS = 30

pwd_contexto = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_plana, senha_hashed):
    """
    Verifica se a senha fornecida corresponde ao hash armazenado

    @param senha_plana: A senha a ser verificada
    @param senha_hashed: A senha armazenada no sistema
    """
    return pwd_contexto.verify(senha_plana, senha_hashed)

def gerar_hash_senha(senha):
    """
    Gera um hash para a senha fornecida

    @param senha: A senha a gerar o hash
    @return: O hash gerado da senha
    """
    return pwd_contexto.hash(senha)

def autenticar_usuario(db: sqlite3.Connection, username: str, senha: str):
    """
    Autentica o usuário verificando suas credenciais.

    @param db: A conexão com o banco de dados
    @param username: O nome de usuário a autenticar no sistema
    @param senha: A senha a autenticar no sistema
    @return: O usuário caso o login seja feito com sucesso, None caso contrário
    """
    usuario = obter_usuario_por_nome(db, username)
    if usuario and verificar_senha(senha, usuario.senha_hashed):
        return usuario
    return None

def criar_token_acesso(dados: dict):
    """
    Cria um token de acesso JWT para o usuário.

    @param dados: Os dados a serem codificados
    @return: O token codificado de acesso
    """
    dados_a_codificar = dados.copy()
    expira = datetime.now(timezone.utc) + timedelta(minutes=TEMPO_EXPIRACAO_TOKEN_MINUTOS)
    print(f"Token codificado: dados: {str(dados)} expira: {expira}")
    dados_a_codificar.update({"exp": expira})
    return jwt.encode(dados_a_codificar, CHAVE_SECRETA, algorithm=ALGORITMO)

def obter_usuario_atual(db, token: str):
    """
    Obtém o usuário atual a partir do token JWT

    @param db: A conexão com o banco de dados
    @param token: O token de acesso do usuário
    @return: A instância de usuário

    Caso o token seja inválido ou o usuário não esteja no sistema, retorna o código 401
    """
    from fastapi import HTTPException, status
    try:
        payload = jwt.decode(token, CHAVE_SECRETA, algorithms=[ALGORITMO])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        usuario = obter_usuario_por_nome(db, username)
        if usuario is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        return usuario
    except JWTError as e:
        print(str(e))
        raise HTTPException(status_code=401, detail="Token inválido")
