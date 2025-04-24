import { FC, useEffect, useState, useRef } from 'react'
import Calendar from 'react-calendar'
import { endOfWeek, format, startOfWeek, Day, addWeeks } from 'date-fns'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Arrow from '../../assets/arrow.svg?react'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Period from '../../assets/period.svg?react'
import { DateRange, Keys, KeyType } from '../../types'
import 'react-calendar/dist/Calendar.css';
import { convertDDMMYYYYToISO } from '../../utils/date-utils'
import { LooseValue } from 'react-calendar/src/shared/types.js'

interface CalendarPropsType {
    value: DateRange
    onlyWeek?: boolean
    onChange: (value: DateRange, type: KeyType) => void
}

const DatePicker: FC<CalendarPropsType> = ({ value, onChange, onlyWeek = false }) => {
    const [renderValue, setRenderValue] = useState<DateRange>(value)
    const [showDropdown, setShowDropdown] = useState(false)

    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (onlyWeek) {
            const nextWeek = addWeeks(new Date(), 1);
            const startOfNextWeek = format(startOfWeek(nextWeek, {weekStartsOn: 1 as Day}), 'dd.MM.yyyy');
            const endOfNextWeek = format(endOfWeek(nextWeek, {weekStartsOn: 1 as Day}), 'dd.MM.yyyy');
            onChange({
                start: startOfNextWeek,
                end: endOfNextWeek
            }, Keys.DATE)
        }
    }, [])

    const handleClickOutside = (event: MouseEvent) => {
        if (ref.current && !ref.current.contains(event.target as Node)) {
            setShowDropdown(false);
        }
    };

    useEffect(() => {
        document.addEventListener('click', handleClickOutside, true);
    
        return () => {
          document.removeEventListener('click', handleClickOutside, true);
        };
    }, []);

    const selectWeekNumber = (_: number, date: Date) => {
        const options = { weekStartsOn: 1 as Day }
        handleChange([
            startOfWeek(date, options),
            endOfWeek(date, options)
        ])
    }

    const selectDay = (date: Date) => {
        if (onlyWeek) {
            selectWeekNumber(0, date)
        }
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handleChange = (value: any) => {
        if (!value || !Array.isArray(value) || value.length !== 2) return
        
        const [start, end] = value

        const newValue = {
            start: format(start, 'dd.MM.yyyy'),
            end: format(end, 'dd.MM.yyyy')
        }
        onChange(newValue, Keys.DATE)
        setRenderValue(newValue)
    }

    const getValue = (value: DateRange) => {
        const val = [convertDDMMYYYYToISO(value.start), convertDDMMYYYYToISO(value.end)]
        return val
    }

    return (
        <div className={`select-element ${showDropdown ? 'active' : ''}`}>
            <Arrow className='shevron'/>
            <Period/>
            <input readOnly type="text" placeholder={'Дата'} onClick={()=> setShowDropdown(st =>!st)} value={`${renderValue.start} - ${renderValue.end}`} />
            {showDropdown ? 
            <div ref={ref} className='dropdown'>
                <Calendar
                    onChange={handleChange}
                    defaultValue={getValue(renderValue) as LooseValue}
                    value={getValue(renderValue) as LooseValue}
                    selectRange={!onlyWeek}
                    locale="ru-RU"
                    formatDay={(_, date) => format(date, 'd')}
                    showWeekNumbers
                    onClickWeekNumber={selectWeekNumber}
                    onClickDay={selectDay}
                />
            </div> : ''
            }
        </div>
    );
}

export default DatePicker