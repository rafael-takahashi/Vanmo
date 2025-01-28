import Cookies from 'js-cookie'
import { useState } from 'react'
import { useSearchParams } from 'react-router'
import { useQuery } from '@tanstack/react-query'

import ProposalItem from './proposal-item'
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from './ui/pagination'
import { getUserProposals } from '@/api/proposals/getUserProposals'
import { getTypeAccount } from '@/api/getTypeAccount'

export default function ProposalList() {
  
  const token = Cookies.get('auth_token')

  const { data: user } = useQuery({
    queryKey: ['user', token],
    queryFn: async () => await getTypeAccount({ token }),
    enabled: !!token,
  })

  const [proposals, setProposals] = useState<any[]>([])

  const fetchAndSetProposals = async () => {
    setProposals(await getUserProposals({ token }))
  }

  useState(() => {
    fetchAndSetProposals()
  },)

  console.log(proposals)

  const [searchParams] = useSearchParams()

  const status = searchParams.get('status')

  return (
    <div>
      {status === 'all' && (
        <h1 className="text-xl text-white">Minhas Propostas</h1>
      )}

      {status === 'active' && (
        <h1 className="text-xl text-white">Minhas Propostas Ativas</h1>
      )}

      {status === 'rejected' && (
        <h1 className="text-xl text-white">Minhas Propostas Rejeitadas</h1>
      )}

      {status === 'done' && (
        <h1 className="text-xl text-white">Minhas Propostas Concluídas</h1>
      )}

      <div className="flex flex-col gap-2 mt-4">
        {proposals && proposals.length > 0 ? (
          <>
          {proposals.map((proposal: any) => (
            <ProposalItem proposal={proposal} key={proposal.id} type={user?.tipo_usuario} />
          ))}
            <Pagination className="col-span-2 mt-4 text-white">
            <PaginationContent>
              <PaginationItem>
                <PaginationPrevious href="#" />
              </PaginationItem>
              <PaginationItem>
                <PaginationLink href="#">1</PaginationLink>
                <PaginationLink href="#">2</PaginationLink>
              </PaginationItem>
              <PaginationItem>
                <PaginationEllipsis />
              </PaginationItem>
              <PaginationItem>
                <PaginationNext href="#" />
              </PaginationItem>
            </PaginationContent>
          </Pagination>
          </>
        ) : (
          <p className="text-white ">Não foram encontradas propostas.</p>
        )}
      </div>
    </div>
  )
}
