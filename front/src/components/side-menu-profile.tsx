import {
  Book,
  CarProfile,
  Link,
  Signature,
  SignOut,
  VectorTwo,
} from '@phosphor-icons/react'
import Cookies from 'js-cookie'
import { useNavigate, useSearchParams } from 'react-router'

import garcia from '../assets/garcia.jpg'
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar'

interface SideMenuProfileProps {
  fullName: string | undefined
  photo: string
  typeAccount: 'cliente' | 'empresa'
  idUsuario: number
}

export default function SideMenuProfile({
  typeAccount,
  fullName,
  idUsuario,
  photo,
}: SideMenuProfileProps) {
  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams()
  const status = searchParams.get('status')

  const url = window.location.pathname

  const isProfileActive = url === '/profile'
  const isProposalActive = url === '/profile/proposals'
  const isVehiclesActive = url === '/profile/vehicles'

  return (
    <>
      {typeAccount === 'cliente' && (
        <div className="relative h-fit w-fit flex flex-col col-span-1 bg-primary-foreground pt-8 pb-16 px-6 rounded-md text-white shadow-lg">
          <div className="flex gap-4 items-center">
            <Avatar>
              <AvatarImage src={`data:image/png;base64,${photo}`} />
              <AvatarFallback>CN</AvatarFallback>
            </Avatar>
            <span className="text-xl mt-2">{fullName}</span>
          </div>

          <nav className="w-[300px] flex flex-col items-start mt-10 text-lg ">
            <span
              className="w-full flex justify-between items-center py-2 px-2 cursor-pointer rounded-md transition-all duration-300 hover:bg-slate-700"
              onClick={() => navigate('/profile')}
            >
              Informações Pessoais
              <Book
                size={16}
                color={isProfileActive ? 'hsl(20 99% 65%)' : 'currentColor'}
              />
            </span>
            <span
              className={`w-full flex justify-between items-center py-2 px-2 cursor-pointer rounded-md transition-all duration-300 hover:bg-slate-700`}
              onClick={() => {
                navigate('/profile/proposals')
                setSearchParams((state) => {
                  state.set('status', 'all')

                  return state
                })
              }}
            >
              Propostas
              <Signature
                size={16}
                color={isProposalActive ? 'hsl(20 99% 65%)' : 'currentColor'}
              />
            </span>

            {status && (
              <div className="w-full flex flex-col items-center justify-center text-base">
                <span
                  className={`w-full flex gap-2 py-2 px-2 cursor-pointer rounded-md transition-all duration-300  ${
                    status === 'pendente'
                      ? 'bg-primary text-primary-foreground disabled font-bold'
                      : 'hover:bg-slate-600'
                  }`}
                  onClick={() =>
                    setSearchParams((state) => {
                      state.set('status', 'pendente')

                      return state
                    })
                  }
                >
                  <VectorTwo size={16} />
                  Propostas Pendentes
                </span>
                <span
                  className={`w-full flex gap-2 py-2 px-2 cursor-pointer rounded-md transition-all duration-300  ${
                    status === 'ativo'
                      ? 'bg-primary text-primary-foreground disabled font-bold'
                      : 'hover:bg-slate-600'
                  }`}
                  onClick={() =>
                    setSearchParams((state) => {
                      state.set('status', 'ativo')

                      return state
                    })
                  }
                >
                  <VectorTwo size={16} />
                  Propostas Ativas
                </span>
                <span
                  className={`w-full flex gap-2 py-2 px-2 cursor-pointer rounded-md transition-all duration-300  ${
                    status === 'rejeitado'
                      ? 'bg-primary text-primary-foreground disabled font-bold'
                      : 'hover:bg-slate-600'
                  }`}
                  onClick={() =>
                    setSearchParams((state) => {
                      state.set('status', 'rejeitado')

                      return state
                    })
                  }
                >
                  <VectorTwo size={16} />
                  Propostas Rejeitadas
                </span>
                <span
                  className={`w-full flex gap-2 py-2 px-2 cursor-pointer rounded-md transition-all duration-300  ${
                    status === 'concluido'
                      ? 'bg-primary text-primary-foreground disabled font-bold'
                      : 'hover:bg-slate-600'
                  }`}
                  onClick={() =>
                    setSearchParams((state) => {
                      state.set('status', 'concluido')

                      return state
                    })
                  }
                >
                  <VectorTwo size={16} />
                  Propostas Concluídas
                </span>
              </div>
            )}
          </nav>

          <SignOut
            size={36}
            className="absolute bottom-4 right-4 cursor-pointer p-2 rounded-xl transition-all duration-300 hover:bg-slate-700"
            color="red"
            onClick={() => {
              Cookies.remove('auth_token')
              navigate('/login')
            }}
          />
        </div>
      )}

      {typeAccount === 'empresa' && (
        <div className="relative h-fit w-fit flex flex-col col-span-1 bg-primary-foreground pt-8 pb-16 px-6 rounded-md text-white shadow-lg">
          <div className="flex gap-4 items-center">
            <Avatar>
              <AvatarImage src={garcia} />
              <AvatarFallback>CN</AvatarFallback>
            </Avatar>
            <span className="text-xl mt-2">{fullName}</span>
          </div>

          <nav className="w-[300px] flex flex-col items-start mt-10 text-lg ">
            <span
              className="w-full flex justify-between items-center py-2 px-2 cursor-pointer rounded-md transition-all duration-300 hover:bg-slate-700"
              onClick={() => navigate('/profile')}
            >
              Informações Pessoais
              <Book
                size={16}
                color={isProfileActive ? 'hsl(20 99% 65%)' : 'currentColor'}
                className="transition-all duration-300"
              />
            </span>
            <span
              className={`w-full flex justify-between items-center py-2 px-2 cursor-pointer rounded-md transition-all duration-300 hover:bg-slate-700`}
              onClick={() => {
                navigate('/profile/proposals')
                setSearchParams((state) => {
                  state.set('status', 'all')

                  return state
                })
              }}
            >
              Propostas
              <Signature
                size={16}
                color={isProposalActive ? 'hsl(20 99% 65%)' : 'currentColor'}
              />
            </span>

            {status && (
              <div className="w-full flex flex-col items-center justify-center text-base">
                <span
                  className={`w-full flex gap-2 py-2 px-2 cursor-pointer rounded-md transition-all duration-300  ${
                    status === 'pendente'
                      ? 'bg-primary text-primary-foreground disabled font-bold'
                      : 'hover:bg-slate-600'
                  }`}
                  onClick={() =>
                    setSearchParams((state) => {
                      state.set('status', 'pendente')

                      return state
                    })
                  }
                >
                  <VectorTwo size={16} />
                  Propostas Pendentes
                </span>
                <span
                  className={`w-full flex gap-2 py-2 px-2 cursor-pointer rounded-md transition-all duration-300  ${
                    status === 'ativo'
                      ? 'bg-primary text-primary-foreground disabled font-bold'
                      : 'hover:bg-slate-600'
                  }`}
                  onClick={() =>
                    setSearchParams((state) => {
                      state.set('status', 'ativo')

                      return state
                    })
                  }
                >
                  <VectorTwo size={16} />
                  Propostas Ativas
                </span>
                <span
                  className={`w-full flex gap-2 py-2 px-2 cursor-pointer rounded-md transition-all duration-300  ${
                    status === 'rejeitado'
                      ? 'bg-primary text-primary-foreground disabled font-bold'
                      : 'hover:bg-slate-600'
                  }`}
                  onClick={() =>
                    setSearchParams((state) => {
                      state.set('status', 'rejeitado')

                      return state
                    })
                  }
                >
                  <VectorTwo size={16} />
                  Propostas Rejeitadas
                </span>
                <span
                  className={`w-full flex gap-2 py-2 px-2 cursor-pointer rounded-md transition-all duration-300  ${
                    status === 'concluido'
                      ? 'bg-primary text-primary-foreground disabled font-bold'
                      : 'hover:bg-slate-600'
                  }`}
                  onClick={() =>
                    setSearchParams((state) => {
                      state.set('status', 'concluido')

                      return state
                    })
                  }
                >
                  <VectorTwo size={16} />
                  Propostas Concluídas
                </span>
              </div>
            )}
            <span
              className="w-full flex justify-between items-center py-2 px-2 cursor-pointer rounded-md transition-all duration-300 hover:bg-slate-700"
              onClick={() => navigate('/profile/vehicles')}
            >
              Meus Veículos
              <CarProfile
                size={16}
                color={isVehiclesActive ? 'hsl(20 99% 65%)' : 'currentColor'}
              />
            </span>
          </nav>

          <SignOut
            size={36}
            className="absolute bottom-4 right-4 cursor-pointer p-2 rounded-xl transition-all duration-300 hover:bg-slate-700"
            color="red"
            onClick={() => {
              Cookies.remove('auth_token')
              navigate('/login')
            }}
          />

          {typeAccount === 'empresa' && (
            <Link
              size={36}
              className="absolute top-4 right-4 cursor-pointer p-2 rounded-xl transition-all duration-300 hover:bg-slate-700"
              onClick={() => {
                navigate(`/empresa/${idUsuario}`)
              }}
            />
          )}
        </div>
      )}
    </>
  )
}
