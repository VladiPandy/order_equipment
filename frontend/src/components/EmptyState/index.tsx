import { FC } from 'react'
import './style.scss'

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import SearchIcon from '../../assets/search.svg?react'

interface EmptyStateProps {
    message?: string
}

const EmptyState: FC<EmptyStateProps> = ({ message = 'Ничего не найдено' }) => {
    return (
        <div className="empty-state">
            <div className="empty-state__content">
                <SearchIcon className="empty-state__icon" />
                <p className="empty-state__message">{message}</p>
            </div>
        </div>
    )
}

export default EmptyState 