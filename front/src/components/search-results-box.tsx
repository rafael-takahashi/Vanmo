import { useNavigate } from 'react-router'

import garcia from '../assets/garcia.jpg'

export function SearchResults() {
  const navigate = useNavigate()

  return (
    <div
      className="bg-white rounded-md p-4 flex cursor-pointer"
      onClick={() => {
        navigate('/empresa/viacao+garcia')
      }}
    >
      <div className="w-[280px] h-[180px] overflow-hidden">
        <img
          src={garcia}
          alt=""
          className="w-full h-full object-cover object-center rounded-md"
        />
      </div>
      <div className="flex-1 ml-4">
        <h2 className="text-center text-xl font-bold">Viação Garcia</h2>

        <p className="text-primary-foreground">
          Endereço:{' '}
          <span className="text-primary font-semibold">Rua Teste XYZ</span>
        </p>

        <p className="text-primary-foreground mt-auto">
          Avaliação: <span className="text-primary font-semibold">4.5</span>
        </p>
      </div>
    </div>
  )
}
