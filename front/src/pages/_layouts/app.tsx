import { User } from '@phosphor-icons/react'
import { useQuery } from '@tanstack/react-query'
import Cookies from 'js-cookie'
import { Search } from 'lucide-react'
import { useState } from 'react'
import { Outlet, useNavigate } from 'react-router'

import { fetchBusinessByName } from '@/api/fetchBusinessByName'
import { Avatar } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import { Dialog, DialogContent, DialogTrigger } from '@/components/ui/dialog'

import logo from '../../assets/logo.jpg'

export function AppLayout() {
  const [nameSearch, setNameSearch] = useState('')
  const auth = Cookies.get('auth_token')
  const navigate = useNavigate()

  const { data, isLoading, isError } = useQuery({
    queryKey: ['buscarEmpresas', nameSearch],
    queryFn: () => fetchBusinessByName({ nome: nameSearch }),
    enabled: nameSearch.trim().length > 0,
    retry: false,
  })

  return (
    <div className="flex flex-col min-h-screen">
      <header className="flex justify-between items-center px-5 py-6 h-[96px] w-full bg-primary-foreground">
        <div className="max-w-[1240px] w-full flex justify-between items-center mx-auto px-5">
          <a className="text-white" href="/">
            <img src={logo} alt="" className="max-w-[120px] h-auto" />
          </a>

          <div className="flex justify-center items-center gap-8">
            <Dialog>
              <DialogTrigger asChild>
                <Button
                  variant="secondary"
                  className="flex justify-center items-center bg-slate-500 py-0 h-9 px-3 "
                >
                  <Search />
                  <span className="mt-1">Procurar empresa...</span>
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-transparent border-none p-0">
                <Command className="rounded-lg border shadow-md">
                  <CommandInput
                    placeholder="Digite o nome da empresa..."
                    value={nameSearch}
                    onValueChange={(value) => setNameSearch(value)}
                  />
                  <CommandList>
                    {isLoading ? (
                      <CommandEmpty>Carregando...</CommandEmpty>
                    ) : isError ? (
                      <CommandEmpty>Erro ao buscar empresas.</CommandEmpty>
                    ) : !data || data.length === 0 ? (
                      <CommandEmpty>Não foi encontrado a empresa.</CommandEmpty>
                    ) : (
                      <CommandGroup heading="Sugestões">
                        {data.slice(0, 5).map((empresa) => (
                          <CommandItem key={empresa.id}>
                            <a href={`/empresa/${empresa.nome_fantasia}`}>
                              <Avatar />
                              <span>{empresa.nome_fantasia}</span>
                            </a>
                          </CommandItem>
                        ))}
                      </CommandGroup>
                    )}
                  </CommandList>
                </Command>
              </DialogContent>
            </Dialog>

            {auth ? (
              <User
                size={32}
                color="#ffffff"
                onClick={() => navigate('/profile')}
                className="cursor-pointer"
              />
            ) : (
              <User
                size={32}
                color="#ffffff"
                onClick={() => navigate('/login')}
                className="cursor-pointer"
              />
            )}
          </div>
        </div>
      </header>
      <main className="flex-grow max-w-[1440px] w-full mx-auto">
        <Outlet />
      </main>
      <footer className="flex justify-between items-center px-5 py-6 h-[288px] w-full bg-primary-foreground mt-20"></footer>
    </div>
  )
}
