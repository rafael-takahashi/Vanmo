import { Card, CardContent, CardHeader, CardTitle } from './ui/card'

interface ProprosalItemProps {
  type: 'cliente' | 'empresa'
}

export default function ProposalItem({ type }: ProprosalItemProps) {
  return (
    <Card className="bg-white rounded-md">
      <CardHeader>
        <CardTitle className="flex justify-between text-xl">
          <span>#12345</span>

          <span className="text-red-500">REJEITADO</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="grid grid-cols-2">
        {type === 'cliente' && (
          <div>
            <h3 className="text-center font-semibold">
              Informações da Empresa
            </h3>

            <p>
              Empresa: <span>Viacao Garcia</span>
            </p>
            <p>
              Veículo: <span>Onibux X</span>
            </p>
            <p>
              Ano: <span>2020</span>
            </p>
            <p>
              Passageiros: <span>24</span>
            </p>
          </div>
        )}

        {type === 'empresa' && (
          <div>
            <h3 className="text-center font-semibold">
              Informações do Cliente
            </h3>

            <p>
              Nome Completo: <span>John Doe</span>
            </p>
            <p>
              Email: <span>johndoe@example.com</span>
            </p>
            <p>
              Data de Nascimento: <span>01/01/2000</span>
            </p>
            <p>
              CPF: <span>12312312312</span>
            </p>
          </div>
        )}

        <div>
          <h3 className="text-center font-semibold">Informações da Viagem</h3>
          <p>
            Partida: <span>Maringá-PR</span>
          </p>
          <p>
            Destino: <span>Rio de Janeiro-RJ</span>
          </p>
          <p>
            Data de ida: <span>04/01/2024</span>
          </p>
          <p>
            Data de retorno: <span>14/01/2024</span>
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
