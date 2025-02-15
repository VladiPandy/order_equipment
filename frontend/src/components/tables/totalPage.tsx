import { FC, useEffect, useState } from 'react'

import { DataType } from '../../types'
import './style.scss'

import { TotalData } from './Data'

const headers = ['Организация', 'Дата бронирования', 'Прибор', 'Анализ', 'Оператор', 'Число образцов']

const TotalTable: FC = () => {
    const [data, handleDataChange] = useState<DataType[]>([]);

    useEffect(() => {
        //fetch data
        handleDataChange(TotalData)
    }, [])

    return (
        <div className="AdminPageTable">
            <table>
                <thead>
                    <tr>
                        {headers.map((header, index) => (
                            <th key={index}>{header}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.map((line, index) => {
                        const {organization, date, item, analyze, executor, sample} = line
                        return (
                            <tr key={index}>
                                <td>{organization}</td>
                                <td>{date}</td>
                                <td>{item}</td>
                                <td>{analyze?.join(', ')}</td>
                                <td>{executor}</td>
                                <td>{sample}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </div>
    )
}

export default TotalTable