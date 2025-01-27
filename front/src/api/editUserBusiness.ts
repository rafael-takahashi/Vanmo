import { api } from '@/lib/axios'

export interface editProfileUserBusinessBody {
  email?: string
  password?: string
  photo?: File | null
  fantasyName?: string
  stateAddress?: string
  cityAddress?: string
  districtAddress?: string
  cep?: string
  streetAddress?: string
  numberAddress?: string
  phone?: string
  token?: string
}

export async function editProfileUserBusiness({
  email,
  password,
  photo,
  fantasyName,
  stateAddress,
  cityAddress,
  districtAddress,
  cep,
  streetAddress,
  numberAddress,
  phone,
  token,
}: editProfileUserBusinessBody) {
  await api.put(
    '/usuario/alterar_dados/empresa',
    {
      email,
      senha: password,
      foto: photo,
      nome_fantasia: fantasyName,
      uf: stateAddress,
      cidade: cityAddress,
      bairro: districtAddress,
      cep,
      rua: streetAddress,
      numero: numberAddress,
      telefone: phone,
    },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )
}
