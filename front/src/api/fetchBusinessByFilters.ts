import { api } from '@/lib/axios'

interface FetchBusinessByFiltersParams {
  data_de_partida?: string
  local_partida?: string
  qtd_passageiros?: string
  pagina?: number
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
  cnpj: string
  email: string
  endereco: Endereco
  foto: string
  id_usuario: number
  nome_fantasia: string
  num_avaliacoes: number
  soma_avaliacoes: number
  telefone: string
  tipo_conta: string
}

export async function fetchBusinessByFilters({
  data_de_partida,
  local_partida,
  pagina,
  qtd_passageiros,
}: FetchBusinessByFiltersParams): Promise<Business[]> {
  try {
    console.log(data_de_partida)
    console.log(local_partida)
    console.log(qtd_passageiros)

    const response = await api.get(
      `/busca/buscar_empresas/criterio/${data_de_partida}/${qtd_passageiros}/${local_partida}/${pagina}`,
    )

    return response.data
  } catch (error) {
    console.error('Erro ao buscar empresas:', error)
    throw error
  }
}
