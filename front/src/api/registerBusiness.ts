import Cookies from 'js-cookie'

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
  districtAddress: string
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
  districtAddress,
  stateAddress,
  streetAddress,
  typeAccount,
}: registerBusinessBody) {
  const response = await api.post('/usuario/cadastro/empresa', {
    email,
    senha: password,
    nome_fantasia: fantasyName,
    tipo_conta: typeAccount,
    cnpj,
    uf: stateAddress,
    cidade: cityAddress,
    bairro: districtAddress,
    cep,
    rua: streetAddress,
    numero: numberAddress,
  })

  const token = response.data.access_token

  Cookies.set('auth_token', token, {
    expires: 7,
    secure: true,
    sameSite: 'strict',
  })
}
