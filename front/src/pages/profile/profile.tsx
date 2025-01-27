import { useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'
import { useEffect } from 'react'

import { getUserBusiness } from '@/api/getUserBusiness'
import { getUserClient } from '@/api/getUserClient'
import ProfileBusinessArea from '@/components/profile-business-area'
import ProfileClientArea from '@/components/profile-client-area'
import SideMenuProfile from '@/components/side-menu-profile'

export default function Profile() {
  const token = Cookies.get('auth_token')

  const { data: dataClient } = useQuery({
    queryKey: ['userClient', token],
    queryFn: () => getUserClient({ token }),
    enabled: !!token,
    retry: false, // Não tentar novamente se falhar
  })

  // Segunda requisição: buscar os dados da empresa apenas se a requisição do cliente falhar
  const { data: dataBusiness } = useQuery({
    queryKey: ['userBusiness', token],
    queryFn: () => getUserBusiness({ token }),
    enabled: !!token, // Só habilita se a requisição do cliente falhar
    retry: false,
  })

  // Determinar qual tipo de conta está disponível
  const tipoConta = dataClient?.tipo_conta === 'cliente' ? 'cliente' : 'empresa'

  return (
    <main className="grid grid-cols-3 gap-4 mt-20">
      <SideMenuProfile
        typeAccount={tipoConta}
        fullName={
          tipoConta === 'empresa'
            ? dataBusiness?.nome_fantasia
            : dataClient?.nome_completo
        }
      />

      {tipoConta === 'cliente' && <ProfileClientArea />}

      {tipoConta === 'empresa' && <ProfileBusinessArea />}
    </main>
  )
}
