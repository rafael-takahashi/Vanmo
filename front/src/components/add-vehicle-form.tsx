import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation } from '@tanstack/react-query'
import Cookies from 'js-cookie'
import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router'
import { toast } from 'sonner'
import { z } from 'zod'

import { registerVehicle } from '@/api/registerVehicle'
import { editVehicle } from "@/api/editVehicle";
import { Input } from './ui/input'
import { Button } from './ui/button'

interface Vehicle {
    ano_fabricacao: number;
    calendario_disponibilidade: null;
    caminho_foto: null;
    capacidade: number;
    cor: string;
    custo_base: number;
    custo_por_km: number;
    id_empresa: number;
    id_veiculo: number;
    nome_veiculo: string;
    placa_veiculo: string;
  }
  
interface VehicleItemProps {
    vehicle: Vehicle;
    editMode: boolean;
}

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

export default function AddVehicleForm({ vehicle, editMode }: VehicleItemProps) {

    const navigate = useNavigate()
    
    const token = Cookies.get('auth_token')
    
    const { 
        register, 
        handleSubmit, 
        formState: { errors },
        setValue
    } = useForm<vehicleForm> ({
    resolver: zodResolver(VehicleSchema),
    })

    useEffect(() => {
        if (vehicle) {
          setValue("name", vehicle.nome_veiculo)
          setValue("licensePlate", vehicle.placa_veiculo)
          setValue("costPerKm", vehicle.custo_por_km.toString())
          setValue("baseCost", vehicle.custo_base.toString())
          setValue("color", vehicle.cor)
          setValue("year", vehicle.ano_fabricacao.toString())
          setValue("capacity", vehicle.capacidade.toString())
        }
      }, [vehicle, setValue]);
    
    useEffect(() => {
    if (Object.keys(errors).length > 0) {
      const firstError = Object.values(errors)[0]
      toast.error(firstError?.message)
    }
  }, [errors])

    const { mutateAsync } = useMutation({
        mutationFn: async (data: any) => {
            if (editMode) {
              // If in edit mode, pass the id and formData to the edit function
              return editVehicle({
                token,id: data.id,
                name: data.name,
                licensePlate: data.licensePlate,
                costPerKm: parseFloat(data.costPerKm),
                baseCost: parseFloat(data.baseCost),
                color: data.color,
                year: parseInt(data.year),
                capacity: parseInt(data.capacity),
                photo: null, // Assuming photo is optional or handled separately
              });
            } else {
              // If in register mode, pass only the formData
              return registerVehicle({
                token,
                name: data.name,
                licensePlate: data.licensePlate,
                costPerKm: parseFloat(data.costPerKm),
                baseCost: parseFloat(data.baseCost),
                color: data.color,
                year: parseInt(data.year),
                capacity: parseInt(data.capacity),
                photo: null, // Assuming photo is optional or handled separately
              });
            }
          },
    })

  async function handleRegisterVehicle(data: vehicleForm) {
    const vehicleData = {
        token,
        id: vehicle?.id_veiculo, // Only in edit mode
        name: data.name,
        licensePlate: data.licensePlate,
        costPerKm: data.costPerKm,
        baseCost: data.baseCost,
        color: data.color,
        year: data.year,
        capacity: data.capacity,
        photo: null, // If there's no photo to upload or if it's optional
    };

    try {
      await mutateAsync(vehicleData)
      toast.success('Veículo cadastrado com sucesso!')
      navigate('/profile/vehicles')
    } catch (error: any) {
      const errorMessage =
        error.response?.data || error.message || 'Erro desconhecido'
      if (errorMessage?.detail) {
        console.error(errorMessage.detail)
      } else {
        console.error('Erro desconhecido')
      }
    }
  }

  return (
    <>
        <div className="col-span-2 bg-primary-foreground rounded-md">
            <h2 className="text-white text-2xl">{editMode ? "Editar Veículo" : "Cadastrar Veículo"}</h2>
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
                    <Button type="submit">{editMode ? "Editar" : "Cadastrar"}</Button>
                </div>
            </form>
        </div>
    </>
  )
}
