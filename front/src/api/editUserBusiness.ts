import { api } from '@/lib/axios'

export interface editProfileUserBusinessBody {
  email?: string
  password?: string
  photo?: File
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
  console.log(email)
  console.log(password)
  console.log(photo)
  console.log(fantasyName)
  console.log(stateAddress)
  console.log(cityAddress)
  console.log(districtAddress)
  console.log(cep)
  console.log(streetAddress)
  console.log(numberAddress)
  console.log(phone)
  console.log(token)

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
