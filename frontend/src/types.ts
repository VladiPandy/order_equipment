export type Keys = 'name' | 'date' | 'analyze' | 'item' | 'executor' | 'sample' | 'status' | 'comment';
export type DaysType = 'ПН' | 'ВТ' | 'СР' | 'ЧТ' | 'ПТ' | 'СБ' | 'ВС'
export type DataType = {
    organization?: string
    name?: string
    date?: string | string[]
    days?: DaysType[]
    analyze?: string[]
    item?: string
    executor?: string
    sample?: string | number | undefined
    status?: string | string[]
    comment?: string | string[]
    monday?: string | string[]
    tuesday?: string | string[]
    wednesday?: string | string[]
    thursday?: string | string[]
    friday?: string | string[]
    saturday?: string | string[]
    sunday?: string | string[]
}

export type FilterChangeType = (atr: string, type: string|undefined) => void
export type SimpleValueChangeType = (value: string | number | undefined) => void

export type Filters = {
    [K in keyof DataType]?: DataType[K] extends (infer I)[]
        ? I
        : DataType[K];
};

export interface BookingListsResponse {
    project: string[];
    date: string[];
    analyse: string[];
    equipment: string[];
    executor: string[];
    status: string[];
}

export interface HeaderInfo {
    is_admin: number;
    project_name: string;
    responsible_fio: string;
}