import { api } from '@/lib/axios'

interface getProposalsBody {
  token: string | undefined
}

interface getProposalsResponse {
  email: string
  foto: string
  id: number
  tipo_conta: string
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

  return response.data
}
