import { useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'
import { useSearchParams } from 'react-router'

import { getTypeAccount } from '@/api/getTypeAccount'

import TableProposalsBusiness from './table-proposals-business'
import TableProposalsClient from './table-proposals-client'

export default function ProposalList() {
  const token = Cookies.get('auth_token')
  const [searchParams] = useSearchParams()
  const status = searchParams.get('status')

  const { data: user } = useQuery({
    queryKey: ['user', token],
    queryFn: async () => await getTypeAccount({ token }),
    enabled: !!token,
  })

  return (
    <div>
      {status === 'all' && (
        <h1 className="text-xl text-white">Todas Propostas</h1>
      )}

      {status === 'pendente' && (
        <h1 className="text-xl text-white">Propostas Pendentes</h1>
      )}

      {status === 'ativo' && (
        <h1 className="text-xl text-white">Propostas Ativos</h1>
      )}

      {status === 'rejeitado' && (
        <h1 className="text-xl text-white">Propostas Rejeitados</h1>
      )}

      {status === 'concluido' && (
        <h1 className="text-xl text-white">Propostas Concluídas</h1>
      )}

      <div className="flex flex-col gap-2 mt-4">
        {user?.tipo_usuario === 'cliente' && (
          <TableProposalsClient id_usuario={user?.id_usuario} status={status} />
        )}

        {user?.tipo_usuario === 'empresa' && (
          <TableProposalsBusiness
            id_usuario={user?.id_usuario}
            status={status}
          />
        )}
      </div>
    </div>
  )
}
