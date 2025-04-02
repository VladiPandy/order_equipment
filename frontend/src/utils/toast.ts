import { Bounce, toast, ToastOptions } from "react-toastify"

const toastBody: ToastOptions = {
    position: 'bottom-right',
    autoClose: 5000,
    closeOnClick: true,
    pauseOnHover: true,
    progress: undefined,
    theme: "light",
    transition: Bounce,
}

export const onSuccess = (message: string) => {
    toast.success(message, toastBody)
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const onError = ({code, message, response}: {code?: number, message: string, response?: any}) => {
    toast.error(
        code && `Error ${response?.status || code}: ${response?.data?.detail || message}`, toastBody);
}


