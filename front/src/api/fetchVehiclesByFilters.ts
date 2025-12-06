import { api } from '@/lib/axios'

interface FetchBusinessByFiltersParams {
  local_saida: string
  local_chegada: string
  data_de_partida: string
  data_de_chegada: string
  qtd_passageiros: string
  id_empresa: string
  pagina: number
}

interface Car {
  ano_fabricacao: number
  capacidade: number
  cor: string
  custo_base: number
  custo_por_km: number
  id_veiculo: number
  id_empresa: number
  nome_veiculo: string
  placa_veiculo: string
  custo_da_viagem: number
  foto_url: string
}

export async function fetchVehiclesByFilters({
  data_de_chegada,
  data_de_partida,
  local_chegada,
  local_saida,
  id_empresa,
  pagina,
  qtd_passageiros,
}: FetchBusinessByFiltersParams): Promise<Car[]> {
  try {
    const response = await api.get(
      `/veiculos/buscar_veiculos_empresa/criterio/${id_empresa}/${data_de_partida}/${data_de_chegada}/${qtd_passageiros}/${local_saida}/${local_chegada}/${pagina}`,
    )

    return response.data
  } catch (error) {
    console.error('Erro ao buscar empresas:', error)
    throw error
  }
}
