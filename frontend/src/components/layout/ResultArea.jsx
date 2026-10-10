// Owner: Lead — shows the right state for a useProcess() result: not implemented / error / loading / results
import ErrorBanner from '../ui/ErrorBanner'
import LoadingOverlay from '../ui/LoadingOverlay'
import NotImplementedCard from '../ui/NotImplementedCard'

/**
 * <ResultArea process={useProcessResult}>{results}</ResultArea>
 * children is only rendered once there is data.
 */
export default function ResultArea({ process, children }) {
  const { data, loading, error, notImplemented } = process

  if (notImplemented) return <NotImplementedCard detail={error} />

  return (
    <div className="relative flex min-h-48 flex-col gap-4">
      {error && <ErrorBanner message={error} />}
      {data && children}
      {!data && !error && !loading && <p className="py-12 text-center text-sm text-zinc-500">Results will appear here.</p>}
      <LoadingOverlay show={loading} />
    </div>
  )
}
