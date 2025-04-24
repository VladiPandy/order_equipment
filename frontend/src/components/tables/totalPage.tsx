import { FC, useContext } from 'react'

import './style.scss'

import { FilteredDataContext } from '../../features/filteredDataProvider'
import { BookingsContext } from '../../features/bookingsProvider'
import { Loader } from '../../ui/Loader'
import EmptyState from '../EmptyState'

const headers = ['Организация', 'Дата бронирования', 'Прибор', 'Анализ', 'Оператор', 'Число образцов']

const TotalTable: FC = () => {
    const { filteredBooking } = useContext(FilteredDataContext)
    const { loading } = useContext(BookingsContext)

    return (
        <div className="AdminPageTable">
            {loading ? <Loader/> : filteredBooking.length === 0 ? <EmptyState/> :
            <table>
                <thead>
                    <tr>
                        {headers.map((header, index) => (
                            <th key={index}>{header}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {filteredBooking.map((line, index) => {
                        const {project, date, equipment, analyse, executor, samples} = line
                        return (
                            <tr key={index}>
                                <td>{project}</td>
                                <td>{date}</td>
                                <td>{equipment}</td>
                                <td>{analyse}</td>
                                <td>{executor}</td>
                                <td>{samples}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
            }
        </div>
    )
}

export default TotalTable