import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  User, 
  Mail, 
  Phone, 
  MapPin, 
  Settings, 
  Star,
  Trophy,
  Calendar,
  Heart,
  ShoppingBag,
  Camera,
  Edit,
  Save,
  X,
  Bell,
  Shield,
  CreditCard,
  MapPin as Address,
  Sparkles,
  TrendingUp,
  Award,
  LogOut
} from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import { UserAPI } from '../services/api'

export default function ProfileScreen({ currentUser }) {
  const { user, updateProfile, updatePreferences, logout } = useAuth()
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [userStats, setUserStats] = useState(null)
  const [achievements, setAchievements] = useState([])
  const [editData, setEditData] = useState({
    name: '',
    email: '',
    phone: '',
    market: 'US',
    preferences: {
      style: 'casual',
      budget: 'medium',
      notifications: true
    }
  })

  // Initialize edit data when user changes
  useEffect(() => {
    if (user) {
      setEditData({
        name: user.name || '',
        email: user.email || '',
        phone: user.phone || '',
        market: user.market || 'US',
        preferences: {
          style: user.preferences?.style || 'casual',
          budget: user.preferences?.budget || 'medium',
          notifications: user.preferences?.notifications !== false
        }
      })
    }
  }, [user])

  // Load user stats and achievements
  useEffect(() => {
    loadUserStats()
    loadAchievements()
  }, [])

  const loadUserStats = async () => {
    try {
      const stats = await UserAPI.getUserStats()
      setUserStats(stats)
    } catch (error) {
      console.error('Failed to load user stats:', error)
    }
  }

  const loadAchievements = async () => {
    try {
      const achievementsList = await UserAPI.getAchievements()
      setAchievements(achievementsList)
    } catch (error) {
      console.error('Failed to load achievements:', error)
    }
  }

  const handleSaveProfile = async () => {
    setIsLoading(true)
    try {
      const profileResult = await updateProfile({
        name: editData.name,
        email: editData.email,
        phone: editData.phone,
        market: editData.market
      })

      const preferencesResult = await updatePreferences(editData.preferences)

      if (profileResult.success && preferencesResult.success) {
        setIsEditing(false)
      }
    } catch (error) {
      console.error('Failed to update profile:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = async () => {
    await logout()
  }

  // Use the user from auth context, fallback to currentUser prop
  const displayUser = user || currentUser

  if (!displayUser) {
    return (
      <div className="p-4 text-center">
        <div className="py-12">
          <User className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-600 mb-2">Not Signed In</h2>
          <p className="text-gray-500 mb-4">Sign in to view your profile</p>
          <Button onClick={() => window.location.href = '/auth'}>
            Sign In
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="p-4 space-y-6">
      {/* Profile Header */}
      <Card className="bg-gradient-to-r from-pink-50 to-purple-50 border-pink-200">
        <CardContent className="pt-6">
          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full flex items-center justify-center text-2xl">
              {displayUser.avatar || '👩'}
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-bold text-gray-800">{displayUser.name}</h2>
              <p className="text-gray-600">{displayUser.email}</p>
              <div className="flex items-center space-x-2 mt-1">
                <Badge variant="outline" className="text-xs">
                  {displayUser.market === 'US' ? '🇺🇸 USA' : '🇮🇳 India'}
                </Badge>
                <Badge variant="outline" className="text-xs">
                  Member since {displayUser.joinedDate}
                </Badge>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsEditing(!isEditing)}
            >
              {isEditing ? <X className="w-4 h-4" /> : <Edit className="w-4 h-4" />}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* User Stats */}
      <div className="grid grid-cols-3 gap-3">
        <Card className="text-center">
          <CardContent className="pt-4">
            <div className="text-2xl font-bold text-pink-600">
              {userStats?.totalOutfits || displayUser.totalOutfits || 47}
            </div>
            <p className="text-xs text-gray-600">Outfits</p>
          </CardContent>
        </Card>
        <Card className="text-center">
          <CardContent className="pt-4">
            <div className="text-2xl font-bold text-purple-600">
              {userStats?.totalPurchases || displayUser.totalPurchases || 23}
            </div>
            <p className="text-xs text-gray-600">Purchases</p>
          </CardContent>
        </Card>
        <Card className="text-center">
          <CardContent className="pt-4">
            <div className="flex items-center justify-center space-x-1">
              <div className="text-2xl font-bold text-yellow-600">
                {userStats?.stylingScore || displayUser.stylingScore || 92}
              </div>
              <Star className="w-4 h-4 text-yellow-500 fill-current" />
            </div>
            <p className="text-xs text-gray-600">Style Score</p>
          </CardContent>
        </Card>
      </div>

      {/* Edit Profile Form */}
      {isEditing && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Edit className="w-5 h-5" />
              <span>Edit Profile</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="name">Full Name</Label>
              <Input
                id="name"
                value={editData.name}
                onChange={(e) => setEditData(prev => ({ ...prev, name: e.target.value }))}
                placeholder="Enter your full name"
              />
            </div>

            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={editData.email}
                onChange={(e) => setEditData(prev => ({ ...prev, email: e.target.value }))}
                placeholder="Enter your email"
              />
            </div>

            <div>
              <Label htmlFor="phone">Phone Number</Label>
              <Input
                id="phone"
                type="tel"
                value={editData.phone}
                onChange={(e) => setEditData(prev => ({ ...prev, phone: e.target.value }))}
                placeholder="+1 (555) 123-4567"
              />
            </div>

            <div>
              <Label htmlFor="market">Shopping Market</Label>
              <select
                id="market"
                value={editData.market}
                onChange={(e) => setEditData(prev => ({ ...prev, market: e.target.value }))}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-pink-500 focus:border-transparent"
              >
                <option value="US">🇺🇸 United States</option>
                <option value="IN">🇮🇳 India</option>
              </select>
            </div>

            <div>
              <Label>Style Preferences</Label>
              <div className="grid grid-cols-3 gap-2 mt-2">
                {['casual', 'formal', 'trendy'].map((style) => (
                  <Button
                    key={style}
                    type="button"
                    variant={editData.preferences.style === style ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setEditData(prev => ({
                      ...prev,
                      preferences: { ...prev.preferences, style }
                    }))}
                    className="capitalize"
                  >
                    {style}
                  </Button>
                ))}
              </div>
            </div>

            <div>
              <Label>Budget Range</Label>
              <div className="grid grid-cols-3 gap-2 mt-2">
                {['low', 'medium', 'high'].map((budget) => (
                  <Button
                    key={budget}
                    type="button"
                    variant={editData.preferences.budget === budget ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setEditData(prev => ({
                      ...prev,
                      preferences: { ...prev.preferences, budget }
                    }))}
                    className="capitalize"
                  >
                    {budget}
                  </Button>
                ))}
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="notifications"
                checked={editData.preferences.notifications}
                onChange={(e) => setEditData(prev => ({
                  ...prev,
                  preferences: { ...prev.preferences, notifications: e.target.checked }
                }))}
                className="rounded border-gray-300 text-pink-600 focus:ring-pink-500"
              />
              <Label htmlFor="notifications">Enable notifications</Label>
            </div>

            <div className="flex space-x-2">
              <Button
                onClick={handleSaveProfile}
                disabled={isLoading}
                className="flex-1 bg-gradient-to-r from-pink-500 to-purple-600"
              >
                {isLoading ? (
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Saving...</span>
                  </div>
                ) : (
                  <>
                    <Save className="w-4 h-4 mr-2" />
                    Save Changes
                  </>
                )}
              </Button>
              <Button
                variant="outline"
                onClick={() => setIsEditing(false)}
                disabled={isLoading}
              >
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Achievements */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Trophy className="w-5 h-5 text-yellow-500" />
            <span>Achievements</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-3">
            {achievements.map((achievement) => (
              <div
                key={achievement.id}
                className={`p-3 rounded-lg border ${
                  achievement.earned 
                    ? 'bg-yellow-50 border-yellow-200' 
                    : 'bg-gray-50 border-gray-200'
                }`}
              >
                <div className="flex items-center space-x-2 mb-1">
                  <span className="text-lg">{achievement.icon}</span>
                  <span className={`text-sm font-medium ${
                    achievement.earned ? 'text-gray-800' : 'text-gray-500'
                  }`}>
                    {achievement.title}
                  </span>
                </div>
                <p className="text-xs text-gray-600">{achievement.description}</p>
                {achievement.earned && achievement.earnedDate && (
                  <p className="text-xs text-yellow-600 mt-1">
                    Earned {achievement.earnedDate}
                  </p>
                )}
                {!achievement.earned && achievement.progress !== undefined && (
                  <div className="mt-2">
                    <div className="w-full bg-gray-200 rounded-full h-1">
                      <div 
                        className="bg-pink-500 h-1 rounded-full" 
                        style={{ width: `${(achievement.progress / 100) * 100}%` }}
                      ></div>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      Progress: {achievement.progress}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Account Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Settings className="w-5 h-5" />
            <span>Account Settings</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <Button variant="ghost" className="w-full justify-start">
            <Bell className="w-4 h-4 mr-3" />
            Notification Settings
          </Button>
          <Button variant="ghost" className="w-full justify-start">
            <Shield className="w-4 h-4 mr-3" />
            Privacy & Security
          </Button>
          <Button variant="ghost" className="w-full justify-start">
            <CreditCard className="w-4 h-4 mr-3" />
            Payment Methods
          </Button>
          <Button variant="ghost" className="w-full justify-start">
            <Address className="w-4 h-4 mr-3" />
            Shipping Addresses
          </Button>
        </CardContent>
      </Card>

      {/* Style Insights */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="w-5 h-5 text-pink-500" />
            <span>Style Insights</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Favorite Style</span>
              <Badge variant="outline">{userStats?.favoriteStyle || 'Casual Chic'}</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Style Level</span>
              <Badge className="bg-gradient-to-r from-pink-500 to-purple-600">
                {userStats?.level || 'Style Expert'}
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Time Saved This Month</span>
              <span className="text-sm font-medium text-green-600">
                {userStats?.timesSaved || 156} minutes
              </span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Logout Button */}
      <Button
        variant="outline"
        onClick={handleLogout}
        className="w-full text-red-600 border-red-200 hover:bg-red-50"
      >
        <LogOut className="w-4 h-4 mr-2" />
        Sign Out
      </Button>

      {/* WS1 Integration Status */}
      <div className="text-center">
        <Badge variant="outline" className="text-xs">
          🔗 WS1: User Management Integration Active
        </Badge>
      </div>
    </div>
  )
}

