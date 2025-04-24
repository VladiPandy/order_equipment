import { FC, useContext } from 'react'

import './style.scss'

import { InfoContext } from '../../features/infoProvider'
import { addSpacesBeforeCapitals } from '../../utils/formatString'
import { Loader } from '../../ui/Loader'
import { FilteredDataContext } from '../../features/filteredDataProvider'
import EmptyState from '../EmptyState'

const headers = ['Оператор', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

const EmployeesTable: FC = () => {
    const {loading } = useContext(InfoContext)

    const {
        filteredExecutors: executors,
    } = useContext(FilteredDataContext)

    return (
        <div className="AdminPageTable">
            {loading ? <Loader/> : executors.length === 0 ? <EmptyState/> :
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