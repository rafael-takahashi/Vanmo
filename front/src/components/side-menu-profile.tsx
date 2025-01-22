import Cookies from 'js-cookie'
import { useNavigate, useSearchParams } from 'react-router'

import garcia from '../assets/garcia.jpg'
import { Button } from './ui/button'

export default function SideMenuProfile() {
  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams()

  const status = searchParams.get('status')

  return (
    <div className="h-fit flex flex-col items-center col-span-1 bg-primary-foreground py-8 px-4 rounded-md text-white ">
      <div className="flex rounded-full w-[256px] h-[256px] bg-white overflow-hidden">
        <img src={garcia} className="object-cover" alt="" />
      </div>
      <span className="text-xl mt-2">USUARIO</span>

      <nav className="w-[256px] flex flex-col items-center mt-10 text-xl ">
        <span
          className="w-full py-2 text-center cursor-pointer rounded-md hover:bg-slate-600"
          onClick={() => navigate('/profile')}
        >
          Informações Pessoais
        </span>
        <div className="w-full h-[1px] bg-gray-400"></div>
        <span
          className={`w-full py-2 text-center cursor-pointer rounded-md  ${
            status ? 'disabled' : 'hover:bg-slate-600'
          }`}
          onClick={() => {
            navigate('/profile/proposals')
            setSearchParams((state) => {
              state.set('status', 'all')

              return state
            })
          }}
        >
          Minhas Propostas
        </span>

        {status && (
          <div className="w-full flex flex-col items-center justify-center text-base">
            <span
              className={`w-full py-2 text-center cursor-pointer rounded-md  ${
                status === 'active'
                  ? 'bg-primary text-primary-foreground disabled font-bold'
                  : 'hover:bg-slate-600'
              }`}
              onClick={() =>
                setSearchParams((state) => {
                  state.set('status', 'active')

                  return state
                })
              }
            >
              Propostas Ativas
            </span>
            <span
              className={`w-full py-2 text-center cursor-pointer rounded-md  ${
                status === 'rejected'
                  ? 'bg-primary text-primary-foreground disabled font-bold'
                  : 'hover:bg-slate-600'
              }`}
              onClick={() =>
                setSearchParams((state) => {
                  state.set('status', 'rejected')

                  return state
                })
              }
            >
              Propostas Rejeitadas
            </span>
            <span
              className={`w-full py-2 text-center cursor-pointer rounded-md  ${
                status === 'done'
                  ? 'bg-primary text-primary-foreground disabled font-bold'
                  : 'hover:bg-slate-600'
              }`}
              onClick={() =>
                setSearchParams((state) => {
                  state.set('status', 'done')

                  return state
                })
              }
            >
              Propostas Concluidas
            </span>
          </div>
        )}
      </nav>

      <Button
        className="mt-10"
        type="button"
        size={'sm'}
        onClick={() => {
          Cookies.remove('auth_token')
          navigate('/login')
        }}
      >
        DESCONECTAR
      </Button>
    </div>
  )
}
