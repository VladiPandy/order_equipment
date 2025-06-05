import { FC } from 'react'
import { DropDownInputProps } from '../types'
import DropDown from '../DropDown'
import { KeyType } from '../../../types'

export const DropDownInput: FC<DropDownInputProps> = ({
    placeholder,
    options,
    children,
    filter,
    value = [],
    setValue,
    isPrioritySupport,
    isMultiple = true,
    enabled = true,
}) => {
    const handleChange = (newValue: string | string[], filter: string) => {
        setValue(newValue, filter as KeyType)
    }

    return (
        <DropDown 
            placeholder={placeholder}
            options={options}
            children={children}
            filter={filter}
            value={value}
            onChange={handleChange}
            isMultiple={isMultiple}
            enabled={enabled}
            isPrioritySupport={isPrioritySupport}
        />
    )
} 