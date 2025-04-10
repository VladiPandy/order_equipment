import { createContext, FC, useState } from "react"
import { globalGet } from "../api/globalFetch"
import { endPoints } from "../api/endPoints"

import { users } from "../api/axiosHelper"

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

    const getNextUser = () => {
        const currUser = localStorage.getItem('user')
        const currIndex = users.findIndex((el) => el === currUser)
        
        if (users[currIndex + 1]) {
            localStorage.setItem('user', users[currIndex + 1])
        } else {
            localStorage.setItem('user', users[0])
        }
    }

    const logOut = () => {
        getNextUser()
        setUser(null)
    }

    const contextData = {
        user,
        logIn,
        logOut
    }
    
    return <UserContext.Provider value={contextData}>{children}</UserContext.Provider>
}