import { format } from 'date-fns'
import { useNavigate, useSearchParams } from 'react-router'

import garcia from '../assets/garcia.jpg'

export function SearchResults() {
  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams()
  const from = searchParams.get('from')
  const to = searchParams.get('to')
  const dateFrom = searchParams.get('dateFrom')
  const dateTo = searchParams.get('dateTo')
  const numberPassengers = searchParams.get('numberPassengers')

  async function handleNavigateSearchResult() {
    setSearchParams((state) => {
      if (from) {
        state.set('from', from)
      } else {
        state.delete('from')
      }

      if (to) {
        state.set('to', to)
      } else {
        state.delete('to')
      }

      if (dateFrom) {
        state.set('dateFrom', format(dateFrom, 'yyyy-MM-dd'))
      } else {
        state.delete('dateFrom')
      }

      if (dateTo) {
        state.set('dateTo', format(dateTo, 'yyyy-MM-dd'))
      } else {
        state.delete('dateTo')
      }

      if (numberPassengers) {
        state.set('numberPassengers', numberPassengers)
      } else {
        state.delete('numberPassengers')
      }

      navigate('/empresa/viacao+garcia')

      return state
    })
  }

  return (
    <div
      className="bg-white rounded-md p-4 flex cursor-pointer"
      onClick={() => handleNavigateSearchResult()}
    >
      <div className="w-[280px] h-[180px] overflow-hidden">
        <img
          src={garcia}
          alt=""
          className="w-full h-full object-cover object-center rounded-md"
        />
      </div>
      <div className="flex-1 ml-4">
        <h2 className="text-center text-xl font-bold">Viação Garcia</h2>

        <p className="text-primary-foreground">
          Endereço:{' '}
          <span className="text-primary font-semibold">Rua Teste XYZ</span>
        </p>

        <p className="text-primary-foreground mt-auto">
          Avaliação: <span className="text-primary font-semibold">4.5</span>
        </p>
      </div>
    </div>
  )
}
