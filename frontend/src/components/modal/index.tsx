import React, {FC, useEffect, useRef, useState} from 'react'
import { createPortal } from "react-dom"

import {Statuses} from '../../const'

import Input from '../../ui/Input'
import { DataType } from '../../types'
import './style.scss'
import Button from '../../ui/Button'
import DayPicker from '../../ui/DayPicker'

import { globalGet, globalPost } from '../../api/globalFetch'
import { endPoints } from '../../api/endPoints'
import { Loader } from '../../ui/Loader'
type ModalPropsType = {
    onClose: () => void
    onSubmit: (args: DataType) => void
    editingEntry?: DataType
    isEditing?: boolean
    // children: React.ReactNode
}

const Modal: FC<ModalPropsType> = ({onClose, onSubmit, editingEntry, isEditing=false}) => {
    const [analyze, setAnalyze] = useState<string[]>(editingEntry?.analyse || [])
    const [date, setDate] = useState<string | undefined>(editingEntry?.date)
    const [item, setItem] = useState<string | undefined>(editingEntry?.equipment || undefined)
    const [executor, setExecutor] = useState<string | undefined>(editingEntry?.executor || undefined)
    const [count, setCount] = useState<number | string | undefined>(editingEntry?.samples)
    const [comment, setComment] = useState<string | undefined>(editingEntry?.comment as string)

    const [loading, setLoading] = useState(true)
    const [options, setOptions] = useState()

    const status = useRef(editingEntry?.status || Statuses.start)

    const [readyToSubmit, setReadyToSubmit] = useState(false)


    useEffect(() => {
        if (loading) {
            const body = {
                date: date || undefined,
                analyse: !Array.isArray(analyze) ? analyze : undefined,
                equipment: item?.[0] || undefined,
                executor: executor?.[0] || undefined,
                samples: count || undefined
            }
            console.log('---useEffect', body)
            console.log(executor, item)
            if (!isEditing) {
                globalPost(endPoints.createFilters, prepareFilterData, body)
            } else {
                globalPost(endPoints.editBooking, prepareFilterData, {...body, status: status.current})
            }
        }
    }, [loading, isEditing])

    const prepareFilterData = (data: string) => {
        console.log('---prepare', data)
        setLoading(false)
        // console.log(data)
        setOptions(data)
    }
    
    const handleSubmit = (e: React.FormEvent) => {
        e.stopPropagation()
        e.preventDefault()
        setLoading(true)
        // const date = getNextWeekday(Days.indexOf(days[0]) + 1)
        // if (!analyze.length || !date || !item || !executor || !count) return
        onSubmit({
            // date: date,
            day: date,
            analyze: analyze,
            item: item,
            executor: executor,
            sample: count,
            status: status.current,
            comment: comment
        })
    }

    const resetForm = () => {
        setAnalyze([])
        setDate(undefined)
        setItem(undefined)
        setExecutor(undefined)
        setCount(undefined)
        setComment(undefined)
        onClose()
    }

    const handleChangeField = (value: string, handleCh: React.Dispatch<React.SetStateAction<string | string[] | undefined>>) => {
        handleCh(value)
    }

    // функция обнуления стейта в зависимости от выбранных фиьтров
    useEffect(() => {
        setLoading(true)
        if (analyze.length && date && item && executor && count) {
            setReadyToSubmit(true)
        } else if (readyToSubmit) {
            setReadyToSubmit(false)
        }
        // eslint-disable-next-line
    }, [analyze, date, item, executor, count])

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
                    setCurrentDay={setDate}
                />
                <Input 
                    placeholder={'Анализ'} 
                    options={options?.analyse} 
                    title={'Анализ'} 
                    isRequired={true}
                    setValue={(atr: string) => handleChangeField(atr, setAnalyze as React.Dispatch<React.SetStateAction<string | string[] | undefined>>)}
                    type='dropDown'
                    value={analyze}
                    isMultiple={false}
                />
                <Input 
                    placeholder={'Прибор'} 
                    options={options?.equipment} 
                    title={'Прибор'}
                    value={item} 
                    isRequired={true}
                    setValue={(atr: string) => handleChangeField(atr, setItem as React.Dispatch<React.SetStateAction<string | string[] | undefined>>)}
                    type='dropDown'
                    isMultiple={false}
                />
                <Input 
                    placeholder={'Исполнитель'} 
                    options={options?.executor} 
                    title={'Исполнитель'} 
                    isRequired={true}
                    value={executor}
                    setValue={(atr: string) => handleChangeField(atr, setExecutor as React.Dispatch<React.SetStateAction<string | string[] | undefined>>)}
                    type='dropDown'
                    isMultiple={false}
                />
                <Input 
                    placeholder={'Количество'} 
                    title={'Количество'} 
                    value={count} 
                    isRequired={true} 
                    setValue={setCount} 
                    max={options?.samples_limit} 
                    type={'number'}
                />
                { isEditing && <Input placeholder={'Комментарий'} title={'Комментарий'} value={comment} setValue={setComment} type={'textArea'}/> }

                <div className='buttonCollection'>
                    <Button onClick={resetForm} type={'secondary'} children={'Отмена'}/>
                    <Button onClick={(e) => handleSubmit(e)} type={'primary'} children={'Подтвердить'} isActive={readyToSubmit}/>
                </div>
            </form>
            }
            </div>
        </div>, document.getElementById('root') as HTMLElement)
}

export default Modal