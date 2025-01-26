import { zodResolver } from '@hookform/resolvers/zod'
import { MagnifyingGlass, MapPin, User } from '@phosphor-icons/react'
import { format, parseISO } from 'date-fns'
import { CalendarIcon } from 'lucide-react'
import { Controller, useForm } from 'react-hook-form'
import { useNavigate, useSearchParams } from 'react-router'
import { z } from 'zod'

import { LocatioInput } from './location-input'
import { Button } from './ui/button'
import { Calendar } from './ui/calendar'
import { Input } from './ui/input'
import { Popover, PopoverContent, PopoverTrigger } from './ui/popover'

const SearchSchema = z.object({
  from: z.string(),
  to: z.string(),
  dateFrom: z.date(),
  dateTo: z.date(),
  numberPassengers: z.string(),
})

type SearchForm = z.infer<typeof SearchSchema>

export default function SearchArea() {
  const [searchParams, setSearchParams] = useSearchParams()
  const navigate = useNavigate()
  const from = searchParams.get('from')
  const to = searchParams.get('to')
  const dateFrom = searchParams.get('dateFrom')
  const dateTo = searchParams.get('dateTo')
  const numberPassengers = searchParams.get('numberPassengers')

  const { register, handleSubmit, control } = useForm<SearchForm>({
    resolver: zodResolver(SearchSchema),
    defaultValues: {
      from: from ?? '',
      to: to ?? '',
      dateFrom: dateFrom ? parseISO(dateFrom) : undefined,
      dateTo: dateTo ? parseISO(dateTo) : undefined,
      numberPassengers: numberPassengers ?? '',
    },
  })

  const url = window.location.pathname

  async function handleSearch({
    from,
    to,
    dateFrom,
    dateTo,
    numberPassengers,
  }: SearchForm) {
    if (!url.startsWith('/empresa')) {
      navigate('/search')
    }

    setSearchParams((state) => {
      if (from) {
        state.set('from', from)
      } else {
        state.delete('from')
      }

      if (to) {
        state.set('to', to)
      } else {
        state.delete('to')
      }

      if (dateFrom) {
        state.set('dateFrom', format(dateFrom, 'yyyy-MM-dd'))
      } else {
        state.delete('dateFrom')
      }

      if (dateTo) {
        state.set('dateTo', format(dateTo, 'yyyy-MM-dd'))
      } else {
        state.delete('dateTo')
      }

      if (numberPassengers) {
        state.set('numberPassengers', numberPassengers)
      } else {
        state.delete('numberPassengers')
      }

      return state
    })
  }

  return (
    <form
      onSubmit={handleSubmit(handleSearch)}
      className="w-full flex flex-col gap-4 bg-primary-foreground rounded-md p-8 mt-8"
    >
      <h2 className="text-background ml-4 text-2xl font-bold">Fretamento</h2>

      <div className="flex gap-4 justify-between">
        <div className="relative">
          <label
            htmlFor=""
            className="absolute left-10 text-xl font-semibold top-1 "
          >
            Partida
          </label>
          {/* <Input
            type="text"
            className="input-bordered h-[96px] !text-xl !pt-8 !pl-10 !w-[230px]"
            placeholder="Insira uma cidade"
            {...register('from')}
          /> */}
          <LocatioInput />
          <MapPin size={32} className="absolute top-11 left-1" />
        </div>
        <div className="relative">
          <label
            htmlFor=""
            className="absolute left-10 text-xl font-semibold top-1 "
          >
            Destino
          </label>
          {/* <Input
            type="text"
            className="input-bordered h-[96px] !text-xl !pt-8 !pl-10 !w-[230px]"
            placeholder="Insira uma cidade"
            {...register('to')}
          /> */}
          <LocatioInput />
          <MapPin size={32} className="absolute top-11 left-1" />
        </div>
        <div className="w-[600px] bg-white rounded-md flex flex-col">
          <label className="text-xl font-semibold ml-10 mt-1">
            Data de ida/retorno
          </label>
          <div className="grid grid-cols-2 mt-2 text-xl">
            <Controller
              name="dateFrom"
              control={control}
              render={({ field: { onChange, value } }) => (
                <Popover>
                  <PopoverTrigger asChild>
                    <div className="flex gap-2 cursor-pointer items-center border-none p-2 rounded">
                      <CalendarIcon />
                      <span>
                        {value ? format(value, 'PPP') : 'Selecione uma data'}
                      </span>
                    </div>
                  </PopoverTrigger>
                  <PopoverContent>
                    <Calendar
                      mode="single"
                      selected={value}
                      onSelect={(date) => {
                        if (date) {
                          onChange(date) // Atualiza o valor do campo
                        }
                      }}
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
              )}
            />
            <Controller
              name="dateTo"
              control={control}
              render={({ field: { onChange, value } }) => (
                <Popover>
                  <PopoverTrigger asChild>
                    <div className="flex gap-2 cursor-pointer items-center border-none p-2 rounded">
                      <CalendarIcon />
                      <span>
                        {value ? format(value, 'PPP') : 'Selecione uma data'}
                      </span>
                    </div>
                  </PopoverTrigger>
                  <PopoverContent>
                    <Calendar
                      mode="single"
                      selected={value}
                      onSelect={(date) => {
                        if (date) {
                          onChange(date) // Atualiza o valor do campo
                        }
                      }}
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
              )}
            />
          </div>
        </div>
        <div className="relative">
          <label
            htmlFor=""
            className="absolute left-10 text-xl font-semibold top-1 "
          >
            Passageiros
          </label>
          <Input
            type="text"
            className="input-bordered h-[96px] !text-xl !pt-8 !pl-10 !w-[180px]"
            placeholder="Qtd"
            {...register('numberPassengers')}
          />
          <User size={32} className="absolute top-11 left-1" />
        </div>
      </div>

      <Button className="w-[180px] h-auto ml-auto flex items-center justify-center py-2 px-4">
        <MagnifyingGlass
          className="text-primary-foreground"
          weight="bold"
          style={{ width: 24, height: 24 }}
        />
        <span className="text-xl font-bold">BUSCAR</span>
      </Button>
    </form>
  )
}
