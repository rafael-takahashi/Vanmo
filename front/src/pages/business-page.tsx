import { MapPin } from '@phosphor-icons/react'
import { useQuery } from '@tanstack/react-query'
import { useSearchParams } from 'react-router'

import { getDataBusiness } from '@/api/getDataBusiness'
import SearchArea from '@/components/search-area'
import { VehicleList } from '@/components/vehicle-list'

export default function BusinessPage() {
  const [searchParams] = useSearchParams()
  const from = searchParams.get('from')
  const to = searchParams.get('to')
  const dateFrom = searchParams.get('dateFrom')
  const dateTo = searchParams.get('dateTo')
  const numberPassengers = searchParams.get('numberPassengers')

  const idBusiness = window.location.pathname.split('/').filter(Boolean).pop()

  const { data } = useQuery({
    queryKey: ['idBusiness', idBusiness],
    queryFn: () => getDataBusiness({ idEmpresa: idBusiness }),
  })

  return (
    <main className=" flex flex-col mt-14">
      <h1 className="text-3xl font-bold">Viacao Garcia</h1>
      <div className="flex mt-2">
        <MapPin size={24} weight="bold" />

        <span>Rua XYZ, 123, Maringá-PR, CEP 12345-123, Brasil</span>

        <span className="ml-auto">
          Avaliação: <span className="text-primary font-bold">4.7</span>
        </span>
      </div>

      <SearchArea />

      <div className="mt-6">
        <span className="text-2xl font-bold text-primary-foreground">
          VEÍCULOS DISPONÍVEIS
        </span>
        {from && (
          <span className="ml-6 text-primary-foreground font-semibold">
            Partida:{` `}
            <span className="text-primary">{from}</span>, Destino:{` `}{' '}
            <span className="text-primary">{to}</span>, Data de ida:{` `}{' '}
            <span className="text-primary">{dateFrom}</span>, Data de retorno:
            {` `} <span className="text-primary">{dateTo}</span>, Passageiros:
            {` `} <span className="text-primary">{numberPassengers}</span>
          </span>
        )}
      </div>

      <VehicleList />
    </main>
  )
}
