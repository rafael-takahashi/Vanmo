import { useMutation, useQuery } from '@tanstack/react-query'
import { MoreHorizontal } from 'lucide-react'
import { useNavigate } from 'react-router'
import { toast } from 'sonner'

import { fetchProposals } from '@/api/proposals/fetchProposals'

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

interface TableProposalsProps {
  id_usuario: number
}

export default function TableProposalsClient({
  id_usuario,
}: TableProposalsProps) {
  const url = window.location.pathname
  const navigate = useNavigate()

  const { data, refetch } = useQuery({
    queryKey: ['proposals', id_usuario],
    queryFn: () => fetchProposals(),
  })

  return (
    <Table className="bg-white rounded-md text-primary-foreground">
      {url === '/profile/vehicles' && (
        <TableCaption className="text-slate-400">
          Todos as propostas realizadas.
        </TableCaption>
      )}

      {url === '/profile' && (
        <TableCaption className="text-slate-400">
          Algumas propostas realizadas.
        </TableCaption>
      )}
      <TableHeader>
        <TableRow>
          <TableHead></TableHead>
          <TableHead colSpan={3}>Empresa</TableHead>
          <TableHead colSpan={5}>Viagem</TableHead>
          <TableHead></TableHead>
        </TableRow>
        <TableRow>
          <TableHead className="w-[40px]">ID</TableHead>
          <TableHead>Nome</TableHead>
          <TableHead>Veículo</TableHead>
          <TableHead>Capac.</TableHead>
          <TableHead>Partida</TableHead>
          <TableHead>Destino</TableHead>
          <TableHead>Data ida</TableHead>
          <TableHead>Data retorno</TableHead>
          <TableHead>Valor</TableHead>
          <TableHead>Status</TableHead>
          <TableHead className="w-[40px]"></TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {data && data.length > 0 ? (
          data?.map((proposta) => (
            <TableRow key={proposta.proposta.id_aluguel}>
              <TableCell>{proposta.proposta.id_aluguel}</TableCell>
              <TableCell>
                {proposta.proposta.id_empresa.nome_fantasia}
              </TableCell>
              <TableCell>{proposta.veiculo.nome_veiculo}</TableCell>
              <TableCell>{proposta.veiculo.capacidade}</TableCell>
              <TableCell>{proposta.proposta.local_partida.nome}</TableCell>
              <TableCell>{proposta.proposta.local_chegada.nome}</TableCell>
              <TableCell>{proposta.proposta.data_inicio}</TableCell>
              <TableCell>{proposta.proposta.data_fim}</TableCell>
              <TableCell>
                {new Intl.NumberFormat('pt-BR', {
                  style: 'currency',
                  currency: 'BRL',
                }).format(proposta.proposta.valor_total)}
              </TableCell>
              <TableCell>{proposta.proposta.estado_aluguel}</TableCell>

              <TableCell>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="h-8 w-8 p-0">
                      <MoreHorizontal />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuLabel>Ações</DropdownMenuLabel>
                    <DropdownMenuItem className="cursor-pointer" disabled>
                      Ver mais detalhes
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))
        ) : (
          <TableRow>
            <TableCell colSpan={11} className="text-center text-gray-500">
              Nenhuma proposta encontrada.
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}
