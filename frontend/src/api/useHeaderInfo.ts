import { useState, useEffect } from "react";
import { HeaderInfo } from "../types";

export const useHeaderInfo = (): [HeaderInfo | null, boolean, any] => {
    const [headerInfo, setHeaderInfo] = useState<HeaderInfo | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<any>(null);

    useEffect(() => {
        const loadHeaderInfo = async () => {
            try {
                // const username = "project"; // замените на нужный логин
                // const password = "1234"; // замените на нужный пароль
                // const credentials = btoa(`${username}:${password}`);

                const response = await fetch("http://127.0.0.1/api/v1/info/project", {
                    method: "GET",
                    headers: {
                        // "Authorization": `Basic ${credentials}`,
                        "Content-Type": "application/json",
                    },
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const info = await response.json();
                console.log("Header info:", info);
                setHeaderInfo(info as HeaderInfo);
            } catch (err) {
                console.error("Ошибка загрузки информации о проекте:", err);
                setError(err);
            } finally {
                setLoading(false);
            }
        };
        loadHeaderInfo();
    }, []);

    return [headerInfo, loading, error];
};