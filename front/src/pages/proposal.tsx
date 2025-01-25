import { useState } from 'react'

import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

export function ProposalPage() {
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

            <div>
              <span>Informações da empresa</span>
              <br />
              <br />
              <span>
                Nome da empresa:{' '}
                <span className="text-primary font-bold">Viação Garcia</span>
                <br />
                Cidade:{' '}
                <span className="text-primary font-bold">Maringá-PR</span>
                <br />
                Endereço:{' '}
                <span className="text-primary font-bold">Rua XYZ</span>
                <br />
                CNPJ:{' '}
                <span className="text-primary font-bold">123123132123101</span>
                <br />
                Telefone:{' '}
                <span className="text-primary font-bold">(44) 123451234</span>
                <br />
                Avaliação: <span className="text-primary font-bold">4.7</span>
              </span>
            </div>

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

            <div>
              <span>Informações do usuário</span>
              <br />
              <br />
              <span>
                Nome: <span className="text-primary font-bold">John Doe</span>
                <br />
                Email:{' '}
                <span className="text-primary font-bold">johndoe@emai.com</span>
                <br />
                CPF:{' '}
                <span className="text-primary font-bold">123123132123101</span>
                <br />
                Telefone:{' '}
                <span className="text-primary font-bold">(44) 123451234</span>
              </span>
            </div>

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

            <div>
              <span>Informações do fretamento</span>
              <br />
              <br />
              <span>
                Local de Partida:{' '}
                <span className="text-primary font-bold">Maringá-PR</span>
                <br />
                Local de Destino:{' '}
                <span className="text-primary font-bold">
                  Rio de Janeiro-RJ
                </span>
                <br />
                Data de Ida:{' '}
                <span className="text-primary font-bold">12/01/2025</span>
                <br />
                Data de Retorno:{' '}
                <span className="text-primary font-bold">24/01/2025</span>
                <br />
                Quantidade de Passageiros:{' '}
                <span className="text-primary font-bold">24</span>
              </span>
            </div>

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
                // onClick={}
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
