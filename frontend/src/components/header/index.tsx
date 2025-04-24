import {FC, useContext, useEffect, useState} from 'react'
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'
import './style.scss'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Logo from '../../assets/logo-2-en-finish.svg?react'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import LogOut from '../../assets/logout.svg?react'

import Button from '../../ui/Button'
import { UserContext } from '../../features/user'

const Header: FC = () => {
    const { user } = useContext(UserContext)
    const [lastUpdate, setLastUpdate] = useState<string>('')

    useEffect(() => {
        const update = localStorage.getItem('lastUpdate')
        if (update) {
            setLastUpdate(format(Number(update), 'HH:mm:ss', { locale: ru }))
        }
    }, [])

    return (
        <div className="header">
            <div className="left">
                <Logo className="logo"/>
                <p>{format(new Date(), 'dd MMMM yyyy', { locale: ru })}</p>
                {lastUpdate && <p className="lastUpdate">Последнее обновление: {lastUpdate}</p>}
            </div>
            {user && 
            <div className="right">
                <p>{user.is_admin ? 'Администратор' : user.project_name}</p>
                <p>{user.responsible_fio}</p>
                <Button type='icon' onClick={()=>{}}><a href='/logout'><LogOut/></a></Button>
            </div>
            }
        </div>
    )
}

export default Header