import { api } from '@/lib/axios'

export interface editVehicleBody {
  token: string | undefined
  id: number
  name: string
  licensePlate: string
  costPerKm: number
  baseCost: number
  color: string
  year: number
  capacity: number
  photo?: FileList
}

export async function editVehicle({
  token,
  id,
  name,
  licensePlate,
  costPerKm,
  baseCost,
  color,
  year,
  capacity,
  photo,
}: editVehicleBody) {
  const formData = new FormData()

  formData.append('id_veiculo', String(id))
  formData.append('nome_veiculo', name)
  formData.append('placa_veiculo', licensePlate)
  formData.append('custo_por_km', String(costPerKm))
  formData.append('custo_base', String(baseCost))
  formData.append('cor', color)
  formData.append('ano_fabricacao', String(year))
  formData.append('capacidade', String(capacity))

  if (photo && photo[0]) {
    formData.append('foto', photo[0])
  }

  try {
    const response = await api.put('/veiculos/editar_veiculo', formData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    return response.data
  } catch (error: any) {
    console.error('Error:', error.response?.data || error.message)
    throw error
  }
}
