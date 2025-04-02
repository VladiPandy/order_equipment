import { FC } from 'react'
import { InputProps } from './types'
import { TextInput } from './components/TextInput'
import { NumberInput } from './components/NumberInput'
import { DropDownInput } from './components/DropDownInput'
import { CalendarInput } from './components/CalendarInput'
import './style.scss'

const Input: FC<InputProps> = (props) => {
    const { title, isRequired, withIcon, className = '' } = props

    const renderLabel = () => (
        title ? <label className={isRequired ? 'required' : ''}>{title}</label> : null
    )

    const renderInput = () => {
        switch (props.type) {
            case 'text':
            case 'textArea':
                return <TextInput {...props} />
            case 'number':
                return <NumberInput {...props} />
            case 'dropDown':
                return <DropDownInput {...props} />
            case 'calendar':
                return <CalendarInput {...props} />
            default:
                return null
        }
    }

    return (
        <div className={`Input ${withIcon ? 'withIcon' : ''} ${className}`}>
            {renderLabel()}
            {renderInput()}
        </div>
    )
}

export default Input