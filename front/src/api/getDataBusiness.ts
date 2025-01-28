import { api } from '@/lib/axios'

interface GetDataBusinessParams {
  idEmpresa: string
}

interface Endereco {
  bairro: string
  cep: string
  cidade: string
  numero: string
  rua: string
  uf: string
  id: number
}

export interface Business {
  foto: string
  nome_fantasia: string
  cnpj: string
  endereco: Endereco
  avaliacoes: number
  telefone: string
}

export async function getDataBusiness({
  idEmpresa,
}: GetDataBusinessParams): Promise<Business> {
  try {
    const response = await api.get(`/busca/buscar_dados_empresa/${idEmpresa}`)

    return response.data
  } catch (error) {
    console.error('Erro ao buscar empresas:', error)
    throw error
  }
}
