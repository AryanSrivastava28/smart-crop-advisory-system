import type { ReactNode } from 'react'
import type { LucideIcon } from 'lucide-react'

interface PageHeaderProps {
  title: string
  subtitle: string
  icon: LucideIcon
  children?: ReactNode
}

export default function PageHeader({ title, subtitle, icon: Icon, children }: PageHeaderProps) {
  return (
    <div className="border-b border-earth-200 bg-gradient-to-br from-primary-50 via-white to-accent-50">
      <div className="section-container py-10 sm:py-14">
        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-primary-600 text-white shadow-lg shadow-primary-600/20">
            <Icon className="h-6 w-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-earth-800 sm:text-3xl">{title}</h1>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-earth-500 sm:text-base">
              {subtitle}
            </p>
          </div>
        </div>
        {children}
      </div>
    </div>
  )
}
