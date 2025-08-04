import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  User, 
  Mail, 
  Lock, 
  Phone, 
  MapPin, 
  Sparkles,
  Eye,
  EyeOff,
  Check,
  AlertCircle
} from 'lucide-react'

export default function AuthScreen({ setCurrentUser }) {
  const [isLogin, setIsLogin] = useState(true)
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    firstName: '',
    lastName: '',
    phone: '',
    market: 'US',
    preferences: {
      style: 'casual',
      budget: 'medium',
      notifications: true
    }
  })
  const [errors, setErrors] = useState({})

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: null
      }))
    }
  }

  const validateForm = () => {
    const newErrors = {}
    
    if (!formData.email) {
      newErrors.email = 'Email is required'
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid'
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required'
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters'
    }
    
    if (!isLogin) {
      if (!formData.firstName) newErrors.firstName = 'First name is required'
      if (!formData.lastName) newErrors.lastName = 'Last name is required'
      if (!formData.phone) newErrors.phone = 'Phone number is required'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) return
    
    setIsLoading(true)
    
    try {
      // Simulate API call to WS1 User Management
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      if (isLogin) {
        // Login simulation
        const user = {
          id: 1,
          name: formData.firstName || 'Jane',
          email: formData.email,
          market: formData.market,
          preferences: formData.preferences,
          avatar: '👩',
          joinedDate: '2024-01-15',
          stylingScore: 92,
          totalOutfits: 47,
          totalPurchases: 23
        }
        setCurrentUser(user)
        window.location.href = '/'
      } else {
        // Registration simulation
        const user = {
          id: Date.now(),
          name: `${formData.firstName} ${formData.lastName}`,
          email: formData.email,
          phone: formData.phone,
          market: formData.market,
          preferences: formData.preferences,
          avatar: '👩',
          joinedDate: new Date().toISOString().split('T')[0],
          stylingScore: 0,
          totalOutfits: 0,
          totalPurchases: 0
        }
        setCurrentUser(user)
        window.location.href = '/'
      }
    } catch (error) {
      setErrors({ submit: 'Authentication failed. Please try again.' })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="p-4 space-y-6">
      {/* Header */}
      <div className="text-center py-6">
        <div className="w-16 h-16 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full flex items-center justify-center mb-4 mx-auto">
          <Sparkles className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent mb-2">
          {isLogin ? 'Welcome Back!' : 'Join Tanvi'}
        </h1>
        <p className="text-gray-600">
          {isLogin ? 'Sign in to continue your fashion journey' : 'Start your AI-powered fashion journey'}
        </p>
      </div>

      {/* Auth Form */}
      <Card>
        <CardHeader>
          <CardTitle className="text-center">
            {isLogin ? 'Sign In' : 'Create Account'}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Registration Fields */}
            {!isLogin && (
              <>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <Label htmlFor="firstName">First Name</Label>
                    <Input
                      id="firstName"
                      type="text"
                      value={formData.firstName}
                      onChange={(e) => handleInputChange('firstName', e.target.value)}
                      className={errors.firstName ? 'border-red-500' : ''}
                    />
                    {errors.firstName && (
                      <p className="text-xs text-red-500 mt-1 flex items-center">
                        <AlertCircle className="w-3 h-3 mr-1" />
                        {errors.firstName}
                      </p>
                    )}
                  </div>
                  <div>
                    <Label htmlFor="lastName">Last Name</Label>
                    <Input
                      id="lastName"
                      type="text"
                      value={formData.lastName}
                      onChange={(e) => handleInputChange('lastName', e.target.value)}
                      className={errors.lastName ? 'border-red-500' : ''}
                    />
                    {errors.lastName && (
                      <p className="text-xs text-red-500 mt-1 flex items-center">
                        <AlertCircle className="w-3 h-3 mr-1" />
                        {errors.lastName}
                      </p>
                    )}
                  </div>
                </div>

                <div>
                  <Label htmlFor="phone">Phone Number</Label>
                  <div className="relative">
                    <Phone className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                    <Input
                      id="phone"
                      type="tel"
                      value={formData.phone}
                      onChange={(e) => handleInputChange('phone', e.target.value)}
                      className={`pl-10 ${errors.phone ? 'border-red-500' : ''}`}
                      placeholder="+1 (555) 123-4567"
                    />
                  </div>
                  {errors.phone && (
                    <p className="text-xs text-red-500 mt-1 flex items-center">
                      <AlertCircle className="w-3 h-3 mr-1" />
                      {errors.phone}
                    </p>
                  )}
                </div>

                <div>
                  <Label htmlFor="market">Shopping Market</Label>
                  <select
                    id="market"
                    value={formData.market}
                    onChange={(e) => handleInputChange('market', e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                  >
                    <option value="US">🇺🇸 United States</option>
                    <option value="IN">🇮🇳 India</option>
                  </select>
                </div>
              </>
            )}

            {/* Common Fields */}
            <div>
              <Label htmlFor="email">Email</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  className={`pl-10 ${errors.email ? 'border-red-500' : ''}`}
                  placeholder="jane@example.com"
                />
              </div>
              {errors.email && (
                <p className="text-xs text-red-500 mt-1 flex items-center">
                  <AlertCircle className="w-3 h-3 mr-1" />
                  {errors.email}
                </p>
              )}
            </div>

            <div>
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={formData.password}
                  onChange={(e) => handleInputChange('password', e.target.value)}
                  className={`pl-10 pr-10 ${errors.password ? 'border-red-500' : ''}`}
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
              {errors.password && (
                <p className="text-xs text-red-500 mt-1 flex items-center">
                  <AlertCircle className="w-3 h-3 mr-1" />
                  {errors.password}
                </p>
              )}
            </div>

            {/* Style Preferences for Registration */}
            {!isLogin && (
              <div>
                <Label>Style Preferences</Label>
                <div className="grid grid-cols-3 gap-2 mt-2">
                  {['casual', 'formal', 'trendy'].map((style) => (
                    <Button
                      key={style}
                      type="button"
                      variant={formData.preferences.style === style ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => handleInputChange('preferences', {
                        ...formData.preferences,
                        style
                      })}
                      className="capitalize"
                    >
                      {style}
                    </Button>
                  ))}
                </div>
              </div>
            )}

            {/* Submit Error */}
            {errors.submit && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-md">
                <p className="text-sm text-red-600 flex items-center">
                  <AlertCircle className="w-4 h-4 mr-2" />
                  {errors.submit}
                </p>
              </div>
            )}

            {/* Submit Button */}
            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700"
              disabled={isLoading}
            >
              {isLoading ? (
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>{isLogin ? 'Signing In...' : 'Creating Account...'}</span>
                </div>
              ) : (
                <span>{isLogin ? 'Sign In' : 'Create Account'}</span>
              )}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Toggle Auth Mode */}
      <div className="text-center">
        <p className="text-gray-600 mb-2">
          {isLogin ? "Don't have an account?" : "Already have an account?"}
        </p>
        <Button
          variant="ghost"
          onClick={() => {
            setIsLogin(!isLogin)
            setErrors({})
            setFormData({
              email: '',
              password: '',
              firstName: '',
              lastName: '',
              phone: '',
              market: 'US',
              preferences: {
                style: 'casual',
                budget: 'medium',
                notifications: true
              }
            })
          }}
          className="text-pink-600 hover:text-pink-700"
        >
          {isLogin ? 'Create Account' : 'Sign In Instead'}
        </Button>
      </div>

      {/* Features Preview */}
      <Card className="bg-gradient-to-r from-pink-50 to-purple-50 border-pink-200">
        <CardContent className="pt-6">
          <h3 className="font-semibold text-gray-800 mb-3">What you'll get:</h3>
          <div className="space-y-2">
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Check className="w-4 h-4 text-green-500" />
              <span>AI-powered styling recommendations</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Check className="w-4 h-4 text-green-500" />
              <span>Smart wardrobe management</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Check className="w-4 h-4 text-green-500" />
              <span>Lightning-fast shopping experience</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Check className="w-4 h-4 text-green-500" />
              <span>Social style sharing & inspiration</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* WS1 Integration Status */}
      <div className="text-center">
        <Badge variant="outline" className="text-xs">
          🔗 WS1: User Management Integration Ready
        </Badge>
      </div>
    </div>
  )
}

