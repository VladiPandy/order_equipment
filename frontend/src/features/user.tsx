import { createContext, FC, useState } from "react"
import { globalGet } from "../api/globalFetch"
import { endPoints } from "../api/endPoints"

type UserType = {
    is_admin: boolean,
    project_name: string,
    responsible_fio: string,
    is_open: boolean
}

type ContextType = {
    user?: UserType
    logIn: () => void
}

const initialValue = {
    logIn: () => {},
}

export const UserContext = createContext<ContextType>(initialValue)

interface PropsType {
    children: React.ReactNode
}

export const UserProvider: FC<PropsType> = ({children}) => {
    const [user, setUser] = useState<UserType>()

    const logIn = async () => {
        globalGet(endPoints.auth, (data: UserType) => setUser(data))
    }

    const contextData = {
        user,
        logIn,
    }
    
    return <UserContext.Provider value={contextData}>{children}</UserContext.Provider>
}