import { useContext, useEffect, useState } from 'react'
import Header from './components/header/index'
import Navigation from './components/navigation'
import MainPage from './pages/main'

import AdminPage from './pages/admin'
import { BookingsProvider } from './features/bookingsProvider'
import { FiltersProvider } from './features/filtersProvider'
import { UserContext } from './features/user'
import { Loader } from './ui/Loader'
import { FilteredDataProvider } from './features/filteredDataProvider'
import { InfoProvider } from './features/infoProvider'



function App() {
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
            <InfoProvider>
              <FilteredDataProvider>
                {renderContent()}
              </FilteredDataProvider>
            </InfoProvider>
          </FiltersProvider>
        </BookingsProvider>
      </div>
    </>
  ) : <Loader/>
}

export default App
