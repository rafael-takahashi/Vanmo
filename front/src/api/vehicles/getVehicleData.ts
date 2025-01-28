import { api } from '@/lib/axios'

interface getVehicleDataBody {
  idVehicle: string
  token: string | undefined
}

export async function getVehicleData({
  idVehicle,
  token,
}: getVehicleDataBody) {
  try {
    const response = await api.get(
      `/veiculos/buscar_dados_veiculo/${idVehicle}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )
    return response.data
  } catch (error: any) {
    console.error('Error:', error.response?.data || error.message)
    throw error
  }
}
