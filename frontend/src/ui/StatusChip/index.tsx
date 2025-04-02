import { FC, useContext, useState } from 'react'
import './style.scss'

import {Statuses} from '../../const'
import FeedbackForm from '../../components/modal/FeedbackForm'
import { UserContext } from '../../features/user'

type StatusChipProps = {
    status: string
    id: number
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

const StatusChip: FC<StatusChipProps> = ({ id, status }) => {
    const { user } = useContext(UserContext)
    const [showFeedback, setShowFeedback] = useState(false)

    const style = getStatusStyle(status)

    return (
        <>
            <div 
                className={`status-chip ${style} ${status === Statuses.checked && !user?.is_admin ? 'clickable' : ''}`}
                onClick={() => !user?.is_admin && status === Statuses.checked && setShowFeedback(true)}
            >
                {status}
            </div>
            {showFeedback && (
                <FeedbackForm selectedBookingId={id} onClose={() => setShowFeedback(false)}/>
            )}
        </>
    )
}

export default StatusChip