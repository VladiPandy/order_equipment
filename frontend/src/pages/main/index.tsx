import React, { FC } from 'react'

import Button from '../../ui/Button'
import StatusChip from '../../ui/StatusChip'
import Modal from '../../components/modal'
import Instruments from '../../ui/Instruments'

import { DataType } from '../../types'
import './style.scss'

interface MainPageProps {
    data: DataType[],
    handleDataChange: (data: DataType[]) => void
}

const headers = ['Проект', 'Дата бронирования', 'Анализ', 'Прибор', 'Исполнитель', 'Число образцов', 'Статус']

const MainPage: FC<MainPageProps> = ({data, handleDataChange}) => {
    const [isCreateModalOpen, setIsCreateModalOpen] = React.useState(false)
    const [isEditModalOpen, setIsEditModalOpen] = React.useState(false)
    const [editingId, setEditingId] = React.useState<number|null>()

    const onSubmitData = (newEntry: DataType) => {
        const newData = [...data, newEntry]
        handleDataChange(newData);
    }
    
    const handleDelete = (id: number) => {
        const newData = data.filter((_, index) => index !== id)
        handleDataChange(newData);
    }
    const handleOpenEditModal = (id: number) => {
        setIsEditModalOpen(true)
        setEditingId(id)
    }

    const handleEdit = (newEntry: DataType) => {
        if (editingId){
            const newData = [...data]
            newData[editingId] = newEntry
            handleDataChange(newData);
        }
    }

    const renderData = (data: DataType[]) => {
        return data.map((line, index) => {
            const {name, date, item, analyze, executor, sample, status, comment} = line
            return (
                <div className="table-line" key={index}>
                    <div className="table-cell">{name}</div>
                    <div className="table-cell">{date}</div>
                    <div className="table-cell">{(analyze as string[]).join(', ')}</div>
                    <div className="table-cell">{item}</div>
                    <div className="table-cell">{executor}</div>
                    <div className="table-cell">{sample}</div>
                    <div className="table-cell">{status && <StatusChip status={status as string}/>}</div>
                    <div className="table-cell">
                        { status && <Instruments status={status as string} id={index} comment={comment as string} handleEdit={() => handleOpenEditModal(index)} handleDelete={handleDelete}/>}
                    </div>
                </div>
            )
        })
    }

    return (
        <div className="MainPageTable">
            {isCreateModalOpen && 
            <Modal onClose={()=>setIsCreateModalOpen(false)} onSubmit={onSubmitData}/> }
            {isEditModalOpen && editingId && 
            <Modal onClose={()=>setIsEditModalOpen(false)} onSubmit={handleEdit} editingEntry={data[editingId]} isEditing />}
            {/* {isCreateModalOpen && 
            <Modal onClose={()=>setIsCreateModalOpen(false)} onSubmit={onSubmitData}/> } */}
            <div className="table-header">
                {headers.map((header, index) => (
                    <div key={index} className="table-cell">
                        <p>{header}</p>
                    </div>
                ))}
                <div className="table-cell">
                    <Button type='secondary' onClick={() => setIsCreateModalOpen(true)}>Добавить запись</Button>
                </div>
            </div>
            <div className="table-body">
                {renderData(data)}
            </div>
        </div>
    )
}

export default MainPage