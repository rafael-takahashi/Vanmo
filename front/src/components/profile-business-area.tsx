import { zodResolver } from '@hookform/resolvers/zod'
import { Plus } from '@phosphor-icons/react'
import { useMutation, useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'
import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate, useSearchParams } from 'react-router'
import { z } from 'zod'

import { editProfileUserBusiness } from '@/api/editUserBusiness'
import { getUserBusiness } from '@/api/getUserBusiness'
import { getUserProposals } from '@/api/proposals/getUserProposals'
import { getBusinessVehicles } from '@/api/vehicles/getBusinessVehicles'

import ProposalItem from './proposal-item'
import TableProposalsBusiness from './table-proposals-business'
import TableVehicles from './table-vehicles'
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
import VehicleItem from './vehicle-item'

const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/jpg']

const BusinessProfile = z.object({
  fantasyName: z.string().optional(),
  cnpj: z.string().optional(),
  email: z.string().email().optional(),
  phone: z.string().optional(),
  cepAddress: z.string().optional(),
  cityAddress: z.string().optional(),
  stateAddress: z.string().optional(),
  streetAddress: z.string().optional(),
  numberAddress: z.string().optional(),
})

type BusinessProfileForm = z.infer<typeof BusinessProfile>

export default function ProfileBusinessArea() {
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
  const [searchParams, setSearchParams] = useSearchParams()
  const [originalData, setOriginalData] = useState<BusinessProfileForm | null>(
    null,
  )
  const navigate = useNavigate()
  const { register, handleSubmit, reset } = useForm<BusinessProfileForm>({
    resolver: zodResolver(BusinessProfile),
  })

  const { data } = useQuery({
    queryKey: ['userBusiness', token],
    queryFn: () => getUserBusiness({ token }),
  })

  // const { data: proposalsList } = useQuery({
  //   queryKey: ['proposals-user', token],
  //   queryFn: () => getUserProposals({ token }),
  // })

  const { mutateAsync } = useMutation({
    mutationFn: editProfileUserBusiness,
  })

  useEffect(() => {
    if (data) {
      const initialData = {
        email: data.email || '',
        fantasyName: data.nome_fantasia || '',
        cnpj: data.cnpj || '',
        cepAddress: data.endereco.cep || '',
        phone: data.telefone || '',
        cityAddress: data.endereco.cidade || '',
        streetAddress: data.endereco.rua || '',
        numberAddress: data.endereco.numero || '',
        stateAddress: data.endereco.uf || '',
      }

      setOriginalData(initialData) // Armazena os dados originais no estado
      reset(initialData)
      // fetchAndSetVehicles(data?.id_usuario)
    }
  }, [data, reset])

  // const [vehicles, setVehicles] = useState<any[]>([])

  // const fetchAndSetVehicles = async (businessId: number | undefined) => {
  //   setVehicles(await getBusinessVehicles(businessId, 1))
  // }

  async function handleEditProfile(data: BusinessProfileForm) {
    try {
      const updatedFields: Partial<BusinessProfileForm> = {}

      // Compara os valores atuais com os valores originais e adiciona os campos alterados
      if (data.email !== originalData?.email) updatedFields.email = data.email
      if (data.fantasyName !== originalData?.fantasyName)
        updatedFields.fantasyName = data.fantasyName
      if (data.cnpj !== originalData?.cnpj) updatedFields.cnpj = data.cnpj
      if (data.cepAddress !== originalData?.cepAddress)
        updatedFields.cepAddress = data.cepAddress
      if (data.phone !== originalData?.phone) updatedFields.phone = data.phone
      if (data.cityAddress !== originalData?.cityAddress)
        updatedFields.cityAddress = data.cityAddress
      if (data.streetAddress !== originalData?.streetAddress)
        updatedFields.streetAddress = data.streetAddress
      if (data.numberAddress !== originalData?.numberAddress)
        updatedFields.numberAddress = data.numberAddress
      if (data.stateAddress !== originalData?.stateAddress)
        updatedFields.stateAddress = data.stateAddress

      // Se houver alterações, envia apenas os campos modificados
      if (Object.keys(updatedFields).length > 0 || photo) {
        await mutateAsync({
          ...updatedFields,
          token,
          photo,
        })

        toast.success('Perfil editado com sucesso.')
      } else {
        console.log('Nenhuma alteração detectada')
      }
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <>
      <div className="flex-1 bg-primary-foreground p-10 rounded-md">
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
                  <form
                    onSubmit={handleSubmit(handleEditProfile)}
                    className="flex flex-col"
                  >
                    <div className="grid gap-4 py-4">
                      <div className="grid grid-cols-4 items-center gap-4">
                        <label htmlFor="fantasyName" className="text-right">
                          Nome Fantasia
                        </label>
                        <Input
                          id="fantasyName"
                          className="input-bordered col-span-3"
                          {...register('fantasyName')}
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
                        <label htmlFor="CNPJ" className="text-right">
                          CNPJ
                        </label>
                        <Input
                          id="CNPJ"
                          className="input-bordered col-span-3"
                          {...register('cnpj')}
                          disabled
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
                      <div className="grid grid-cols-4 items-center gap-4">
                        <label htmlFor="cep" className="text-right">
                          CEP
                        </label>
                        <Input
                          id="cep"
                          className="input-bordered col-span-3"
                          {...register('cepAddress')}
                        />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <label htmlFor="city" className="text-right">
                          Cidade
                        </label>
                        <Input
                          id="city"
                          className="input-bordered col-span-3"
                          {...register('cityAddress')}
                        />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <label htmlFor="uf" className="text-right">
                          UF
                        </label>
                        <Input
                          id="uf"
                          className="input-bordered col-span-3"
                          {...register('stateAddress')}
                        />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <label htmlFor="street" className="text-right">
                          Endereço
                        </label>
                        <Input
                          id="street"
                          className="input-bordered col-span-3"
                          {...register('streetAddress')}
                        />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <label htmlFor="number" className="text-right">
                          Número
                        </label>
                        <Input
                          id="number"
                          className="input-bordered col-span-3"
                          {...register('numberAddress')}
                        />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
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
                      </div>
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
          <TableProposalsBusiness id_usuario={data?.id_usuario} />
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
        <div className="flex flex-col gap-4 mt-4">
          <TableVehicles id_usuario={data?.id_usuario} />
        </div>

        <div className="flex flex-col gap-4 mt-4"></div>
      </div>
    </>
  )
}
