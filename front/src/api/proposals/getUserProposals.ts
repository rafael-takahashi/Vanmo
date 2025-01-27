import { api } from '@/lib/axios'

interface getUserProposalsBody {
  token: string | undefined
}

export async function getUserProposals({ token }: getUserProposalsBody) {
  try {
    const response = await api.get('/propostas/buscar_propostas', {
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
