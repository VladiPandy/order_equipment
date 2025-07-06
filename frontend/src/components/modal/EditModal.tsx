import React, { FC, useEffect, useState } from 'react'
import { createPortal } from "react-dom"
import { BookingType, FilterBodyType, FilterChangeType, OptionsType } from '../../types'
import './style.scss'
import Input from '../../ui/Input'
import Button from '../../ui/Button'
import DayPicker from '../../ui/DayPicker'
import { globalPost } from '../../api/globalFetch'
import { endPoints } from '../../api/endPoints'
import { Loader } from '../../ui/Loader'

import {Statuses_2} from '../../const'
import {Statuses} from '../../const'

type EditModalProps = {
    onClose: () => void
    onSubmit: (args: BookingType) => void
    editingEntry: BookingType
}

const EditModal: FC<EditModalProps> = ({ onClose, onSubmit, editingEntry }) => {
    const [analyze, setAnalyze] = useState<string>(editingEntry.analyse)
    const [date, setDate] = useState<string>(editingEntry.date)
    const [item, setItem] = useState<string>(editingEntry.equipment)
    const [executor, setExecutor] = useState<string>(editingEntry.executor)
    const [count, setCount] = useState<number>(Number(editingEntry.samples))
    const [comment, setComment] = useState<string>(editingEntry.comment)
    
    const [loading, setLoading] = useState(true)
    const [status, setStatus] = useState(editingEntry.status)

    const [options, setOptions] = useState<OptionsType>()
    const [readyToSubmit, setReadyToSubmit] = useState(false)

    const [hasPriorityExecutor, setHasPriorityExecutor] = useState(false)

    useEffect(() => {
        if (loading) {
            const body = {
                id: editingEntry.id,
                start: date,
                end: date,
                analyse: analyze || undefined,
                equipment: item || undefined,
                executor: executor || undefined,
                samples: String(count) || undefined,
                status: status
            }
            globalPost(endPoints.checkEditBooking, prepareFilterData, body)
        }
    }, [loading, date, analyze, item, executor])

    const prepareFilterData = (data: FilterBodyType) => {
        setLoading(false)
        const options = {} as OptionsType
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-expect-error
        Object.entries(data.change).forEach(([key, value]) => {
            switch(key) {
                case 'executor':
                    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
                    // @ts-expect-error
                    options[key] = Object.entries(value).map(([id, name]) => {
                        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
                        // @ts-expect-error
                        if (data.is_priority?.[id] === 'True') {
                            setHasPriorityExecutor(true)
                        }
                        return {
                            name,
                            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
                            // @ts-expect-error
                            isPriority: data.is_priority?.[id] === 'True'
                        }
                    })
                    break
                default:
                    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
                    // @ts-expect-error
                    options[key] = value
                    break
            }
        })
        
        setOptions(options)
    }
    
    const handleSubmit = (e: React.FormEvent) => {
        e.stopPropagation()
        e.preventDefault()
        setLoading(true)
        
        onSubmit({
            date: date,
            analyse: analyze,
            equipment: item,
            executor: executor,
            samples: `${count}`,
            comment,
            status: status,
            id: editingEntry.id,
            project: editingEntry.project
        })
    }

    const resetForm = () => {
        setAnalyze(editingEntry.analyse)
        setDate(editingEntry.date)
        setItem(editingEntry.equipment)
        setExecutor(editingEntry.executor)
        setCount(Number(editingEntry.samples))
        setComment(editingEntry.comment)
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
            case 'status':
                setStatus(value[0])
                break
            case 'sample':
                setCount(Number(value))
                break
            case 'date':
                setDate(value[0])
                break
        }
    }

    useEffect(() => {
        setLoading(true)
        if (analyze && date && item && executor && count >= 0) {
            setReadyToSubmit(true)
        } else if (readyToSubmit) {
            setReadyToSubmit(false)
        }
    }, [analyze, date, item, executor, readyToSubmit])

    useEffect(() => {
        if (analyze && date && item && executor && count >= 0) {
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
            {loading ? <Loader /> : 
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
                    value={[analyze]}
                    filter='analyse'
                    isMultiple={false}
                />
                <Input 
                    placeholder={'Прибор'} 
                    options={options?.equipment as string[]} 
                    title={'Прибор'}
                    value={[item]} 
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
                    value={[executor]}
                    setValue={handleChangeField}
                    type='dropDown'
                    filter='executor'
                    isMultiple={false}
                    isPrioritySupport={hasPriorityExecutor}
                />
                <Input 
                    placeholder={'Статус'} 
                    options={Statuses_2}
                    title={'Статус'} 
                    isRequired={true}
                    value={[status]}
                    setValue={handleChangeField}
                    type='dropDown'
                    filter='status'
                    isMultiple={false}
                />
                <Input 
                    placeholder={`Количество (макс. ${options?.samples_limit})`} 
                    title={`Количество (макс. ${options?.samples_limit})`} 
                    value={count} 
                    isRequired={true} 
                    setValue={(value) => setCount(Number(value))} 
                    type={'number'}
                    max={options?.samples_limit} 
                />
                <Input 
                    placeholder={'Комментарий'} 
                    title={'Комментарий'} 
                    value={comment} 
                    setValue={(value) => setComment(String(value))} 
                    type={'textArea'}
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

export default EditModal 