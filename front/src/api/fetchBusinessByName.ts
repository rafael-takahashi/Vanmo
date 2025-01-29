import { api } from '@/lib/axios'

interface FetchBusinessByNameParams {
  nome: string
}

export interface Endereco {
  bairro: string
  cep: string
  cidade: string
  numero: string
  rua: string
  uf: string
  id: number
}

export interface Business {
  cnpj: string
  email: string
  endereco: Endereco
  foto: string
  id: number
  nome_fantasia: string
  num_avaliacoes: number
  soma_avaliacoes: number
  telefone: string
  tipo_conta: string
}

export async function fetchBusinessByName({
  nome,
}: FetchBusinessByNameParams): Promise<Business[]> {
  try {
    const response = await api.get(`/busca/buscar_empresas/nome/${nome}`)

    return response.data
  } catch (error) {
    console.error('Erro ao buscar empresas:', error)
    throw error
  }
}
