import Cookies from 'js-cookie'
import { useNavigate } from 'react-router'
import { useQuery } from '@tanstack/react-query'

import { getTypeAccount } from '../api/getTypeAccount'
import garcia from '../assets/garcia.jpg'
import { Button } from './ui/button'

interface VehicleBoxProps {
  ano_fabricacao: number
  capacidade: number
  cor: string
  custo_base: number
  custo_por_km: number
  id_veiculo: number
  id_empresa: number
  nome_veiculo: string
  placa_veiculo: string
  custo_da_viagem: number
  proposal: object
}

export function VehicleBox({
  ano_fabricacao,
  capacidade,
  cor,
  custo_base,
  custo_da_viagem,
  custo_por_km,
  id_empresa,
  id_veiculo,
  nome_veiculo,
  placa_veiculo,
  proposal,
}: VehicleBoxProps) {
  const token = Cookies.get('auth_token')
  
  const { data } = useQuery({
    queryKey: ['user', token],
    queryFn: async () => await getTypeAccount({ token }),
    enabled: !!token,
  })

  const navigate = useNavigate()

  const valorFormatado = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(custo_da_viagem)

  const handleProposalButtonClick = () => {
    navigate('/proposta', {
      state: { id_empresa, id_veiculo, proposal },
    })
  }

  return (
    <div className="bg-white rounded-md p-4 flex shadow-lg">
      <div className="w-[280px] h-[180px] overflow-hidden">
        <img
          src={garcia}
          alt=""
          className="w-full h-full object-cover object-center rounded-md "
        />
      </div>
      <div className="flex-1 flex flex-col ml-4">
        <h2 className="text-center text-xl font-bold">{nome_veiculo}</h2>

        <p className="text-primary-foreground">
          Cor: <span className="text-primary font-semibold">{cor}</span>
        </p>

        <p className="text-primary-foreground">
          Ano:{' '}
          <span className="text-primary font-semibold">{ano_fabricacao}</span>
        </p>

        <p className="text-primary-foreground">
          Capacidade:{' '}
          <span className="text-primary font-semibold">{capacidade}</span>
        </p>

        <p className="text-primary-foreground">
          Valor base para a viagem:{' '}
          <span className="text-primary font-semibold">{valorFormatado}</span>
        </p>

        <Button
          className="mt-auto h-8 flex justify-center items-center text-sm font-semibold self-end shadow-lg"
          onClick={handleProposalButtonClick}
          disabled={data?.tipo_usuario === 'cliente' ? false : true}
        >
          Proposta
        </Button>
      </div>
    </div>
  )
}
