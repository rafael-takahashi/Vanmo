import { api } from '@/lib/axios'

export interface editVehicleBody {
    token: string | undefined
    id: number
    name: string
    licensePlate: string
    costPerKm: number
    baseCost: number
    color: string
    year: number
    capacity: number
    photo: File | null
}

export async function editVehicle({
    token,
    id,
    name,
    licensePlate,
    costPerKm,
    baseCost,
    color,
    year,
    capacity,
    photo
}: editVehicleBody) {
    const jsonBody = JSON.stringify({
        id_veiculo: id,
        nome_veiculo: name,
        placa_veiculo: licensePlate,
        custo_por_km: costPerKm,
        custo_base: baseCost,
        cor: color,
        ano_fabricacao: year,
        capacidade: capacity,
        foto: photo
    })
    try {
        const response = await api.put('/veiculos/editar_veiculo', jsonBody, {
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        })
    } catch (error: any) {
        console.error('Error:', error.response?.data || error.message)
        throw error
    }
}
