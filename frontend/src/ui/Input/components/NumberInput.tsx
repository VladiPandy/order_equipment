import { FC, ChangeEvent, useState, useEffect } from 'react'
import { NumberInputProps } from '../types'

import '../style.scss'

export const NumberInput: FC<NumberInputProps> = ({
    placeholder,
    value,
    setValue,
    max
}) => {
    const [inputValue, setInputValue] = useState<number | undefined>(value)
    const [isCorrect, setIsCorrect] = useState<boolean>(Number(max) >= Number(value || 0))

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        const newIsCorrect = Number(max) >= Number(e.target.value)
        if (newIsCorrect) setInputValue(Number(e.target.value))
        setIsCorrect(newIsCorrect)
    }

    useEffect(() => setValue(Number(inputValue)), [inputValue])
    
    return (
        <input 
            className={`${!isCorrect ? 'blocked' : ''}`}
            type="number"
            value={inputValue || ''}
            onChange={handleChange}
            placeholder={placeholder}
            max={max}
            min={1}
        />
    )
} 