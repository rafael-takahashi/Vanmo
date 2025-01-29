import { useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'

import { getTypeAccount } from '@/api/getTypeAccount'
import { getUserBusiness } from '@/api/getUserBusiness'
import { getUserClient } from '@/api/getUserClient'
import ProfileBusinessArea from '@/components/profile-business-area'
import ProfileClientArea from '@/components/profile-client-area'
import SideMenuProfile from '@/components/side-menu-profile'

export default function Profile() {
  const token = Cookies.get('auth_token')

  const { data } = useQuery({
    queryKey: ['user', token],
    queryFn: async () => await getTypeAccount({ token }),
    enabled: !!token,
  })

  const { data: dataClient } = useQuery({
    queryKey: ['userClient', token],
    queryFn: () => getUserClient({ token }),
    enabled: data?.tipo_usuario === 'cliente',
  })

  const { data: dataBusiness } = useQuery({
    queryKey: ['userBusiness', token],
    queryFn: () => getUserBusiness({ token }),
    enabled: data?.tipo_usuario === 'empresa',
  })

  return (
    <main className="flex gap-4 mt-20">
      <SideMenuProfile
        typeAccount={data?.tipo_usuario}
        fullName={
          data?.tipo_usuario === 'empresa'
            ? dataBusiness?.nome_fantasia
            : dataClient?.nome_completo
        }
        idUsuario={data?.id_usuario}
        photo={
          data?.tipo_usuario === 'empresa'
            ? dataBusiness.foto
            : dataClient?.foto
        }
      />

      {data?.tipo_usuario === 'cliente' && <ProfileClientArea />}

      {data?.tipo_usuario === 'empresa' && <ProfileBusinessArea />}
    </main>
  )
}
