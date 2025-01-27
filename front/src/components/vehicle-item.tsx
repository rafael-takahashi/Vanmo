import { Pencil, Trash } from '@phosphor-icons/react'
import Cookies from 'js-cookie'
import { toast } from 'sonner'

import { deleteVehicle } from '@/api/deleteVehicle'

import garcia from '../assets/garcia.jpg'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { useNavigate } from 'react-router';

interface Vehicle {
  ano_fabricacao: number
  calendario_disponibilidade: null
  caminho_foto: null
  capacidade: number
  cor: string
  custo_base: number
  custo_por_km: number
  id_empresa: number
  id_veiculo: number
  nome_veiculo: string
  placa_veiculo: string
}

interface VehicleItemProps {
  vehicle: Vehicle
}

export default function VehicleItem({ vehicle }: VehicleItemProps) {
    const navigate = useNavigate();

    const handleEditVehicle = (vehicle: Vehicle) => {
        navigate("/profile/add-vehicle", {
            state: { vehicle }
        })
    }

    const handleDeleteVehicle = async (id_veiculo: number) => {
        const token = Cookies.get('auth_token');
        
        if (!token) {
          console.error('No authorization token found.')
          return;
        }
      
        try {
          await deleteVehicle({ id_veiculo, token })
          toast.success('Vehicle deleted successfully')
          window.location.reload();
        } catch {
          toast.error('Failed to delete vehicle')
        }
    };

    return (
        <Card className="bg-white rounded-md">
        <CardHeader>
            <CardTitle className="flex justify-between text-xl">
                <span>Placa {vehicle.placa_veiculo}</span>
                <div className="flex space-x-4">
                    <Pencil 
                        size={24}
                        className="ml-auto cursor-pointer"
                        onClick={() => {handleEditVehicle(vehicle)}}
                    />
                    <Trash 
                        size={24} 
                        color="#FF0000"
                        className="ml-auto cursor-pointer"
                        onClick={() => {handleDeleteVehicle(vehicle.id_veiculo)}}
                    />
                </div>
            </CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-2">
        <div className="w-[280px] h-[180px] overflow-hidden">
          <img
            src={garcia}
            alt=""
            className="w-full h-full object-cover object-center rounded-md "
          />
        </div>
        <div className="flex-1 flex flex-col ml-4">
          <h2 className="text-center text-xl font-bold">
            {vehicle.nome_veiculo}
          </h2>

          <p className="text-primary-foreground">
            Cor:{' '}
            <span className="text-primary font-semibold">{vehicle.cor}</span>
          </p>

          <p className="text-primary-foreground">
            Ano:{' '}
            <span className="text-primary font-semibold">
              {vehicle.ano_fabricacao}
            </span>
          </p>

          <p className="text-primary-foreground">
            Capacidade:{' '}
            <span className="text-primary font-semibold">
              {vehicle.capacidade}
            </span>
          </p>

          <p className="text-primary-foreground">
            Valor base para a viagem:{' '}
            <span className="text-primary font-semibold">
              R${vehicle.custo_base}
            </span>
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
