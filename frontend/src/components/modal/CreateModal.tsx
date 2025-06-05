import React, { FC, useEffect, useState } from 'react'
import { createPortal } from "react-dom"
import { FilterChangeType, OptionsType } from '../../types'
import './style.scss'
import Input from '../../ui/Input'
import Button from '../../ui/Button'
import DayPicker from '../../ui/DayPicker'
import { globalPost } from '../../api/globalFetch'
import { endPoints } from '../../api/endPoints'
import { Loader } from '../../ui/Loader'

type CreateProps = {
    onClose: () => void
    onSubmit: (args: SubmitDataType) => void
}

type SubmitDataType = {
    date?: string
    analyse?: string
    equipment?: string
    executor?: string
    samples?: number
}

type API_FilterType = {
    date: {[key: string]: 0 | 1 | 2}
    analyse: {[key: string]: string}
    equipment: {[key: string]: string}
    executor: {[key: string]: string}
    samples: number
    used: number
    is_priority: {[key: string]: string}
}

const CreateModal: FC<CreateProps> = ({ onClose, onSubmit }) => {
    const [analyze, setAnalyze] = useState<string>()
    const [date, setDate] = useState<string>()
    const [item, setItem] = useState<string>()
    const [executor, setExecutor] = useState<string>()
    const [count, setCount] = useState<number>()
    
    const [loading, setLoading] = useState(true)
    const [sending, setSending] = useState(false)
    const [options, setOptions] = useState<OptionsType>()
    const [readyToSubmit, setReadyToSubmit] = useState(false)

    const [hasPriorityExecutor, setHasPriorityExecutor] = useState(false)

    useEffect(() => {
        if (loading) {
            const body = {
                date: date || undefined,
                analyse: analyze || undefined,
                equipment: item || undefined,
                executor: executor || undefined,
                samples: count || undefined
            }
            globalPost(endPoints.createFilters, prepareFilterData, body)
        }
    }, [loading])

    const prepareFilterData = (data: API_FilterType) => {
        const options = {} as OptionsType
        Object.entries(data).forEach(([key, value]) => {
            switch(key) {
                case 'samples_limit':
                case 'used':
                    options[key] = value as number
                    break
                case 'date':
                    options[key] = value as {[key: string]: 0 | 1 | 2}
                    break
                case 'executor':
                    options[key] = Object.entries(value).map(([id, name]) => {
                        if (data.is_priority?.[id] === 'True') {
                            setHasPriorityExecutor(true)
                        }
                        return {
                            name,
                            isPriority: data.is_priority?.[id] === 'True'
                        }})
                    break
                default:
                    options[key] = [] as string[]
                    Object.entries(value).forEach(([, value]) => {
                        if (Array.isArray(options[key])) {
                            (options[key] as string[]).push(value)
                        }
                    })
                    break
            }
        })
        setLoading(false)

        setOptions(options)
    }
    
    const handleSubmit = (e: React.FormEvent) => {
        e.stopPropagation()
        e.preventDefault()
        setSending(true)
        onSubmit({
            date: date,
            analyse: analyze,
            equipment: item,
            executor: executor,
            samples: count,
        })
    }

    const resetForm = () => {
        setAnalyze(undefined)
        setDate(undefined)
        setItem(undefined)
        setExecutor(undefined)
        setCount(undefined)
        onClose()
    }

    const handleChangeField: FilterChangeType = (value, type) => {
        switch(type) {
            case 'analyse':
                setAnalyze(value[0])
                break
            case 'equipment':
                setItem(value[0])
                break
            case 'executor':
                setExecutor(value[0])
                break
            case 'sample':
                setCount(value ? Number(value) : undefined)
                break
            case 'date':
                setDate(value as string)
                break
            default:
                break
        }
    }

    useEffect(() => {
        setLoading(true)
        if (analyze && date && item && executor && count) {
            setReadyToSubmit(true)
        } else if (readyToSubmit) {
            setReadyToSubmit(false)
        }
    }, [analyze, date, item, executor])
    useEffect(() => {
        if (analyze && date && item && executor && count) {
            setReadyToSubmit(true)
        } else if (readyToSubmit) {
            setReadyToSubmit(false)
        }
    }, [count])

    const handleDateChange = (value: string | undefined) => {
        setDate(value || '')
    }

    return createPortal(
        <div className="modal" onClick={onClose}>
            <div className="content" onClick={(e) => e.stopPropagation()}>
            {loading || sending ? <Loader /> : 
            <form>
                <DayPicker 
                    title={'Дата бронирования'} 
                    isRequired={true}
                    availableDates={options?.date}
                    currentDay={date}
                    setCurrentDay={handleDateChange}
                />
                <Input 
                    placeholder={'Анализ'} 
                    options={options?.analyse as string[]} 
                    title={'Анализ'} 
                    isRequired={true}
                    setValue={handleChangeField}
                    type='dropDown'
                    value={analyze ? [analyze] : []}
                    filter='analyse'
                    isMultiple={false}
                />
                <Input 
                    placeholder={'Прибор'} 
                    options={options?.equipment as string[]} 
                    title={'Прибор'}
                    value={item ? [item] : []} 
                    isRequired={true}
                    setValue={handleChangeField}
                    type='dropDown'
                    filter='equipment'
                    isMultiple={false}
                />
                <Input 
                    placeholder={'Исполнитель'} 
                    options={options?.executor as string[]} 
                    title={'Исполнитель'} 
                    isRequired={true}
                    value={executor ? [executor] : []}
                    setValue={handleChangeField}
                    type='dropDown'
                    filter='executor'
                    isMultiple={false}
                    isPrioritySupport={hasPriorityExecutor}
                />
                <Input 
                    placeholder={`Количество (макс. ${options?.samples_limit})`} 
                    title={`Количество (макс. ${options?.samples_limit})`} 
                    value={count} 
                    isRequired={true} 
                    setValue={(value) => setCount(value ? Number(value) : undefined)} 
                    type={'number'}
                    max={options?.samples_limit} 
                />

                <div className='buttonCollection'>
                    <Button onClick={resetForm} type={'secondary'} children={'Отмена'}/>
                    <Button onClick={(e) => handleSubmit(e)} type={'primary'} children={'Подтвердить'} isActive={readyToSubmit}/>
                </div>
            </form>
            }
            </div>
        </div>, 
        document.getElementById('root') as HTMLElement
    )
}

export default CreateModal 