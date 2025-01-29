import Cookies from 'js-cookie'

import { api } from '@/lib/axios'

import { Endereco } from '../fetchBusinessByName'
import { Vehicles } from '../vehicles/getBusinessVehicles'

interface getUserProposalsBody {
  status_aluguel?: string | null
}

interface Cliente {
  cpf: string
  data_nascimento: string
  email: string
  foto: string
  id_usuario: number
  nome_completo: string
  senha_hashed: string
  telefone: string
  tipo_conta: string
}

interface Local {
  id_local: number
  latitude: number
  longitude: number
  nome: string
}

interface Empresa {
  cnpj: string
  email: string
  endereco: Endereco
  foto: string
  id_usuario: number
  local: Local
  nome_fantasia: string
  num_avaliacoes: number
  senha_hashed: string
  soma_avaliacoes: number
  telefone: string
  tipo_conta: string
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
  valor_total: 0
}

interface Proposals {
  proposta: Proposal
  veiculo: Vehicles
}

export async function getUserProposals({
  status_aluguel,
}: getUserProposalsBody): Promise<Proposals[]> {
  try {
    const token = Cookies.get('auth_token')

    const response = await api.get(
      `/propostas/buscar_propostas/${status_aluguel}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    )

    return response.data
  } catch (error: any) {
    console.error('Error:', error.response?.data || error.message)
    throw error
  }
}
