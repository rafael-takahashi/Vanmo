import { api } from '@/lib/axios'

interface GetBusinessVehiclesParams {
  id_empresa: number
  pagina: number
}

export interface Vehicles {
  ano_fabricacao: number
  calendario_disponibilidade: null
  caminho_foto: null
  capacidade: number
  cor: string
  custo_base: number
  custo_por_km: number
  id_empresa: number
  id_veiculo: number
  nome_veiculo: string
  placa_veiculo: string
}

export async function getBusinessVehicles({
  id_empresa,
  pagina,
}: GetBusinessVehiclesParams): Promise<Vehicles[]> {
  try {
    const response = await api.get(
      `/veiculos/buscar_veiculos_empresa/${id_empresa}/${pagina}`,
    )
    return response.data
  } catch (error: any) {
    console.error('Error:', error.response?.data || error.message)
    throw error
  }
}
