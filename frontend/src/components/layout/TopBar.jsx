// Owner: Lead — top bar: menu button (small screens) + theme toggle
import { Menu, Moon, Sun } from 'lucide-react'
import Button from '../ui/Button'
import { useTheme } from '../../hooks/useTheme'

export default function TopBar({ onMenu }) {
  const { dark, toggle } = useTheme()
  return (
    <header className="sticky top-0 z-30 flex h-14 items-center justify-between gap-3 border-b border-zinc-200 bg-zinc-50/80 px-4 backdrop-blur dark:border-zinc-800 dark:bg-zinc-950/80 lg:justify-end">
      <div className="flex items-center gap-2 lg:hidden">
        <Button variant="ghost" size="icon" aria-label="Open menu" onClick={onMenu} icon={Menu} />
        <span className="text-sm font-semibold">CV Image Lab</span>
      </div>
      <Button
        variant="ghost"
        size="icon"
        aria-label={dark ? 'Switch to light mode' : 'Switch to dark mode'}
        title={dark ? 'Light mode' : 'Dark mode'}
        onClick={toggle}
        icon={dark ? Sun : Moon}
      />
    </header>
  )
}
