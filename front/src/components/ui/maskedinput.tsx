import React from 'react'
import InputMask from 'react-input-mask'

import { Input } from '@/components/ui/input'

interface MaskedInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  mask: string
}

const MaskedInput = React.forwardRef<HTMLInputElement, MaskedInputProps>(
  ({ mask, ...props }, ref) => {
    return (
      <InputMask mask={mask} {...props}>
        {(inputProps) => <Input {...inputProps} ref={ref} />}
      </InputMask>
    )
  },
)

MaskedInput.displayName = 'MaskedInput'

export default MaskedInput
