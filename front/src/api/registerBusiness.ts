import { api } from '@/lib/axios'

export interface registerBusinessBody {
  typeAccount: 'cliente' | 'empresa'
  fantasyName: string
  cnpj: string
  email: string
  phone: string
  cep: string
  cityAddress: string
  stateAddress: string
  streetAddress: string
  numberAddress: string
  password: string
}

export async function registerBusiness({
  cep,
  cityAddress,
  cnpj,
  email,
  fantasyName,
  numberAddress,
  password,
  phone,
  stateAddress,
  streetAddress,
  typeAccount,
}: registerBusinessBody) {
  await api.post('/usuario/registrar', {
    email,
    senha: password,
    tipo_conta: typeAccount,
  })
}
