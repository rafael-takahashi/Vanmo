import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation, useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'
import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'

import { editProfileUserClient } from '@/api/editUserClient'
import { getUserClient } from '@/api/getUseClient'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

import garcia from '../assets/garcia.jpg'

const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/jpg']

const PersonalProfile = z.object({
  fullName: z.string(),
  email: z.string().email(),
  photo: z
    .any()
    .refine((fileList) => fileList && fileList.length > 0, 'File is required')
    .refine(
      (fileList) =>
        fileList[0] && ALLOWED_MIME_TYPES.includes(fileList[0].type),
      'Only JPEG and PNG files are allowed',
    ),
})

type PersonalProfileForm = z.infer<typeof PersonalProfile>

export default function Profile() {
  const token = Cookies.get('auth_token')

  const { register, handleSubmit, reset } = useForm<PersonalProfileForm>({
    resolver: zodResolver(PersonalProfile),
  })

  const { mutateAsync } = useMutation({
    mutationFn: editProfileUserClient,
  })

  const { data } = useQuery({
    queryKey: ['user', token],
    queryFn: () => getUserClient({ token }),
  })

  useEffect(() => {
    if (data) {
      reset({
        email: data.email || '',
        fullName: '',
        photo: '', // Deixe vazio para o campo de arquivo
      })
    }
  }, [data, reset])

  async function handleEditProfile(data: PersonalProfileForm) {
    try {
      await mutateAsync({
        email: data.email,
        photo: data.photo,
        token,
      })
    } catch (error) {
      console.log(error)
    }
  }

  return (
    <main className="grid grid-cols-3 gap-4 mt-20">
      <div className="flex flex-col items-center col-span-1 bg-primary-foreground py-8 px-4 rounded-md text-white">
        <div className="flex rounded-full w-[256px] h-[256px] bg-white overflow-hidden">
          <img src={garcia} className="object-cover" alt="" />
        </div>
        <span className="text-xl mt-2">USUARIO</span>

        <nav className="flex flex-col items-center mt-10 text-xl ">
          <a href="#">Informações Pessoais</a>
          <div className="w-full h-[1px] bg-gray-400 my-2"></div>
          <a href="#">Minhas Propostas</a>
        </nav>

        <Button className="mt-10" type="button" size={'lg'}>
          DESCONECTAR
        </Button>
      </div>
      <div className="col-span-2 bg-primary-foreground p-6 rounded-md">
        <h2 className="text-white text-2xl">Informações Pessoais</h2>
        <form
          className="grid grid-cols-2 gap-4 mt-6"
          onSubmit={handleSubmit(handleEditProfile)}
        >
          <div>
            <label htmlFor="" className="text-white">
              Nome Completo
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('fullName')}
            />
          </div>
          <div>
            <label htmlFor="" className="text-white">
              E-mail
            </label>
            <Input
              className="input-bordered"
              type="email"
              {...register('email')}
              disabled
            />
          </div>
          <div>
            <label htmlFor="" className="text-white">
              Foto
            </label>
            <Input
              className="input-bordered"
              type="file"
              accept="image/jpeg, image/png, image/jpg"
              {...register('photo')}
            />
          </div>
          <Button type="submit">Teste</Button>
        </form>

        <h2 className="text-white text-2xl mt-14">Minhas Propostas</h2>
      </div>
    </main>
  )
}
