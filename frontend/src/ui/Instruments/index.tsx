import './style.scss'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Trash from '../../assets/trash.svg?react'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Edit from '../../assets/edit.svg?react'
import { FC, useContext } from 'react'
import Button from '../Button'
import { UserContext } from '../../features/user'

interface CommentIndicatorProps {
    comment?: string
}
const CommentIndicator: FC<CommentIndicatorProps> = ({comment}) => {
    return (<div className={`indicator ${comment ? 'active' : ''}`}>
        <div className='comment'>
            <div className='content'>
                <h4>Комментарий изменения</h4>
                <p>{comment}</p>
            </div>
        </div>
    </div>)
}
interface InstrumentsProps {
    id: number
    handleEdit: (id: number) => void
    handleDelete: (id: number) => void
    comment?: string,
    status: string
}
const Instruments: FC<InstrumentsProps> = ({id, handleEdit, handleDelete, comment, status}) => {
    const { user } = useContext(UserContext)
    const isEditButtonShow = user?.is_admin && !['Выполнено','Оценить'].includes(status)

    const handleEditClick = (id: number) => {
        return isEditButtonShow && handleEdit(id)
    }

    return (
        <div className={`instuments`}>
            <CommentIndicator comment={comment}/>
            <Button className={'active'} type='icon' onClick={()=>handleDelete(id)}><Trash/></Button>
            <Button className={isEditButtonShow ? 'active' : ''} type='icon' onClick={()=>handleEditClick(id)}><Edit/></Button>
        </div>
    )
}

export default Instruments