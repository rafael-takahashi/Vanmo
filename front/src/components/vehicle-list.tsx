import { useQuery } from '@tanstack/react-query'
import { useSearchParams } from 'react-router'

import { fetchVehiclesByFilters } from '@/api/fetchVehiclesByFilters'

import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from './ui/pagination'
import { VehicleBox } from './vehicle-box'

export function VehicleList() {
  const [searchParams] = useSearchParams()
  const from = searchParams.get('from') || ''
  const to = searchParams.get('to') || ''
  const dateFrom = searchParams.get('dateFrom') || ''
  const dateTo = searchParams.get('dateTo') || ''
  const numberPassengers = searchParams.get('numberPassengers') || ''

  const idBusiness =
    window.location.pathname.split('/').filter(Boolean).pop() || ''

  const { data } = useQuery({
    queryKey: ['vehicles', { from, to, dateFrom, dateTo, numberPassengers }],
    queryFn: () =>
      fetchVehiclesByFilters({
        data_de_chegada: dateTo,
        data_de_partida: dateFrom,
        id_empresa: idBusiness,
        local_chegada: to,
        local_saida: from,
        qtd_passageiros: numberPassengers,
        pagina: 1,
      }),
    enabled: !!from && !!to && !!dateFrom && !!dateTo && !!numberPassengers,
  })

  return (
    <>
      {data && data.length > 0 ? (
        <div className="w-full grid grid-cols-2 gap-3 mt-4">
          {data.map((car) => (
            <VehicleBox
              key={car.id_veiculo}
              ano_fabricacao={car.ano_fabricacao}
              capacidade={car.capacidade}
              cor={car.cor}
              custo_base={car.custo_base}
              custo_da_viagem={car.custo_da_viagem}
              custo_por_km={car.custo_por_km}
              id_empresa={car.id_empresa}
              id_veiculo={car.id_veiculo}
              nome_veiculo={car.nome_veiculo}
              placa_veiculo={car.placa_veiculo}
              proposal={{ from, to, dateFrom, dateTo, numberPassengers }}
            />
          ))}
        </div>
      ) : (
        <>
          <p className="w-full text-center text-primary-foreground mt-4 text-xl">
            Nenhum veículo encontrado.
          </p>
          <p className="w-full text-center text-primary-foreground mt-4 text-xl">
            Tente novamente inserir os filtros.
          </p>
        </>
      )}

      {Array.isArray(data) && data.length > 6 && (
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
    </>
  )
}
