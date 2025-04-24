import { FC } from 'react'
import Button from '../../ui/Button'
import './style.scss'
import { createPortal } from 'react-dom'

type DeleteFormProps = {
    onSubmit: () => void
    onClose: () => void
}

export type DeleteData = {
    onSubmit: () => void
}

const DeleteForm: FC<DeleteFormProps> = ({ onSubmit, onClose }) => {
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        onSubmit()
    }

    return createPortal(
        <div className="modal" onClick={onClose}>
            <div className="content DeleteForm" onClick={(e) => e.stopPropagation()}>
                <p>Вы действительно хотите удалить бронирование?</p>
                <div className="buttonCollection">
                    <Button type="secondary" onClick={onClose}>Отмена</Button>
                    <Button type="danger" onClick={handleSubmit}>Удалить</Button>
                </div>
            </div>
        </div>,  document.getElementById('root') as HTMLElement
    )
}

export default DeleteForm 