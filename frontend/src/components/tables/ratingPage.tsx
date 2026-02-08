import { FC, useContext, useEffect } from 'react'

import './style.scss'

import { InfoContext } from '../../features/infoProvider'
import { Loader } from '../../ui/Loader'
import { FilteredDataContext } from '../../features/filteredDataProvider'
import EmptyState from '../EmptyState'
import { addSpacesBeforeCapitals } from '../../utils/formatString'

const headers = [
    'Исполнитель',
    'Средняя оценка',
    'Без задержек',
    'Полный набор измерений',
    'Качество работы',
    'Кол-во оценённых',
    'Всего завершённых',
]

const RatingsTable: FC = () => {
    const { loading } = useContext(InfoContext)

    const {
        filteredRatings,
        loadRatings,
    } = useContext(FilteredDataContext)

    useEffect(() => {
        loadRatings()
    }, [loadRatings])

    return (
        <div className="AdminPageTable">
            {loading ? (
                <Loader />
            ) : !filteredRatings || filteredRatings.length === 0 ? (
                <EmptyState />
            ) : (
                <table>
                    <thead>
                        <tr>
                            {headers.map((header, index) => (
                                <th key={index}>{header}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                    {filteredRatings.map((line, index) => {
                        const {
                            executor,
                            avgTotal,
                            avgOnTime,
                            avgFullSet,
                            avgQuality,
                            totalAnswerAnalyses,
                            totalAnalyses,
                        } = line

                        return (
                            <tr key={index}>
                                <td>{addSpacesBeforeCapitals(executor || '')}</td>

                                <td className={avgTotal == null ? 'empty' : ''}>
                                    {avgTotal}
                                </td>

                                <td className={avgOnTime == null ? 'empty' : ''}>
                                    {avgOnTime}
                                </td>

                                <td className={avgFullSet == null ? 'empty' : ''}>
                                    {avgFullSet}
                                </td>

                                <td className={avgQuality == null ? 'empty' : ''}>
                                    {avgQuality}
                                </td>

                                <td className={totalAnswerAnalyses == null ? 'empty' : ''}>
                                    {totalAnswerAnalyses}
                                </td>

                                <td className={totalAnalyses == null ? 'empty' : ''}>
                                    {totalAnalyses}
                                </td>
                            </tr>
                        )
                    })}
                    </tbody>
                </table>
            )}
        </div>
    )
}

export default RatingsTable