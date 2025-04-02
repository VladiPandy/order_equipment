import { parse, format } from 'date-fns'

export function formatDateToDDMMYYYY(date: Date, separator = '.') {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    
    return `${day}${separator}${month}${separator}${year}`;
}

export function getNextWeekday(targetDay: number) {
    const result = new Date();
    const currentDay = result.getDay();
    let daysUntilTarget = targetDay - currentDay;
    
    // Если выбранный день недели уже был в текущей неделе, добавим 7 дней
    if (daysUntilTarget <= 0) {
        daysUntilTarget += 7;
    }

    result.setDate(result.getDate() + daysUntilTarget);
    return formatDateToDDMMYYYY(result);
}

export function formatDateToYYYYMMDD(date: Date) {
    const day = String(date.getDate()).padStart(2, '0'); 
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    
    return `${year}-${month}-${day}`;
}

export function getDaysOfWeek(weekNumber: number, year: number) {
    const firstDayOfYear = new Date(year, 0, 1);
    const dayOfWeek = firstDayOfYear.getDay(); 

    const firstMonday = dayOfWeek <= 1 
      ? new Date(year, 0, 1 + 1 - dayOfWeek) 
      : new Date(year, 0, 1 + 8 - dayOfWeek);

    const daysInWeek = 7;
    const startOfWeek = new Date(firstMonday);
    startOfWeek.setDate(firstMonday.getDate() + daysInWeek * (weekNumber - 1));

    const days = [];
    for (let i = 0; i < daysInWeek; i++) {
        const day = new Date(startOfWeek);
        day.setDate(startOfWeek.getDate() + i);
        days.push(day);
    }

    return days;
}

export function convertYearMonthDayToDayMonthYear(date: string, separator = '.') {
    const day = date.split('-');
    
    return `${day[2]}${separator}${day[1]}${separator}${day[0]}`;
}

export const convertDDMMYYYYToISO = (dateStr: string): string => {
    const date = parse(dateStr, 'dd.MM.yyyy', new Date())
    return format(date, 'yyyy-MM-dd')
}

export const convertISOToDDMMYYYY = (dateStr: string): string => {
    const date = parse(dateStr, 'yyyy-MM-dd', new Date())
    return format(date, 'dd.MM.yyyy')
}