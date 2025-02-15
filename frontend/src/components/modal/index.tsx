import React, {FC, useEffect, useState} from 'react'
import { createPortal } from "react-dom"

import {Options, Statuses, Days} from '../../const'

import Input from '../../ui/Input'
import { DataType, DaysType } from '../../types'
import './style.scss'
import Button from '../../ui/Button'
import DayPicker from '../../ui/DayPicker'

import { getNextWeekday } from '../../utils/date-utils'
type ModalPropsType = {
    onClose: () => void
    onSubmit: (args: DataType) => void
    editingEntry?: DataType
    isEditing?: boolean
    // children: React.ReactNode
}

const Modal: FC<ModalPropsType> = ({onClose, onSubmit, editingEntry, isEditing=false}) => {
    const [project, setProject] = useState<string | undefined>(editingEntry?.name)
    const [analys, setAnalys] = useState<string[]>(editingEntry?.analyze || [])
    const [days, setDays] = useState<DaysType[]>(editingEntry?.days || [])
    const [item, setItem] = useState<string | undefined>(editingEntry?.item)
    const [executor, setExecutor] = useState<string | undefined>(editingEntry?.executor)
    const [count, setCount] = useState<number | string | undefined>(editingEntry?.sample)
    const [comment, setComment] = useState<string | undefined>(editingEntry?.comment as string)
    const [status, setStatus] = useState<string | string[] | undefined>(editingEntry?.status || Statuses.start)

    const [readyToSubmit, setReadyToSubmit] = useState(false)
    
    const handleSubmit = (e: React.FormEvent) => {
        e.stopPropagation()
        e.preventDefault()
        const date = getNextWeekday(Days.indexOf(days[0]) + 1)
        if (!project || !analys.length || !days.length || !item || !executor || !count) return
        onSubmit({
            name: project,
            date: date,
            days: days,
            analyze: analys,
            item: item,
            executor: executor,
            sample: count,
            status: status,
            comment: comment
        })
        onClose()
    }

    const resetForn = () => {
        setProject(undefined)
        setAnalys([])
        setDays([])
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
        if (project && analys.length && days.length && item && executor && count) {
            setReadyToSubmit(true)
        } else if (readyToSubmit) {
            setReadyToSubmit(false)
        }
    }, [project, analys, days, item, executor, count])

    return createPortal(
        <div className="modal" onClick={onClose}>
            <div className="content" onClick={(e) => e.stopPropagation()}>
                <form>
                    <Input 
                        placeholder={'Название проекта'} 
                        options={Options.Project} 
                        title={'Название проекта'} 
                        isRequired={true}
                        value={project}
                        setValue={(atr: string) => handleChangeField(atr, setProject as React.Dispatch<React.SetStateAction<string | string[] | undefined>>)}
                        type='dropDown'
                    />
                    <Input 
                        placeholder={'Анализ'} 
                        options={Options.Analys} 
                        title={'Анализ'} 
                        isRequired={true}
                        setValue={(atr: string) => handleChangeField(atr, setAnalys as React.Dispatch<React.SetStateAction<string | string[] | undefined>>)}
                        type='dropDown'
                        value={analys}
                        isMultiple
                    />
                    <DayPicker 
                        title={'Дата бронирования'} 
                        isRequired={true}
                        currentDays={days}
                        setCurrentDays={setDays}
                    />
                    <Input 
                        placeholder={'Прибор'} 
                        options={Options.Item} 
                        title={'Прибор'}
                        value={item} 
                        isRequired={true}
                        setValue={(atr: string) => handleChangeField(atr, setItem as React.Dispatch<React.SetStateAction<string | string[] | undefined>>)}
                        type='dropDown'
                    />
                    <Input 
                        placeholder={'Исполнитель'} 
                        options={Options.Executor} 
                        title={'Исполнитель'} 
                        isRequired={true}
                        value={executor}
                        setValue={(atr: string) => handleChangeField(atr, setExecutor as React.Dispatch<React.SetStateAction<string | string[] | undefined>>)}
                        type='dropDown'
                    />
                    <Input placeholder={'Количество'} title={'Количество'} value={count} isRequired={true} setValue={setCount} type={'number'}/>
                    { isEditing && <Input placeholder={'Комментарий'} title={'Комментарий'} value={comment} setValue={setComment} type={'textArea'}/> }

                    <div className='buttonCollection'>
                        <Button onClick={resetForn} type={'secondary'} children={'Отмена'}/>
                        <Button onClick={(e) => handleSubmit(e)} type={'primary'} children={'Подтвердить'} isActive={readyToSubmit}/>
                    </div>
                </form>
            </div>
        </div>, document.getElementById('root') as HTMLElement)
}

export default Modal