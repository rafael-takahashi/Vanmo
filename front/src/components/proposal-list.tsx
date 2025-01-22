import { useSearchParams } from 'react-router'

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

export default function ProposalList() {
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
        <ProposalItem />
        <ProposalItem />
        <ProposalItem />

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
      </div>
    </div>
  )
}
