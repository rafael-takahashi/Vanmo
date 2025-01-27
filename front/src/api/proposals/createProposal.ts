import { api } from '@/lib/axios'

/*
    Exemplo de de data:
    const tsDate = new Date()

    // Get the ISO string from the Date object
    const isoString = tsDate.toISOString() // Returns a string like "2025-01-27T15:30:00.000Z"

    // Now you can safely use split on the string
    const dateOnly = isoString.split('T')[0] // "2025-01-27"
  
*/

interface createProposalBody {
  id_empresa: number
  id_veiculo: number
  cidade_saida: string
  cidade_chegada: string
  distancia_extra_km: number
  data_saida: string // Make sure Date is converted to ISO8601 before sending to FastAPI
  data_chegada: string // .toISOString()
  token: string | undefined
}

export async function createProposal({
  id_empresa,
  id_veiculo,
  cidade_saida,
  cidade_chegada,
  distancia_extra_km,
  data_saida,
  data_chegada,
  token,
}: createProposalBody) {
  const jsonBody = JSON.stringify({
    id_empresa,
    id_veiculo,
    cidade_saida,
    cidade_chegada,
    distancia_extra_km,
    data_saida,
    data_chegada,
  })
  try {
    const response = await api.post(`/propostas/criar_proposta/`, jsonBody, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
    })
    return response.data
  } catch (error: any) {
    console.error('Error:', error.response?.data || error.message)
    throw error
  }
}
