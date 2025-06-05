import { KeyType, DateRange, SimpleValueChangeType } from '../../types'

export type InputType = 'text' | 'number' | 'textArea' | 'dropDown' | 'calendar'

export type InputValue = string | number | string[] | DateRange | undefined

export interface BaseInputProps {
    placeholder: string
    title?: string
    isRequired?: boolean
    withIcon?: boolean
    className?: string
}

export interface TextInputProps extends BaseInputProps {
    type: 'text' | 'textArea'
    value?: string
    setValue: SimpleValueChangeType
}

export interface NumberInputProps extends BaseInputProps {
    type: 'number'
    value?: number
    setValue: SimpleValueChangeType
    max?: number
}

export interface DropDownInputProps extends BaseInputProps {
    type: 'dropDown'
    value?: string[]
    setValue: (value: string | string[], filter: KeyType) => void
    options: string[] | {[key in string]: string}
    children?: JSX.Element
    filter: KeyType
    isMultiple?: boolean
    enabled?: boolean
    isPrioritySupport?: boolean
}

export interface CalendarInputProps extends BaseInputProps {
    type: 'calendar'
    value: DateRange
    setValue: (value: DateRange, filter: KeyType) => void
    filter: KeyType,
    onlyWeek?: boolean
}

export type InputProps = 
    | TextInputProps 
    | NumberInputProps 
    | DropDownInputProps 
    | CalendarInputProps & { isPrioritySupport?: boolean }