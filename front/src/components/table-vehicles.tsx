import { useMutation, useQuery } from '@tanstack/react-query'
import { MoreHorizontal } from 'lucide-react'
import { useNavigate } from 'react-router'
import { toast } from 'sonner'

import { deleteVehicle } from '@/api/vehicles/deleteVehicle'
import {
  getBusinessVehicles,
  Vehicles,
} from '@/api/vehicles/getBusinessVehicles'

import { Button } from './ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from './ui/dropdown-menu'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from './ui/table'

interface TableVehiclesProps {
  id_usuario: number
}

export default function TableVehicles({ id_usuario }: TableVehiclesProps) {
  const url = window.location.pathname
  const navigate = useNavigate()

  const { data, refetch } = useQuery({
    queryKey: ['vehicles', id_usuario],
    queryFn: () => getBusinessVehicles({ id_empresa: id_usuario, pagina: 1 }),
  })

  const { mutateAsync } = useMutation({
    mutationFn: deleteVehicle,
  })

  async function handleDeleteVehicle(id_veiculo: number) {
    try {
      await mutateAsync({ id_veiculo })

      refetch()
      toast.success('Veículo deletado com sucesso.')
    } catch (error) {
      console.error('Erro ao deletar veículo: ', error)
      toast.error('Erro ao deletar veículo, tente novamente.')
    }
  }

  async function handleEditVehicle(vehicle: Vehicles) {
    navigate('/profile/add-vehicle', { state: { vehicle } })
  }

  return (
    <Table className="bg-white rounded-md text-primary-foreground">
      {url === '/profile/vehicles' && (
        <TableCaption className="text-slate-400">
          Todos os veículos cadastrados.
        </TableCaption>
      )}

      {url === '/profile' && (
        <TableCaption className="text-slate-400">
          Alguns dos veículos cadastrados.
        </TableCaption>
      )}
      <TableHeader>
        <TableRow>
          <TableHead className="w-[60px]">ID</TableHead>
          <TableHead>Modelo</TableHead>
          <TableHead>Placa</TableHead>
          <TableHead>Cor</TableHead>
          <TableHead>Ano</TableHead>
          <TableHead>Capacidade</TableHead>
          <TableHead className="w-[60px]"></TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {data && data.length > 0 ? (
          data.slice(0, 5).map((veiculo) => (
            <TableRow key={veiculo.id_veiculo}>
              <TableCell>{veiculo.id_veiculo}</TableCell>
              <TableCell>{veiculo.nome_veiculo}</TableCell>
              <TableCell>{veiculo.placa_veiculo}</TableCell>
              <TableCell>{veiculo.cor}</TableCell>
              <TableCell>{veiculo.ano_fabricacao}</TableCell>
              <TableCell>{veiculo.capacidade}</TableCell>
              <TableCell>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="h-8 w-8 p-0">
                      <MoreHorizontal />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuLabel>Ações</DropdownMenuLabel>
                    <DropdownMenuItem className="cursor-pointer">
                      Ver mais detalhes
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem
                      className="cursor-pointer"
                      onClick={() => handleEditVehicle(veiculo)}
                    >
                      Editar veículo
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      className="cursor-pointer text-red-500"
                      onClick={() => handleDeleteVehicle(veiculo.id_veiculo)}
                    >
                      Deletar veículo
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))
        ) : (
          <TableRow>
            <TableCell colSpan={7} className="text-center text-gray-500">
              Nenhum veículo encontrado.
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}
