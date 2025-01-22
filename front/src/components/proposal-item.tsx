import { Card, CardContent, CardHeader, CardTitle } from './ui/card'

export default function ProposalItem() {
  return (
    <Card className="bg-white rounded-md">
      <CardHeader>
        <CardTitle className="flex justify-between text-xl">
          <span>#12345</span>

          <span className="text-red-500">REJEITADO</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="grid grid-cols-2">
        <div>
          <h3 className="text-center font-semibold">Informações da Empresa</h3>

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
