import Cookies from 'js-cookie'

import { api } from '@/lib/axios'

interface handleProposalBody {
  idProposal: number
  state: boolean
}

export async function handleProposal({
  idProposal,
  state,
}: handleProposalBody) {
  try {
    const token = Cookies.get('auth_token')

    const response = await api.post(
      '/propostas/aceitar_ou_rejetar_proposta',
      {
        id_proposta: idProposal,
        opcao: state,
      },
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
