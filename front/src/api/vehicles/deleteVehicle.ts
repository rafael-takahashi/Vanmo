import Cookies from 'js-cookie'

import { api } from '@/lib/axios'

interface deleteVehicleBody {
  id_veiculo: number
}

export async function deleteVehicle({ id_veiculo }: deleteVehicleBody) {
  try {
    const token = Cookies.get('auth_token')

    const response = await api.delete(
      `/veiculos/apagar_veiculo/${id_veiculo}`,
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
