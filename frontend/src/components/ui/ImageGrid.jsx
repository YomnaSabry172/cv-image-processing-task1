// Owner: Lead — responsive grid of ImagePanels
const COLS = {
  1: 'grid-cols-1',
  2: 'grid-cols-1 sm:grid-cols-2',
  3: 'grid-cols-1 sm:grid-cols-2 xl:grid-cols-3',
  4: 'grid-cols-1 sm:grid-cols-2 2xl:grid-cols-4',
}

export default function ImageGrid({ cols = 2, children }) {
  return <div className={`grid gap-4 ${COLS[cols] || COLS[2]}`}>{children}</div>
}
