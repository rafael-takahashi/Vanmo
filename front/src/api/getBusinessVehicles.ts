import { api } from '@/lib/axios'

export async function getBusinessVehicles(id_empresa: number | undefined) {
  try {
    const response = await api.get(`/veiculos/buscar_veiculos_empresa/${id_empresa}`)
    return response.data
  } catch (error: any) {
    console.error('Error:', error.response?.data || error.message)
    throw error
  }
}
