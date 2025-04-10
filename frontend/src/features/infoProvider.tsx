import { createContext, FC, useCallback, useState } from "react"
import { globalPost } from "../api/globalFetch"
import { endPoints } from "../api/endPoints"
import { EquipmentInfo, ExecutorInfo, FilterBodyType } from "../types"

type ContextType = {
    instruments: EquipmentInfo[],
    executors: ExecutorInfo[],
    loading: boolean,
    getInstruments: (body: FilterBodyType) => void
    getExecutors: (body: FilterBodyType) => void
}

const initialValue = {
    instruments: [],
    executors: [],
    loading: false,
    getInstruments: () => {},
    getExecutors: () => {}
}

export const InfoContext = createContext<ContextType>(initialValue)

interface PropsType {
    children: React.ReactNode
}

export const InfoProvider: FC<PropsType> = ({children}) => {
    const [instruments, setInstruments] = useState<EquipmentInfo[]>([])
    const [executors, setExecutors] = useState<ExecutorInfo[]>([])
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



    const contextData = {
        instruments,
        executors,
        loading,
        getInstruments,
        getExecutors,
    }
    
    return <InfoContext.Provider value={contextData}>{children}</InfoContext.Provider>
}