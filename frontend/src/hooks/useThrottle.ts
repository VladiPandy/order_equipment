import { useCallback } from 'react'

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const useThrottle = <T extends (...args: any[]) => void>(
    callback: T,
    delay: number = 400
): T => {
    return useCallback(
        (...args: Parameters<T>) => {
            setTimeout(() => {
                callback(...args)
            }, delay)
        },
        [callback, delay]
    ) as T
} 