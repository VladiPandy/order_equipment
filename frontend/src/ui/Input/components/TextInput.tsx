import { FC, ChangeEvent } from 'react'
import { TextInputProps } from '../types'

export const TextInput: FC<TextInputProps> = ({
    placeholder,
    value = '',
    setValue,
    type = 'text'
}) => {
    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        setValue(e.target.value)
    }

    return (
        <input 
            type={type === 'textArea' ? 'textarea' : 'text'}
            value={value}
            onChange={handleChange}
            placeholder={placeholder}
        />
    )
} 