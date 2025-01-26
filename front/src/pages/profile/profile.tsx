import { useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'

import { getUserClient } from '@/api/getUserClient'
import ProfileBusinessArea from '@/components/profile-business-area'
import ProfileClientArea from '@/components/profile-client-area'
import SideMenuProfile from '@/components/side-menu-profile'

export default function Profile() {
  const token = Cookies.get('auth_token')

  const { data } = useQuery({
    queryKey: ['user', token],
    queryFn: () => getUserClient({ token }),
  })

  return (
    <main className="grid grid-cols-3 gap-4 mt-20">
      <SideMenuProfile typeAccount={data?.tipo_conta} email={data?.email} />

      {data?.tipo_conta === 'cliente' && <ProfileClientArea />}

      {data?.tipo_conta === 'empresa' && <ProfileBusinessArea />}
    </main>
  )
}
