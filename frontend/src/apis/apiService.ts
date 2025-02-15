// apiService.ts
import { DataType } from "./types"; // Импортируйте типы данных, если они определены в отдельном файле

export const fetchBookingsData = async (datePeriod: string): Promise<DataType[]> => {
    try {
        // const username = "admin"; // замените на нужный логин
        // const password = "admin"; // замените на нужный пароль
        // const credentials = btoa(`${username}:${password}`);
        // // Формируем URL с query-параметром
        // console.log(datePeriod)
        const url = new URL("http://127.0.0.1/api/v1/info/bookings");

        const response = await fetch(url.toString(), {
            method: "POST",
            headers: {
                // "Authorization": `Basic ${credentials}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ date_period: datePeriod })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();

        // Преобразуем данные, если требуется
        const transformedData: DataType[] = result.map((item: any) => ({
            name: item.project,
            date: item.date,
            days: [], // если API не возвращает список дней, оставляем пустым
            analyze: [item.analyse],
            item: item.equipment,
            executor: item.executor,
            sample: item.samples,
            status: item.status,
            comment: item.comment || "",
        }));

        console.log("Данные загружены:", transformedData);
        return transformedData;
    } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
        throw error;
    }
};