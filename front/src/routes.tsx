import { createBrowserRouter } from 'react-router'

import AuthMiddleware from './middlewares/auth'
import { AppLayout } from './pages/_layouts/app'
import { AuthLayout } from './pages/_layouts/auth'
import { HomePage } from './pages/homepage'
import { Login } from './pages/login'
import Profile from './pages/profile'
import { RegisterUser } from './pages/register-user'

export const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      {
        path: '/',
        element: <HomePage />,
      },
      {
        path: '/profile',
        element: (
          <AuthMiddleware>
            <Profile />
          </AuthMiddleware>
        ),
      },
    ],
  },
  {
    element: <AuthLayout />,
    children: [
      {
        path: '/register',
        element: <RegisterUser />,
      },
      {
        path: '/login',
        element: <Login />,
      },
    ],
  },
])
