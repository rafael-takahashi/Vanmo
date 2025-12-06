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
  photo?: FileList | null
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
  photo,
}: registerVehicleBody) {
  const formData = new FormData()

  // 1. Adiciona campos de texto e converte números para String
  formData.append('nome_veiculo', name)
  formData.append('placa_veiculo', licensePlate)
  formData.append('custo_por_km', String(costPerKm))
  formData.append('custo_base', String(baseCost))
  formData.append('cor', color)
  formData.append('ano_fabricacao', String(year))
  formData.append('capacidade', String(capacity))

  // 2. Adiciona o arquivo apenas se ele não for nulo
  if (photo) {
    formData.append('foto', photo[0])
  }

  try {
    const response = await api.post('/veiculos/cadastrar_veiculo/', formData, {
      headers: {
        // Removemos o 'Content-Type': 'application/json'
        // O Axios gerencia o boundary do multipart automaticamente
        Authorization: `Bearer ${token}`,
      },
    })
    return response.data
  } catch (error: any) {
    console.error('Error:', error.response?.data || error.message)
    throw error
  }
}
