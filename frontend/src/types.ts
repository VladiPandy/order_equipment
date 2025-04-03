export const Keys = {
    DATE: 'date',
    ANALYZE: 'analyse',
    EQUIPMENT: 'equipment',
    EXECUTOR: 'executor',
    SAMPLE: 'sample',
    STATUS: 'status',
    COMMENT: 'comment'
} as const;

export type KeyType = 'date' | 'analyse' | 'equipment' | 'executor' | 'sample' | 'status'

export type DaysType = 'ПН' | 'ВТ' | 'СР' | 'ЧТ' | 'ПТ' | 'СБ' | 'ВС'

export type InputType = 'text' | 'number' | 'textArea' | 'dropDown' | 'calendar'

export interface DateRange {
    start: string
    end: string
}

export type FilterValue = string | string[] | DateRange

export type Filters = {
    date: DateRange
    analyse: string[]
    equipment: string[]
    executor: string[]
    sample: string[]
    status: string[]
}

// export type FilterBodyType = {
//     [key in KeyType]?: string
// }

export type SimpleValueChangeType = (value: string | number) => void

export type FilterChangeType = (value: string[] | string, type: KeyType) => void

export type OptionsType = {
    date: {[key: string]: boolean}
    analyse: string[]
    equipment: string[]
    executor: string[]
    samples_limit: number
    used: number
}


export type BookingType = {
    id?: number,
    project?: string,
    date: string,
    analyse: string,
    equipment: string,
    executor: string,
    samples: string,
    status: string,
    comment: string
}

export type FilterBodyType = {
    start: string,
    end: string,
    analyse?: string,
    equipment?: string,
    executor?: string,
    sample?: string,
    status?: string,
    comment?: string
}

export type FilterBody = {
    date?: {
        start: string
        end: string
    }
    period?: string
    analyse?: string[]
    equipment?: string[]
    executor?: string[]
    status?: string[]
}

export type Booking = {
    id: number
    date: string
    analyse: string[]
    equipment: string
    executor: string
    samples: number
    status: string
    comment?: string
}
