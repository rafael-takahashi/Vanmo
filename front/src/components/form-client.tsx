import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router'
import { z } from 'zod'

import { registerClient } from '@/api/registerClient'

import { Button } from './ui/button'
import { Input } from './ui/input'

const registerUserPersonSchema = z.object({
  typeAccount: z.enum(['cliente', 'empresa']).default('cliente'),
  fullName: z.string().nonempty(),
  cpf: z.string().nonempty(),
  email: z.string().email().nonempty(),
  phone: z.string().nonempty(),
  password: z.string().min(8, 'A senha é muito curta').nonempty(),
  confirmPassword: z.string().min(8, 'A senha é muito curta').nonempty(),
})

type RegisterUserPersonForm = z.infer<typeof registerUserPersonSchema>

export default function FormClient({ setSuccess }: any) {
  const navigate = useNavigate()
  const { register: registerUserPerson, handleSubmit: handleSubmitUserPerson } =
    useForm<RegisterUserPersonForm>({
      resolver: zodResolver(registerUserPersonSchema),
    })

  const { mutateAsync } = useMutation({
    mutationFn: registerClient,
  })

  async function handleUserPersonRegister(data: RegisterUserPersonForm) {
    try {
      await mutateAsync({
        email: data.email,
        password: data.password,
        typeAccount: data.typeAccount,
        fullName: data.fullName,
        cpf: data.cpf,
        phone: data.phone,
      })

      setSuccess(true)

      setTimeout(() => {
        navigate('/')
      }, 3000)
    } catch (err) {
      console.log(err)
    }
  }

  return (
    <form
      className="flex flex-col gap-1 w-full focus:border-none"
      onSubmit={handleSubmitUserPerson(handleUserPersonRegister)}
    >
      <div className="grid grid-cols-4 gap-[20px] mt-[26px]">
        <Input
          type="text"
          placeholder="Nome completo*"
          className="input-bordered col-span-2 "
          {...registerUserPerson('fullName')}
        />

        <Input
          type="text"
          placeholder="CPF*"
          className="input-bordered col-span-2"
          {...registerUserPerson('cpf')}
        />

        <Input
          type="email"
          placeholder="E-mail*"
          className="input-bordered col-span-2"
          {...registerUserPerson('email')}
        />

        <Input
          type="text"
          placeholder="Telefone celular*"
          className="input-bordered col-span-2"
          {...registerUserPerson('phone')}
        />

        <Input
          type="password"
          placeholder="Crie sua senha*"
          className="input-bordered col-span-2"
          {...registerUserPerson('password')}
        />

        <Input
          type="password"
          placeholder="Confirme sua senha*"
          className="input-bordered col-span-2"
          {...registerUserPerson('confirmPassword')}
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
