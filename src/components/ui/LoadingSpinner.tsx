import { Loader as Loader2 } from 'lucide-react'

export default function LoadingSpinner({ label = 'Analyzing...' }: { label?: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-12">
      <div className="relative">
        <Loader2 className="h-10 w-10 animate-spin text-primary-500" />
        <div className="absolute inset-0 h-10 w-10 animate-ping rounded-full bg-primary-200 opacity-20" />
      </div>
      <p className="text-sm font-medium text-earth-500">{label}</p>
    </div>
  )
}
