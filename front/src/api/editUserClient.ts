import { api } from '@/lib/axios'

export interface editProfileUserClientBody {
  email?: string
  password?: string
  photo?: FileList
  token?: string
}

export async function editProfileUserClient({
  email,
  password,
  photo,
  token,
}: editProfileUserClientBody) {
  await api.put(
    '/usuario/alterar_dados',
    {
      email,
      senha: password,
      foto: photo,
    },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )
}
