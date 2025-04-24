import React, { FC, useContext, useEffect } from 'react'

import Button from '../../ui/Button'
import StatusChip from '../../ui/StatusChip'
import CreateModal from '../../components/modal/CreateModal'
import Instruments from '../../ui/Instruments'
import DeleteModal from '../../components/modal/DeleteModal'

import { BookingType } from '../../types'
import './style.scss'
import { BookingsContext } from '../../features/bookingsProvider'
import { UserContext } from '../../features/user'
import { Loader } from '../../ui/Loader'
import { FiltersContext } from '../../features/filtersProvider'
import EmptyState from '../../components/EmptyState'
import EditModal from '../../components/modal/EditModal'
import { onSuccess } from '../../utils/toast'
import { FilteredDataContext } from '../../features/filteredDataProvider'
import FiltersLine from '../../components/filtersLine'

const headers = ['Проект', 'Дата бронирования', 'Анализ', 'Прибор', 'Исполнитель', 'Число образцов', 'Статус']

type SubmitDataType = {
    date?: string
    analyse?: string
    equipment?: string
    executor?: string
    samples?: number
}

const MainPage: FC = () => {
    const [isCreateModalOpen, setIsCreateModalOpen] = React.useState(false)
    const [isDeleteModalOpen, setIsDeleteModalOpen] = React.useState(false)
    const [isEditModalOpen, setIsEditModalOpen] = React.useState(false)
    const [editingItem, setEditingItem] = React.useState<number | null>(null)

    localStorage.setItem('currentPage', 'main')

    const { user } = useContext(UserContext)
    const {
        loading: bookingsLoading, 
        getBookings, 
        deleteBooking, 
        createBooking, 
        editBooking,
    } = React.useContext(BookingsContext)

    const {
        filteredBooking: bookings,
        filterBookings
    } = React.useContext(FilteredDataContext)
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
    
    const sendData = () => {
        onSuccess(isCreateModalOpen ? 'Запись успешно добавлена' : 'Запись успешно изменена')
        getFilters()
        getBookings(getFilterBody())
        setIsCreateModalOpen(false)
        setIsEditModalOpen(false)
    }

    const onSubmitData = (newEntry: SubmitDataType) => {
        createBooking({
            ...newEntry,
            status: 'start',
            comment: '',
            date: newEntry.date || '',
            analyse: newEntry.analyse || '',
            equipment: newEntry.equipment || '',
            executor: newEntry.executor || '',
            samples: String(newEntry.samples || 0),
            project: ''
        }, sendData)
    }

    const handleOpenEditModal = (editingItem: number) => {
        setIsEditModalOpen(true)
        setEditingItem(editingItem)
    }
    const handleOpenDeleteModal = (editingItem: number) => {
        setIsDeleteModalOpen(true)
        setEditingItem(editingItem)
    }

    const handleEdit = (newEntry: BookingType) => {
        editBooking(newEntry, sendData)
    }

    const handleDelete = () => {
        if (!editingItem) return
        deleteBooking(editingItem, (response: { message: string }) => {
            getFilters()
            getBookings(getFilterBody())
            setIsDeleteModalOpen(false)
            onSuccess(response.message)
        })
    }

    const renderData = (data: BookingType[]) => {
        return data.length === 0 ? <EmptyState /> : data.map((line, index) => {
            const {project, date, equipment, analyse, executor, samples, status, id, comment} = line
            return (
                <div className="table-line" key={index}>
                    <div className="table-cell">{project}</div>
                    <div className="table-cell">{date}</div>
                    <div className="table-cell">{analyse}</div>
                    <div className="table-cell">{equipment}</div>
                    <div className="table-cell">{executor}</div>
                    <div className="table-cell">{samples}</div>
                    <div className="table-cell">{status && <StatusChip id={id || 0} status={status as string}/>}</div>
                    <div className="table-cell">
                        { status && 
                            <Instruments 
                                status={status as string} 
                                id={id as number} 
                                comment={comment as string} 
                                handleEdit={() => handleOpenEditModal(id || 0)}
                                handleDelete={() => handleOpenDeleteModal(id || 0)}
                            />
                        }
                    </div>
                </div>
            )
        })
    }

    return (
        <div className="MainPageTable">
            <FiltersLine />

            {isCreateModalOpen && 
            <CreateModal onClose={()=>setIsCreateModalOpen(false)} onSubmit={onSubmitData}/> }
            {isDeleteModalOpen && 
            <DeleteModal onClose={()=>setIsDeleteModalOpen(false)} onSubmit={handleDelete}/> }
            {(isEditModalOpen && editingItem) && 
                <EditModal 
                    onClose={()=>setIsEditModalOpen(false)} 
                    onSubmit={handleEdit} 
                    editingEntry={bookings.find(booking => booking.id === editingItem) as BookingType} 
                />
            }

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