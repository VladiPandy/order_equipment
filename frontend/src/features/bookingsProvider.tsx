import { createContext, FC, useCallback, useEffect, useState } from "react"
// import { Filters } from "../types"
import { globalDelete, globalPost } from "../api/globalFetch"
import { endPoints } from "../api/endPoints"
import { BookingType, FilterBodyType } from "../types"
import { parse, isWithinInterval } from 'date-fns'

type ContextType = {
    bookings: BookingType[], 
    loading: boolean,
    isFiltered: boolean,
    getBookings: (body: FilterBodyType) => void
    createBooking: (body: BookingType, callback: () => void) => void
    editBooking: (body: BookingType, callback: () => void) => void
    filterBookings: (body: BookingType[]) => void,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    deleteBooking: (id: number, callback: (response: any) => void) => void
    feedbackBooking: (feedback: any, callback: () => void) => void
}

const initialValue = {
    bookings: [],
    loading: false,
    isFiltered: false,
    filterBookings: () => {},
    getBookings: () => {},
    createBooking: () => {},
    editBooking: () => {},
    deleteBooking: () => {},
    feedbackBooking: () => {}
}

export const BookingsContext = createContext<ContextType>(initialValue)

interface PropsType {
    children: React.ReactNode
}

export const BookingsProvider: FC<PropsType> = ({children}) => {
    const [data, setData] = useState<BookingType[]>([])
    const [filteredBooking, setFilteredBooking] = useState<BookingType[]>([])
    const [loading, setLoading] = useState<boolean>(false)
    const [isFiltered, setIsFiltered] = useState<boolean>(false)

    useEffect(() => {
        setFilteredBooking(data)
        setIsFiltered(true)
    }, [data])

    const getBookings = useCallback((body: FilterBodyType) => {
        setLoading(true)
        if (loading) return
        globalPost(endPoints.booking, (response: BookingType[]) => {
            localStorage.setItem('lastUpdate', Date.now().toString())
            setData(response)
            setLoading(false)
            return response
        }, body)
    }, [])

    const createBooking = useCallback((newEntry: BookingType, callback: (response: BookingType) => void) => {
        const body = {
            analyse: newEntry.analyse,
            date: newEntry.date,
            equipment: newEntry.equipment,
            executor: newEntry.executor,
            samples: newEntry.samples
        }
        globalPost(endPoints.newBooking, callback, body)
    }, [])

    const editBooking = useCallback((newEntry: BookingType, callback: (response: BookingType) => void) => {
        const body = {
            id: newEntry.id,
            project: newEntry.project,
            date: newEntry.date,
            analyse: newEntry.analyse,
            equipment: newEntry.equipment,
            executor: newEntry.executor,
            samples: newEntry.samples,
            status: newEntry.status,
            comment: newEntry.comment
        }
        globalPost(endPoints.editBooking, callback, body)
    }, [])

    const feedbackBooking = useCallback((feedback: any, callback: (response: BookingType) => void) => {
        globalPost(endPoints.feedback, callback, feedback)
    }, [])
    

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const deleteBooking = useCallback((id: number, callback: (response: any) => void) => {
        globalDelete(endPoints.deleteBooking, (response: BookingType[]) => {
            callback(response)
        }, {id})
    }, [])

    const filterBookings = (filters) => {
        const filtered = data.filter((booking) => {
            return Object.entries(booking).reduce((acc, [key, value]) => {
                if (!acc) return false
                
                if (key === 'date') {
                    const bookingDate = parse(value, 'dd.MM.yyyy', new Date())
                    const startDate = parse(filters.date.start, 'dd.MM.yyyy', new Date())
                    const endDate = parse(filters.date.end, 'dd.MM.yyyy', new Date())
                    return isWithinInterval(bookingDate, { start: startDate, end: endDate })
                }

                if (!filters[key]?.length) return true
                if (filters[key].includes(value)) return true
                return false
            }, true)
        })
        setFilteredBooking(filtered)
    }

    const contextData = {
        bookings: filteredBooking,
        loading,
        isFiltered,
        filterBookings,
        getBookings,
        createBooking,
        editBooking,
        deleteBooking,
        feedbackBooking
    }
    
    return <BookingsContext.Provider value={contextData}>{children}</BookingsContext.Provider>
}