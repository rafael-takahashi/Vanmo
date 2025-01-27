import { api } from '@/lib/axios'

interface getProposalDataBody {
  idProposal: number
  token: string | undefined
}

export async function getProposalData({
  idProposal,
  token,
}: getProposalDataBody) {
  try {
    const response = await api.get(
      `/propostas/buscar_dados_proposta/${idProposal}`,
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
