import { api } from '@/lib/axios'
interface getUserBusinessBody {
  token: string | undefined
}

interface Endereco {
  bairro: string
  cep: string
  cidade: string
  numero: string
  rua: string
  uf: string
  id: number
}

interface getUserBusinessResponse {
  cnpj: string
  email: string
  endereco: Endereco
  foto: string
  id_usuario: number
  nome_fantasia: string
  num_avaliacoes: number
  soma_avaliacoes: number
  telefone: string
  tipo_conta: string
}

export async function getUserBusiness({ token }: getUserBusinessBody) {
  const response = await api.get<getUserBusinessResponse>(
    '/usuario/buscar_dados_cadastrais/empresa',
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )

  return response.data
}
