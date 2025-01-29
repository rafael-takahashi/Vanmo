import { useQuery } from '@tanstack/react-query'
import { useSearchParams } from 'react-router'

import { fetchBusinessByFilters } from '@/api/fetchBusinessByFilters'

import { SearchResults } from './search-results-box'
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from './ui/pagination'

export function Results() {
  const [searchParams] = useSearchParams()
  const from = searchParams.get('from') || ''
  const dateFrom = searchParams.get('dateFrom') || ''
  const numberPassengers = searchParams.get('numberPassengers') || ''

  const { data } = useQuery({
    queryKey: ['results', from, dateFrom, numberPassengers],
    queryFn: () =>
      fetchBusinessByFilters({
        data_de_partida: dateFrom,
        local_partida: from,
        pagina: 1,
        qtd_passageiros: numberPassengers,
      }),
  })

  return (
    <div className="w-full grid grid-cols-4 gap-3 mt-8">
      {data?.map((empresa) => (
        <SearchResults
          address={empresa.endereco}
          fantasyName={empresa.nome_fantasia}
          idBusiness={empresa.id_usuario}
          phone={empresa.telefone}
          rate={empresa.soma_avaliacoes}
          key={empresa.id_usuario}
          photo={empresa.foto}
        />
      ))}

      {Array.isArray(data) && data.length > 10 && (
        <Pagination className="col-span-2 mt-4">
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
      )}
    </div>
  )
}
