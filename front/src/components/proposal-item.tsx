import Cookies from 'js-cookie'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { getVehicleData } from '@/api/vehicles/getVehicleData'

interface Cliente {
  cpf: string
  data_nascimento: string
  email: string
  nome_completo: string
  telefone: string
}

interface Empresa {
  cnpj: string
  email: string
  telefone: string
  nome_fantasia: string
}

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
  id_cliente: Cliente
  id_empresa: Empresa
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

            {proposal.id_empresa &&
            <p>
              Empresa: <span>{proposal.id_empresa.nome_fantasia}</span>
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

            <p>
              Nome Completo: <span>{proposal.id_cliente.nome_completo}</span>
            </p>
            <p>
              Email: <span>{proposal.id_cliente.email}</span>
            </p>
            <p>
              Data de Nascimento: <span>{new Date(proposal.id_cliente.data_nascimento).toLocaleDateString('pt-BR')}</span>
            </p>
            <p>
              CPF: <span>{proposal.id_cliente.cpf}</span>
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
