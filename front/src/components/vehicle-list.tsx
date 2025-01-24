import { Button } from './ui/button'
import { VehicleBox } from './vehicle-box'

export function VehicleList() {
  return (
    <>
      <div className="w-full grid grid-cols-2 gap-3 mt-8">
          <VehicleBox />
          <VehicleBox />
          <VehicleBox />
          <VehicleBox />
          <VehicleBox />
          <VehicleBox />
      </div>
      
      <div className="flex justify-center mt-8">
        <Button
          className="h-10 px-12 flex justify-center items-center text-xl font-semibold self-end"
          size={'lg'}
          >
              Ver Mais
        </Button>
      </div>
    </>
  )
}