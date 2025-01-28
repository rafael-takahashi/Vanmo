import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation, useQuery } from '@tanstack/react-query'
import { addDays, format } from 'date-fns'
import Cookies from 'js-cookie'
import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate, useSearchParams } from 'react-router'
import { z } from 'zod'

import { editProfileUserClient } from '@/api/editUserClient'
import { getUserClient } from '@/api/getUserClient'
import { getUserProposals } from '@/api/proposals/getUserProposals'

import ProposalItem from './proposal-item'
import { Button } from './ui/button'
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from './ui/dialog'
import { Input } from './ui/input'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'

const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/jpg']

const PersonalProfile = z.object({
  fullName: z.string(),
  dateOfBirth: z.string(),
  email: z.string().email(),
  phone: z.string(),
  // photo: z
  //   .any()
  //   .refine((fileList) => fileList && fileList.length > 0, 'File is required')
  //   .refine(
  //     (fileList) =>
  //       fileList[0] && ALLOWED_MIME_TYPES.includes(fileList[0].type),
  //     'Only JPEG and PNG files are allowed',
  //   ),
})

type PersonalProfileForm = z.infer<typeof PersonalProfile>

export default function ProfileClientArea() {
  const [photo, setPhoto] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [preview, setPreview] = useState<string | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]

    // Validate the file
    if (!file) {
      setError('Please select a file.')
      setPhoto(null)
      setPreview(null)
      return
    }

    if (!ALLOWED_MIME_TYPES.includes(file.type)) {
      setError('Only JPEG, PNG, and JPG files are allowed.')
      setPhoto(null)
      setPreview(null)
      return
    }

    setPhoto(file)
    setError(null)
    setPreview(URL.createObjectURL(file))
  }

  const token = Cookies.get('auth_token')
  const [originalData, setOriginalData] = useState<PersonalProfileForm | null>(
    null,
  )
  const [searchParams, setSearchParams] = useSearchParams()
  const navigate = useNavigate()
  const { register, handleSubmit, reset } = useForm<PersonalProfileForm>({
    resolver: zodResolver(PersonalProfile),
  })

  const { data } = useQuery({
    queryKey: ['userClient', token],
    queryFn: () => getUserClient({ token }),
  })

  const { data: proposalsList } = useQuery({
    queryKey: ['proposals-user', token],
    queryFn: () => getUserProposals({ token }),
  })

  const { mutateAsync } = useMutation({
    mutationFn: editProfileUserClient,
  })

  useEffect(() => {
    if (!data?.data_nascimento) {
      return
    }

    const date = new Date(data.data_nascimento)
    const adjustedDate = addDays(date, 1)

    if (data) {
      const initialData = {
        email: data.email || '',
        fullName: data.nome_completo || '',
        dateOfBirth: format(adjustedDate, 'yyyy-MM-dd') || '',
        phone: data.telefone || '',
      }

      setOriginalData(initialData) // Armazena os dados originais no estado
      reset(initialData)
    }
  }, [data, reset])

  async function handleEditProfile(data: PersonalProfileForm) {
    try {
      const updatedFields: Partial<PersonalProfileForm> = {}

      // Compara os valores atuais com os valores originais e adiciona os campos alterados
      if (data.email !== originalData?.email) updatedFields.email = data.email
      if (data.fullName !== originalData?.fullName)
        updatedFields.fullName = data.fullName
      if (data.dateOfBirth !== originalData?.dateOfBirth)
        updatedFields.dateOfBirth = data.dateOfBirth
      if (data.phone !== originalData?.phone) updatedFields.phone = data.phone

      // Se houver alterações, envia apenas os campos modificados
      if (Object.keys(updatedFields).length > 0 || photo) {
        await mutateAsync({
          ...updatedFields,
          token,
          photo,
        })
      } else {
        console.log('Nenhuma alteração detectada')
      }
    } catch (error) {
      console.log(error)
    }
  }

  return (
    <>
      <div className="flex-1 bg-primary-foreground p-10 rounded-md">
        <div className="flex justify-between">
          <h2 className="text-white text-2xl">Informações Pessoais</h2>
          <Dialog>
            <DialogTrigger className="text-white text-sm border p-2 rounded-md">
              Editar Perfil
            </DialogTrigger>
            <DialogContent>
              <Tabs defaultValue="account" className="w-full mt-4">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="account">
                    Informações Pessoais
                  </TabsTrigger>
                  <TabsTrigger value="password">Senha</TabsTrigger>
                </TabsList>
                <TabsContent value="account" className="mt-4">
                  <DialogHeader>
                    <DialogTitle>Editar Perfil</DialogTitle>
                  </DialogHeader>
                  <form
                    onSubmit={handleSubmit(handleEditProfile)}
                    className="flex flex-col"
                  >
                    <div className="grid gap-4 py-4">
                      <div className="grid grid-cols-4 items-center gap-4">
                        <label htmlFor="name" className="text-right">
                          Nome Completo
                        </label>
                        <Input
                          id="name"
                          className="input-bordered col-span-3"
                          {...register('fullName')}
                        />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <label htmlFor="email" className="text-right">
                          E-mail
                        </label>
                        <Input
                          id="email"
                          className="input-bordered col-span-3"
                          {...register('email')}
                          disabled
                        />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <label htmlFor="dateOfBirth" className="text-right">
                          Data de Nascimento
                        </label>
                        <Input
                          id="dateOfBirth"
                          type="date"
                          className="input-bordered col-span-3"
                          {...register('dateOfBirth')}
                        />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <label htmlFor="phone" className="text-right">
                          Telefone Celular
                        </label>
                        <Input
                          id="phone"
                          className="input-bordered col-span-3"
                          {...register('phone')}
                        />
                      </div>
                      {/* <div className="grid grid-cols-4 items-center gap-4">
                        <label htmlFor="phone" className="text-right">
                          Foto
                        </label>
                        <input
                          id="photo"
                          type="file"
                          accept={ALLOWED_MIME_TYPES.join(',')}
                          multiple
                          onChange={handleFileChange}
                        />
                        {error && (
                          <p className="text-red-500 text-sm mt-1">{error}</p>
                        )}
                        {preview && (
                          <div className="mt-2">
                            <img
                              src={preview}
                              alt="Preview"
                              className="h-20 w-20 object-cover rounded"
                            />
                          </div>
                        )}
                      </div> */}
                    </div>

                    <Button type="submit" className="ml-auto">
                      Salvar Perfil
                    </Button>
                  </form>
                </TabsContent>
                <TabsContent value="password" className="mt-4">
                  <DialogHeader>
                    <DialogTitle>Editar Senha</DialogTitle>
                  </DialogHeader>
                  <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                      <label htmlFor="oldPassword" className="text-right">
                        Senha atual
                      </label>
                      <Input
                        id="oldPassword"
                        className="input-bordered col-span-3"
                      />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <label htmlFor="newPassword" className="text-right">
                        Nova senha
                      </label>
                      <Input
                        id="newPassword"
                        className="input-bordered col-span-3"
                      />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <label htmlFor="confirmPassword" className="text-right">
                        Confirmar senha
                      </label>
                      <Input
                        id="confirmPassword"
                        className="input-bordered col-span-3"
                      />
                    </div>
                  </div>
                  <DialogFooter>
                    <Button type="submit">Trocar Senha</Button>
                  </DialogFooter>
                </TabsContent>
              </Tabs>
            </DialogContent>
          </Dialog>
        </div>
        <form className="grid grid-cols-2 gap-4 mt-6">
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
          {proposalsList && proposalsList.length > 0 ? (
            proposalsList
              .slice(0, 2)
              .map((proposal: any) => (
                <ProposalItem
                  proposal={proposal}
                  key={proposal.id_aluguel}
                  type="cliente"
                />
              ))
          ) : (
            <p className="text-white ">Não foram encontradas propostas.</p>
          )}
        </div>
      </div>
    </>
  )
}
