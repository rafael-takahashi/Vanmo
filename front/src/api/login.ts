import Cookies from 'js-cookie'

import { api } from '@/lib/axios'
interface signInBody {
  email: string
  password: string
}

export async function signIn({ email, password }: signInBody) {
  const response = await api.post('/usuario/login', {
    email,
    senha: password,
  })

  const token = response.data.access_token

  Cookies.set('auth_token', token, {
    expires: 7,
    secure: true,
    sameSite: 'strict',
  })
}
