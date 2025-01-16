import Cookies from 'js-cookie'
import { ReactNode } from 'react'
import { Navigate } from 'react-router'

interface AuthMiddlewareProps {
  children: ReactNode
}

export default function AuthMiddleware({ children }: AuthMiddlewareProps) {
  const token = Cookies.get('auth_token')

  if (!token) {
    return <Navigate to="/login" replace />
  }

  return children
}
