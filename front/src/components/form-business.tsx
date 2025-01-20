import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation, useQuery } from '@tanstack/react-query'
import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router'
import { z } from 'zod'

import { registerBusiness } from '@/api/registerBusiness'
import { searchCEP, searchCepResponse } from '@/api/searchCEP'

import { Button } from './ui/button'
import { Input } from './ui/input'

const registerUserBusinessSchema = z.object({
  typeAccount: z.enum(['cliente', 'empresa']).default('empresa'),
  fantasyName: z.string().nonempty(),
  cnpj: z.string().nonempty(),
  email: z.string().email().nonempty(),
  phone: z.string().nonempty(),
  cepAddress: z.string().nonempty(),
  cityAddress: z.string().nonempty(),
  stateAddress: z.string().nonempty(),
  streetAddress: z.string().nonempty(),
  numberAddress: z.string().nonempty(),
  password: z.string().min(8, 'A senha é muito curta').nonempty(),
  confirmPassword: z.string().min(8, 'A senha é muito curta').nonempty(),
})

type RegisterUserBusinessForm = z.infer<typeof registerUserBusinessSchema>

export default function FormBusiness() {
  const navigate = useNavigate()
  const {
    register: registerUserBusiness,
    handleSubmit: handleSubmitUserBusiness,
    watch,
    setValue,
  } = useForm<RegisterUserBusinessForm>({
    resolver: zodResolver(registerUserBusinessSchema),
  })

  const cep = watch('cepAddress')

  const { mutateAsync } = useMutation({
    mutationFn: registerBusiness,
  })

  const { data } = useQuery<searchCepResponse, Error>({
    queryKey: ['searchCEP', cep], // Chave única baseada no CEP
    queryFn: () => searchCEP({ cep }), // Função para buscar o CEP
    enabled: !!cep && cep.length === 8, // Só executa se o CEP tiver 8 dígitos
  })

  useEffect(() => {
    if (data) {
      setValue('cityAddress', data.localidade)
      setValue('stateAddress', data.estado)
      setValue('streetAddress', data.logradouro)
    }
  }, [data, setValue])

  async function handleUserBusinessRegister(data: RegisterUserBusinessForm) {
    try {
      await mutateAsync({
        cep: data.cepAddress,
        cityAddress: data.cityAddress,
        cnpj: data.cnpj,
        email: data.email,
        fantasyName: data.fantasyName,
        numberAddress: data.numberAddress,
        password: data.password,
        phone: data.phone,
        stateAddress: data.stateAddress,
        streetAddress: data.streetAddress,
        typeAccount: data.typeAccount,
      })
    } catch (err) {
      console.log(err)
    }
  }

  return (
    <form
      className="flex flex-col gap-1 w-full"
      onSubmit={handleSubmitUserBusiness(handleUserBusinessRegister)}
    >
      <div className="grid grid-cols-4 gap-[20px] mt-[26px]">
        <Input
          type="text"
          placeholder="Nome fantasia*"
          className="input-bordered col-span-2"
          {...registerUserBusiness('fantasyName')}
        />

        <Input
          type="text"
          placeholder="CNPJ*"
          className="input-bordered col-span-2"
          {...registerUserBusiness('cnpj')}
        />

        <Input
          type="email"
          placeholder="E-mail*"
          className="input-bordered col-span-2"
          {...registerUserBusiness('email')}
        />

        <Input
          type="text"
          placeholder="Telefone para contato*"
          className="input-bordered col-span-2"
          {...registerUserBusiness('phone')}
        />

        <Input
          type="text"
          placeholder="CEP*"
          className="input-bordered col-span-2"
          {...registerUserBusiness('cepAddress')}
        />

        <Input
          type="text"
          placeholder="Cidade*"
          className="input-bordered"
          {...registerUserBusiness('cityAddress')}
        />

        <Input
          type="text"
          placeholder="Estado*"
          className="input-bordered"
          {...registerUserBusiness('stateAddress')}
        />

        <Input
          type="text"
          placeholder="Endereço*"
          className="input-bordered col-span-3"
          {...registerUserBusiness('streetAddress')}
        />

        <Input
          type="text"
          placeholder="Número*"
          className="input-bordered col-span-1"
          {...registerUserBusiness('numberAddress')}
        />

        <Input
          type="password"
          placeholder="Crie sua senha*"
          className="input-bordered col-span-2"
          {...registerUserBusiness('password')}
        />

        <Input
          type="password"
          placeholder="Confirme sua senha*"
          className="input-bordered col-span-2"
          {...registerUserBusiness('confirmPassword')}
        />
      </div>

      <div className="flex items-center gap-2 mt-[32px] mb-[16px]">
        <label className="text-base">
          Ao continuar, você concorda com nossos{' '}
          <a href="" className="underline underline-offset-4 text-primary">
            termos de serviço
          </a>{' '}
          e{' '}
          <a href="" className="underline underline-offset-4 text-primary">
            políticas de privacidade
          </a>
          .
        </label>
      </div>
      <Button
        className="font-bold px-24 text-xl py-6 max-w-[96px] mx-auto"
        size={'lg'}
        type="submit"
      >
        Continuar
      </Button>

      <div className="flex flex-col justify-center items-center gap-3 mt-[16px]">
        <span className="text-sm text-primary-foreground">
          Já possui cadastro?{' '}
          <span
            className="underline text-primary cursor-pointer"
            onClick={() => navigate('/login')}
          >
            ENTRAR
          </span>
        </span>
      </div>
    </form>
  )
}
