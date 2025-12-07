import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation } from '@tanstack/react-query'
import { AxiosError } from 'axios'
import { parse, subDays } from 'date-fns'
import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router'
import { toast } from 'sonner'
import { z } from 'zod'

import { registerClient } from '@/api/registerClient'

import { Button } from './ui/button'
import { Checkbox } from './ui/checkbox'
import { Input } from './ui/input'
import MaskedInput from './ui/maskedinput'

const registerUserPersonSchema = z
  .object({
    typeAccount: z.enum(['cliente', 'empresa']).default('cliente'),
    fullName: z.string().nonempty('Nome é obrigatório'),
    cpf: z.string().nonempty('CPF é obrigatório'),
    email: z
      .string()
      .email('E-mail é inválido')
      .nonempty('E-mail é obrigatório'),
    phone: z.string().nonempty('Telefone é obrigatório'),
    dateOfBirth: z.string(),
    password: z
      .string()
      .min(8, 'A senha é muito curta')
      .nonempty('Senha é obrigatória'),
    confirmPassword: z.string().nonempty('Confirme sua senha'),
    privacyTerms: z.boolean().refine((value) => value === true, {
      message: 'Você deve aceitar os termos de privacidade para continuar.',
    }),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'As senhas devem ser iguais',
  })

type RegisterUserPersonForm = z.infer<typeof registerUserPersonSchema>

interface FormClientProps {
  setSuccess: (success: boolean) => void
}

export default function FormClient({ setSuccess }: FormClientProps) {
  const navigate = useNavigate()
  const [privacyTerms, setPrivacyTerms] = useState(false)
  const {
    register: registerUserPerson,
    handleSubmit: handleSubmitUserPerson,
    formState: { errors },
    setValue,
  } = useForm<RegisterUserPersonForm>({
    resolver: zodResolver(registerUserPersonSchema),
    defaultValues: {
      privacyTerms: false,
    },
  })

  useEffect(() => {
    if (Object.keys(errors).length > 0) {
      const firstError = Object.values(errors)[0]
      toast.error(firstError?.message)
    }
  }, [errors])

  const { mutateAsync } = useMutation({
    mutationFn: registerClient,
  })

  async function handleUserPersonRegister(data: RegisterUserPersonForm) {
    try {
      const parsedDate = parse(data.dateOfBirth, 'dd/MM/yyyy', new Date())
      const dateOfBirth = subDays(parsedDate, 1)

      await mutateAsync({
        email: data.email,
        password: data.password,
        typeAccount: data.typeAccount,
        fullName: data.fullName,
        dateOfBirth,
        cpf: data.cpf,
        phone: data.phone,
      })

      setSuccess(true)

      setTimeout(() => {
        navigate('/login')
      }, 3000)
    } catch (err: unknown) {
      console.error(err)
      if (err instanceof AxiosError) {
        toast.error(err.response?.data?.detail)
      } else {
        toast.error('Erro ao cadastrar usuário')
      }
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

        <MaskedInput
          mask="(99) 99999-9999"
          type="text"
          placeholder="Telefone celular*"
          className="input-bordered col-span-1"
          {...registerUserPerson('phone')}
        />

        <MaskedInput
          id="date"
          mask="99/99/9999" // Formato de data DD/MM/YYYY
          placeholder="Data de nascimento*"
          {...registerUserPerson('dateOfBirth')}
          className="input-bordered col-span-1"
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
        <Checkbox
          id="privacyTerms"
          checked={privacyTerms}
          onCheckedChange={() => {
            const newValue = !privacyTerms
            setPrivacyTerms(newValue)
            setValue('privacyTerms', newValue)
          }}
        />
        <label htmlFor="privacyTerms" className="text-base">
          Eu li e aceito os{' '}
          <a
            href="/termos_de_privacidade.pdf"
            download
            className="underline underline-offset-4 text-primary"
          >
            Termos de privacidade
          </a>
        </label>
      </div>
      <Button
        className="font-bold px-24 text-xl py-6 max-w-[96px] mx-auto"
        size={'lg'}
        type="submit"
        disabled={!privacyTerms}
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
