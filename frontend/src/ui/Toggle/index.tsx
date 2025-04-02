import { FC } from 'react'
import './style.scss'

type ToggleProps = {
    checked: boolean
    onChange: () => void
    label?: string
}

const Toggle: FC<ToggleProps> = ({ checked, onChange, label }) => {
    return (
        <div className="toggle-wrapper">
            {label && <span className="toggle-label">{label}</span>}
            <label className="toggle">
                <input
                    type="checkbox"
                    checked={checked}
                    onChange={onChange}
                />
                <span className="toggle-slider" />
            </label>
        </div>
    )
}

export default Toggle 