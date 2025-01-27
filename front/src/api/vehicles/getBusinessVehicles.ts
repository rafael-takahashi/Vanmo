import { api } from '@/lib/axios'

export async function getBusinessVehicles(id_empresa: number | undefined, pagina: number) {
  try {
    const response = await api.get(`/veiculos/buscar_veiculos_empresa/${id_empresa}/${pagina}`)
    return response.data
  } catch (error: any) {
    console.error('Error:', error.response?.data || error.message)
    throw error
  }
}
