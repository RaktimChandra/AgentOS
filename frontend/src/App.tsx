import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Agents from './pages/Agents'
import Policies from './pages/Policies'
import Executions from './pages/Executions'
import Layout from './components/Layout'

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/agents" element={<Agents />} />
          <Route path="/policies" element={<Policies />} />
          <Route path="/executions" element={<Executions />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
