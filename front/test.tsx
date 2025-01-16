import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

export function RegisterUser() {
  return (
    <div
      className="w-full flex flex-col justify-center items-center"
      style={{ height: 'calc(100vh - 96px)' }}
    >
      <h1 className="text-primary font-bold text-[2rem] mb-[55px]">
        CRIAR CONTA
      </h1>

      <form className="flex flex-col gap-1 w-full">
        <span>Tipo de conta</span>

        <RadioGroup className="flex items-center" defaultValue="usuario">
          <div>
            <RadioGroupItem value="usuario" />
            <span className="ml-2">Pessoa Física</span>
          </div>
          <div>
            <RadioGroupItem value="empresa" />
            <span className="ml-2">Pessoa Juridica</span>
          </div>
        </RadioGroup>

        <div className="grid grid-cols-2 gap-[20px] mt-[26px]">
          <Input
            type="email"
            placeholder="Nome completo*"
            className="input-bordered"
          />

          <Input type="text" placeholder="CPF*" className="input-bordered" />

          <Input type="text" placeholder="E-mail*" className="input-bordered" />

          <Input
            type="text"
            placeholder="Telefone celular*"
            className="input-bordered"
          />

          <Input
            type="text"
            placeholder="Crie sua senha*"
            className="input-bordered"
          />

          <Input
            type="text"
            placeholder="Confirme sua senha*"
            className="input-bordered"
          />
        </div>

        <div className="flex items-center gap-2 mt-[26px]">
          <Checkbox />
          <label>
            Li e estou de acordo com as{' '}
            <span className="underline">
              políticas da empresa e políticas de privacidade.
            </span>
          </label>
        </div>

        <div className="flex flex-col justify-center items-center gap-3 mt-[24px]">
          <Button className="font-bold px-24 text-xl py-6" size={'lg'}>
            Continuar
          </Button>
          <span className="text-sm">
            Já possui cadastro ?{' '}
            <span className="underline text-primary">ENTRAR</span>
          </span>
        </div>
      </form>
    </div>
  )
}
