import { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router';
import { useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'

import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { getDataBusiness } from '@/api/getDataBusiness';
import { getUserClient } from '@/api/getUserClient';
import { createProposal } from '@/api/proposals/createProposal';
import { calculateProposalCost } from '@/api/proposals/calculateProposalCost';
import { toast } from 'sonner';

type Proposal = {
  from: string;
  to: string;
  dateFrom: string;
  dateTo: string;
  numberPassengers: string;
};

export function ProposalPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { id_empresa, id_veiculo, proposal } = location.state as { id_empresa: string, id_veiculo: number, proposal: Proposal }
  
  const { data: dataBusiness, isSuccess: isSucessBusiness } = useQuery({
    queryKey: ['idBusiness', id_empresa],
    queryFn: () => getDataBusiness({ idEmpresa: id_empresa }),
  })

  const token = Cookies.get('auth_token')

  const { data: dataClient } = useQuery({
    queryKey: ['userClient', token],
    queryFn: () => getUserClient({ token }),
  })
  
  const [proposedCost, setProposedCost] = useState<number | null>(0)

  const getProposalCost = async () => {
    setProposedCost(await calculateProposalCost({ 
      id_empresa: parseInt(id_empresa),
      id_veiculo,
      local_saida: proposal.from,
      local_chegada: proposal.to,
      distancia_extra_km: 0,
      data_saida: proposal.dateFrom,
      data_chegada: proposal.dateTo,
      token,
    }))
  }

  useEffect(() => {
    getProposalCost()
  }, [])

  const handleCreateProposal = async (id_empresa: number, id_veiculo: number, proposal: Proposal) => {
    const token = Cookies.get('auth_token')

    if (!token) {
      console.error('No authorization token found.')
      return
    }

    try {
      await createProposal({ 
        id_empresa,
        id_veiculo,
        local_saida: proposal.from,
        local_chegada: proposal.to,
        distancia_extra_km: 0,
        data_saida: proposal.dateFrom,
        data_chegada: proposal.dateTo,
        token,
      })
      toast.success('Proposta realizada com sucesso')
      navigate('/profile/proposals?status=all')
    } catch {
      toast.error('Falha na realização da proposta')
    }
  }

  const [step, setStep] = useState(33)

  return (
    <div
      className="container h-screen flex justify-center items-center"
      style={{ height: 'calc(100vh - 200px)' }}
    >
      <div className="" style={{ width: '35vw', height: '50vh' }}>
        <h1 className="text-primary font-bold text-[2rem] text-center mb-4">
          CHECK-OUT
        </h1>

        <Progress
          value={step}
          className="w-full mb-10 transition-all duration-500"
        />

        {step === 33 && (
          <>
            <span className="font-bold text-lg mb-4">
              Verifique as informações da proposta
            </span>

            {isSucessBusiness && 
            <div>
              <span>Informações da empresa</span>
              <br />
              <br />
              <span>
                Nome da empresa:{' '}
                <span className="text-primary font-bold">{dataBusiness.nome_fantasia}</span>
                <br />
                Cidade:{' '}
                <span className="text-primary font-bold">{dataBusiness.endereco.cidade}</span>
                <br />
                Endereço:{' '}
                <span className="text-primary font-bold">{dataBusiness.endereco.rua}</span>
                <br />
                CNPJ:{' '}
                <span className="text-primary font-bold">{dataBusiness.cnpj}</span>
                <br />
                Telefone:{' '}
                <span className="text-primary font-bold">{dataBusiness.telefone}</span>
                <br />
                Avaliação: <span className="text-primary font-bold">{dataBusiness.avaliacao}</span>
              </span>
            </div>
            }

            <div className="flex justify-center mt-8">
              <Button
                className="h-12 px-24 flex justify-center items-center text-xl font-semibold self-end"
                size={'lg'}
                onClick={() => setStep(66)}
              >
                Próximo
              </Button>
            </div>
          </>
        )}

        {step === 66 && (
          <>
            <span className="font-bold text-lg mb-4">
              Verifique as informações da proposta
            </span>

            {dataClient &&
            <div>
              <span>Informações do usuário</span>
              <br />
              <br />
              <span>
                Nome: <span className="text-primary font-bold">{dataClient.nome_completo}</span>
                <br />
                Email:{' '}
                <span className="text-primary font-bold">{dataClient.email}</span>
                <br />
                CPF:{' '}
                <span className="text-primary font-bold">{dataClient.cpf}</span>
                <br />
                Telefone:{' '}
                <span className="text-primary font-bold">{dataClient.telefone}</span>
              </span>
            </div>
            }

            <div className="flex justify-center mt-8 space-x-24">
              <Button
                className="h-12 px-12 flex justify-center items-center text-xl font-semibold self-end"
                size={'lg'}
                onClick={() => setStep(33)}
              >
                Anterior
              </Button>
              <Button
                className="h-12 px-12 flex justify-center items-center text-xl font-semibold self-end"
                size={'lg'}
                onClick={() => setStep(100)}
              >
                Próximo
              </Button>
            </div>
          </>
        )}

        {step === 100 && (
          <>
            <span className="font-bold text-lg mb-4">
              Verifique as informações da proposta
            </span>
            {proposal &&
            <div>
              <span>Informações do fretamento</span>
              <br />
              <br />
              <span>
                Local de Partida:{' '}
                <span className="text-primary font-bold">{proposal.from}</span>
                <br />
                Local de Destino:{' '}
                <span className="text-primary font-bold">
                {proposal.to}
                </span>
                <br />
                Data de Ida:{' '}
                <span className="text-primary font-bold">{proposal.dateFrom}</span>
                <br />
                Data de Retorno:{' '}
                <span className="text-primary font-bold">{proposal.dateTo}</span>
                <br />
                Quantidade de Passageiros:{' '}
                <span className="text-primary font-bold">{proposal.numberPassengers}</span>
                <br />
                Valor Proposto:{' '}
                <span className="text-primary font-bold">
                  {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' })
                  .format(proposedCost ?? 0)}
                </span>
              </span>
            </div>
            }

            <div className="flex justify-center mt-8 space-x-24">
              <Button
                className="h-12 px-12 flex justify-center items-center text-xl font-semibold self-end"
                size={'lg'}
                onClick={() => setStep(66)}
              >
                Anterior
              </Button>
              <Button
                className="h-12 px-12 flex justify-center items-center text-xl font-semibold self-end"
                size={'lg'}
                onClick={() => {
                  handleCreateProposal(parseInt(id_empresa), id_veiculo, proposal)
                }}
              >
                Realizar Proposta
              </Button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
