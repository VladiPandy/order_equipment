import { FC, useContext, useEffect,useRef, useState } from 'react'

import Button from '../../ui/Button'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Download from '../../assets/download.svg?react'
import './style.scss'
import { format, subMonths } from 'date-fns'
import TotalTable from '../../components/tables/totalPage'
import EmployeesTable from '../../components/tables/employeesPage'
import RatingsTable from '../../components/tables/ratingPage'
import InstrumentsTable from '../../components/tables/instrumentsPage'
import FiltersLine from '../../components/filtersLine'
import { download } from '../../api/globalFetch'
import { endPoints } from '../../api/endPoints'
import { FiltersContext } from '../../features/filtersProvider'
import { DateRange } from '../../types'

const adminSubPages = {total: 'total', instruments: 'instruments', employees: 'employees', ratings: 'ratings'}

const AdminPage: FC = () => {
    const [currentPage, setCurrentPage] = useState<string>(adminSubPages.total)
    const {filters, changeFilters, getFilterBody, getFilters} = useContext(FiltersContext)

    useEffect(() => getFilters(), [])

    const lastWeekRangeRef = useRef<DateRange>(filters.date ?? { start: '', end: '' })

    const lastWeeklyFiltersRef = useRef(filters)

    const prevPageRef = useRef(currentPage)
    const ratingsInitializedRef = useRef(false)

    const getLastHalfYearRange = (): DateRange => {
      const end = new Date()
      const start = subMonths(end, 6)
      return {
        start: format(start, 'dd.MM.yyyy'),
        end: format(end, 'dd.MM.yyyy'),
      }
    }
    useEffect(() => {
      const prevPage = prevPageRef.current
      prevPageRef.current = currentPage

      const isLeavingRatings = prevPage === adminSubPages.ratings
      const isGoingToWeekly = currentPage !== adminSubPages.ratings

      if (isLeavingRatings && isGoingToWeekly) {
        const prevWeekly = lastWeeklyFiltersRef.current
        ratingsInitializedRef.current = false
        changeFilters(prevWeekly.date, 'date')
        changeFilters(prevWeekly.equipment, 'equipment')
        changeFilters(prevWeekly.analyse, 'analyse')
        changeFilters(prevWeekly.executor, 'executor')
        changeFilters(prevWeekly.status, 'status')
      }

      if (currentPage === adminSubPages.ratings && !ratingsInitializedRef.current) {
        changeFilters(getLastHalfYearRange(), 'date')
        ratingsInitializedRef.current = true
      }
    }, [currentPage, changeFilters])

    useEffect(() => {
      const isWeeklyPage = currentPage !== adminSubPages.ratings
      if (isWeeklyPage && filters.date) {
        lastWeekRangeRef.current = filters.date
      }
    }, [currentPage, filters.date])

    useEffect(() => {
      const isWeeklyPage = currentPage !== adminSubPages.ratings
      if (isWeeklyPage) {
        lastWeeklyFiltersRef.current = filters
      }
    }, [currentPage, filters])

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
        }
        else if (currentPage === adminSubPages.employees) {
            endPoint = endPoints.downloadExecutors
            fileName = 'Занятость сотрудников'
        }
        else if (currentPage === adminSubPages.ratings) {
            endPoint = endPoints.downloadRatings
            fileName = 'Оценка сотрудников'
        }
        download(endPoint, date, `${fileName}_за_${date.start}-${date.end}`)
    }

    const goToPage = (page: string) => {
      setCurrentPage(page)
    }

    const renderPage = () => {
        switch (currentPage) {
            case adminSubPages.instruments:
                return <InstrumentsTable />
            case adminSubPages.employees:
                return <EmployeesTable />
            case adminSubPages.ratings:
                 return <RatingsTable />
            default:
                return <TotalTable/>
        }
    }

    return (
        <>
            <FiltersLine onTables
            onlyWeek={currentPage !== adminSubPages.ratings}/>
            <div className="AdminPage">
                <div className='AdminPage_navigation'>
                    <Button type={currentPage === adminSubPages.total ? 'primary' : 'secondary'} onClick={()=>goToPage(adminSubPages.total)}>Общая информация</Button>
                    <Button type={currentPage === adminSubPages.instruments ? 'primary' : 'secondary'} onClick={()=>goToPage(adminSubPages.instruments)}>Занятость приборов</Button>
                    <Button type={currentPage === adminSubPages.employees ? 'primary' : 'secondary'} onClick={()=>goToPage(adminSubPages.employees)}>Занятость сотрудников</Button>
                    <Button type={currentPage === adminSubPages.ratings ? 'primary' : 'secondary'} onClick={()=>goToPage(adminSubPages.ratings)}>Оценка сотрудников</Button>
                    <Button type={'icon'} onClick={handleDownload}><Download/></Button>
                </div>
                {renderPage()}
            </div>
        </>
    )
}

export default AdminPage