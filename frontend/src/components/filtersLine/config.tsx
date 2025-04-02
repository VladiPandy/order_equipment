import { InputType, KeyType } from '../../types'


// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Date from '../../assets/period.svg?react'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import User from '../../assets/user.svg?react'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Status from '../../assets/status.svg?react'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Analys from '../../assets/analys.svg?react'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Item from '../../assets/item.svg?react'

export interface FilterConfig {
    placeholder: string
    type: InputType
    filter: KeyType
    icon: JSX.Element
    isMultiple?: boolean
}

export const FILTERS_CONFIG: FilterConfig[] = [
    {
        placeholder: 'Период бронирования',
        type: 'calendar',
        filter: 'date',
        icon: <Date />
    },
    {
        placeholder: 'Прибор',
        type: 'dropDown',
        filter: 'equipment',
        icon: <Item />
    },
    {
        placeholder: 'Анализ',
        type: 'dropDown',
        filter: 'analyse',
        icon: <Analys />
    },
    {
        placeholder: 'Исполнитель',
        type: 'dropDown',
        filter: 'executor',
        icon: <User />
    },
    {
        placeholder: 'Статус',
        type: 'dropDown',
        filter: 'status',
        icon: <Status />
    }
]