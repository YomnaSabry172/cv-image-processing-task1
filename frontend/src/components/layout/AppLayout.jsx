// Owner: Lead — page frame: sidebar (drawer on small screens) + top bar + content
import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import TopBar from './TopBar'

export default function AppLayout() {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <div className="min-h-full lg:pl-64">
      {/* Desktop sidebar */}
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-zinc-200 bg-zinc-100/60 dark:border-zinc-800 dark:bg-zinc-900/40 lg:block">
        <Sidebar />
      </aside>

      {/* Mobile drawer */}
      {menuOpen && (
        <div className="fixed inset-0 z-40 lg:hidden">
          <div className="absolute inset-0 bg-zinc-950/60" onClick={() => setMenuOpen(false)} aria-hidden="true" />
          <aside className="absolute inset-y-0 left-0 w-72 max-w-[85vw] border-r border-zinc-200 bg-zinc-50 shadow-xl dark:border-zinc-800 dark:bg-zinc-950">
            <Sidebar onNavigate={() => setMenuOpen(false)} onClose={() => setMenuOpen(false)} />
          </aside>
        </div>
      )}

      <TopBar onMenu={() => setMenuOpen(true)} />
      <main className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6">
        <Outlet />
      </main>
    </div>
  )
}
