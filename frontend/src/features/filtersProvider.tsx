import { createContext, FC, useState } from "react"
import { globalPost } from "../api/globalFetch"
import { endPoints } from "../api/endPoints"
import { Filters, KeyType, FilterBodyType, DateRange, FilterValue } from "../types"
import { format, subDays, addDays, addWeeks, startOfWeek, endOfWeek, Day } from 'date-fns'

export const getDefaultDateRange = (): DateRange => {
    const today = new Date()
    return {
        start: format(subDays(today, 14), 'dd.MM.yyyy'),
        end: format(addDays(today, 14), 'dd.MM.yyyy')
    }
}

export const getNextWeekDateRange = (): DateRange => {
    const nextWeek = addWeeks(new Date(), 1)
    return {
        start: format(startOfWeek(nextWeek, { weekStartsOn: 1 as Day }), 'dd.MM.yyyy'),
        end: format(endOfWeek(nextWeek, { weekStartsOn: 1 as Day }), 'dd.MM.yyyy')
    }
}

const initialFilters: Filters = {
    date: getDefaultDateRange(),
    analyse: [],
    equipment: [],
    executor: [],
    sample: [],
    status: [],
}

type ContextType = {
    filters: Filters,
    filtersOptions: Filters,
    loading: boolean,
    changeFilters: (atr: FilterValue, type: KeyType) => void,
    resetFilters: () => void,
    getFilterBody: () => FilterBodyType,
    getFilters: () => void
}

const initialValue: ContextType = {
    filters: initialFilters,
    filtersOptions: initialFilters,
    loading: false,
    changeFilters: () => {},
    resetFilters: () => {},
    getFilterBody: () => (getDefaultDateRange()),
    getFilters: () => {}
}

export const FiltersContext = createContext<ContextType>(initialValue)

interface PropsType {
    children: React.ReactNode
}

export const FiltersProvider: FC<PropsType> = ({children}) => {
    const [filtersOptions, setFiltersOptions] = useState<Filters>(initialFilters)
    const [filters, setFilters] = useState<Filters>(initialFilters)
    const [loading, setLoading] = useState<boolean>(true)

    const prepareFiltersOptions = (data: Filters) => {
        Object.keys(data).forEach(key => {
            const typedKey = key as KeyType;
            if (typedKey !== 'date' && Array.isArray(data[typedKey])) {
                (data[typedKey] as string[]).unshift('Не выбран')
            }
        })
        setFiltersOptions(data)
    }

    const convertFiltersToBody = (filters: Filters): FilterBodyType => {
        const body: FilterBodyType = {
            ...getDefaultDateRange()
        };
        
        Object.entries(filters).forEach(([key, value]) => {
            if (value) {
                const typedKey = key as keyof FilterBodyType;
                if (key === 'date') {
                    const dateRange = value as DateRange;
                    body.start = dateRange.start;
                    body.end = dateRange.end;
                } else {
                    const values = value as string[];
                    if (values.length > 0) {
                        body[typedKey] = values.join(',');
                    }
                }
            }
        });

        return body;
    };

    const getFilterBody = () => {
        return convertFiltersToBody(filters);
    };

    const getFilters = () => {
        setLoading(true)
        globalPost(endPoints.filters, (data: Filters) => {
            prepareFiltersOptions(data)
            setLoading(false)
        }, {
            start: filters.date?.start,
            end: filters.date?.end
        })
    }

    const changeFilters = (atr: FilterValue, type: KeyType) => {
        if (type === 'date') {
            const dateRange = atr as DateRange;
            setFilters({
                ...filters,
                date: dateRange
            })
        } else {
            const attribute = atr as string[] | string
            const isReset = !attribute || attribute === 'Не выбран';
            setFilters(prev => ({
                ...prev,
                [type]: isReset ? [] : Array.isArray(attribute) ? attribute : [attribute as string],
            }));
        }
    };

    const resetFilters = () => {
        setFilters({
            ...initialFilters,
        })
    }

    const contextData = {
        filters,
        filtersOptions,
        loading,
        getFilters,
        changeFilters,
        resetFilters,
        getFilterBody
    }
    
    return <FiltersContext.Provider value={contextData}>{children}</FiltersContext.Provider>
}