import { Routes, Route } from "react-router-dom"
import { DashboardPage } from "./pages/DashboardPage"
import { InventoryPage } from "./pages/InventoryPage"
import { HistoryPage } from "./pages/HistoryPage"

function App() {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/inventory" element={<InventoryPage />} />
      <Route path="/history" element={<HistoryPage />} />
    </Routes>
  )
}

export default App
