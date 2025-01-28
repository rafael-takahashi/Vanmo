import { MapPin, Phone } from '@phosphor-icons/react'
import { useQuery } from '@tanstack/react-query'
import { useSearchParams } from 'react-router'

import { getDataBusiness } from '@/api/getDataBusiness'
import SearchArea from '@/components/search-area'
import { VehicleList } from '@/components/vehicle-list'
import { Separator } from '@/components/ui/separator'

export default function BusinessPage() {
  const [searchParams] = useSearchParams()
  const from = searchParams.get('from') || '';
  const to = searchParams.get('to') || '';
  const dateFrom = searchParams.get('dateFrom') || '';
  const dateTo = searchParams.get('dateTo') || '';
  const numberPassengers = searchParams.get('numberPassengers') || '';

  const idBusiness = window.location.pathname.split('/').filter(Boolean).pop() || ''

  const { data: dataBusiness, isSuccess: isSucessBusiness } = useQuery({
    queryKey: ['idBusiness', idBusiness],
    queryFn: () => getDataBusiness({ idEmpresa: idBusiness }),
  })

  return (
    <>
      {isSucessBusiness ? (
        <main className="flex flex-col mt-14">
          <h1 className="text-3xl font-bold">{dataBusiness.nome_fantasia}</h1>
          <div className="flex mt-2 gap-1">
            <MapPin size={20} weight="bold" />

            <span>
              {dataBusiness.endereco.rua}, {dataBusiness.endereco.numero},{' '}
              {dataBusiness.endereco.bairro}, CEP {dataBusiness.endereco.cep},{' '}
              {dataBusiness.endereco.cidade}-{dataBusiness.endereco.uf}
            </span>

            <span className="ml-auto">
              Avaliação:{' '}
              <span className="text-primary font-bold">
                {dataBusiness.avaliacao}
              </span>
            </span>
          </div>
          <div className="flex gap-1 mt-2">
            <Phone size={20} />
            <span className="underline">{dataBusiness.telefone}</span>
          </div>

          <div className="mt-2">
            <SearchArea />
          </div>

          <div className="mt-6">
            <span className="text-2xl font-bold text-primary-foreground">
              VEÍCULOS DISPONÍVEIS
            </span>

            
            {from && (
              <span className="ml-6 text-primary-foreground font-semibold">
                Partida:{` `}
                <span className="text-primary">{from}</span>, Destino:{` `}{' '}
                <span className="text-primary">{to}</span>, Data de ida:{` `}{' '}
                <span className="text-primary">{dateFrom}</span>, Data de
                retorno:
                {` `} <span className="text-primary">{dateTo}</span>,
                Passageiros:
                {` `} <span className="text-primary">{numberPassengers}</span>
              </span>
            )}
          </div>

          <Separator className="my-4" />

          <VehicleList />
        </main>
      ) : (
        <h2 className="text-2xl text-primary font-bold flex items-center justify-center">
          Erro ao carregar a página
        </h2>
      )}
    </>
  )
}
