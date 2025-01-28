import Cookies from 'js-cookie'
import { useQuery } from '@tanstack/react-query'
import { getDataBusiness } from '@/api/getDataBusiness'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { getVehicleData } from '@/api/vehicles/getVehicleData'
import { getUserClient } from '@/api/getUserClient'

interface Local {	
  id_local: number
  latitude: number
  longitude: number
  nome: string
}

interface Proposal {
  data_fim: string
  data_inicio: string
  distancia_extra: number
  distancia_trajeto: number
  estado_aluguel: string
  id_aluguel: number
  id_cliente: number
  id_empresa: number
  id_veiculo: number
  local_chegada: Local
  local_partida: Local
  valor_total: number
}

interface ProprosalItemProps {
  proposal: Proposal
  type: string | undefined
}

export default function ProposalItem({ proposal, type }: ProprosalItemProps) {

  const token = Cookies.get('auth_token')

  const { data: dataBusiness, isSuccess: isSucessBusiness } = useQuery({
    queryKey: ['idBusiness', proposal.id_empresa],
    queryFn: () => getDataBusiness({ idEmpresa: proposal.id_empresa.toString() }),
  })

  const { data: dataVehicle, isSuccess: isSucessVehicle } = useQuery({
    queryKey: ['idVehicle', proposal.id_veiculo],
    queryFn: () => getVehicleData({ idVehicle: proposal.id_veiculo.toString(), token }),
  })

  return (
    <Card className="bg-white rounded-md">
      <CardHeader>
        <CardTitle className="flex justify-between text-xl">
          <span>{proposal.id_aluguel}</span>

          {
          proposal.estado_aluguel == "ativo" &&
          <span className="text-green-500">ATIVO</span>
          }
          {
          proposal.estado_aluguel == "proposto" &&
          <span className="text-yellow-500">PROPOSTO</span>
          }
          {
          proposal.estado_aluguel == "rejeitado" &&
          <span className="text-red-500">REJEITADO</span>
          }
        </CardTitle>
      </CardHeader>
      <CardContent className="grid grid-cols-2">
        {type === 'cliente' && (
          <div>
            <h3 className="text-center font-semibold">
              Informações da Empresa
            </h3>

            {isSucessBusiness &&
            <p>
              Empresa: <span>{dataBusiness?.nome_fantasia}</span>
            </p>
            }
            {isSucessVehicle &&
            <>
              <p>
                Veículo: <span>{dataVehicle.nome_veiculo}</span>
              </p>
              <p>
                Ano: <span>{dataVehicle.ano_fabricacao}</span>
              </p>
              <p>
                Passageiros: <span>{dataVehicle.capacidade}</span>
              </p>
            </>
            }
          </div>
        )}

        {type === 'empresa' && (
          <div>
            <h3 className="text-center font-semibold">
              Informações do Cliente
            </h3>
            {/*Alterar para dados reais do cliente*/}
            <p>
              Nome Completo: <span>John Doe</span>
            </p>
            <p>
              Email: <span>johndoe@example.com</span>
            </p>
            <p>
              Data de Nascimento: <span>01/01/2000</span>
            </p>
            <p>
              CPF: <span>12312312312</span>
            </p>
          </div>
        )}

        <div>
          <h3 className="text-center font-semibold">Informações da Viagem</h3>
          <p>
            Partida: <span>{proposal.local_partida.nome}</span>
          </p>
          <p>
            Destino: <span>{proposal.local_chegada.nome}</span>
          </p>
          <p>
            Data de ida: <span>{proposal.data_inicio}</span>
          </p>
          <p>
            Data de retorno: <span>{proposal.data_fim}</span>
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
