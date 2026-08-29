interface ConfidenceBarProps {
  value: number
  label?: string
}

export default function ConfidenceBar({ value, label = 'Confidence' }: ConfidenceBarProps) {
  const color =
    value >= 85 ? 'bg-primary-500' : value >= 70 ? 'bg-accent-500' : 'bg-amber-500'

  return (
    <div>
      <div className="mb-1.5 flex items-center justify-between text-sm">
        <span className="font-medium text-earth-600">{label}</span>
        <span className="font-semibold text-earth-800">{value}%</span>
      </div>
      <div className="h-2.5 w-full overflow-hidden rounded-full bg-earth-100">
        <div
          className={`h-full rounded-full ${color} transition-all duration-700 ease-out`}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  )
}
