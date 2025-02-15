import {FC} from 'react'
import './style.scss'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Project from '../../assets/project.svg?react'
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
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Filter from '../../assets/filter.svg?react'

import { FilterChangeType, SimpleValueChangeType, Keys, Filters } from '../../types'
import Input from '../../ui/Input'

interface ComponentPropsType {
    handleFilterChange: (atr: string, type: Keys) => void
    resetFilters: () => void
    currentFilter: Filters
}

import {Options} from '../../const'
import Button from '../../ui/Button'
const FiltersLine: FC<ComponentPropsType> = ({handleFilterChange, resetFilters, currentFilter}) => {
    return (
        <div className="Filter-line">
            <Input
                withIcon={true} 
                placeholder='Проект' 
                options={Options.Project} 
                setValue={handleFilterChange as FilterChangeType} 
                type='dropDown'
                filter='name'
                value={currentFilter.name}
            >
                <Project/>
            </Input>
            <Input 
                withIcon={true}
                placeholder='Период бронирования'
                setValue={handleFilterChange as SimpleValueChangeType} 
                type='calendar'
                filter='date'
                value={currentFilter.date}
            >
                <Date/>
            </Input>
            <Input 
                withIcon={true}
                placeholder='Прибор' 
                options={Options.Item} 
                setValue={handleFilterChange as FilterChangeType} 
                type='dropDown'
                filter='item'
                value={currentFilter.item}
            >
                <Item/>
            </Input>
            <Input 
                withIcon={true}
                placeholder='Анализ' 
                options={Options.Analys} 
                setValue={handleFilterChange as FilterChangeType} 
                type='dropDown'
                filter='analyze'
                value={currentFilter.analyze}
            >
                <Analys/>
            </Input>
            <Input 
                withIcon={true}
                placeholder='Исполнитель' 
                options={Options.Executor} 
                setValue={handleFilterChange as FilterChangeType} 
                type='dropDown'
                filter='executor'
                value={currentFilter.executor}
            >
                <User/>
            </Input>
            <Input 
                withIcon={true}
                placeholder='Статус' 
                options={Options.Status} 
                setValue={handleFilterChange as FilterChangeType} 
                type='dropDown'
                filter='status'
                value={currentFilter.status}
            >
                <Status/>
            </Input>
            <Button type='icon'onClick={resetFilters}><Filter/></Button>
        </div>
    )
}
export default FiltersLine