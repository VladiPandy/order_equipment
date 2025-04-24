import { FC, useContext, useEffect, useState } from 'react'

import Button from '../../ui/Button'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Download from '../../assets/download.svg?react'
import './style.scss'
import TotalTable from '../../components/tables/totalPage'
import EmployeesTable from '../../components/tables/employeesPage'
import InstrumentsTable from '../../components/tables/instrumentsPage'
import FiltersLine from '../../components/filtersLine'
import { download } from '../../api/globalFetch'
import { endPoints } from '../../api/endPoints'
import { FiltersContext } from '../../features/filtersProvider'

const adminSubPages = {total: 'total', instruments: 'instruments', employees: 'employees'}

const AdminPage: FC = () => {
    const [currentPage, setCurrentPage] = useState<string>(adminSubPages.total)
    const {getFilterBody} = useContext(FiltersContext)

    useEffect(() => {
        localStorage.setItem('currentPage', currentPage)
    }, [currentPage])

    const handleDownload = () => {
        const date = getFilterBody()
        let endPoint = endPoints.downloadBookings
        let fileName = 'Общая информация'
        if (currentPage === adminSubPages.instruments) {
            endPoint = endPoints.downloadEquipment; 
            fileName = 'Занятость приборов' 
        } else if (currentPage === adminSubPages.employees) {
            endPoint = endPoints.downloadExecutors
            fileName = 'Занятость сотрудников'
        }
        download(endPoint, date, `${fileName}_за_${date.start}-${date.end}`)
    }

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
        <>
            <FiltersLine onTables />
            <div className="AdminPage">
                <div className='AdminPage_navigation'>
                    <Button type={currentPage === adminSubPages.total ? 'primary' : 'secondary'} onClick={()=>setCurrentPage(adminSubPages.total)}>Общая информация</Button>
                    <Button type={currentPage === adminSubPages.instruments ? 'primary' : 'secondary'} onClick={()=>setCurrentPage(adminSubPages.instruments)}>Занятость приборов</Button>
                    <Button type={currentPage === adminSubPages.employees ? 'primary' : 'secondary'} onClick={()=>setCurrentPage(adminSubPages.employees)}>Занятость сотрудников</Button>
                    <Button type={'icon'} onClick={handleDownload}><Download/></Button>
                </div>
                {renderPage()}
            </div>
        </>
    )
}

export default AdminPage