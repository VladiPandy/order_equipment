import { FC, ChangeEvent, useEffect, useState } from 'react'
import { NumberInputProps } from '../types'
import { useThrottle } from '../../../hooks/useThrottle'

export const NumberInput: FC<NumberInputProps> = ({
    placeholder,
    value,
    setValue,
    max
}) => {
    const [inputValue, setInputValue] = useState<number | undefined>(value)
    
    const throttledChange = useThrottle(() => setValue(Number(inputValue)))

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        setInputValue(Number(e.target.value))
    }
    
    useEffect(() => throttledChange(), [inputValue])
    

    return (
        <input 
            type="number"
            value={inputValue}
            onChange={handleChange}
            placeholder={placeholder}
            max={max}
            disabled={!max || max <= 0}
            min={1}
        />
    )
} 