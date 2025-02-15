import {FC} from 'react'
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

interface NavigationProps {
    currentPage: string
    onPageChange: (pageName: string) => void
}
const Navigation: FC<NavigationProps> = ({currentPage, onPageChange}) => {
    return (
        <ul className="navigation">
            <li className={currentPage === 'main' ? 'active' : ''}>
                <button onClick={()=>onPageChange('main')}>
                    <UserIcon/>
                    {/* <img src="" /> */}
                </button>
            </li>
            <li className={currentPage === 'django' ? 'active' : ''}>
                <button onClick={()=>onPageChange('django')}>
                    <PanelIcon/>
                    {/* <img src="/left.png"/> */}
                </button>
            </li>
            <li className={currentPage === 'admin' ? 'active' : ''}>
                <button onClick={()=>onPageChange('admin')}>
                    <ExportIcon/>
                    {/* <img src="/left.png"/> */}
                </button>
            </li>
        </ul>
    )
}

export default Navigation