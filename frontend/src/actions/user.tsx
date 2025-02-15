type ChangeUserType = (user: string | null) => void
export const onlogOut = (changeUser: ChangeUserType) => {
    changeUser(null)
    localStorage.removeItem('user')
}

export const onLogIn = (changeUser: ChangeUserType, data: { name: string, project: string, isAdmin: boolean }) => {
    localStorage.setItem('user', JSON.stringify(data))
    changeUser(localStorage.getItem('user'))
}