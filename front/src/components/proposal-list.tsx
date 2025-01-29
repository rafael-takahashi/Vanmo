import { useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'
import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router'

import { getTypeAccount } from '@/api/getTypeAccount'
import { getUserProposals } from '@/api/proposals/getUserProposals'

import ProposalItem from './proposal-item'
import TableProposalsBusiness from './table-proposals-business'
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from './ui/pagination'

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

      {status === 'pending' && (
        <h1 className="text-xl text-white">Propostas Pendentes</h1>
      )}

      {status === 'active' && (
        <h1 className="text-xl text-white">Propostas Ativos</h1>
      )}

      {status === 'rejected' && (
        <h1 className="text-xl text-white">Propostas Rejeitados</h1>
      )}

      {status === 'done' && (
        <h1 className="text-xl text-white">Propostas Concluídas</h1>
      )}

      <div className="flex flex-col gap-2 mt-4">
        <TableProposalsBusiness id_usuario={user?.id_usuario} status={status} />
      </div>
    </div>
  )
}
