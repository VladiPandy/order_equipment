import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { UserProvider } from './features/user.tsx'
import { ToastContainer } from 'react-toastify'

createRoot(document.getElementById('root')!).render(
    <UserProvider>
        <ToastContainer />
        <App />
    </UserProvider>
)
