import { User } from '@phosphor-icons/react'
import Cookies from 'js-cookie'
import { Outlet, useNavigate } from 'react-router'

export function AppLayout() {
  const meuCookie = Cookies.get('auth_token')
  const navigate = useNavigate()

  return (
    <div>
      <header className="flex justify-between items-center px-5 py-6 h-[96px] w-full bg-primary-foreground">
        <div className="max-w-[1240px] w-full flex justify-between items-center mx-auto px-5">
          <a className="text-white" href="/">
            LOGO
          </a>

          {meuCookie ? (
            <>
              <User
                size={32}
                color="#ffffff"
                onClick={() => navigate('/profile')}
                className="cursor-pointer"
              />
            </>
          ) : (
            <>
              <User
                size={32}
                color="#ffffff"
                onClick={() => navigate('/login')}
                className="cursor-pointer"
              />
            </>
          )}
        </div>
      </header>
      <main className="max-w-[1240px] w-full mx-auto">
        <Outlet />
      </main>
      <footer className="flex justify-between items-center px-5 py-6 h-[288px] w-full bg-primary-foreground mt-20"></footer>
    </div>
  )
}
