import { Outlet } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute'

export default function ChatBotsLayout() {
  return (
    <>
      <ProtectedRoute>
        <Outlet />
      </ProtectedRoute>
    </>
  )
}
