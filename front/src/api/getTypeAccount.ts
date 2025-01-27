import { api } from '@/lib/axios'
interface getTypeAccountHeader {
  token: string | undefined
}

interface getTypeAccountResponse {
  tipo_usuario: string
}

export async function getTypeAccount({ token }: getTypeAccountHeader) {
  const response = await api.get<getTypeAccountResponse>(
    '/usuario/verifica_tipo_usuario',
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )
  return response.data
}
