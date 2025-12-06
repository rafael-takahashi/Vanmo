import os
import httpx
from dotenv import load_dotenv
from supabase import create_client, Client
from fastapi import UploadFile, HTTPException

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "fotos"
print(SUPABASE_URL)
print(SUPABASE_KEY)

def get_supabase_client() -> Client:
    """
    Inicializa e retorna o cliente Supabase
    
    :return: Cliente Supabase configurado
    :raises HTTPException: Se as variáveis de ambiente não estiverem configuradas
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise HTTPException(
            status_code=500,
            detail="Configurações do Supabase não encontradas. Verifique SUPABASE_URL e SUPABASE_KEY no arquivo .env"
        )
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)

async def upload_foto_empresa(id_empresa: int, file: UploadFile) -> str:
    """
    Faz upload da foto de uma empresa para o Supabase Storage
    
    :param id_empresa: ID da empresa
    :param file: Arquivo de imagem a ser enviado
    :return: URL pública da imagem no Supabase
    :raises HTTPException: Se houver erro no upload
    """
    try:
        supabase = get_supabase_client()
        
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ".png"
        file_path = f"empresas/{id_empresa}{file_extension}"
        
        file_content = await file.read()
        
        try:
            buckets = supabase.storage.list_buckets()
            bucket_names = [bucket.name for bucket in buckets] if buckets else []
            if BUCKET_NAME not in bucket_names:
                raise HTTPException(
                    status_code=500,
                    detail=f"Bucket '{BUCKET_NAME}' não encontrado. Crie o bucket no Supabase Storage primeiro."
                )
        except Exception as bucket_error:
            pass
        
        upload_url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{file_path}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": file.content_type or "image/png",
            "x-upsert": "true"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                upload_url,
                content=file_content,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code not in [200, 201]:
                error_text = response.text if response.text else "Sem detalhes do erro"
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro ao fazer upload no Supabase (status {response.status_code}): {error_text}. Verifique se o bucket '{BUCKET_NAME}' existe, está público e as políticas RLS estão configuradas."
                )
        
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{file_path}"
        
        return public_url
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer upload da foto: {error_msg}"
        )

async def upload_foto_cliente(id_cliente: int, file: UploadFile) -> str:
    """
    Faz upload da foto de um cliente para o Supabase Storage
    
    :param id_cliente: ID do cliente
    :param file: Arquivo de imagem a ser enviado
    :return: URL pública da imagem no Supabase
    :raises HTTPException: Se houver erro no upload
    """
    try:
        supabase = get_supabase_client()
        
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ".png"
        file_path = f"clientes/{id_cliente}{file_extension}"
        
        file_content = await file.read()
        
        try:
            buckets = supabase.storage.list_buckets()
            bucket_names = [bucket.name for bucket in buckets] if buckets else []
            if BUCKET_NAME not in bucket_names:
                raise HTTPException(
                    status_code=500,
                    detail=f"Bucket '{BUCKET_NAME}' não encontrado. Crie o bucket no Supabase Storage primeiro."
                )
        except Exception as bucket_error:
            pass
        
        upload_url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{file_path}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": file.content_type or "image/png",
            "x-upsert": "true"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                upload_url,
                content=file_content,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code not in [200, 201]:
                error_text = response.text if response.text else "Sem detalhes do erro"
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro ao fazer upload no Supabase (status {response.status_code}): {error_text}. Verifique se o bucket '{BUCKET_NAME}' existe, está público e as políticas RLS estão configuradas."
                )
        
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{file_path}"
        
        return public_url
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer upload da foto: {error_msg}"
        )

async def upload_foto_veiculo(id_empresa: int, id_veiculo: int, file: UploadFile) -> str:
    """
    Faz upload da foto de um veículo para o Supabase Storage
    
    :param id_empresa: ID da empresa dona do veículo
    :param id_veiculo: ID do veículo
    :param file: Arquivo de imagem a ser enviado
    :return: URL pública da imagem no Supabase
    :raises HTTPException: Se houver erro no upload
    """
    try:
        supabase = get_supabase_client()
        
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ".png"
        file_path = f"veiculos/{id_empresa}/{id_veiculo}{file_extension}"
        
        file_content = await file.read()
        
        try:
            buckets = supabase.storage.list_buckets()
            bucket_names = [bucket.name for bucket in buckets] if buckets else []
            if BUCKET_NAME not in bucket_names:
                raise HTTPException(
                    status_code=500,
                    detail=f"Bucket '{BUCKET_NAME}' não encontrado. Crie o bucket no Supabase Storage primeiro."
                )
        except Exception as bucket_error:
            pass
        
        upload_url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{file_path}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": file.content_type or "image/png",
            "x-upsert": "true"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                upload_url,
                content=file_content,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code not in [200, 201]:
                error_text = response.text if response.text else "Sem detalhes do erro"
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro ao fazer upload no Supabase (status {response.status_code}): {error_text}. Verifique se o bucket '{BUCKET_NAME}' existe, está público e as políticas RLS estão configuradas."
                )
        
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{file_path}"
        
        return public_url
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer upload da foto: {error_msg}"
        )
