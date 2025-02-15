import { useState, FC, useEffect, useRef } from 'react';
import Calendar from 'react-calendar';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import type { Value } from 'react-calendar/dist/cjs/shared/types';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Arrow from '../../assets/arrow.svg?react'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Period from '../../assets/period.svg?react'
import 'react-calendar/dist/Calendar.css';

import { formatDateToDDMMYYYY, formatDateToYYYYMMDD, getDaysOfWeek } from '../../utils/date-utils'

function arraysAreEqual(arr1: string[], arr2: string[]) {
    if (arr1.length !== arr2.length) {
        return false;
    }
  
    for (let i = 0; i < arr1.length; i++) {
        if (arr1[i] !== arr2[i]) {
            return false;
        }
    }
  
    return true;
  }

type handleChangePropsType = {
    value: Value, 
    type: string|undefined
}

type CalendarPropsType = {
    handleChangeValue: ({value, type}: handleChangePropsType, e?: React.ChangeEvent<HTMLInputElement>) => void
    initialValue?: string | string[] | undefined
}

const DatePicker: FC<CalendarPropsType> = ({handleChangeValue, initialValue}) => {
    const [showDropdown, setShowDropdown] = useState(false)
    const [value, setValue] = useState<string | string[] | undefined>()

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

    const onChange = (value: Value) => {
        setValue(formatDateToYYYYMMDD(value[0]))
    }

    const selectWeekNumber = (week: number, date: Date) => {
        const days = getDaysOfWeek(week, date.getFullYear())
        const dataForView = days.map(day => formatDateToYYYYMMDD(day))
        const dataForFilter = days.map(day => formatDateToDDMMYYYY(day))
        if (arraysAreEqual(initialValue as string[], dataForFilter)) {
            setValue(undefined);
            handleChangeValue({value: [], type: 'date'})
            return
        }
        handleChangeValue({value: dataForFilter, type: 'date'})
        setValue([dataForView[0], dataForView[dataForView.length - 1]])
    }

    const getValue = (): string => {
        if (!initialValue?.length) return ''
        if (Array.isArray(initialValue)) {
            return `${initialValue[0]} - ${initialValue[initialValue.length - 1]}`
        }
        return `${initialValue}`
    }

    return (
    <div className={`selec-element ${showDropdown ? 'active' : ''}`}>
        <Arrow className='shevron'/>
        <Period/>
        <input readOnly type="text" placeholder={'Дата'} onClick={()=> setShowDropdown(st =>!st)} value={getValue()} />
        {showDropdown ? 
        <div ref={ref} className='dropdown'>
            <Calendar
                onChange={onChange}
                value={value as Value}
                // selectRange
                showWeekNumbers
                // activeStartDate={Array.isArray(value) ? new Date(value[0]) : undefined}
                onClickWeekNumber={selectWeekNumber}
            />
        </div> : ''
        }
    </div>
    );
}

export default DatePicker