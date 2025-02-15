import { FC } from 'react'
import './style.scss'

import {Statuses} from '../../const'
interface StatusChipPropsType {
    status: string
}
const getStatusStyle = (status: string) => {
    switch (status) {
        case Statuses.start:
            return 'pending'
        case Statuses.get:
            return 'agreed'
        case Statuses.rejected:
            return 'rejected'
        case Statuses.checked:
            return 'checked'
        case Statuses.done:
            return 'done'
        default:
            return ''
    }
}
const StatusChip: FC<StatusChipPropsType> = ({status}) => {
    const style = getStatusStyle(status)

    return (
        <div className={`status-chip ${style}`}>
            {status}
        </div>
    )
}

export default StatusChip