import { FC, useEffect, useState } from 'react'

import { DataType } from '../../types'
import './style.scss'

import { EmployeesData } from './Data'

const headers = ['Оператор', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

const EmployeesTable: FC = () => {
    const [data, handleDataChange] = useState<DataType[]>([]);

    useEffect(() => {
        //fetch data
        handleDataChange(EmployeesData)
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
                        const {executor, monday, tuesday, wednesday, thursday, friday, saturday, sunday} = line
                        return (
                            <tr key={index}>
                                <td>{executor}</td>
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
        </div>
    )
}

export default EmployeesTable