import { FC } from 'react'
import { CalendarInputProps } from '../types'
import DatePicker from '../Calendar'
import { DateRange } from '../../../types'

export const CalendarInput: FC<CalendarInputProps> = ({
    value,
    setValue,
    filter
}) => {
    const handleChange = (newValue: DateRange) => {
        setValue(newValue, filter)
    }

    return (
        <DatePicker 
            value={value}
            onChange={handleChange}
        />
    )
} 