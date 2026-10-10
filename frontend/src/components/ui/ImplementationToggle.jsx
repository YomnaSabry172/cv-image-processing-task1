// Owner: Lead — choose built-in / manual (/ compare) implementation
import SegmentedControl from './SegmentedControl'

export default function ImplementationToggle({ value, onChange, allowCompare = true }) {
  const options = [
    { value: 'builtin', label: 'Built-in' },
    { value: 'manual', label: 'Manual' },
  ]
  if (allowCompare) options.push({ value: 'compare', label: 'Compare' })
  return <SegmentedControl label="Implementation" options={options} value={value} onChange={onChange} />
}
