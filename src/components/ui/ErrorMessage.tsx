import { CircleAlert as AlertCircle } from 'lucide-react'

export default function ErrorMessage({
  message,
  onRetry,
}: {
  message: string
  onRetry?: () => void
}) {
  return (
    <div className="flex flex-col items-center gap-4 rounded-2xl border border-red-200 bg-red-50 px-6 py-8 text-center">
      <AlertCircle className="h-10 w-10 text-red-500" />
      <div>
        <p className="font-semibold text-red-800">Something went wrong</p>
        <p className="mt-1 text-sm text-red-600">{message}</p>
      </div>
      {onRetry && (
        <button onClick={onRetry} className="btn-secondary border-red-200 text-red-700 hover:bg-red-50">
          Try Again
        </button>
      )}
    </div>
  )
}
