import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import garcia from '../assets/garcia.jpg'

interface Vehicle {
    ano_fabricacao: number;
    calendario_disponibilidade: null;
    caminho_foto: null;
    capacidade: number;
    cor: string;
    custo_base: number;
    custo_por_km: number;
    id_empresa: number;
    id_veiculo: number;
    nome_veiculo: string;
    placa_veiculo: string;
  }
  
interface VehicleItemProps {
vehicle: Vehicle;
}

export default function VehicleItem({ vehicle }: VehicleItemProps) {
  return (
    <Card className="bg-white rounded-md">
      <CardHeader>
        <CardTitle className="flex justify-between text-xl">
          <span>Placa {vehicle.placa_veiculo}</span>
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
        <h2 className="text-center text-xl font-bold">{vehicle.nome_veiculo}</h2>

        <p className="text-primary-foreground">
          Cor: <span className="text-primary font-semibold">{vehicle.cor}</span>
        </p>

        <p className="text-primary-foreground">
          Ano: <span className="text-primary font-semibold">{vehicle.ano_fabricacao}</span>
        </p>

        <p className="text-primary-foreground">
          Capacidade: <span className="text-primary font-semibold">{vehicle.capacidade}</span>
        </p>

        <p className="text-primary-foreground">
          Valor base para a viagem:{' '}
          <span className="text-primary font-semibold">R${vehicle.custo_base}</span>
        </p>
      </div>
      </CardContent>
    </Card>
  )
}