import { useMutation, useQuery } from '@tanstack/react-query'
import { MoreHorizontal } from 'lucide-react'
import { useEffect } from 'react'
import { useNavigate } from 'react-router'
import { toast } from 'sonner'

import { fetchProposals } from '@/api/proposals/fetchProposals'
import { getUserProposals } from '@/api/proposals/getUserProposals'
import { handleProposal } from '@/api/proposals/handleProposal'

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
  status: string
}

export default function TableProposalsBusiness({
  id_usuario,
  status,
}: TableProposalsProps) {
  const url = window.location.pathname

  const { data, refetch } = useQuery({
    queryKey: ['proposals', id_usuario, status], // Inclua status para evitar colisão de cache
    queryFn: () => {
      if (status === 'all') {
        return fetchProposals()
      } else {
        return getUserProposals({ status_aluguel: status })
      }
    },
  })

  const { mutateAsync } = useMutation({
    mutationFn: handleProposal,
  })

  useEffect(() => {
    if (status) {
      refetch()
    }
  }, [status])

  async function handleProposals(id_proposta: number, state: boolean) {
    try {
      await mutateAsync({ idProposal: id_proposta, state })

      refetch()
      toast.success('Proposta modificada')
    } catch (error) {
      toast.error('Erro ao modificar')
      console.log(error)
    }
  }

  return (
    <Table className="bg-white rounded-md text-primary-foreground">
      {url === '/profile/proposals' && (
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
          <TableHead colSpan={2}>Cliente</TableHead>
          <TableHead colSpan={5}>Viagem</TableHead>
          <TableHead></TableHead>
        </TableRow>
        <TableRow>
          <TableHead className="w-[40px]">ID</TableHead>
          <TableHead>Nome</TableHead>
          <TableHead>Telefone</TableHead>
          <TableHead>Partida</TableHead>
          <TableHead>Destino</TableHead>
          <TableHead>Data ida</TableHead>
          <TableHead>Data retorno</TableHead>
          <TableHead>Passag.</TableHead>
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
                {proposta.proposta.id_cliente.nome_completo}
              </TableCell>
              <TableCell>{proposta.proposta.id_cliente.telefone}</TableCell>
              <TableCell>{proposta.proposta.local_partida.nome}</TableCell>
              <TableCell>{proposta.proposta.local_chegada.nome}</TableCell>
              <TableCell>{proposta.proposta.data_inicio}</TableCell>
              <TableCell>{proposta.proposta.data_fim}</TableCell>
              <TableCell>TESTE</TableCell>
              <TableCell>
                {' '}
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
                    <DropdownMenuSeparator />
                    <DropdownMenuItem
                      className="cursor-pointer"
                      onClick={() => {
                        handleProposals(proposta.proposta.id_aluguel, true)
                      }}
                    >
                      Aceitar proposta
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      className="cursor-pointer text-red-500"
                      onClick={() => {
                        handleProposals(proposta.proposta.id_aluguel, false)
                      }}
                    >
                      Rejeitar proposta
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
