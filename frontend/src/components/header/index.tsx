import {FC} from 'react'
import './style.scss'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Logo from '../../assets/logo-2-en-finish.svg?react'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import LogOut from '../../assets/logout.svg?react'

import Button from '../../ui/Button'


interface HeaderProps {
    date: string
    userInfo: string
    onLogout: () => void
}
const Header: FC<HeaderProps> = ({date, userInfo, onLogout}) => {
    const user = JSON.parse(userInfo || '')
    return (
        <div className="header">
            <div className="left">
                <Logo className="logo"/>
                <p>{date}</p>
            </div>
            <div className="right">
                <p>{user.isAdmin ? 'Администратор' : user.project}</p>
                <p>{user.name}</p>
                <Button type='icon'onClick={onLogout}><LogOut/></Button>
            </div>
        </div>
    )
}

export default Header