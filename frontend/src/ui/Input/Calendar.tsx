import { FC, useEffect, useState, useRef } from 'react'
import Calendar from 'react-calendar'
import { format, parse } from 'date-fns'
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
    onChange: (value: DateRange, type: KeyType) => void
}

const DatePicker: FC<CalendarPropsType> = ({ value, onChange }) => {
    const [showDropdown, setShowDropdown] = useState(false)

    const ref = useRef<HTMLDivElement>(null);

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
        handleChange([
            parse(value.start, 'dd.MM.yyyy', new Date(date)),
            parse(value.end, 'dd.MM.yyyy', new Date(date.setDate(date.getDate() + 6)))
        ])
    }

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const handleChange = (value: any) => {
        if (!value || !Array.isArray(value) || value.length !== 2) return
        
        const [start, end] = value
        onChange({
            start: format(start, 'dd.MM.yyyy'),
            end: format(end, 'dd.MM.yyyy')
        }, Keys.DATE)
    }

    const getValue = (value: DateRange) => {
        return [convertDDMMYYYYToISO(value.start), convertDDMMYYYYToISO(value.end)]
    }

    return (
        <div className={`select-element ${showDropdown ? 'active' : ''}`}>
            <Arrow className='shevron'/>
            <Period/>
            <input readOnly type="text" placeholder={'Дата'} onClick={()=> setShowDropdown(st =>!st)} value={`${value.start} - ${value.end}`} />
            {showDropdown ? 
            <div ref={ref} className='dropdown'>
                <Calendar
                    onChange={handleChange}
                    defaultValue={getValue(value) as LooseValue}
                    selectRange
                    locale="ru-RU"
                    formatDay={(_, date) => format(date, 'd')}
                    showWeekNumbers
                    onClickWeekNumber={selectWeekNumber}
                />
            </div> : ''
            }
        </div>
    );
}

export default DatePicker