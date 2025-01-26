import { api } from '@/lib/axios'

interface getProposalDataBody {
  idProposal: string
  token: string | undefined
}

interface getProposalDataResponse {
  email: string
  foto: string
  id: number
  tipo_conta: string
}

export async function getProposalData({
  idProposal,
  token,
}: getProposalDataBody) {
  const response = await api.get<getProposalDataResponse>(
    '/propostas/buscar_dados_proposta',
    {
      params: {
        id_proposta: idProposal,
      },
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )

  return response.data
}
