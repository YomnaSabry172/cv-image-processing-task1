// Owner: Lead — global image state (original upload + current working image)
import { createContext, useCallback, useContext, useMemo, useState } from 'react'
import { readImageFile } from '../lib/image'

const ImageContext = createContext(null)

/**
 * original — the uploaded image: { dataUrl, name, width, height, isColor }
 * working  — the input every page uses (a data URL). Starts equal to original.dataUrl.
 *            "Use as input" on any result replaces it, so you can chain: noise → filter.
 */
export function ImageProvider({ children }) {
  const [original, setOriginal] = useState(null)
  const [working, setWorkingState] = useState(null)

  const upload = useCallback(async (file) => {
    const info = await readImageFile(file)
    setOriginal(info)
    setWorkingState(info.dataUrl)
    return info
  }, [])

  const setWorking = useCallback((dataUrl) => setWorkingState(dataUrl), [])

  const resetWorking = useCallback(() => {
    if (original) setWorkingState(original.dataUrl)
  }, [original])

  const value = useMemo(
    () => ({
      original,
      working,
      isModified: Boolean(original && working !== original.dataUrl),
      upload,
      setWorking,
      resetWorking,
    }),
    [original, working, upload, setWorking, resetWorking],
  )

  return <ImageContext.Provider value={value}>{children}</ImageContext.Provider>
}

export function useImage() {
  const ctx = useContext(ImageContext)
  if (!ctx) throw new Error('useImage must be used inside <ImageProvider>')
  return ctx
}
