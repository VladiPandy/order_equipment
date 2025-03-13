import { DataType } from "../types";
import { BookingListsResponse } from "../types";

export const fetchBookingsData = async (datePeriod: string): Promise<DataType[]> => {
    try {
        const username = "project1"; // замените на нужный логин
        const password = "project1"; // замените на нужный пароль
        const credentials = btoa(`${username}:${password}`);
        // console.log(datePeriod)
        const url = new URL("http://80.209.240.64/api/v1/info/bookings");

        const response = await fetch(url.toString(), {
            method: "GET",
            headers: {
                "Authorization": `Basic ${credentials}`,
                "Content-Type": "application/json",
            },
            // body: JSON.stringify({ year: 2025, week: 10 })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();

        // Преобразуем данные, если требуется
        const transformedData: DataType[] = result.map((item: any) => ({
            name: item.project,
            date: item.date,
            days: [],
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

export const fetchBookingLists = async (datePeriod: string): Promise<BookingListsResponse> => {
    try {
        const username = "project1"; // замените на нужный логин
        const password = "project1"; // замените на нужный пароль
        const credentials = btoa(`${username}:${password}`);
        const response = await fetch("http://80.209.240.64/api/v1/info/booking_lists", {
            method: "GET",
            headers: {
                "Authorization": `Basic ${credentials}`,
                "Content-Type": "application/json",
            },
            // body: JSON.stringify({ year: 2025, week: 10 })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("API booking lists:", data);
        return data as BookingListsResponse;
    } catch (error) {
        console.error("Ошибка при загрузке списка бронирований:", error);
        throw error;
    }
};

export const arrayToOptions = (arr: string[]): Record<string, string> => {
    return arr.reduce((acc, cur, idx) => {
        acc[idx.toString()] = cur;
        return acc;
    }, {} as Record<string, string>);
};