import { zodResolver } from '@hookform/resolvers/zod'
import { Plus } from '@phosphor-icons/react'
import { useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'
import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate, useSearchParams } from 'react-router'
import { z } from 'zod'

import { getUserClient } from '@/api/getUserClient'

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

const BusinessProfile = z.object({
  fantasyName: z.string().nonempty('Nome fantasia é obrigatório'),
  cnpj: z.string().nonempty('CNPJ é obrigatório'),
  email: z.string().email('E-mail é inválido').nonempty('E-mail é obrigatório'),
  phone: z.string().nonempty('Telefone é obrigatório'),
  cepAddress: z.string().nonempty('CEP é obrigatório'),
  cityAddress: z.string().nonempty('Cidade é obrigatória'),
  stateAddress: z.string().nonempty('Estado é obrigatório'),
  streetAddress: z.string().nonempty('Endereço é obrigatório'),
  numberAddress: z.string().nonempty('Número é obrigatório'),
  password: z
    .string()
    .min(8, 'A senha é muito curta')
    .nonempty('Senha é obrigatória'),
  photo: z
    .any()
    .refine((fileList) => fileList && fileList.length > 0, 'File is required')
    .refine(
      (fileList) =>
        fileList[0] && ALLOWED_MIME_TYPES.includes(fileList[0].type),
      'Only JPEG and PNG files are allowed',
    ),
})

type BusinessProfileForm = z.infer<typeof BusinessProfile>

export default function ProfileBusinessArea() {
  const token = Cookies.get('auth_token')
  const [searchParams, setSearchParams] = useSearchParams()
  const navigate = useNavigate()
  const { register, handleSubmit, reset } = useForm<BusinessProfileForm>({
    resolver: zodResolver(BusinessProfile),
  })

  const { data } = useQuery({
    queryKey: ['user', token],
    queryFn: () => getUserClient({ token }),
  })

  useEffect(() => {
    if (data) {
      reset({
        email: data.email || '',
        // fullName: '',
        photo: '', // Deixe vazio para o campo de arquivo
      })
    }
  }, [data, reset])

  async function handleEditProfile(data: BusinessProfileForm) {
    try {
      // await mutateAsync({
      //   email: data.email,
      //   photo: data.photo,
      //   token,
      // })
      console.log(data)
    } catch (error) {
      console.log(error)
    }
  }

  return (
    <>
      <div className="col-span-2 bg-primary-foreground p-10 rounded-md">
        <div className="flex justify-between">
          <h2 className="text-white text-2xl">Informações da Empresa</h2>
          <Dialog>
            <DialogTrigger className="text-white text-sm border p-2 rounded-md">
              Editar Perfil
            </DialogTrigger>
            <DialogContent>
              <Tabs defaultValue="account" className="w-full mt-4">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="account">
                    Informações da Empresa
                  </TabsTrigger>
                  <TabsTrigger value="password">Senha</TabsTrigger>
                </TabsList>
                <TabsContent value="account" className="mt-4">
                  <DialogHeader>
                    <DialogTitle>Editar Perfil</DialogTitle>
                  </DialogHeader>
                  <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                      <label htmlFor="fantasyName" className="text-right">
                        Nome Fantasia
                      </label>
                      <Input
                        id="fantasyName"
                        className="input-bordered col-span-3"
                      />
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
                      <label htmlFor="CNPJ" className="text-right">
                        CNPJ
                      </label>
                      <Input id="CNPJ" className="input-bordered col-span-3" />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <label htmlFor="phone" className="text-right">
                        Telefone Celular
                      </label>
                      <Input id="phone" className="input-bordered col-span-3" />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <label htmlFor="cep" className="text-right">
                        CEP
                      </label>
                      <Input id="cep" className="input-bordered col-span-3" />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <label htmlFor="city" className="text-right">
                        Cidade
                      </label>
                      <Input id="city" className="input-bordered col-span-3" />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <label htmlFor="street" className="text-right">
                        Endereço
                      </label>
                      <Input
                        id="street"
                        className="input-bordered col-span-3"
                      />
                    </div>
                    <div className="grid grid-cols-4 items-center gap-4">
                      <label htmlFor="number" className="text-right">
                        Número
                      </label>
                      <Input
                        id="number"
                        className="input-bordered col-span-3"
                      />
                    </div>
                  </div>
                  <DialogFooter>
                    <Button type="submit">Salvar Perfil</Button>
                  </DialogFooter>
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
        <form
          className="grid grid-cols-2 gap-4 mt-6"
          onSubmit={handleSubmit(handleEditProfile)}
        >
          <div>
            <label htmlFor="" className="text-white">
              Nome Fantasia
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('fantasyName')}
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
              CNPJ
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('cnpj')}
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
          <div>
            <label htmlFor="" className="text-white">
              CEP
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('cepAddress')}
              disabled
            />
          </div>
          <div>
            <label htmlFor="" className="text-white">
              Cidade
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('cityAddress')}
              disabled
            />
          </div>
          <div>
            <label htmlFor="" className="text-white">
              Endereço
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('streetAddress')}
              disabled
            />
          </div>
          <div>
            <label htmlFor="" className="text-white">
              Número
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('numberAddress')}
              disabled
            />
          </div>
        </form>

        <div className="flex items-end gap-4 mt-14">
          <h2 className="text-white text-2xl">Propostas</h2>
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
          <ProposalItem type="empresa" />
          <ProposalItem type="empresa" />
        </div>
        <div className="flex items-end gap-4 mt-14">
          <h2 className="text-white text-2xl">Veículos</h2>
          <span
            className="text-white text-sm font-thin cursor-pointer"
            onClick={() => {
              navigate('/profile/vehicles')
            }}
          >
            Ver Mais
          </span>

          <Plus 
            size={24}
            color="#6af42a"
            className="ml-auto cursor-pointer"
            onClick={() => navigate('/profile/add-vehicle')}
          />
        </div>

        <div className="flex flex-col gap-4 mt-4"></div>
      </div>
    </>
  )
}
