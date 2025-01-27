import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation } from '@tanstack/react-query'
import Cookies from 'js-cookie'
import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { toast } from 'sonner'
import { z } from 'zod'

import { registerVehicle } from '@/api/registerVehicle'

import { Button } from './ui/button'
import { Input } from './ui/input'

const VehicleSchema = z.object({
  name: z.string().nonempty('Nome é obrigatório'),
  licensePlate: z.string().nonempty('Placa é obrigatória'),
  costPerKm: z
    .string()
    .nonempty('Custo por km é obrigatório')
    .transform((value) => value.replace(',', '.')) // Replace comma with dot for consistency
    .refine((value) => {
      const parsedValue = parseFloat(value)
      return !isNaN(parsedValue) && /^[0-9]+(\.[0-9]+)?$/.test(value) // Ensure it's a valid number with optional decimal
    }, 'Custo por km deve ser um número válido'),
  baseCost: z
    .string()
    .nonempty('Custo base é obrigatório')
    .transform((value) => value.replace(',', '.'))
    .refine((value) => {
      const parsedValue = parseFloat(value)
      return !isNaN(parsedValue) && /^[0-9]+(\.[0-9]+)?$/.test(value) // Ensure it's a valid number with optional decimal
    }, 'Custo base deve ser um número válido'),
  color: z.string().nonempty('Cor é obrigatória'),
  year: z
    .string()
    .nonempty('Ano de fabricação é obrigatório')
    .refine((val) => !isNaN(parseInt(val)), 'Ano deve ser um número válido'),
  capacity: z
    .string()
    .nonempty('Capacidade é obrigatória')
    .refine(
      (val) => !isNaN(parseInt(val)),
      'Capacidade deve ser um número válido',
    ),
})

type vehicleForm = z.infer<typeof VehicleSchema>

export default function AddVehicleForm() {
  const token = Cookies.get('auth_token')
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<vehicleForm>({
    resolver: zodResolver(VehicleSchema),
  })

  useEffect(() => {
    if (Object.keys(errors).length > 0) {
      const firstError = Object.values(errors)[0]
      toast.error(firstError?.message)
    }
  }, [errors])

  const { mutateAsync } = useMutation({
    mutationFn: registerVehicle,
  })

  async function handleRegisterVehicle(data: vehicleForm) {
    try {
      await mutateAsync({
        token,
        name: data.name,
        licensePlate: data.licensePlate,
        costPerKm: parseFloat(data.costPerKm),
        baseCost: parseFloat(data.baseCost),
        color: data.color,
        year: parseInt(data.year),
        capacity: parseInt(data.capacity),
        photo: null,
      })
      toast.success('Veículo cadastrado com sucesso!')
    } catch (error: any) {
      const errorMessage =
        error.response?.data || error.message || 'Erro desconhecido'
      if (errorMessage?.detail) {
        toast.error(errorMessage.detail)
      } else {
        toast.error('Erro desconhecido')
      }
    }
  }

  return (
    <>
      <div className="col-span-2 bg-primary-foreground rounded-md">
        <h2 className="text-white text-2xl">Cadastro Veículo</h2>
        <form
          className="grid grid-cols-2 gap-4 mt-6"
          onSubmit={handleSubmit(handleRegisterVehicle)}
        >
          <div>
            <label htmlFor="" className="text-white">
              Nome
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('name')}
            />
          </div>
          <div>
            <label htmlFor="" className="text-white">
              Placa
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('licensePlate')}
            />
          </div>
          <div>
            <label htmlFor="" className="text-white">
              Custo por km
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('costPerKm')}
            />
          </div>
          <div>
            <label htmlFor="" className="text-white">
              Custo base
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('baseCost')}
            />
          </div>
          {/* Input para foto */}
          <div>
            <label htmlFor="" className="text-white">
              Cor
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('color')}
            />
          </div>
          <div>
            <label htmlFor="" className="text-white">
              Ano de Fabricação
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('year')}
            />
          </div>
          <div>
            <label htmlFor="" className="text-white">
              Capacidade
            </label>
            <Input
              className="input-bordered"
              type="text"
              {...register('capacity')}
            />
          </div>
          <div className="col-span-2 flex justify-center mt-4">
            <Button type="submit">Cadastrar</Button>
          </div>
        </form>
      </div>
    </>
  )
}
