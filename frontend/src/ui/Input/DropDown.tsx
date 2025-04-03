import { useEffect, useRef, useState } from 'react'
import './style.scss'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Arrow from '../../assets/arrow.svg?react'
import { KeyType } from '../../types'

interface DropDownProps {
    placeholder: string
    options: string[] | {[key in string]: string}
    value?: string[]
    filter: KeyType
    children?: JSX.Element
    onChange: (atr: string[], type: KeyType) => void
    isMultiple?: boolean
}

const DropDown: React.FC<DropDownProps> = ({
    placeholder,
    options,
    value = [],
    filter,
    children,
    onChange,
    isMultiple = true
}) => {
    const [selected, setSelected] = useState<string[]>(value)
    const [isOpen, setIsOpen] = useState(false)
    const dropdownRef = useRef<HTMLDivElement>(null)

    useEffect(() => setSelected(value), [value])

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsOpen(false)
            }
        }

        document.addEventListener('click', handleClickOutside, true)
        return () => document.removeEventListener('click', handleClickOutside, true)
    }, [])

    useEffect(() => {
        setIsOpen(false)
        onChange(selected, filter)
    }, [selected])

    const handleSelect = (option: string) => {
        if (option === 'Не выбран') {
            setSelected([])
            return
        }

        if (isMultiple) {
            setSelected(prev => 
                prev.includes(option)
                    ? prev.filter(item => item !== option)
                    : [...prev, option]
            )
        } else {
            if (option === selected[0]) {
                setSelected([])
            } else if (option) {
                setSelected([option])
            }
        }
    }

    const handleToggle = (e: React.MouseEvent) => {
        e.stopPropagation()
        setIsOpen(prev => !prev)
    }

    const displayValue = selected.length ? selected.join(', ') : ''

    const renderOptions = () => {
        if (Array.isArray(options)) {
            return options.map((option, index) => (
                <p
                    key={index}
                    className={selected.includes(option) ? 'active' : ''}
                    onClick={(e) => {
                        e.stopPropagation()
                        handleSelect(option)
                    }}
                >
                    {option}
                </p>
            ))
        }

        return Object.entries(options).map(([key, value]) => (
            <p
                key={key}
                className={selected.includes(value) ? 'active' : ''}
                onClick={(e) => {
                    e.stopPropagation()
                    handleSelect(value)
                }}
            >
                {value}
            </p>
        ))
    }

    return (
        <div className={`select-element ${isOpen ? 'active' : ''}`}>
            {children}
            <Arrow className='shevron' />
            <input
                readOnly
                type="text"
                placeholder={placeholder}
                onClick={handleToggle}
                value={displayValue}
            />
            {isOpen && (
                <div ref={dropdownRef} className='dropdown'>
                    {renderOptions()}
                </div>
            )}
        </div>
    )
}

export default DropDown