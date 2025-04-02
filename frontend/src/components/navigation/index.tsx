import {FC, useContext} from 'react'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import UserIcon from '../../assets/user.svg?react'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import PanelIcon from '../../assets/Panel.svg?react'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import ExportIcon from '../../assets/Export.svg?react'
import './style.scss'
import { UserContext } from '../../features/user'

interface NavigationProps {
    currentPage: string
    onPageChange: (pageName: string) => void
}
const Navigation: FC<NavigationProps> = ({currentPage, onPageChange}) => {
    const { user } = useContext(UserContext)

    return (
        <ul className="navigation">
            <li className={currentPage === 'main' ? 'active' : ''}>
                <button onClick={()=>onPageChange('main')}>
                    <UserIcon/>
                </button>
            </li>
            { user?.is_admin &&
                <>
                    <li className={currentPage === 'django' ? 'active' : ''}>
                        <button onClick={()=>onPageChange('django')}>
                            <a href="/admin"><PanelIcon/></a>
                        </button>
                    </li>
                    <li className={currentPage === 'admin' ? 'active' : ''}>
                        <button onClick={()=>onPageChange('admin')}>
                            <ExportIcon/>
                        </button>
                    </li>
                </>
            }
        </ul>
    )
}

export default Navigation