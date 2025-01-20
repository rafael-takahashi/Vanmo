import { useSearchParams } from 'react-router'

import { Results } from '@/components/results'
import SearchArea from '@/components/search-area'

export default function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const from = searchParams.get('from')
  const to = searchParams.get('to')
  const dateFrom = searchParams.get('dateFrom')
  const dateTo = searchParams.get('dateTo')
  const numberPassengers = searchParams.get('numberPassengers')

  return (
    <main>
      <SearchArea />

      <div className="ml-8 mt-6">
        <span className="text-2xl font-bold text-primary-foreground">
          Resultados da busca
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

      <Results />
    </main>
  )
}
