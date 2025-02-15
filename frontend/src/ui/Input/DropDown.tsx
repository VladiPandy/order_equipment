import { useEffect, useRef, useState } from 'react'
import './style.scss'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Arrow from '../../assets/arrow.svg?react'

type handleSubmitPropsType = {
    value: string | number | string[] | undefined, 
    type: string|undefined
}

interface InputPropsType {
    placeholder: string,
    options: {[key in string]: string} | undefined,
    handleSubmit: ({value, type}: handleSubmitPropsType, e?: React.ChangeEvent<HTMLInputElement>) => void,
    children?: JSX.Element,
    filter?: string
    isMultiple?: boolean,
    value?: number | string | string[]
}
type Selected = string[] | string | number | undefined


const Input: React.FC<InputPropsType> = ({placeholder, options, handleSubmit, children, filter, isMultiple, value}) => {
    const [selected, setSelected] = useState<Selected>(value)
    const [showDropdown, setShowDropdown] = useState(false)

    const ref = useRef<HTMLDivElement>(null);

    const handleClickOutside = (event: MouseEvent) => {
        if (ref.current && !ref.current.contains(event.target as Node)) {
            setShowDropdown(false);
        }
    };
    
    useEffect(()=>{
        setShowDropdown(false)
        handleSubmit({value: selected, type: filter})
    }, [selected])

    const handleSelected = (e: React.MouseEvent, value: string) => {
        e.stopPropagation()
        e.preventDefault()
        if (isMultiple && Array.isArray(selected)) {
            if (value === 'Не выбран') setSelected([])
            else if (selected?.includes(value)) setSelected(selected.filter(item => item !== value))
            else setSelected([...selected, value])
        } else if (!isMultiple) {
            if (value === 'Не выбран' || selected === value) setSelected(undefined)
            else setSelected(value)
        }
    }

    useEffect(() => {
        document.addEventListener('click', handleClickOutside, true);
    
        return () => {
          document.removeEventListener('click', handleClickOutside, true);
        };
      }, []);

    const handleStichDropdownShow = (e: React.MouseEvent) => {
        e.stopPropagation()
        e.preventDefault()
        setShowDropdown(st =>!st)
    }

    
    const renderOptions = (options: {[key in string]: string}) => {
        const optionsItems = []
        for(const key of Object.keys(options)) {
            optionsItems.push(
                <p 
                    key={key} 
                    className={selected === options[key] || ( selected && Array.isArray(selected) && selected?.includes(options[key])) ? 'active' : ''} 
                    onClick={(e)=>handleSelected(e, options[key])}
                >
                    {options[key]}
                </p>
            )
        }
        return optionsItems
    }

    const valueRender = () => {
        if ((selected || (Array.isArray(selected) && selected.length)) && !value) return ''
        if (isMultiple && Array.isArray(selected)) {
            if (selected.length) {
                return selected.join(', ')
            }
            return ''
        }
        return selected || ''
    }

    return (
        <div className={`selec-element ${showDropdown ? 'active' : ''}`}>
            {children}
            <Arrow className='shevron'/>
            <input readOnly type="text" placeholder={placeholder} onClick={handleStichDropdownShow} value={valueRender()} />
            {showDropdown ? 
            <div ref={ref} className='dropdown'>
                {options && renderOptions(options)}
            </div> : ''
            }
        </div>
    )
}

export default Input