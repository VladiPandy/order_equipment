import { useEffect, useState } from "react";
import Header from "./components/header/index";
import Navigation from "./components/navigation";
import FiltersLine from "./components/filtersLine/index";
import MainPage from "./pages/main";
import LoginPage from "./pages/login";
import AdminPage from "./pages/admin";
import { DataType, Filters, Keys, HeaderInfo } from "./types";
import { Statuses } from "./const";
import { onLogIn, onlogOut } from "./actions/user";
import { fetchBookingsData } from "./api/bookingService.ts";
import { useHeaderInfo } from "./api/useHeaderInfo"; // импорт хука

const initialFilters: Filters = {
  name: undefined,
  date: [] as string[],
  analyze: [] as string[],
  item: undefined,
  executor: undefined,
  sample: undefined,
  status: undefined,
};

function App() {
  const [data, setData] = useState<DataType[]>([]);
  const [filteredData, setFilteredData] = useState<DataType[]>([]);
  const [filters, setFilters] = useState<Filters>(initialFilters);
  const [currentPage, setCurrentPage] = useState<string>("main");
  const [user, setUser] = useState<string | null>(localStorage.getItem("user"));


  const [headerInfo, loadingHeader, headerError] = useHeaderInfo();


  useEffect(() => {
    const loadData = async () => {
      try {
        const result = await fetchBookingsData("19.01.2024-27.10.2024");
        setData(result);
        setFilteredData(result);
      } catch (error) {
        console.error("Ошибка загрузки данных:", error);
      }
    };
    loadData();
  }, []);

  useEffect(() => {
    const filtered = data.filter((item) => {
      return Object.keys(filters).every((filter) => {
        const filterValue = filters[filter as Keys];
        const itemValue = item[filter as Keys];
        if (!filterValue || (Array.isArray(filterValue) && filterValue.length === 0))
          return true;
        if (Array.isArray(filterValue)) {
          return filterValue.some((f) =>
              Array.isArray(itemValue) ? itemValue.includes(f) : false
          );
        } else {
          return filterValue === itemValue;
        }
      });
    });
    setFilteredData(filtered);
  }, [filters, data]);

  const handleLogin = (data: { name: string; project: string; isAdmin: boolean }) => {
    onLogIn(setUser, data);
  };

  const resetFilters = () => {
    setFilters(initialFilters);
  };

  const changeFilters = (atr: string | string[], type: Keys) => {
    const filterItem = filters[type];
    const isReset = !atr || atr === "Не выбран";
    if (Array.isArray(filterItem)) {
      setFilters({
        ...filters,
        [type]: isReset ? [] : (atr as string[]),
      });
    } else {
      setFilters({
        ...filters,
        [type]: isReset ? undefined : atr,
      });
    }
  };

  const renderContent = () => {
    switch (currentPage) {
      case "django":
        return <div className="content">Django content</div>;
      case "admin":
        return <AdminPage />;
      default:
        return <MainPage data={filteredData} handleDataChange={setData} />;
    }
  };

  return user ? (
      <>
        <Header
            date={new Date().toLocaleDateString()}
            userInfo={user}
            headerInfo={headerInfo || undefined}
            onLogout={() => onlogOut(setUser)}
        />
        <Navigation currentPage={currentPage} onPageChange={setCurrentPage} />
        <div className="App">
          <FiltersLine handleFilterChange={changeFilters} currentFilter={filters} resetFilters={resetFilters} />
          {renderContent()}
        </div>
      </>
  ) : (
      <LoginPage onLogin={handleLogin} />
  );
}

export default App;
