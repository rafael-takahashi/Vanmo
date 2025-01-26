import { createBrowserRouter } from 'react-router'

import AuthMiddleware from './middlewares/auth'
import { AppLayout } from './pages/_layouts/app'
import { AuthLayout } from './pages/_layouts/auth'
import { Login } from './pages/auth/login'
import { RegisterUser } from './pages/auth/register-user'
import BusinessPage from './pages/business-page'
import { HomePage } from './pages/homepage'
import MyProposalsPage from './pages/profile/my-proposals-page'
import MyVehiclesPage from './pages/profile/my-vehicles.page'
import Profile from './pages/profile/profile'
import { ProposalPage } from './pages/proposal'
import SearchPage from './pages/search'
import AddVehiclePage from './pages/profile/add-vehicle-page'

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
        path: '/profile/proposals',
        element: (
          <AuthMiddleware>
            <MyProposalsPage />
          </AuthMiddleware>
        ),
      },
      {
        path: '/profile/vehicles',
        element: (
          <AuthMiddleware>
            <MyVehiclesPage />
          </AuthMiddleware>
        ),
      },
      {
        path: '/profile/add-vehicle',
        element: (
          <AuthMiddleware>
            <AddVehiclePage />
          </AuthMiddleware>
        ),
      },
      {
        path: '/empresa/:name',
        element: <BusinessPage />,
      },
      {
        path: '/proposta',
        element: (
          <AuthMiddleware>
            <ProposalPage />
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
