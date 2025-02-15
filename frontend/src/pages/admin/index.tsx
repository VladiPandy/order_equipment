import { FC, useState } from 'react'

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
const pages = {total: 'total', instruments: 'instruments', employees: 'employees'}

const AdminPage: FC = () => {
    const [currentPage, setCurrentPage] = useState<string>(pages.total)

    const renderPage = () => {
        switch (currentPage) {
            case pages.instruments:
                return <InstrumentsTable />
            case pages.employees:
                return <EmployeesTable />
            default:
                return <TotalTable/>
        }
    }

    return (
        <div className="AdminPage">
            <div className='AdminPage_navigation'>
                <Button type={currentPage === pages.total ? 'primary' : 'secondary'} onClick={()=>setCurrentPage(pages.total)}>Общая информация</Button>
                <Button type={currentPage === pages.instruments ? 'primary' : 'secondary'} onClick={()=>setCurrentPage(pages.instruments)}>Зантость приборов</Button>
                <Button type={currentPage === pages.employees ? 'primary' : 'secondary'} onClick={()=>setCurrentPage(pages.employees)}>Занятость сотрудников</Button>
            </div>
            {renderPage()}
        </div>
    )
}

export default AdminPage