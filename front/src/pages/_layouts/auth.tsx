import { Outlet } from 'react-router'

import logo from '../../assets/logo.jpg'

export function AuthLayout() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="flex justify-between items-center px-5 py-6 h-[96px] w-full bg-primary-foreground">
        <div className="max-w-[1240px] w-full flex justify-between items-center mx-auto px-5">
          <a className="text-white" href="/">
            <img src={logo} alt="" className="max-w-[120px] h-auto" />
          </a>
        </div>
      </header>
      <div className="max-w-[1240px] w-full mx-auto px-5">
        <Outlet />
      </div>
    </div>
  )
}
