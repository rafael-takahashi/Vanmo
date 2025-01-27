import { api } from '@/lib/axios'

interface FetchBusinessByName {
  nome: string
}

export async function fetchBusinessByName({ nome }: FetchBusinessByName) {
  try {
    console.log(nome)
    const response = await api.get(`/busca/buscar_empresas/${nome}`)
    return response.data
  } catch (error) {
    console.error('Erro ao buscar empresas:', error)
    throw error
  }
}
