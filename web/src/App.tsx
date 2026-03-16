import { Routes, Route } from "react-router-dom"
import { DashboardPage } from "./pages/DashboardPage"
import { InventoryPage } from "./pages/InventoryPage"
import { HistoryPage } from "./pages/HistoryPage"
import { NewLocalPage } from "./pages/NewLocalPage"
import { EditLocalPage } from "./pages/EditLocalPage"

function App() {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/inventory" element={<InventoryPage />} />
      <Route path="/history" element={<HistoryPage />} />
      <Route path="/locais/novo" element={<NewLocalPage />} />
      <Route path="/locais/:localId/editar" element={<EditLocalPage />} />
    </Routes>
  )
}

export default App
