import Cookies from 'js-cookie'

import { api } from '@/lib/axios'

interface getUserProposalsBody {
  status_aluguel?: string | null
}

export async function getUserProposals({
  status_aluguel,
}: getUserProposalsBody) {
  try {
    const token = Cookies.get('auth_token')

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
