import { Link } from 'react-router-dom'
import { useAuth } from './contexts/Auth'

export default function MainNavigation() {
  const { user } = useAuth()
  const { signOut } = useAuth()
  const handleLogout = () => {
    signOut()
  }

  return (
    <ul>
      <li>
        <Link to="/">Dashboard</Link>
        {user ? (
          <a href="#" onClick={handleLogout}>
            Logout
          </a>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </li>
      <li>Welcome back, {user?.email} !</li>
    </ul>
  )
}
