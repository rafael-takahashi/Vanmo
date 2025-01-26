import Cookies from 'js-cookie'

import { api } from '@/lib/axios'

interface handleProposalBody {
  idProposal: string
  state: boolean
  token: string | undefined
}

export async function signIn({ idProposal, state, token }: handleProposalBody) {
  const response = await api.post(
    '/propostas/aceitar_ou_rejeitar_proposta',
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
}
