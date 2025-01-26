import Cookies from 'js-cookie'

import { api } from '@/lib/axios'

export interface registerClientBody {
  fullName: string
  cpf: string
  email: string
  phone: string
  password: string
  typeAccount: 'cliente' | 'empresa'
}

export async function registerClient({
  fullName,
  email,
  cpf,
  phone,
  password,
  typeAccount,
}: registerClientBody) {
  const response = await api.post('/usuario/registrar', {
    email,
    senha: password,
    tipo_conta: typeAccount,
  })

  const token = response.data.access_token

  Cookies.set('auth_token', token, {
    expires: 7,
    secure: true,
    sameSite: 'strict',
  })
}
