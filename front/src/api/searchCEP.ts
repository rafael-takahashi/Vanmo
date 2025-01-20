import { apiCEP } from '@/lib/axios'

interface searchCepParams {
  cep: string
}

export interface searchCepResponse {
  cep: string
  logradouro: string
  complemento: string
  unidade: string
  bairro: string
  localidade: string
  uf: string
  estado: string
  regiao: string
  ibge: string
  gia: string
  ddd: string
  siafi: string
}

export async function searchCEP({
  cep,
}: searchCepParams): Promise<searchCepResponse> {
  const response = await apiCEP.get(`/${cep}/json`)
  return response.data
}
