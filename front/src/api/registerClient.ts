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
  await api.post('/usuario/registrar', {
    email,
    senha: password,
    tipo_conta: typeAccount,
  })
}
