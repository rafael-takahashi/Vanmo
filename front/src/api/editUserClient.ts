import { api } from '@/lib/axios'

export interface editProfileUserClientBody {
  email?: string
  password?: string
  photo?: File | null
  fullName?: string
  dateOfBirth?: string
  phone?: string
  token?: string
}

export async function editProfileUserClient({
  email,
  password,
  photo,
  fullName,
  dateOfBirth,
  phone,
  token,
}: editProfileUserClientBody) {
  const formData = new FormData();
  formData.append('email', email || '');
  formData.append('senha', password || '');
  if (photo) {
    formData.append('foto', photo as File);
  }
  formData.append('nome_completo', fullName || '');
  formData.append('data_nascimento', dateOfBirth || '');
  formData.append('telefone', phone || '');

  await api.put(
    '/usuario/alterar_dados/cliente',
    formData,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )
}
