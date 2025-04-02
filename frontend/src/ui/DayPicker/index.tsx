import {FC} from 'react'
import {DaysType} from '../../types'
import './style.scss'

type DayPickerProps = {
    currentDay: string | undefined,
    setCurrentDay: (args?: string) => void,
    isRequired: boolean,
    title: string,
    availableDates?: { [key: string]: boolean }
}

const days: DaysType[] = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
const DayPicker: FC<DayPickerProps> = ({currentDay, setCurrentDay, isRequired, title, availableDates}) => {



    const onClickDay = (e: React.MouseEvent, day: string, isAvailable: boolean) => {
        e.preventDefault()
        e.stopPropagation()
        if (!isAvailable) return
        if (currentDay === day) {
            setCurrentDay()
        } else {
            setCurrentDay(day)
        }
    }

    const renderDays = () => {
        return Object.entries(availableDates || {}).map(([key, value], index) => 
            <button 
                key={key} 
                onClick={(e) => onClickDay(e, key, value)} 
                className={`${currentDay?.includes(key) ? 'active' : ''} ${!value ? 'disabled' : ''}`}
            >
                {days[index]}
            </button>
        )
    }

    const renderLabel = () => (
        <label 
            className={isRequired ? 'required' : ''}>
                {title} c {Object.keys(availableDates || {})[0]} по {Object.keys(availableDates || {})[6]}
        </label>
    )

    return (
        <div className="DayPicker">
            {title ? renderLabel() : ''}
            <div className="week"> 
                {renderDays()}
            </div>
        </div>
    )
}

export default DayPicker