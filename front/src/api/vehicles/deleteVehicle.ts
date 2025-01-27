import { api } from '@/lib/axios'

interface deleteVehicleBody {
  id_veiculo: number
  token: string | undefined
}

export async function deleteVehicle({ id_veiculo, token }: deleteVehicleBody) {
  try {
    const response = await api.delete(`/veiculos/apagar_veiculo/${id_veiculo}`, {
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
