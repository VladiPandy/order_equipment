import { FC, useEffect, useState } from 'react'

import Button from '../../ui/Button'
// import StatusChip from '../../ui/StatusChip'
// import Modal from '../../components/modal'
// import Instruments from '../../ui/Instruments'

// import { DataType } from '../../types'
import './style.scss'
import TotalTable from '../../components/tables/totalPage'
import EmployeesTable from '../../components/tables/employeesPage'
import InstrumentsTable from '../../components/tables/instrumentsPage'

// const headers = ['Проект', 'Дата бронирования', 'Анализ', 'Прибор', 'Исполнитель', 'Число образцов', 'Статус']
export const adminSubPages = {total: 'total', instruments: 'instruments', employees: 'employees'}

const AdminPage: FC = () => {
    const [currentPage, setCurrentPage] = useState<string>(adminSubPages.total)

    useEffect(() => {
        localStorage.setItem('currentPage', currentPage)
    }, [currentPage])

    const renderPage = () => {
        switch (currentPage) {
            case adminSubPages.instruments:
                return <InstrumentsTable />
            case adminSubPages.employees:
                return <EmployeesTable />
            default:
                return <TotalTable/>
        }
    }

    return (
        <div className="AdminPage">
            <div className='AdminPage_navigation'>
                <Button type={currentPage === adminSubPages.total ? 'primary' : 'secondary'} onClick={()=>setCurrentPage(adminSubPages.total)}>Общая информация</Button>
                <Button type={currentPage === adminSubPages.instruments ? 'primary' : 'secondary'} onClick={()=>setCurrentPage(adminSubPages.instruments)}>Занятость приборов</Button>
                <Button type={currentPage === adminSubPages.employees ? 'primary' : 'secondary'} onClick={()=>setCurrentPage(adminSubPages.employees)}>Занятость сотрудников</Button>
            </div>
            {renderPage()}
        </div>
    )
}

export default AdminPage