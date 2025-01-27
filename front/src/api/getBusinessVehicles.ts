import { api } from '@/lib/axios'

export async function getBusinessVehicles(businessId: number | undefined) {
  try {
    const response = await api.get('/veiculos/buscar_veiculos_empresa', {
      params: {
        id_empresa: businessId,
      },
    })
    return response.data
  } catch (error: any) {
    console.error('Error:', error.response?.data || error.message)
    throw error
  }
}
