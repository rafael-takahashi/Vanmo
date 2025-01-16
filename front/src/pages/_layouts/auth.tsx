import { Outlet } from 'react-router'

export function AuthLayout() {
  return (
    <div>
      <header className="flex justify-between items-center px-[100px] py-[24px] h-[96px] w-full bg-primary-foreground">
        <h1 className="text-white">LOGO</h1>
      </header>
      <div className="max-w-[1240px] w-full mx-auto px-5">
        <Outlet />
      </div>
    </div>
  )
}
