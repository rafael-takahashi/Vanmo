import { api } from '@/lib/axios'

export interface registerVehicleBody {
    token: string | undefined
    name: string
    licensePlate: string
    costPerKm: string
    baseCost: string
    color: string
    year: string
    capacity: string
    //TODO: add foto
}

export async function registerVehicle({ 
    token,
    name,
    licensePlate,
    costPerKm,
    baseCost,
    color,
    year,
    capacity
    //TODO: add foto
}: registerVehicleBody) {
    const formData = new FormData();
    formData.append('nome_veiculo', name);
    formData.append('placa_veiculo', licensePlate);
    formData.append('custo_por_km', costPerKm);
    formData.append('custo_base', baseCost);
    formData.append('cor', color);
    formData.append('ano_fabricacao', year);
    formData.append('capacidade', capacity);
    //TODO: add foto
    try {
        const response = await api.post('/veiculos/cadastrar_veiculo/', formData, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error: any) {
        console.error('Error:', error.response?.data || error.message);
        throw error;
    }
}