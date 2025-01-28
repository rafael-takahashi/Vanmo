import { api } from '@/lib/axios'

interface getUserProposalsBody {
  status_aluguel?: string | null
  token: string | undefined
}

export async function getUserProposals({ status_aluguel, token }: getUserProposalsBody) {
  try {
    const url = status_aluguel
      ? `/propostas/buscar_propostas/${status_aluguel}`
      : '/propostas/buscar_propostas'

    const response = await api.get(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    console.log(response.data)
    return response.data
  } catch (error: any) {
    console.error('Error:', error.response?.data || error.message)
    throw error
  }
}
