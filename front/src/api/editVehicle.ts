import { api } from '@/lib/axios'

export interface editVehicleBody {
    id_veiculo: number,
    nome_veiculo: string,
    placa_veiculo: string,
    custo_por_km: number,
    custo_base: number,
    foto: File | null,
    cor: string,
    ano_fabricacao: number,
    token: string
}

export async function editVehicle({
    id_veiculo,
    nome_veiculo,
    placa_veiculo,
    custo_por_km,
    custo_base,
    foto,
    cor,
    ano_fabricacao,
    token,
}: editVehicleBody) {
    const jsonBody = JSON.stringify({
        id_veiculo,
        nome_veiculo,
        placa_veiculo,
        custo_por_km,
        custo_base,
        foto,
        cor,
        ano_fabricacao,
    })
  await api.put('/veiculos/editar_veiculo', jsonBody, {
    headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
    },
  })
}
