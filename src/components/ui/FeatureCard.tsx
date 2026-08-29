import { Link } from 'react-router-dom'
import type { LucideIcon } from 'lucide-react'
import { ArrowRight } from 'lucide-react'

interface FeatureCardProps {
  icon: LucideIcon
  title: string
  description: string
  to: string
  delay?: number
}

export default function FeatureCard({
  icon: Icon,
  title,
  description,
  to,
  delay = 0,
}: FeatureCardProps) {
  return (
    <Link
      to={to}
      className="card card-hover group flex flex-col gap-3 p-6 animate-fade-in-up"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-50 text-primary-600 transition-colors group-hover:bg-primary-600 group-hover:text-white">
        <Icon className="h-6 w-6" />
      </div>
      <h3 className="text-lg font-semibold text-earth-800">{title}</h3>
      <p className="flex-1 text-sm leading-relaxed text-earth-500">{description}</p>
      <span className="mt-2 inline-flex items-center gap-1.5 text-sm font-medium text-primary-600 transition-all group-hover:gap-2.5">
        Learn more <ArrowRight className="h-4 w-4" />
      </span>
    </Link>
  )
}
