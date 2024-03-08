import { useQuery } from 'react-query'
import { useNavigate } from '@tanstack/react-router'

import {
  Body_login_login_access_token as AccessToken,
  LoginService,
  UserOut,
  UsersService,
} from '../client'

const isLoggedIn = () => {
  return localStorage.getItem('access_token') !== null
}

const useAuth = () => {
  const navigate = useNavigate()
  const { data: user, isLoading } = useQuery<UserOut | null, Error>(
    'currentUser',
    UsersService.readUserMe,
    {
      enabled: isLoggedIn(),
    },
  )

  const login = async (data: AccessToken) => {
    const response = await LoginService.loginAccessToken({
      formData: data,
    })
    localStorage.setItem('access_token', response.access_token)
    navigate({ to: '/' })
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    navigate({ to: '/login' })
  }

  return { login, logout, user, isLoading }
}

export { isLoggedIn }
export default useAuth
