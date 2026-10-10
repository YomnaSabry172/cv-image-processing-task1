// Owner: Lead — React entry point
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import { ImageProvider } from './context/ImageContext'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <ImageProvider>
        <App />
      </ImageProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
