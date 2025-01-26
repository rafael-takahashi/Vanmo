import { api } from '@/lib/axios'
interface getUserClientBody {
  token: string | undefined
}

interface getUserClientResponse {
  email: string
  foto: string
  id: number
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
