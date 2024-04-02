import { useNavigate } from "@tanstack/react-router"
import { useState } from "react"
import { useMutation, useQuery } from "react-query"

import {
  type Body_login_login_access_token as AccessToken,
  type ApiError,
  LoginService,
  type UserOut,
  UsersService,
} from "../client"

const isLoggedIn = () => {
  return localStorage.getItem("access_token") !== null
}

const useAuth = () => {
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()
  const { data: user, isLoading } = useQuery<UserOut | null, Error>(
    "currentUser",
    UsersService.readUserMe,
    {
      enabled: isLoggedIn(),
    },
  )

  const login = async (data: AccessToken) => {
    const response = await LoginService.loginAccessToken({
      formData: data,
    })
    localStorage.setItem("access_token", response.access_token)
  }

  const loginMutation = useMutation(login, {
    onSuccess: () => {
      navigate({ to: "/" })
    },
    onError: (err: ApiError) => {
      const errDetail = err.body.detail
      setError(errDetail)
    },
  })

  const logout = () => {
    localStorage.removeItem("access_token")
    navigate({ to: "/login" })
  }

  return {
    loginMutation,
    logout,
    user,
    isLoading,
    error,
  }
}

export { isLoggedIn }
export default useAuth
