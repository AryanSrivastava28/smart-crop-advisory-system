import { useState } from 'react'
import type { FormEvent } from 'react'

interface FieldConfig {
  value: string
  min?: number
  max?: number
  required?: boolean
  label: string
}

export function useForm<T extends Record<string, FieldConfig>>(
  initial: T,
  validate?: (values: Record<string, string>) => Record<string, string>,
) {
  const [values, setValues] = useState(
    Object.fromEntries(Object.entries(initial).map(([k, v]) => [k, v.value])) as Record<string, string>,
  )
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [touched, setTouched] = useState<Record<string, boolean>>({})

  const onChange = (name: string, value: string) => {
    setValues((prev) => ({ ...prev, [name]: value }))
    if (errors[name]) {
      setErrors((prev) => {
        const next = { ...prev }
        delete next[name]
        return next
      })
    }
  }

  const onBlur = (name: string) => {
    setTouched((prev) => ({ ...prev, [name]: true }))
  }

  const validateFields = (): boolean => {
    const newErrors: Record<string, string> = {}

    for (const [key, config] of Object.entries(initial)) {
      const val = values[key]
      if (config.required && !val) {
        newErrors[key] = `${config.label} is required`
        continue
      }
      const num = Number(val)
      if (config.min !== undefined && num < config.min) {
        newErrors[key] = `${config.label} must be at least ${config.min}`
      }
      if (config.max !== undefined && num > config.max) {
        newErrors[key] = `${config.label} must be at most ${config.max}`
      }
    }

    if (validate) {
      const custom = validate(values)
      Object.assign(newErrors, custom)
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (onValid: () => void) => (e: FormEvent) => {
    e.preventDefault()
    if (validateFields()) {
      onValid()
    }
  }

  const reset = () => {
    setValues(Object.fromEntries(Object.entries(initial).map(([k, v]) => [k, v.value])))
    setErrors({})
    setTouched({})
  }

  return { values, errors, touched, onChange, onBlur, handleSubmit, reset }
}
