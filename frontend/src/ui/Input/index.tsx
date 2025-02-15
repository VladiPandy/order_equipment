
import DropDown from './DropDown'
import DatePicker from './Calendar'
import './style.scss'

import { SimpleValueChangeType, FilterChangeType } from '../../types'

type handleChangePropsType = {
    value: string | number | string[] | undefined, 
    type?: string|undefined
}

interface InputPropsType {
    placeholder: string,
    title?: string,
    isRequired?: boolean,
    value?: string | number | string[],
    setValue: SimpleValueChangeType | FilterChangeType,
    type?: string,
    withIcon?: boolean,
    options?: {[key in string]: string},
    children?: JSX.Element,
    filter?: string,
    isMultiple?: boolean
}

const Input: React.FC<InputPropsType> = (
    {placeholder, title, value, setValue, isRequired, type, withIcon, options, children, filter, isMultiple}
) => {

    const handleChangeValue = ({value, type}: handleChangePropsType, e?: React.ChangeEvent<HTMLInputElement>) => {
        e?.preventDefault()
        if (type) {
            return(setValue as FilterChangeType)(value as string, type)
        }
        if (Number(value)) return(setValue as SimpleValueChangeType)(Number(value))
        return (setValue as SimpleValueChangeType)(value as string)
    }
    
    const renderLabel = () => <label className={isRequired ? 'required' : ''}>{title}</label>

    const renderInput = () => {
        switch (type) {
            case 'number':
                return <input 
                    onChange={e => handleChangeValue({value: e.target.value}, e)} 
                    type="number" 
                    placeholder={placeholder} 
                    value={value} />
            case 'textArea':
                return <input onChange={e => handleChangeValue({value: e.target.value}, e)} type="textArea" placeholder={placeholder} value={value} />
            case 'dropDown':
                return <DropDown placeholder={placeholder} handleSubmit={handleChangeValue} options={options} children={children} filter={filter} isMultiple={isMultiple} value={value}/>
            case 'calendar':
                return <DatePicker handleChangeValue={handleChangeValue} initialValue={value as string | string[] | undefined}/>
            default:
                return <input onChange={e => handleChangeValue({value: e.target.value}, e)} type="text" placeholder={placeholder} value={value} />
        }
    }
    
    return (
        <div className={`Input ${withIcon ? 'withIcon' : ''}`}>
            {title ? renderLabel() : ''}
            {renderInput()}
        </div>
    )
}

export default Input