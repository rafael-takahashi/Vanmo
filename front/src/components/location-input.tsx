import { useQuery } from '@tanstack/react-query'
import { Check, ChevronsUpDown } from 'lucide-react'
import { useEffect, useState } from 'react'
import { UseFormRegister, UseFormSetValue } from 'react-hook-form'
import { useSearchParams } from 'react-router'

import { getCities } from '@/api/getCities'
import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { cn } from '@/lib/utils'

import { SearchForm } from './search-area'

interface LocationInputProps {
  register: UseFormRegister<SearchForm>
  setValue: UseFormSetValue<SearchForm>
  field: 'from' | 'to'
}

export default function LocationInput({
  register,
  setValue,
  field,
}: LocationInputProps) {
  const [open, setOpen] = useState(false)
  const [value, setValueLocal] = useState('')
  const [searchParams] = useSearchParams()

  const from = searchParams.get('from')
  const to = searchParams.get('to')

  // Carregar a lista de cidades com react-query
  const { data } = useQuery({
    queryKey: ['cities'],
    queryFn: getCities,
  })

  // Tratamento para remover as aspas extras de cada cidade
  const citiesWithoutQuotes = data
    ? data.map((city: string) => city.replace(/"/g, '')) // Remove todas as aspas duplas
    : []

  // Filtra as cidades com base no input do usuário
  const filteredCities = citiesWithoutQuotes.filter((city: string) =>
    city.toLowerCase().includes(value.toLowerCase()),
  )

  useEffect(() => {
    if (field === 'from' && from) {
      setValue(field, from)
      setValueLocal(from)
    }
    if (field === 'to' && to) {
      setValue(field, to)
      setValueLocal(to)
    }
  }, [from, to, field, setValue])

  return (
    <>
      {data ? (
        <Popover open={open} onOpenChange={setOpen}>
          <PopoverTrigger asChild>
            <Button
              variant="outline"
              role="combobox"
              aria-expanded={open}
              className="h-fit !text-base !pt-8 !pl-9 !w-[230px] flex justify-between bg-white"
            >
              {value || 'Insira uma cidade'}
              <ChevronsUpDown className="opacity-50" />
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-[200px] p-0">
            <Command>
              {/* Register aplicado no input */}
              <input
                type="text"
                placeholder="Procure uma cidade..."
                {...register(field)} // Vincula o campo ao react-hook-form
                value={value}
                onChange={(e) => setValueLocal(e.target.value)} // Atualiza o valor local
                className="w-full p-2 border rounded"
              />
              <CommandList>
                <CommandEmpty>Cidade não encontrada.</CommandEmpty>
                <CommandGroup>
                  {filteredCities.length > 0 ? (
                    filteredCities
                      .slice(0, 10)
                      .map((city: string, index: number) => (
                        <CommandItem
                          key={index}
                          value={city}
                          onSelect={(currentValue) => {
                            setValueLocal(currentValue) // Atualiza o valor local
                            setValue(field, currentValue) // Registra o valor no formulário
                            setOpen(false) // Fecha o popover após seleção
                          }}
                        >
                          {city}
                          <Check
                            className={cn(
                              'ml-auto',
                              value === city ? 'opacity-100' : 'opacity-0',
                            )}
                          />
                        </CommandItem>
                      ))
                  ) : (
                    <CommandEmpty>Cidade não encontrada.</CommandEmpty>
                  )}
                </CommandGroup>
              </CommandList>
            </Command>
          </PopoverContent>
        </Popover>
      ) : (
        <p>Carregando...</p>
      )}
    </>
  )
}
