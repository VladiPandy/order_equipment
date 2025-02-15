import React, { FC } from 'react'
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import Logo from '../../assets/logo-2-en-finish.svg?react'

import Button from '../../ui/Button'

import './style.scss'

interface LoginPageProps {
    onLogin: (args: {name: string, project: string, isAdmin: boolean}) => void
}

const LoginPage: FC<LoginPageProps> = ({onLogin}) => {

    const handleLogin = (e: React.MouseEvent) => {
        e.preventDefault()
        const form = e.currentTarget.closest('form');
        if (form) { 
            const login = form.elements[0] as HTMLInputElement;
            // const pass = form.elements[1] as HTMLInputElement;
            onLogin({name: login.value, project: 'Project', isAdmin: true})
        }
    }

    return (
        <div className="LoginPage">
            <form className='login-form'>
                <Logo/>
                <input type="text" placeholder="Логин"  />
                <input type="password" placeholder="Пароль" />
                <Button type="primary" onClick={(e) => handleLogin(e)}>Войти</Button>
            </form>
        </div>
    )
}

export default LoginPage