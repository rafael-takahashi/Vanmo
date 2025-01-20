import { api } from '@/lib/axios'

export interface registerBody {
  typeAccount: 'empresa' | 'cliente'
  fullName: string
  cpf: string
  email: string
  phone: string
  password: string
}

export async function register({
  fullName,
  typeAccount,
  email,
  cpf,
  phone,
  password,
}: registerBody) {
  await api
    .post('/usuario/registrar', {
      email,
      password,
      typeAccount,
    })
    .then(() => {
      console.log('deu certo')
    })
}
