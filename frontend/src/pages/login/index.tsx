// import React, { FC } from 'react'
// // eslint-disable-next-line @typescript-eslint/ban-ts-comment
// // @ts-expect-error
// import Logo from '../../assets/logo-2-en-finish.svg?react'

// import Button from '../../ui/Button'

// import './style.scss'

// interface LoginPageProps {
//     onLogin: (args: {name: string, password: string, project: string, isAdmin: boolean}) => void,
//     children: React.ReactNode
// }

// const LoginPage: FC<LoginPageProps> = ({onLogin, children}) => {

//     const handleLogin = (e: React.FormEvent) => {
//         e.preventDefault()
//         const login = e.target.login.value;
//         const password = e.target.password.value;
//         onLogin({name: login, password: password, project: 'Project', isAdmin: true})
//     }

//     return (
//         <div className="LoginPage">
//             {children}
//             <form className='login-form' onSubmit={(e) => handleLogin(e)}>
//                 <Logo/>
//                 <input type="text" name="login" placeholder="Логин"  />
//                 <input type="password" name="password" placeholder="Пароль" />
//                 <input type="submit" value="Войти" />
//                 {/* <Button type="primary" onClick={(e) => handleLogin(e)}>Войти</Button> */}
//             </form>
//         </div>
//     )
// }

// export default LoginPage