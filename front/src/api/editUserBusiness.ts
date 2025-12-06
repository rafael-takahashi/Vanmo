import Cookies from 'js-cookie'

import { api } from '@/lib/axios'

export interface editProfileUserBusinessBody {
  email?: string
  password?: string
  fantasyName?: string
  stateAddress?: string
  cityAddress?: string
  districtAddress?: string
  cep?: string
  streetAddress?: string
  numberAddress?: string
  phone?: string
  photo?: FileList
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
}: editProfileUserBusinessBody) {
  const token = Cookies.get('auth_token')

  const formData = new FormData()

  if (email) formData.append('email', email)
  if (password) formData.append('senha', password)
  if (fantasyName) formData.append('nome_fantasia', fantasyName)
  if (stateAddress) formData.append('uf', stateAddress)
  if (cityAddress) formData.append('cidade', cityAddress)
  if (districtAddress) formData.append('bairro', districtAddress)
  if (cep) formData.append('cep', cep)
  if (streetAddress) formData.append('rua', streetAddress)
  if (numberAddress) formData.append('numero', numberAddress)
  if (phone) formData.append('telefone', phone)

  if (photo?.[0]) {
    formData.append('foto', photo[0])
  }

  await api.put('/usuario/alterar_dados/empresa', formData, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}
