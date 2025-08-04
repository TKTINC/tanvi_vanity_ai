import { useState, useEffect, useContext, createContext } from 'react'
import { UserAPI, TokenManager } from '../services/api'

// Auth Context
const AuthContext = createContext(null)

// Auth Provider Component
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // Initialize auth state on app load
  useEffect(() => {
    initializeAuth()
  }, [])

  const initializeAuth = async () => {
    setIsLoading(true)
    
    try {
      const token = TokenManager.getToken()
      
      if (token && !TokenManager.isTokenExpired(token)) {
        // Token exists and is valid, get user profile
        const profile = await UserAPI.getProfile()
        setUser(profile)
        setIsAuthenticated(true)
      } else {
        // No valid token, clear any stored tokens
        TokenManager.removeToken()
        TokenManager.removeRefreshToken()
        setUser(null)
        setIsAuthenticated(false)
      }
    } catch (error) {
      console.error('Auth initialization error:', error)
      // Clear tokens on error
      TokenManager.removeToken()
      TokenManager.removeRefreshToken()
      setUser(null)
      setIsAuthenticated(false)
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (email, password) => {
    try {
      setIsLoading(true)
      const response = await UserAPI.login(email, password)
      
      setUser(response)
      setIsAuthenticated(true)
      
      return { success: true, user: response }
    } catch (error) {
      console.error('Login error:', error)
      return { 
        success: false, 
        error: error.message || 'Login failed. Please check your credentials.' 
      }
    } finally {
      setIsLoading(false)
    }
  }

  const register = async (userData) => {
    try {
      setIsLoading(true)
      const response = await UserAPI.register(userData)
      
      setUser(response)
      setIsAuthenticated(true)
      
      return { success: true, user: response }
    } catch (error) {
      console.error('Registration error:', error)
      return { 
        success: false, 
        error: error.message || 'Registration failed. Please try again.' 
      }
    } finally {
      setIsLoading(false)
    }
  }

  const logout = async () => {
    try {
      await UserAPI.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      setUser(null)
      setIsAuthenticated(false)
      TokenManager.removeToken()
      TokenManager.removeRefreshToken()
    }
  }

  const updateProfile = async (profileData) => {
    try {
      const response = await UserAPI.updateProfile(profileData)
      
      if (response.success) {
        // Update local user state
        setUser(prevUser => ({
          ...prevUser,
          ...response.profile
        }))
      }
      
      return response
    } catch (error) {
      console.error('Profile update error:', error)
      return { 
        success: false, 
        error: error.message || 'Failed to update profile' 
      }
    }
  }

  const updatePreferences = async (preferences) => {
    try {
      const response = await UserAPI.updatePreferences(preferences)
      
      if (response.success) {
        // Update local user state
        setUser(prevUser => ({
          ...prevUser,
          preferences: {
            ...prevUser.preferences,
            ...response.preferences
          }
        }))
      }
      
      return response
    } catch (error) {
      console.error('Preferences update error:', error)
      return { 
        success: false, 
        error: error.message || 'Failed to update preferences' 
      }
    }
  }

  const changePassword = async (currentPassword, newPassword) => {
    try {
      const response = await UserAPI.changePassword(currentPassword, newPassword)
      return response
    } catch (error) {
      console.error('Password change error:', error)
      return { 
        success: false, 
        error: error.message || 'Failed to change password' 
      }
    }
  }

  const refreshUserData = async () => {
    try {
      const profile = await UserAPI.getProfile()
      setUser(profile)
      return profile
    } catch (error) {
      console.error('Refresh user data error:', error)
      return null
    }
  }

  const value = {
    user,
    isLoading,
    isAuthenticated,
    login,
    register,
    logout,
    updateProfile,
    updatePreferences,
    changePassword,
    refreshUserData,
    initializeAuth
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

// Custom hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext)
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  
  return context
}

// Higher-order component for protected routes
export function withAuth(Component) {
  return function AuthenticatedComponent(props) {
    const { isAuthenticated, isLoading } = useAuth()
    
    if (isLoading) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-indigo-50 flex items-center justify-center">
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full flex items-center justify-center mb-4 mx-auto animate-pulse">
              <span className="text-2xl">✨</span>
            </div>
            <p className="text-gray-600">Loading...</p>
          </div>
        </div>
      )
    }
    
    if (!isAuthenticated) {
      window.location.href = '/auth'
      return null
    }
    
    return <Component {...props} />
  }
}

export default useAuth

