import { api } from '@/lib/axios'
interface getUserBusinessBody {
  token: string | undefined
}

interface getUserBusinessResponse {
  email: string
  foto: string
  id: number
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
