import {FC} from 'react'
import {DaysType} from '../../types'
import './style.scss'
type DayPickerProps = {
    currentDays: DaysType[] | undefined,
    setCurrentDays: (args: DaysType[]) => void,
    isRequired: boolean,
    title: string
}

const days: DaysType[] = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
const DayPicker: FC<DayPickerProps> = ({currentDays, setCurrentDays, isRequired, title}) => {

    const onClickDay = (e: React.MouseEvent, day: DaysType) => {
        e.preventDefault()
        e.stopPropagation()
        if (!currentDays) return
        if (currentDays.includes(day)) {
            setCurrentDays([])
        } else {
            setCurrentDays([day])
        }
    }

    const renderDays = () => {
        return days.map((day, index) => <button key={index} onClick={(e) => onClickDay(e, day)} className={currentDays?.includes(day) ? 'active' : ''}>{day}</button>)
    }

    const rentetLable = () => <label className={isRequired ? 'required' : ''}>{title}</label>

    return (
        <div className="DayPicker">
            {title ? rentetLable() : ''}
            <div className="week"> 
                {renderDays()}
            </div>
        </div>
    )
}

export default DayPicker