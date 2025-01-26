import { useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'

import { getUserClient } from '@/api/getUserClient'
import SideMenuProfile from '@/components/side-menu-profile'
import AddVehicleForm from '@/components/add-vehicle-form'

export default function AddVehiclePage() {
  const token = Cookies.get('auth_token')

  const { data } = useQuery({
    queryKey: ['user', token],
    queryFn: () => getUserClient({ token }),
  })

  return (
    <main className="grid grid-cols-3 gap-4 mt-20">
      <SideMenuProfile typeAccount={data?.tipo_conta} />

      <div className="col-span-2 bg-primary-foreground p-10 rounded-md">
        <AddVehicleForm />
      </div>
    </main>
  )
}