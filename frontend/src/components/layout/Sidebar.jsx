// Owner: Lead — grouped navigation + working-image thumbnail
import { NavLink } from 'react-router-dom'
import { RotateCcw, X } from 'lucide-react'
import { APP_ICON as AppIcon, NAV_GROUPS } from '../../lib/nav'
import { useImage } from '../../context/ImageContext'
import ApiStatus from './ApiStatus'
import Button from '../ui/Button'

function WorkingImage() {
  const { original, working, isModified, resetWorking } = useImage()
  if (!original) {
    return <p className="rounded-lg border border-dashed border-zinc-300 p-3 text-xs text-zinc-500 dark:border-zinc-700">No image loaded yet.</p>
  }
  return (
    <div className="rounded-lg border border-zinc-200 bg-white p-2 dark:border-zinc-800 dark:bg-zinc-900">
      <div className="mb-2 flex items-center justify-between gap-2">
        <span className="text-[11px] font-semibold uppercase tracking-wide text-zinc-500">Input image</span>
        {isModified && (
          <span className="rounded bg-indigo-100 px-1.5 py-0.5 text-[10px] font-medium text-indigo-700 dark:bg-indigo-500/15 dark:text-indigo-300">
            modified
          </span>
        )}
      </div>
      <div className="flex aspect-4/3 items-center justify-center rounded-md bg-zinc-900 dark:bg-zinc-950">
        <img src={working} alt="Current input" className="max-h-full max-w-full object-contain" />
      </div>
      <p className="mt-2 truncate text-[11px] text-zinc-500" title={original.name}>
        {original.name} · {original.width}×{original.height} · {original.isColor ? 'RGB' : 'Gray'}
      </p>
      {isModified && (
        <Button size="sm" variant="ghost" icon={RotateCcw} className="mt-1 w-full justify-center" onClick={resetWorking}>
          Reset to original
        </Button>
      )}
    </div>
  )
}

export default function Sidebar({ onNavigate, onClose }) {
  return (
    <nav className="flex h-full flex-col gap-5 overflow-y-auto p-4" aria-label="Main">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-white">
            <AppIcon className="h-4 w-4" aria-hidden="true" />
          </span>
          <div>
            <div className="text-sm font-semibold leading-tight">CV Image processing</div>
            <div className="text-[11px] text-zinc-500">Task 1 · Image processing</div>
          </div>
        </div>
        {onClose && <Button variant="ghost" size="icon" aria-label="Close menu" onClick={onClose} icon={X} />}
      </div>

      <div className="flex flex-col gap-4">
        {NAV_GROUPS.map((group) => (
          <div key={group.label}>
            <div className="mb-1 px-2 text-[11px] font-semibold uppercase tracking-wide text-zinc-500">{group.label}</div>
            <ul className="flex flex-col gap-0.5">
              {group.items.map(({ path, label, icon: Icon }) => (
                <li key={path}>
                  <NavLink
                    to={path}
                    end={path === '/'}
                    onClick={onNavigate}
                    className={({ isActive }) =>
                      `flex items-center gap-2.5 rounded-lg px-2 py-1.5 text-sm transition-colors ${
                        isActive
                          ? 'bg-indigo-50 font-medium text-indigo-700 dark:bg-indigo-500/15 dark:text-indigo-300'
                          : 'text-zinc-600 hover:bg-zinc-200/60 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-800/70 dark:hover:text-zinc-100'
                      }`
                    }
                  >
                    <Icon className="h-4 w-4 shrink-0" aria-hidden="true" />
                    {label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <div className="mt-auto flex flex-col gap-3">
        <WorkingImage />
        <ApiStatus />
      </div>
    </nav>
  )
}
