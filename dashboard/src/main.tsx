import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import FloorPlanDashboard from './FloorPlanDashboard.tsx'
import React from 'react'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <FloorPlanDashboard />
  </StrictMode>,
)
