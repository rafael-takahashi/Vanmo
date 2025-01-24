import garcia from '../assets/garcia.jpg'
import { Button } from './ui/button'

export function VehicleBox() {

  return (
    <div
      className="bg-white rounded-md p-4 flex"
    >
        <div className="w-[280px] h-[180px] overflow-hidden">
            <img
            src={garcia}
            alt=""
            className="w-full h-full object-cover object-center rounded-md"
            />
        </div>
        <div className="flex-1 flex flex-col ml-4">
            <h2 className="text-center text-xl font-bold">Onibus X</h2>

            <p className="text-primary-foreground">
            Modelo:{' '}
            <span className="text-primary font-semibold">Modelo X</span>
            </p>

            <p className="text-primary-foreground">
            Ano:{' '}
            <span className="text-primary font-semibold">2000</span>
            </p>

            <p className="text-primary-foreground">
            Capacidade:{' '}
            <span className="text-primary font-semibold">60</span>
            </p>
            
            <Button
            className="mt-6 h-12 flex justify-center items-center text-xl font-semibold self-end"
            size={'lg'}
            >
                Proposta
            </Button>
        </div>
    </div>
  )
}