import { Plus } from '@phosphor-icons/react'
import { useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router'

import { getBusinessVehicles } from '@/api/vehicles/getBusinessVehicles'
import { getUserBusiness } from '@/api/getUserBusiness'
import SideMenuProfile from '@/components/side-menu-profile'
import VehicleItem from '@/components/vehicle-item'

export default function MyVehiclesPage() {
  const navigate = useNavigate()

  const token = Cookies.get('auth_token')

  const { data } = useQuery({
    queryKey: ['userBusiness', token],
    queryFn: () => getUserBusiness({ token }),
  })

  const [vehicles, setVehicles] = useState<any[]>([])

  const fetchAndSetVehicles = async (businessId: number | undefined) => {
    setVehicles(await getBusinessVehicles(businessId, 1))
  }

  useEffect(() => {
    if (data?.id_usuario) fetchAndSetVehicles(data?.id_usuario)
  }, [data?.id_usuario])

  return (
    <main className="grid grid-cols-3 gap-4 mt-20">
      <SideMenuProfile typeAccount={'empresa'} fullName={data?.nome_fantasia} />
      <div className="col-span-2 bg-primary-foreground p-10 rounded-md">
        <div className="flex items-center mb-4">
          <h1 className="text-xl text-white">Meus Veículos</h1>
          <Plus
            size={24}
            color="#6af42a"
            className="ml-auto cursor-pointer"
            onClick={() => navigate('/profile/add-vehicle')}
          />
        </div>
        {vehicles &&
          vehicles.map((vehicle) => (
            <div className="mb-6">
              <VehicleItem vehicle={vehicle} key={vehicle.id_veiculo} />
            </div>
          ))}
      </div>
    </main>
  )
}
