import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation, useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'
import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate, useSearchParams } from 'react-router'
import { z } from 'zod'

import { editProfileUserClient } from '@/api/editUserClient'
import { getUserClient } from '@/api/getUseClient'
import ProposalItem from '@/components/proposal-item'
import SideMenuProfile from '@/components/side-menu-profile'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'

const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/jpg']

const PersonalProfile = z.object({
  fullName: z.string(),
  email: z.string().email(),
  dateOfBirth: z.string(),
  phone: z.string(),
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
  const [searchParams, setSearchParams] = useSearchParams()
  const navigate = useNavigate()

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
      <SideMenuProfile />

      <div className="col-span-2 bg-primary-foreground p-10 rounded-md">
        <div className="flex justify-between">
          <h2 className="text-white text-2xl">Informações Pessoais</h2>
          <Dialog>
            <DialogTrigger className="text-white text-sm border p-2 rounded-md">
              Editar Perfil
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Editar Perfil</DialogTitle>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <label htmlFor="name" className="text-right">
                    Nome Completo
                  </label>
                  <Input id="name" className="input-bordered col-span-3" />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <label htmlFor="email" className="text-right">
                    E-mail
                  </label>
                  <Input
                    id="email"
                    className="input-bordered col-span-3"
                    disabled
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <label htmlFor="dateOfBirth" className="text-right">
                    Data de Nascimento
                  </label>
                  <Input
                    id="dateOfBirth"
                    className="input-bordered col-span-3"
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <label htmlFor="phone" className="text-right">
                    Telefone Celular
                  </label>
                  <Input id="phone" className="input-bordered col-span-3" />
                </div>
              </div>
              <DialogFooter>
                <Button type="submit">Salvar Perfil</Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
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
              disabled
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
              Data de Nascimento
            </label>
            <Input
              className="input-bordered"
              type="date"
              {...register('dateOfBirth')}
              disabled
            />
          </div>
          <div>
            <label htmlFor="" className="text-white">
              Telefone Celular
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('phone')}
              disabled
            />
          </div>
        </form>

        <div className="flex items-end gap-4 mt-14">
          <h2 className="text-white text-2xl">Minhas Propostas</h2>
          <span
            className="text-white text-sm font-thin cursor-pointer"
            onClick={() => {
              navigate('/profile/proposals')
              setSearchParams((state) => {
                state.set('status', 'all')

                return state
              })
            }}
          >
            Ver Mais
          </span>
        </div>

        <div className="flex flex-col gap-4 mt-4">
          <ProposalItem />
          <ProposalItem />
        </div>
      </div>
    </main>
  )
}
