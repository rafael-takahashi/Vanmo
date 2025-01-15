import { useState } from 'react'

import FormBusiness from '@/components/form-business'
import FormClient from '@/components/form-client'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

export function RegisterUser() {
  const [accountType, setAccountType] = useState<'cliente' | 'empresa'>(
    'cliente',
  )

  return (
    <div
      className="w-full flex flex-col justify-center items-center"
      style={{ height: 'calc(100vh - 96px)' }}
    >
      <h1 className="text-primary font-bold text-[2rem] mb-[55px]">
        CRIAR CONTA
      </h1>

      <div className="flex flex-col gap-1 w-full">
        <span>Tipo de conta</span>

        <RadioGroup
          className="flex items-center gap-4"
          defaultValue="cliente"
          onValueChange={(value) =>
            setAccountType(value as 'cliente' | 'empresa')
          }
        >
          <div>
            <RadioGroupItem value="cliente" id="cliente" />
            <label htmlFor="cliente" className="ml-2">
              Pessoa Física
            </label>
          </div>
          <div>
            <RadioGroupItem value="empresa" id="empresa" />
            <label htmlFor="empresa" className="ml-2">
              Pessoa Jurídica
            </label>
          </div>
        </RadioGroup>
      </div>

      <div className="w-full">
        {accountType === 'cliente' ? <FormClient /> : <FormBusiness />}
      </div>
    </div>
  )
}
