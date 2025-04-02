import './Button.scss'

interface ButtonProps<T extends (...args: never[]) => void> {
    type?: string
    className?: string
    icon?: JSX.Element
    onClick: T
    children?: string | JSX.Element  
    isActive?: boolean
}

const Button = <T extends (...args: never[]) => void>({
    onClick,
    children,
    type,
    isActive = true,
    className
  }: ButtonProps<T>) => {
    return <button className={`button ${type} ${!isActive ? 'disabled' : ''} ${className}`} onClick={isActive ? onClick : undefined}>
       {children}
    </button>
}

export default Button