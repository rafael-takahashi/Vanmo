import { MapPin } from '@phosphor-icons/react'
import { useSearchParams } from 'react-router'

import SearchArea from '@/components/search-area'

export default function BusinessPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const from = searchParams.get('from')
  const to = searchParams.get('to')
  const dateFrom = searchParams.get('dateFrom')
  const dateTo = searchParams.get('dateTo')
  const numberPassengers = searchParams.get('numberPassengers')

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
        {searchParams && (
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
    </main>
  )
}
