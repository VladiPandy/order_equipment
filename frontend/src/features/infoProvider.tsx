import { createContext, FC, useCallback, useState } from "react"
import { globalPost } from "../api/globalFetch"
import { endPoints } from "../api/endPoints"
import { EquipmentInfo, ExecutorInfo, FilterBodyType, RatingRow } from "../types"

type ContextType = {
    instruments: EquipmentInfo[],
    executors: ExecutorInfo[],

    ratings: RatingRow[],

    loading: boolean,
    getInstruments: (body: FilterBodyType) => void
    getExecutors: (body: FilterBodyType) => void
    getRatings: (body: FilterBodyType) => void
}

const initialValue: ContextType = {
    instruments: [],
    executors: [],
    ratings: [],

    loading: false,
    getInstruments: () => {},
    getExecutors: () => {},

    getRatings: () => {},
}

export const InfoContext = createContext<ContextType>(initialValue)

interface PropsType {
    children: React.ReactNode
}

export const InfoProvider: FC<PropsType> = ({children}) => {
    const [instruments, setInstruments] = useState<EquipmentInfo[]>([])
    const [executors, setExecutors] = useState<ExecutorInfo[]>([])
    const [ratings, setRatings] = useState<RatingRow[]>([])
    const [loading, setLoading] = useState<boolean>(false)

    const getInstruments = useCallback((body: FilterBodyType) => {
        setLoading(true)
        if (loading) return
        globalPost(endPoints.infoEquipment, (response: EquipmentInfo[]) => {
            setInstruments(response)
            setLoading(false)
            return response
        }, body)
    }, [])

    const getExecutors = useCallback((body: FilterBodyType) => {
        setLoading(true)
        if (loading) return
        globalPost(endPoints.infoExecutor, (response: ExecutorInfo[]) => {
            setExecutors(response)
            setLoading(false)
            return response
        }, body)
    }, [])

    const getRatings = useCallback((body: FilterBodyType) => {
        setLoading(true)
        globalPost(endPoints.infoRatings, (response: RatingRow[]) => {
            setRatings(response)
            setLoading(false)
            return response
        }, body)
    }, [])

    const contextData = {
        instruments,
        executors,
        ratings,
        loading,
        getInstruments,
        getExecutors,
        getRatings,
    }

    return <InfoContext.Provider value={contextData}>{children}</InfoContext.Provider>
}