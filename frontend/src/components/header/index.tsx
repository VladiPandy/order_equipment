import {FC} from 'react'
import './style.scss'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Logo from '../../assets/logo-2-en-finish.svg?react'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import LogOut from '../../assets/logout.svg?react'

import Button from '../../ui/Button'
import { HeaderInfo } from "../../types";

interface HeaderProps {
    date: string;
    userInfo?: string; // можно оставить, если нужно
    headerInfo?: HeaderInfo;
    onLogout: () => void;
}

const Header: FC<HeaderProps> = ({ date, userInfo, headerInfo, onLogout }) => {
    const info = headerInfo || (userInfo ? JSON.parse(userInfo) : {});
    return (
        <div className="header">
            <div className="left">
                <Logo className="logo" />
                <p>{date}</p>
            </div>
            <div className="right">
                <p>
                    {info.is_admin === 1
                        ? `Администратор (${info.responsible_fio})`
                        : `${info.project_name} (${info.responsible_fio})`}
                </p>
                <Button type="icon" onClick={onLogout}>
                    <LogOut />
                </Button>
            </div>
        </div>
    );
};

export default Header;