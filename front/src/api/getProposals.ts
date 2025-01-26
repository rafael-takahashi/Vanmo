import { api } from '@/lib/axios'

interface getProposalsBody {
  token: string | undefined
}

interface Proposal {
  email: string
  foto: string
  id: number
  tipo_conta: string
}

interface getProposalsResponse {
  data: Proposal[]
}

export async function getProposals({ token }: getProposalsBody) {
  const response = await api.get<getProposalsResponse>(
    '/propostas/buscar_propostas',
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )

  return response.data.data
}
