import { FC, useContext, useEffect } from 'react'

import './style.scss'
import { FiltersContext } from '../../features/filtersProvider';
import { InfoContext } from '../../features/infoProvider';
import { Loader } from '../../ui/Loader';
import { FilteredDataContext } from '../../features/filteredDataProvider';

const headers = ['Прибор', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

const InstrumentsTable: FC = () => {
    const { getFilters, filters, getFilterBody } = useContext(FiltersContext)
    const { getInstruments, loading } = useContext(InfoContext)

    const {
        filteredInstruments: instruments,
        filterInstruments
    } = useContext(FilteredDataContext)

    useEffect(() => {
        getFilters()
        getInstruments(getFilterBody())
        const timer = setInterval(() => {
            getFilters()
            getInstruments(getFilterBody())
        }, 1000 * 60 * 10)
        return () => clearInterval(timer)
    }, [])

    useEffect(() => {
        if (loading) {
            getInstruments(getFilterBody())
        }

        filterInstruments(filters)
    }, [filters])

    useEffect(() => {
        getInstruments(getFilterBody())
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
                {instruments.map((line, index) => {
                    const {equipment, monday, tuesday, wednesday, thursday, friday, saturday, sunday} = line
                    return (
                        <tr key={index}>
                            <td>{equipment}</td>
                            <td className={` ${!monday ? 'empty' : ''}`}>{monday}</td>
                            <td className={` ${!tuesday ? 'empty' : ''}`}>{tuesday}</td>
                            <td className={` ${!wednesday ? 'empty' : ''}`}>{wednesday}</td>
                            <td className={` ${!thursday ? 'empty' : ''}`}>{thursday}</td>
                            <td className={` ${!friday ? 'empty' : ''}`}>{friday}</td>
                            <td className={` ${!saturday ? 'empty' : ''}`}>{saturday}</td>
                            <td className={` ${!sunday ? 'empty' : ''}`}>{sunday}</td>
                        </tr>
                    )
                })}
            </tbody>
        </table>
        }
    </div>
    )
}

export default InstrumentsTable
