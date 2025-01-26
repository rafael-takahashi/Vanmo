import { api } from '@/lib/axios'

export interface editProfileUserClientBody {
  email?: string
  password?: string
  photo?: FileList
  fullName?: string
  dateOfBirth?: string
  phone?: string
  token?: string
}

export async function editProfileUserClient({
  email,
  password,
  photo,
  fullName,
  dateOfBirth,
  phone,
  token,
}: editProfileUserClientBody) {
  await api.put(
    '/usuario/alterar_dados/cliente',
    {
      email,
      senha: password,
      foto: photo,
      nome_completo: fullName,
      data_nascimento: dateOfBirth,
      telefone: phone,
    },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )
}
