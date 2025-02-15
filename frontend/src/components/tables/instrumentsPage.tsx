import { FC, useEffect, useState } from 'react'

import { DataType } from '../../types'
import './style.scss'

import { InstrumentsData } from './Data'

const headers = ['Прибор', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

const InstrumentsTable: FC = () => {
    const [data, handleDataChange] = useState<DataType[]>([]);

    useEffect(() => {
        //fetch data
        handleDataChange(InstrumentsData)
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
                    const {item, monday, tuesday, wednesday, thursday, friday, saturday, sunday} = line
                    return (
                        <tr key={index}>
                            <td>{item}</td>
                            <td className={` ${!monday ? 'empty' : ''}`}>{(monday as string[])?.join(', ')}</td>
                            <td className={` ${!tuesday ? 'empty' : ''}`}>{(tuesday as string[])?.join(', ')}</td>
                            <td className={` ${!wednesday ? 'empty' : ''}`}>{(wednesday as string[])?.join(', ')}</td>
                            <td className={` ${!thursday ? 'empty' : ''}`}>{(thursday as string[])?.join(', ')}</td>
                            <td className={` ${!friday ? 'empty' : ''}`}>{(friday as string[])?.join(', ')}</td>
                            <td className={` ${!saturday ? 'empty' : ''}`}>{(saturday as string[])?.join(', ')}</td>
                            <td className={` ${!sunday ? 'empty' : ''}`}>{(sunday as string[])?.join(', ')}</td>
                        </tr>
                    )
                })}
            </tbody>
        </table>
    </div>
    )
}

export default InstrumentsTable
