import { createContext, FC, useContext, useEffect, useRef, useState } from "react"
import { BookingType, DateRange, Filters, EquipmentInfo, ExecutorInfo } from "../types"
import { parse, isWithinInterval } from 'date-fns'
import { BookingsContext } from "./bookingsProvider"
import { FiltersContext } from "./filtersProvider"
import { InfoContext } from "./infoProvider"

type ContextType = {
    filteredBooking: BookingType[],
    filteredInstruments: EquipmentInfo[],
    filteredExecutors: ExecutorInfo[],
    filterBookings: (filters: Filters) => void,
    filterExecutors: (filters: Filters) => void,
    filterInstruments: (filters: Filters) => void,
}

const initialValue = {
    filteredBooking: [],
    filteredInstruments: [],
    filteredExecutors: [],
    filterBookings: () => {},
    filterExecutors: () => {},
    filterInstruments: () => {},
}

export const FilteredDataContext = createContext<ContextType>(initialValue)

interface PropsType {
    children: React.ReactNode
}

export const FilteredDataProvider: FC<PropsType> = ({children}) => {
    const [filteredBooking, setFilteredBooking] = useState<BookingType[]>([])
    const [filteredInstruments, setFilteredInstruments] = useState<EquipmentInfo[]>([])
    const [filteredExecutors, setFilteredExecutors] = useState<ExecutorInfo[]>([])

    const {
        bookings,
        getBookings
    } = useContext(BookingsContext)
    const {
        instruments,
        executors,
        getInstruments,
        getExecutors
    } = useContext(InfoContext)
    const { filters } = useContext(FiltersContext)

    const prevDate = useRef(filters.date)

    const instrumentsDateRef = useRef(filters.date)
    const executorsDateRef = useRef(filters.date)
    const bookingsDateRef = useRef(filters.date)

    const filterOnDate = (value: string, getter: (date: DateRange) => void) => {
        const bookingDate = parse(value as string, 'dd.MM.yyyy', new Date())
        const startDate = parse(filters.date.start, 'dd.MM.yyyy', new Date())
        const endDate = parse(filters.date.end, 'dd.MM.yyyy', new Date())
        
        const prevStartDate = parse(prevDate.current.start, 'dd.MM.yyyy', new Date())
        const prevEndDate = parse(prevDate.current.end, 'dd.MM.yyyy', new Date())
        
        if (startDate < prevStartDate || endDate > prevEndDate) {
            getter(filters.date)
            prevDate.current = filters.date
            return false
        }
        
        return isWithinInterval(bookingDate, { start: startDate, end: endDate })
    }

    useEffect(() => {
        filterBookings(filters)
    }, [bookings, filters])
    useEffect(() => {
        filterInstruments(filters)
    }, [instruments, filters])
    useEffect(() => {
        filterExecutors(filters)
    }, [executors, filters])

    const filterBookings = (filters: Filters) => {
        if (filters.date.start !== bookingsDateRef.current.start || filters.date.end !== bookingsDateRef.current.end) {
            bookingsDateRef.current = filters.date
            getBookings(filters.date)
        } else {
            const filtered = bookings.filter((booking) => {
                return Object.entries(booking).reduce((acc, [key, value]) => {
                    if (!acc) return false
    
                    if (key in filters) {
                        const filterValue = filters[key as keyof Filters]
                        if (key === 'date') {
                            return filterOnDate(value as string, getBookings)
                        }
                        if (Array.isArray(filterValue)) {
                            if (!filterValue.length) return true
                            if (filterValue.includes(value as string)) return true
                        }
                        return false
                    }
                    return true
                }, true)
            })
            setFilteredBooking(filtered)
        }
    }

    const filterInstruments = (filters: Filters) => {
        const { date } = filters
        setFilteredInstruments(instruments)
        if (date.start !== instrumentsDateRef.current.start || date.end !== instrumentsDateRef.current.end) {
            instrumentsDateRef.current = date
            getInstruments(date)
        }
    }

    const filterExecutors = (filters: Filters) => {
        const { date } = filters
        setFilteredExecutors(executors)
        if (date.start !== executorsDateRef.current.start || date.end !== executorsDateRef.current.end) {
            executorsDateRef.current = date
            getExecutors(date)
        }
    }

    const contextData = {
        filteredBooking,
        filteredInstruments,
        filteredExecutors,
        filterBookings,
        filterExecutors,
        filterInstruments,
    }
    
    return <FilteredDataContext.Provider value={contextData}>{children}</FilteredDataContext.Provider>
}