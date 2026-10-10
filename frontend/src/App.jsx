// Owner: Lead — routes (pre-wired for every page; nobody needs to edit this)
import { Navigate, Route, Routes } from 'react-router-dom'
import AppLayout from './components/layout/AppLayout'
import Home from './pages/Home'
import Grayscale from './pages/Grayscale'
import Noise from './pages/Noise'
import Filters from './pages/Filters'
import Edges from './pages/Edges'
import Histogram from './pages/Histogram'
import Equalize from './pages/Equalize'
import Normalize from './pages/Normalize'
import Frequency from './pages/Frequency'
import Hybrid from './pages/Hybrid'

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<Home />} />
        <Route path="grayscale" element={<Grayscale />} />
        <Route path="noise" element={<Noise />} />
        <Route path="filters" element={<Filters />} />
        <Route path="edges" element={<Edges />} />
        <Route path="histogram" element={<Histogram />} />
        <Route path="equalize" element={<Equalize />} />
        <Route path="normalize" element={<Normalize />} />
        <Route path="frequency" element={<Frequency />} />
        <Route path="hybrid" element={<Hybrid />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}
