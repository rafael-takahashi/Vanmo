import { createBrowserRouter } from 'react-router'

import AuthMiddleware from './middlewares/auth'
import { AppLayout } from './pages/_layouts/app'
import { AuthLayout } from './pages/_layouts/auth'
import BusinessPage from './pages/business-page'
import { HomePage } from './pages/homepage'
import { Login } from './pages/login'
import Profile from './pages/profile'
import { RegisterUser } from './pages/register-user'
import SearchPage from './pages/search'

export const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      {
        path: '/',
        element: <HomePage />,
      },
      {
        path: '/search',
        element: <SearchPage />,
      },
      {
        path: '/profile',
        element: (
          <AuthMiddleware>
            <Profile />
          </AuthMiddleware>
        ),
      },
      {
        path: '/empresa/:name',
        element: <BusinessPage />,
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
