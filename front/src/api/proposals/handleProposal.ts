import { api } from '@/lib/axios'

interface handleProposalBody {
  idProposal: number
  state: boolean
  token: string | undefined
}

export async function handleProposal({
  idProposal,
  state,
  token,
}: handleProposalBody) {
  try {
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
