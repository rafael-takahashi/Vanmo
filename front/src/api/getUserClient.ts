import { api } from '@/lib/axios'
interface getUserClientBody {
  token: string | undefined
}

interface getUserClientResponse {
  cpf: string
  data_nascimento: string
  email: string
  foto: string
  id: number
  nome_completo: string
  telefone: string
  tipo_conta: string
}

export async function getUserClient({ token }: getUserClientBody) {
  const response = await api.get<getUserClientResponse>(
    '/usuario/buscar_dados_cadastrais/cliente',
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )

  return response.data
}
