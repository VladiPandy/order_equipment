import { FC, useContext, useEffect } from 'react'

import './style.scss'

import { InfoContext } from '../../features/infoProvider'
import { FiltersContext } from '../../features/filtersProvider'
import { addSpacesBeforeCapitals } from '../../utils/formatString'
import { Loader } from '../../ui/Loader'
import { FilteredDataContext } from '../../features/filteredDataProvider'

const headers = ['Оператор', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

const EmployeesTable: FC = () => {
    const { getFilters, filters, getFilterBody } = useContext(FiltersContext)
    const { getExecutors, loading } = useContext(InfoContext)

    const {
        filteredExecutors: executors,
        filterExecutors
    } = useContext(FilteredDataContext)

    useEffect(() => {
        getFilters()
        getExecutors(getFilterBody())
        const timer = setInterval(() => {
            getFilters()
            getExecutors(getFilterBody())
        }, 1000 * 60 * 10)
        return () => clearInterval(timer)
    }, [])

    useEffect(() => {
        if (loading) {
            getExecutors(getFilterBody())
        }

        filterExecutors(filters)
    }, [filters])

    useEffect(() => {
        getExecutors(getFilterBody())
    }, [])

    return (
        <div className="AdminPageTable">
            {loading ? <Loader/> : 
            <table>
                <thead>
                    <tr>
                        {headers.map((header, index) => (
                            <th key={index}>{header}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {executors.map((line, index) => {
                        const {executor, monday, tuesday, wednesday, thursday, friday, saturday, sunday} = line
                        return (
                            <tr key={index}>
                                <td>{addSpacesBeforeCapitals(executor || '')}</td>
                                <td className={`${!monday ? 'empty' : ''}`}>{monday}</td>
                                <td className={`${!tuesday ? 'empty' : ''}`}>{tuesday}</td>
                                <td className={`${!wednesday ? 'empty' : ''}`}>{wednesday}</td>
                                <td className={`${!thursday ? 'empty' : ''}`}>{thursday}</td>
                                <td className={`${!friday ? 'empty' : ''}`}>{friday}</td>
                                <td className={`${!saturday ? 'empty' : ''}`}>{saturday}</td>
                                <td className={`${!sunday ? 'empty' : ''}`}>{sunday}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
            }
        </div>
    )
}

export default EmployeesTable