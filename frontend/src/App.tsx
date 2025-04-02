import { useContext, useEffect, useState } from 'react'
import Header from './components/header/index'
import Navigation from './components/navigation'
import FiltersLine from './components/filtersLine/index'
import MainPage from './pages/main'

// import {DataType, Keys} from './types'
// import { Statuses } from './const'

import AdminPage from './pages/admin'
import { BookingsProvider } from './features/bookingsProvider'
import { FiltersProvider } from './features/filtersProvider'
import { UserContext } from './features/user'
import { Loader } from './ui/Loader'



function App() {
  // const [data, setData] = useState<DataType[]>(Data)
  // const [filteredData, setFilteredData] = useState<DataType[]>(Data)
  const [currentPage, setCurrentPage] = useState<string>('main')

  const {user, logIn} = useContext(UserContext)

  useEffect(() => {
    if (!user) logIn()
  }, [])

  const renderContent = () => {
    switch (currentPage) {
      case 'admin':
        return <AdminPage/>
      default:
        return <MainPage/>
    }
  }

  return user ? (
    <>
      <Header/>
      <Navigation currentPage={currentPage} onPageChange={setCurrentPage} />
      <div className="App">
        <BookingsProvider>
          <FiltersProvider>
            <FiltersLine />
            {renderContent()}
          </FiltersProvider>
        </BookingsProvider>
      </div>
    </>
  ) : <Loader/>
}

export default App
