import { FC, useContext } from 'react'
import './style.scss'

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Filter from '../../assets/filter.svg?react'

import { FILTERS_CONFIG, FilterConfig } from './config.tsx'
import FiltersSkeleton from './FiltersSkeleton'
import Input from '../../ui/Input'
import Button from '../../ui/Button'
import { FiltersContext } from '../../features/filtersProvider'
import { DateRange } from '../../types'
import { adminSubPages } from '../../pages/admin/index.tsx'

const FiltersLine: FC = () => {
    const { filters, filtersOptions, changeFilters, resetFilters, loading } = useContext(FiltersContext)

    const filtersIsActive = ![adminSubPages.instruments, adminSubPages.employees].includes(localStorage.getItem('currentPage') as string)

    const handleReset = () => {
        resetFilters()
    }

    const renderFilter = (config: FilterConfig, key: number) => {
        const { placeholder, type, filter, icon, isMultiple } = config
        if (loading) return <FiltersSkeleton key={key}/>

        const commonProps = {
            placeholder,
            withIcon: true,
            children: icon,
            filter
        }

        if (type === 'calendar') {
            return (
                <Input
                    {...commonProps}
                    key={key}
                    type="calendar"
                    value={filters[filter] as DateRange}
                    setValue={changeFilters}
                />
            )
        }

        if (type === 'dropDown') {
            return (
                <Input
                    {...commonProps}
                    key={key}
                    type="dropDown"
                    value={filters[filter] as string[]}
                    setValue={changeFilters}
                    options={filtersOptions[filter] as string[]}
                    isMultiple={isMultiple}
                    enabled={filtersIsActive}
                />
            )
        }

        return null
    }

    return (
        <div className="Filter-line">
            {FILTERS_CONFIG.map((config, index) => renderFilter(config, index))}
            {!loading && <Button type="icon" onClick={handleReset}>
                <Filter />
            </Button>}
        </div>
    )
}

export default FiltersLine