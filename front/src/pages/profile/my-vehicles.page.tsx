import { useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'

import { getUserBusiness } from '@/api/getUserBusiness'
import SideMenuProfile from '@/components/side-menu-profile'
import VehicleItem from '@/components/vehicle-item'
import { useEffect, useState } from 'react'
import { getBusinessVehicles } from '@/api/getBusinessVehicles'
import { Plus } from '@phosphor-icons/react'
import { useNavigate } from 'react-router'

export default function MyVehiclesPage() {
  const navigate = useNavigate()

  const token = Cookies.get('auth_token')

  const { data } = useQuery({
    queryKey: ['userBusiness', token],
    queryFn: () => getUserBusiness({ token }),
  })

  const [vehicles, setVehicles] = useState<any[]>([]);
  
  const fetchAndSetVehicles = async (businessId: number | undefined) => {
    setVehicles(await getBusinessVehicles(businessId))
  }

  useEffect(() => {
    if (data?.id)
      fetchAndSetVehicles(data?.id)
  }, [data?.id]);

  return (
    <main className="grid grid-cols-3 gap-4 mt-20">
      <SideMenuProfile typeAccount={'empresa'}
      fullName={
          data?.nome_fantasia
        } 
      />
      <div className="col-span-2 bg-primary-foreground p-10 rounded-md">
        <div className='flex items-center mb-4'>
          <h1 className="text-xl text-white">Meus Veículos</h1>
          <Plus
              size={24}
              color="#6af42a"
              className="ml-auto cursor-pointer"
              onClick={() => navigate('/profile/add-vehicle')}
          />
        </div>
          {vehicles && vehicles.map((vehicle) => (
            <div className='mb-6'>
              <VehicleItem
                vehicle={vehicle} 
                key={vehicle.id_veiculo}
              />
             </div>
          ))}
      </div>
    </main>
  )
}
