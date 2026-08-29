import type { ReactNode } from 'react'
import type { LucideIcon } from 'lucide-react'

interface ResultCardProps {
  icon: LucideIcon
  title: string
  children: ReactNode
  className?: string
}

export default function ResultCard({ icon: Icon, title, children, className = '' }: ResultCardProps) {
  return (
    <div className={`card animate-slide-up overflow-hidden ${className}`}>
      <div className="flex items-center gap-3 border-b border-earth-100 bg-primary-50/50 px-6 py-4">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary-100 text-primary-700">
          <Icon className="h-5 w-5" />
        </div>
        <h3 className="text-base font-semibold text-earth-800">{title}</h3>
      </div>
      <div className="p-6">{children}</div>
    </div>
  )
}
