import './App.css'
import Login from './pages/Login'
import Account from './pages/Account'
import { BrowserRouter, Outlet, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './contexts/Auth'
import RootLayout from './RootLayout'
import ProtectedRoute from './components/ProtectedRoute'
import Privacy from './pages/Privacy'
import NotFound from './pages/NotFound'
import ChatBotsPage from './pages/ChatBotsPage'
import ChatBotsDetailPage from './pages/ChatBotsDetailPage'
import ChatBotsNewPage from './pages/ChatBotsNewPage'
import ChatBotsLayout from './ChatBotsLayout'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <RootLayout>
          <Routes>
            <Route element={<ProtectedRoute />}>
              <Route path="/" element={<Account />} />
            </Route>

            <Route path="/chatbots" element={<ChatBotsLayout />}>
              <Route index element={<ChatBotsPage />} />
              <Route path=":id" element={<ChatBotsDetailPage />} />
              <Route path="/chatbots/new" element={<ChatBotsNewPage />} />
            </Route>

            {/* Public Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/privacy" element={<Privacy />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </RootLayout>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
