import { MapPin, Phone, Star } from '@phosphor-icons/react'
import { format } from 'date-fns'
import { useNavigate, useSearchParams } from 'react-router'

import garcia from '../assets/garcia.jpg'

interface Endereco {
  bairro: string
  cep: string
  cidade: string
  numero: string
  rua: string
  uf: string
}

interface SearchResultsProps {
  idBusiness: number
  fantasyName: string
  rate: number
  phone: string
  address: Endereco
  photo: string
}

export function SearchResults({
  address,
  fantasyName,
  idBusiness,
  phone,
  photo,
  rate,
}: SearchResultsProps) {
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

      navigate(`/empresa/${idBusiness}`)

      return state
    })
  }

  return (
    <div
      className="bg-white w-[280px] rounded-md flex flex-col cursor-pointer shadow-lg pb-6"
      onClick={() => handleNavigateSearchResult()}
    >
      <div className="w-full h-[180px] overflow-hidden">
        <img
          src={garcia}
          alt=""
          className="w-full h-full object-cover object-center rounded-md shadow-lg"
        />
      </div>
      <h2 className="text-center text-2xl font-semibold mt-3">{fantasyName}</h2>
      <div className="flex flex-col ml-2 text-base">
        <div className="flex gap-1 items-center mt-1">
          <MapPin size={20} weight="fill" />
          <span>
            {address.cidade}-{address.uf}
          </span>
        </div>
        <div className="flex gap-1 items-center mt-1">
          <Phone size={20} weight="fill" />
          <span>{phone}</span>
        </div>
        <div className="flex gap-1 items-center mt-1">
          Avaliação: {rate}
          <Star size={20} weight="fill" color="yellow" />
        </div>
      </div>
    </div>
  )
}
