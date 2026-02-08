import { createContext, FC, useContext,useCallback, useEffect, useRef, useState } from "react"
import { BookingType, DateRange,RatingRow, Filters, EquipmentInfo, ExecutorInfo } from "../types"
import { parse, isWithinInterval } from 'date-fns'
import { BookingsContext } from "./bookingsProvider"
import { FiltersContext } from "./filtersProvider"
import { InfoContext } from "./infoProvider"

type ContextType = {
    filteredBooking: BookingType[],
    filteredInstruments: EquipmentInfo[],
    filteredExecutors: ExecutorInfo[],
    // filteredRatings: RatingRow[],
    filteredRatings: RatingRow[],

    filterBookings: (filters: Filters) => void,
    filterExecutors: (filters: Filters) => void,
    filterInstruments: (filters: Filters) => void,
    loadRatings: () => Promise<void>,
}

const initialValue = {
    filteredBooking: [],
    filteredInstruments: [],
    filteredExecutors: [],
    filteredRatings: [],

    filterBookings: () => {},
    filterExecutors: () => {},
    filterInstruments: () => {},

    loadRatings: async () => {},
}

export const FilteredDataContext = createContext<ContextType>(initialValue)

interface PropsType {
    children: React.ReactNode
}

export const FilteredDataProvider: FC<PropsType> = ({children}) => {
    const [filteredBooking, setFilteredBooking] = useState<BookingType[]>([])
    const [filteredInstruments, setFilteredInstruments] = useState<EquipmentInfo[]>([])
    const [filteredExecutors, setFilteredExecutors] = useState<ExecutorInfo[]>([])
    const [filteredRatings, setFilteredRatings] = useState<RatingRow[]>([])

    const {
        bookings,
        getBookings
    } = useContext(BookingsContext)
    const {
        instruments,
        executors,
        ratings,
        getInstruments,
        getExecutors,
        getRatings,
    } = useContext(InfoContext)
    const { filters, getFilterBody } = useContext(FiltersContext)


    const prevDate = useRef(filters.date)

    const instrumentsDateRef = useRef(filters.date)
    const executorsDateRef = useRef(filters.date)
    const bookingsDateRef = useRef(filters.date)

    const filterOnDate = (value: string) => {
        const bookingDate = parse(value, 'dd.MM.yyyy', new Date())
        const startDate = parse(filters.date.start, 'dd.MM.yyyy', new Date())
        const endDate = parse(filters.date.end, 'dd.MM.yyyy', new Date())

        const prevStartDate = parse(prevDate.current.start, 'dd.MM.yyyy', new Date())
        const prevEndDate = parse(prevDate.current.end, 'dd.MM.yyyy', new Date())

        if (startDate < prevStartDate || endDate > prevEndDate) {
            getBookings(getFilterBody())
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

    useEffect(() => {
        setFilteredRatings(
            (ratings ?? []).map((r) => ({
                executor: r.executor,
                avgTotal: r.avg_total,
                avgOnTime: r.avg_on_time,
                avgFullSet: r.avg_full_set,
                avgQuality: r.avg_quality,
                totalAnswerAnalyses: r.total_answer_analyses,
                totalAnalyses: r.total_analyses,
            }))
        )
    }, [ratings])

    const filterBookings = (filters: Filters) => {
        if (filters.date.start !== bookingsDateRef.current.start || filters.date.end !== bookingsDateRef.current.end) {
            bookingsDateRef.current = filters.date
            getBookings(getFilterBody())
        } else {
            const filtered = bookings.filter((booking) => {
                return Object.entries(booking).reduce((acc, [key, value]) => {
                    if (!acc) return false
    
                    if (key in filters) {
                        const filterValue = filters[key as keyof Filters]
                        if (key === 'date') {
                            return filterOnDate(value as string)
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

    const loadRatings = useCallback(async (): Promise<void> => {
        const date = getFilterBody()
        await getRatings(date)
    }, [getFilterBody, getRatings])

    const contextData = {
        filteredBooking,
        filteredInstruments,
        filteredExecutors,
        filteredRatings,
        filterBookings,
        filterExecutors,
        filterInstruments,
        loadRatings,
    }
    
    return <FilteredDataContext.Provider value={contextData}>{children}</FilteredDataContext.Provider>
}