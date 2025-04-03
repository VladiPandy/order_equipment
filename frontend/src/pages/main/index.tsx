import React, { FC, useContext, useEffect } from 'react'

import Button from '../../ui/Button'
import StatusChip from '../../ui/StatusChip'
import CreateModal from '../../components/modal/CreateModal'
import Instruments from '../../ui/Instruments'

import { DataType } from '../../types'
import './style.scss'
import { BookingsContext } from '../../features/bookingsProvider'
import { UserContext } from '../../features/user'
import { Loader } from '../../ui/Loader'
import { FiltersContext } from '../../features/filtersProvider'
import EmptyState from '../../components/EmptyState'
import EditModal from '../../components/modal/EditModal'
import { onSuccess } from '../../utils/toast'

const headers = ['Проект', 'Дата бронирования', 'Анализ', 'Прибор', 'Исполнитель', 'Число образцов', 'Статус']

const MainPage: FC = () => {
    const [isCreateModalOpen, setIsCreateModalOpen] = React.useState(false)
    const [isEditModalOpen, setIsEditModalOpen] = React.useState(false)
    const [editingItem, setEditingItem] = React.useState<number|null>()

    const { user } = useContext(UserContext)
    const {
        bookings, 
        loading: bookingsLoading, 
        getBookings, 
        deleteBooking, 
        createBooking, 
        editBooking,
        filterBookings
    } = React.useContext(BookingsContext)
    const {getFilters, filters, getFilterBody} = React.useContext(FiltersContext)

    useEffect(() => {
        getFilters()
        getBookings(getFilterBody())
        const timer = setInterval(() => {
            getFilters()
            getBookings(getFilterBody())
        }, 1000 * 60 * 10)
        return () => clearInterval(timer)
    }, [])

    useEffect(() => {
        if (bookingsLoading) {
            getBookings(getFilterBody())
        }

        filterBookings(filters)
    }, [filters])
    
    const sendData = (body: any) => {
        if (body.id >= 0) {
            onSuccess(isCreateModalOpen ? 'Запись успешно добавлена' : 'Запись успешно изменена')
            getBookings(getFilterBody())
            setIsCreateModalOpen(false)
            setIsEditModalOpen(false)
        }
    }

    const onSubmitData = (newEntry: DataType) => {
        createBooking(newEntry, sendData)
    }

    const handleOpenEditModal = (editingItem) => {
        setIsEditModalOpen(true)
        setEditingItem(editingItem)
    }

    const handleEdit = (newEntry: DataType) => {
        if (editingItem) {
            editBooking(newEntry, sendData)
        }
    }

    const handleDelete = (id: number) => {
        deleteBooking(id, (response: any) => {
            getBookings(getFilterBody())
            onSuccess(response.message);
        })
    }

    const renderData = (data) => {
        return data.length === 0 ? <EmptyState /> : data.map((line, index) => {
            const {project, date, equipment, analyse, executor, samples, status, comment, id} = line
            return (
                <div className="table-line" key={index}>
                    <div className="table-cell">{project}</div>
                    <div className="table-cell">{date}</div>
                    <div className="table-cell">{analyse}</div>
                    <div className="table-cell">{equipment}</div>
                    <div className="table-cell">{executor}</div>
                    <div className="table-cell">{samples}</div>
                    <div className="table-cell">{status && <StatusChip id={id} status={status as string}/>}</div>
                    <div className="table-cell">
                        { status && 
                            <Instruments 
                                status={status as string} 
                                id={id as number} 
                                comment={comment as string} 
                                handleEdit={() => handleOpenEditModal(line)} 
                                handleDelete={() => handleDelete(id)}
                            />
                        }
                    </div>
                </div>
            )
        })
    }

    return (
        <div className="MainPageTable">
            {isCreateModalOpen && 
            <CreateModal onClose={()=>setIsCreateModalOpen(false)} onSubmit={onSubmitData}/> }
            {(isEditModalOpen && editingItem) && 
            <EditModal onClose={()=>setIsEditModalOpen(false)} onSubmit={handleEdit} editingEntry={editingItem} />}
            {/* {isCreateModalOpen && 
            <Modal onClose={()=>setIsCreateModalOpen(false)} onSubmit={onSubmitData}/> } */}
            <div className="table-header">
                {headers.map((header, index) => (
                    <div key={index} className="table-cell">
                        <p>{header}</p>
                    </div>
                ))}
                <div className="table-cell">
                    <Button type='secondary' isActive={user?.is_open} onClick={() => setIsCreateModalOpen(true)}>Добавить запись</Button>
                </div>
            </div>
            <div className="table-body">
                {bookingsLoading ? <Loader/> : renderData(bookings)}
            </div>
        </div>
    )
}

export default MainPage