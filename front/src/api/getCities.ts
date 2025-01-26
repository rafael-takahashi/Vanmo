import { api } from '@/lib/axios'

export async function getCities() {
  const response = await api.get('/cidades/lista_de_cidades')

  return response.data
}
