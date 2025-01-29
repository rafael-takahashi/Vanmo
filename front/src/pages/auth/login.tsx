import { zodResolver } from '@hookform/resolvers/zod'
import { LockKey, SignIn, User } from '@phosphor-icons/react'
import { useMutation } from '@tanstack/react-query'
import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router'
import { toast } from 'sonner'
import { z } from 'zod'

import { signIn } from '@/api/login'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

const loginSchema = z.object({
  email: z.string().email('E-mail é inválido').nonempty('E-mail é obrigatório'),
  password: z.string().nonempty('Senha é obrigatória'),
})

type loginForm = z.infer<typeof loginSchema>

export function Login() {
  const navigate = useNavigate()
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<loginForm>({
    resolver: zodResolver(loginSchema),
  })

  useEffect(() => {
    if (Object.keys(errors).length > 0) {
      const firstError = Object.values(errors)[0]
      toast.error(firstError?.message)
    }
  }, [errors])

  const { mutateAsync: signInAccount } = useMutation({
    mutationFn: signIn,
  })

  async function handleLogin(data: loginForm) {
    try {
      await signInAccount({
        email: data.email,
        password: data.password,
      })

      navigate('/')
    } catch {
      toast.error('Credenciais inválidas.')
    }
  }

  return (
    <div
      className="w-full flex flex-col justify-center items-center"
      style={{ height: 'calc(100vh - 96px)' }}
    >
      <h1 className="text-primary font-bold text-[2rem] mb-[35px]">
        ACESSE SUA CONTA
      </h1>

      <form
        className="w-full max-w-[400px] flex flex-col gap-7"
        onSubmit={handleSubmit(handleLogin)}
      >
        <div>
          <label htmlFor="email" className="text-primary-foreground">
            Email
          </label>
          <div className="relative">
            <User
              size={24}
              weight="fill"
              className="absolute top-1/2 left-3 transform -translate-y-1/2 text-gray-500"
            />
            <Input
              type="text"
              className="!pl-10 input-bordered h-14"
              {...register('email')}
            />
          </div>
        </div>
        <div>
          <label htmlFor="password" className="text-primary-foreground">
            Senha
          </label>
          <div className="relative">
            <LockKey
              size={24}
              weight="fill"
              className="absolute top-1/2 left-3 transform -translate-y-1/2 text-gray-500"
            />
            <Input
              type="password"
              className="!pl-10 input-bordered h-14"
              {...register('password')}
            />
          </div>
        </div>

        <Button
          className="h-14 flex justify-center items-center text-xl font-semibold"
          size={'lg'}
          type="submit"
        >
          <SignIn size={36} className="" />
          <span>ENTRAR</span>
        </Button>

        <span className="underline -mt-4 ml-auto text-sm text-primary-foreground">
          Esqueceu a senha?
        </span>
      </form>

      {/* <div className="w-full max-w-[400px]">
        <div className="flex items-center gap-4 mt-5">
          <div className="h-px flex-1 bg-gray-900"></div>
          <span className="text-sm text-gray-900">OU</span>
          <div className="h-px flex-1 bg-gray-900"></div>
        </div>
      </div> */}

      <label className="mt-4 text-primary-foreground">
        Novo no Vanmo?{' '}
        <a
          className="underline text-primary font-semibold cursor-pointer"
          onClick={() => navigate('/register')}
        >
          CADASTRE-SE
        </a>
      </label>
    </div>
  )
}
