import { FC, useContext, useState } from 'react'
import Button from '../../ui/Button'
import Toggle from '../../ui/Toggle'
import './style.scss'
import { createPortal } from 'react-dom'
import { Loader } from '../../ui/Loader'
import { BookingsContext } from '../../features/bookingsProvider'
import { onSuccess } from '../../utils/toast'
import { FiltersContext } from '../../features/filtersProvider'

type FeedbackFormProps = {
    selectedBookingId: number
    onClose: () => void
}

export type FeedbackData = {
    id: number
    question_1: boolean
    question_2: boolean
    question_3: boolean
}

const FeedbackForm: FC<FeedbackFormProps> = ({ selectedBookingId, onClose }) => {
    const [loading, setLoading] = useState(false)
    const [feedback, setFeedback] = useState<FeedbackData>({
        id: selectedBookingId,
        question_1: false,
        question_2: false,
        question_3: false
    })

    const { feedbackBooking, getBookings } = useContext(BookingsContext)
    const { getFilterBody } = useContext(FiltersContext)

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        feedbackBooking(feedback, () => {
            onClose()
            getBookings(getFilterBody())
            onSuccess('Отзыв отправлен')
        })
    }

    const handleToggle = (key: keyof FeedbackData) => {
        setFeedback(prev => ({
            ...prev,
            [key]: !prev[key]
        }))
    }

    return createPortal(
        <div className="modal" onClick={onClose}>
            <div className="content feedbackForm" onClick={(e) => e.stopPropagation()}>
                {loading ? <Loader /> : 
                    <form onSubmit={handleSubmit}>
                        <div className="toggles">
                            <Toggle
                                checked={feedback.question_1}
                                onChange={() => handleToggle('question_1')}
                                label="Выполнено без задержек"
                            />
                            <Toggle
                                checked={feedback.question_2}
                                onChange={() => handleToggle('question_2')}
                                label="Выполнен полный набор измерений"
                            />
                            <Toggle
                                checked={feedback.question_3}
                                onChange={() => handleToggle('question_3')}
                                label="Нет замечаний по качеству работы"
                            />
                        </div>
                        <div className="buttonCollection">
                            <Button type="secondary" onClick={onClose}>Отмена</Button>
                            <Button type="primary" onClick={handleSubmit}>Отправить</Button>
                        </div>
                    </form> 
            }
        </div>
    </div>,  document.getElementById('root') as HTMLElement
    )
}

export default FeedbackForm 