import Cookies from 'js-cookie'

import { api } from '@/lib/axios'

export interface registerClientBody {
  email: string
  password: string
  fullName: string
  typeAccount: 'cliente' | 'empresa'
  cpf: string
  dateOfBirth: Date
  phone: string
}

export async function registerClient({
  email,
  password,
  fullName,
  typeAccount,
  cpf,
  dateOfBirth,
  phone,
}: registerClientBody) {
  const response = await api.post('/usuario/cadastro/cliente', {
    email,
    senha: password,
    nome_completo: fullName,
    tipo_conta: typeAccount,
    cpf,
    data_nascimento: dateOfBirth,
    telefone: phone,
  })

  const token = response.data.access_token

  Cookies.set('auth_token', token, {
    expires: 7,
    secure: true,
    sameSite: 'strict',
  })
}
