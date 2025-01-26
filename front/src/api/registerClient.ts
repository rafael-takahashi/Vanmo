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
  await api.post('/usuario/cadastro/cliente', {
    email,
    senha: password,
    nome_completo: fullName,
    tipo_conta: typeAccount,
    cpf,
    data_nascimento: dateOfBirth,
    telefone: phone,
  })
}
