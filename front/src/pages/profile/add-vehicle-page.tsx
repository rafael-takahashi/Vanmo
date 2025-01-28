import { useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'
import { useLocation } from 'react-router'

import { getUserBusiness } from '@/api/getUserBusiness'
import AddVehicleForm from '@/components/add-vehicle-form'
import SideMenuProfile from '@/components/side-menu-profile'

export default function AddVehiclePage() {
  const location = useLocation()
  const vehicle = location.state?.vehicle
  const editMode = vehicle != null

  const token = Cookies.get('auth_token')

  const { data: dataBusiness } = useQuery({
    queryKey: ['userBusiness', token],
    queryFn: () => getUserBusiness({ token }),
    enabled: !!token,
    retry: false,
  })

  return (
    <main className="flex gap-4 mt-20">
      <SideMenuProfile
        typeAccount={dataBusiness?.tipo_conta}
        fullName={dataBusiness?.nome_fantasia}
        idUsuario={dataBusiness.id}
      />

      <div className="flex-1 bg-primary-foreground p-10 rounded-md">
        <AddVehicleForm vehicle={vehicle} editMode={editMode} />
      </div>
    </main>
  )
}
