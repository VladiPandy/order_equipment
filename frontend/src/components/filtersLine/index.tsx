import { FC, useEffect, useState } from "react";
import "./style.scss";

// Импорт иконок (с использованием ?react, как в вашем примере)
import ProjectIcon from "../../assets/project.svg?react";
import DateIcon from "../../assets/period.svg?react";
import UserIcon from "../../assets/user.svg?react";
import StatusIcon from "../../assets/status.svg?react";
import AnalysIcon from "../../assets/analys.svg?react";
import ItemIcon from "../../assets/item.svg?react";
import FilterIcon from "../../assets/filter.svg?react";

import { FilterChangeType, SimpleValueChangeType, Keys, Filters } from "../../types";
import Input from "../../ui/Input";
import Button from "../../ui/Button";
import { Options } from "../../const";
import { fetchBookingLists, arrayToOptions } from "../../api/bookingService.ts";

interface ComponentPropsType {
    handleFilterChange: (atr: string, type: Keys) => void;
    resetFilters: () => void;
    currentFilter: Filters;
}

const FiltersLine: FC<ComponentPropsType> = ({ handleFilterChange, resetFilters, currentFilter }) => {
    const [dynamicOptions, setDynamicOptions] = useState<{
        project: Record<string, string>;
        date: Record<string, string>;
        analyse: Record<string, string>;
        equipment: Record<string, string>;
        executor: Record<string, string>;
        status: Record<string, string>;
    } | null>(null);

    useEffect(() => {
        const loadOptions = async () => {
            try {
                // Передаем нужный диапазон дат
                const data = await fetchBookingLists("19.01.2024-27.10.2024");
                // Преобразуем полученные массивы в объекты опций
                const opts = {
                    project: arrayToOptions(data.project),
                    date: arrayToOptions(data.date),
                    analyse: arrayToOptions(data.analyse),
                    equipment: arrayToOptions(data.equipment),
                    executor: arrayToOptions(data.executor),
                    status: arrayToOptions(data.status),
                };
                setDynamicOptions(opts);
            } catch (error) {
                console.error("Ошибка загрузки динамических опций:", error);
            }
        };
        loadOptions();
    }, []);

    return (
        <div className="Filter-line">
            <Input
                withIcon={true}
                placeholder="Проект"
                options={dynamicOptions ? dynamicOptions.project : Options.Project}
                setValue={handleFilterChange as FilterChangeType}
                type="dropDown"
                filter="name"
                value={currentFilter.name}
            >
                <ProjectIcon />
            </Input>
            <Input
                withIcon={true}
                placeholder="Период бронирования"
                setValue={handleFilterChange as SimpleValueChangeType}
                type="calendar"
                filter="date"
                value={currentFilter.date}
            >
                <DateIcon />
            </Input>
            <Input
                withIcon={true}
                placeholder="Прибор"
                options={dynamicOptions ? dynamicOptions.equipment : Options.Item}
                setValue={handleFilterChange as FilterChangeType}
                type="dropDown"
                filter="item"
                value={currentFilter.item}
            >
                <ItemIcon />
            </Input>
            <Input
                withIcon={true}
                placeholder="Анализ"
                options={dynamicOptions ? dynamicOptions.analyse : Options.Analys}
                setValue={handleFilterChange as FilterChangeType}
                type="dropDown"
                filter="analyze"
                value={currentFilter.analyze}
            >
                <AnalysIcon />
            </Input>
            <Input
                withIcon={true}
                placeholder="Исполнитель"
                options={dynamicOptions ? dynamicOptions.executor : Options.Executor}
                setValue={handleFilterChange as FilterChangeType}
                type="dropDown"
                filter="executor"
                value={currentFilter.executor}
            >
                <UserIcon />
            </Input>
            <Input
                withIcon={true}
                placeholder="Статус"
                options={dynamicOptions ? dynamicOptions.status : Options.Status}
                setValue={handleFilterChange as FilterChangeType}
                type="dropDown"
                filter="status"
                value={currentFilter.status}
            >
                <StatusIcon />
            </Input>
            <Button type="icon" onClick={resetFilters}>
                <FilterIcon />
            </Button>
        </div>
    );
};

export default FiltersLine;