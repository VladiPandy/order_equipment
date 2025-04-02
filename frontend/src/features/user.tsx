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
    user: UserType | null
    logIn: () => void
    logOut: () => void
}

const initialValue = {
    user: null,
    logIn: () => {},
    logOut: () => {}
}

export const UserContext = createContext<ContextType>(initialValue)

interface PropsType {
    children: React.ReactNode
}

export const UserProvider: FC<PropsType> = ({children}) => {
    const [user, setUser] = useState(null)

    const logIn = async () => {
        globalGet(endPoints.auth, (data: unknown) => setUser(data))
    }

    const logOut = () => {
        setUser(null)
    }

    const contextData = {
        user,
        logIn,
        logOut
    }
    
    return <UserContext.Provider value={contextData}>{children}</UserContext.Provider>
}