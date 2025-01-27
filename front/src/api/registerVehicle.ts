import { api } from '@/lib/axios'

export interface registerVehicleBody {
  token: string | undefined
  name: string
  licensePlate: string
  costPerKm: number
  baseCost: number
  color: string
  year: number
  capacity: number
  photo: File | null
}

export async function registerVehicle({
  token,
  name,
  licensePlate,
  costPerKm,
  baseCost,
  color,
  year,
  capacity,
  photo
}: registerVehicleBody) {
  const jsonBody = JSON.stringify({
    nome_veiculo: name,
    placa_veiculo: licensePlate,
    custo_por_km: costPerKm,
    custo_base: baseCost,
    cor: color,
    ano_fabricacao: year,
    capacidade: capacity,
    foto: photo
  })
  try {
    const response = await api.post('/veiculos/cadastrar_veiculo/', jsonBody, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
    return response.data
  } catch (error: any) {
    console.error('Error:', error.response?.data || error.message)
    throw error
  }
}
