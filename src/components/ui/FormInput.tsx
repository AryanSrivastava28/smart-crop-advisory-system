interface InputProps {
  label: string
  name: string
  value: string
  onChange: (name: string, value: string) => void
  onBlur?: (name: string) => void
  error?: string
  type?: string
  placeholder?: string
  min?: number
  max?: number
  step?: string
  unit?: string
  hint?: string
}

export default function FormInput({
  label,
  name,
  value,
  onChange,
  onBlur,
  error,
  type = 'number',
  placeholder,
  min,
  max,
  step,
  unit,
  hint,
}: InputProps) {
  return (
    <div>
      <label htmlFor={name} className="label-field">
        {label} {unit && <span className="text-xs font-normal text-earth-400">({unit})</span>}
      </label>
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={(e) => onChange(name, e.target.value)}
        onBlur={() => onBlur?.(name)}
        placeholder={placeholder}
        min={min}
        max={max}
        step={step}
        className={`input-field ${error ? 'border-red-400 focus:border-red-500 focus:ring-red-500/20' : ''}`}
      />
      {hint && !error && <p className="mt-1 text-xs text-earth-400">{hint}</p>}
      {error && <p className="mt-1 text-xs text-red-500">{error}</p>}
    </div>
  )
}

interface SelectProps {
  label: string
  name: string
  value: string
  onChange: (name: string, value: string) => void
  onBlur?: (name: string) => void
  error?: string
  options: { value: string; label: string }[]
  placeholder?: string
}

export function FormSelect({
  label,
  name,
  value,
  onChange,
  onBlur,
  error,
  options,
  placeholder = 'Select...',
}: SelectProps) {
  return (
    <div>
      <label htmlFor={name} className="label-field">{label}</label>
      <select
        id={name}
        name={name}
        value={value}
        onChange={(e) => onChange(name, e.target.value)}
        onBlur={() => onBlur?.(name)}
        className={`input-field ${error ? 'border-red-400 focus:border-red-500 focus:ring-red-500/20' : ''}`}
      >
        <option value="">{placeholder}</option>
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>{opt.label}</option>
        ))}
      </select>
      {error && <p className="mt-1 text-xs text-red-500">{error}</p>}
    </div>
  )
}
