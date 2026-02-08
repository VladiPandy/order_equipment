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

export type SimpleValueChangeType = (value: string | number) => void

export type FilterChangeType = (value: string[] | string, type: KeyType) => void

export type ExecutorOption = {
    name: string
    isPriority: boolean
}

export type OptionsType = {
    [key: string]: string[] | number | {[key: string]: 0 | 1 | 2} | ExecutorOption[]
    samples_limit: number
    used: number
    date: {[key: string]: 0 | 1 | 2}
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

    messages_count?: number
    last_message_is_me?: boolean | null
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

interface BaseInfo {
    monday: string
    tuesday: string
    wednesday: string
    thursday: string
    friday: string
    saturday: string
    sunday: string
}

export interface EquipmentInfo extends BaseInfo {
    equipment: string
}
export interface ExecutorInfo extends BaseInfo {
    executor: string
}

export type RatingRow = {
    executor: string
    avgTotal: number
    avgOnTime: number
    avgFullSet: number
    avgQuality: number
    totalAnswerAnalyses: number
    totalAnalyses: number
}