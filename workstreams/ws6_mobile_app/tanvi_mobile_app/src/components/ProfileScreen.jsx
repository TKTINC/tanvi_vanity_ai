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
  Edit,
  Save,
  X,
  Star,
  ShoppingBag,
  Sparkles,
  TrendingUp,
  Calendar,
  Award,
  Bell,
  Shield,
  CreditCard,
  LogOut
} from 'lucide-react'

export default function ProfileScreen({ currentUser }) {
  const [isEditing, setIsEditing] = useState(false)
  const [editData, setEditData] = useState({})
  const [userStats, setUserStats] = useState({})
  const [achievements, setAchievements] = useState([])

  useEffect(() => {
    if (currentUser) {
      setEditData({
        name: currentUser.name,
        email: currentUser.email,
        phone: currentUser.phone || '+1 (555) 123-4567',
        market: currentUser.market,
        preferences: currentUser.preferences || {
          style: 'casual',
          budget: 'medium',
          notifications: true
        }
      })

      // Simulate loading user stats
      setUserStats({
        stylingScore: currentUser.stylingScore || 92,
        totalOutfits: currentUser.totalOutfits || 47,
        totalPurchases: currentUser.totalPurchases || 23,
        timesSaved: 156,
        favoriteStyle: 'Casual Chic',
        joinedDate: currentUser.joinedDate || '2024-01-15',
        level: 'Style Expert'
      })

      setAchievements([
        { id: 1, title: 'Style Starter', description: 'Created your first outfit', earned: true, icon: '🎯' },
        { id: 2, title: 'Shopping Pro', description: 'Made 20+ purchases', earned: true, icon: '🛍️' },
        { id: 3, title: 'AI Enthusiast', description: 'Used AI styling 50+ times', earned: true, icon: '🤖' },
        { id: 4, title: 'Community Star', description: 'Shared 10+ outfits', earned: false, icon: '⭐' },
        { id: 5, title: 'Fashion Guru', description: 'Reach 95% styling score', earned: false, icon: '👑' }
      ])
    }
  }, [currentUser])

  const handleSave = async () => {
    // Simulate API call to WS1 User Management
    await new Promise(resolve => setTimeout(resolve, 1000))
    setIsEditing(false)
    // In real app, would update currentUser state
  }

  const handleLogout = () => {
    // Clear user session and redirect
    window.location.href = '/auth'
  }

  if (!currentUser) {
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
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full flex items-center justify-center text-2xl">
              {currentUser.avatar || '👩'}
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-bold text-gray-800">{currentUser.name}</h2>
              <p className="text-gray-600">{currentUser.email}</p>
              <div className="flex items-center space-x-2 mt-1">
                <Badge variant="secondary" className="text-xs">
                  {userStats.level}
                </Badge>
                <Badge variant="outline" className="text-xs">
                  {currentUser.market === 'US' ? '🇺🇸 USA' : '🇮🇳 India'}
                </Badge>
              </div>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setIsEditing(!isEditing)}
            >
              {isEditing ? <X className="w-4 h-4" /> : <Edit className="w-4 h-4" />}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Edit Profile Form */}
      {isEditing && (
        <Card>
          <CardHeader>
            <CardTitle>Edit Profile</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="name">Full Name</Label>
              <Input
                id="name"
                value={editData.name}
                onChange={(e) => setEditData({...editData, name: e.target.value})}
              />
            </div>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={editData.email}
                onChange={(e) => setEditData({...editData, email: e.target.value})}
              />
            </div>
            <div>
              <Label htmlFor="phone">Phone</Label>
              <Input
                id="phone"
                value={editData.phone}
                onChange={(e) => setEditData({...editData, phone: e.target.value})}
              />
            </div>
            <div>
              <Label>Preferred Style</Label>
              <div className="grid grid-cols-3 gap-2 mt-2">
                {['casual', 'formal', 'trendy'].map((style) => (
                  <Button
                    key={style}
                    type="button"
                    variant={editData.preferences?.style === style ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setEditData({
                      ...editData,
                      preferences: {
                        ...editData.preferences,
                        style
                      }
                    })}
                    className="capitalize"
                  >
                    {style}
                  </Button>
                ))}
              </div>
            </div>
            <div className="flex space-x-2">
              <Button onClick={handleSave} className="flex-1">
                <Save className="w-4 h-4 mr-2" />
                Save Changes
              </Button>
              <Button variant="outline" onClick={() => setIsEditing(false)}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* User Stats */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="w-5 h-5 text-green-500" />
            <span>Your Fashion Stats</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-4 bg-gradient-to-r from-pink-50 to-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-pink-600 mb-1">{userStats.stylingScore}%</div>
              <div className="text-sm text-gray-600">Styling Score</div>
              <div className="flex items-center justify-center mt-1">
                {[1,2,3,4,5].map((star) => (
                  <Star 
                    key={star} 
                    className={`w-3 h-3 ${star <= Math.floor(userStats.stylingScore/20) ? 'text-yellow-400 fill-current' : 'text-gray-300'}`} 
                  />
                ))}
              </div>
            </div>
            <div className="text-center p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600 mb-1">{userStats.totalOutfits}</div>
              <div className="text-sm text-gray-600">Outfits Created</div>
              <div className="text-xs text-blue-500 mt-1">+3 this week</div>
            </div>
            <div className="text-center p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600 mb-1">{userStats.totalPurchases}</div>
              <div className="text-sm text-gray-600">Items Purchased</div>
              <div className="text-xs text-green-500 mt-1">$1,247 saved</div>
            </div>
            <div className="text-center p-4 bg-gradient-to-r from-orange-50 to-red-50 rounded-lg">
              <div className="text-2xl font-bold text-orange-600 mb-1">{userStats.timesSaved}m</div>
              <div className="text-sm text-gray-600">Time Saved</div>
              <div className="text-xs text-orange-500 mt-1">This month</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Achievements */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Award className="w-5 h-5 text-yellow-500" />
            <span>Achievements</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {achievements.map((achievement) => (
              <div 
                key={achievement.id} 
                className={`flex items-center space-x-3 p-3 rounded-lg ${
                  achievement.earned 
                    ? 'bg-gradient-to-r from-yellow-50 to-orange-50 border border-yellow-200' 
                    : 'bg-gray-50 border border-gray-200'
                }`}
              >
                <div className={`text-2xl ${achievement.earned ? '' : 'grayscale opacity-50'}`}>
                  {achievement.icon}
                </div>
                <div className="flex-1">
                  <p className={`font-medium ${achievement.earned ? 'text-gray-800' : 'text-gray-500'}`}>
                    {achievement.title}
                  </p>
                  <p className={`text-sm ${achievement.earned ? 'text-gray-600' : 'text-gray-400'}`}>
                    {achievement.description}
                  </p>
                </div>
                {achievement.earned && (
                  <Badge variant="secondary" className="text-xs bg-yellow-100 text-yellow-800">
                    Earned
                  </Badge>
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
            <Settings className="w-5 h-5 text-gray-500" />
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
            <MapPin className="w-4 h-4 mr-3" />
            Shipping Addresses
          </Button>
        </CardContent>
      </Card>

      {/* Account Info */}
      <Card>
        <CardContent className="pt-6">
          <div className="space-y-2 text-sm text-gray-600">
            <div className="flex items-center justify-between">
              <span>Member since</span>
              <span>{new Date(userStats.joinedDate).toLocaleDateString()}</span>
            </div>
            <div className="flex items-center justify-between">
              <span>Favorite style</span>
              <span>{userStats.favoriteStyle}</span>
            </div>
            <div className="flex items-center justify-between">
              <span>Market</span>
              <span>{currentUser.market === 'US' ? 'United States' : 'India'}</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Logout */}
      <Card className="border-red-200">
        <CardContent className="pt-6">
          <Button 
            variant="outline" 
            className="w-full text-red-600 border-red-200 hover:bg-red-50"
            onClick={handleLogout}
          >
            <LogOut className="w-4 h-4 mr-2" />
            Sign Out
          </Button>
        </CardContent>
      </Card>

      {/* WS1 Integration Status */}
      <div className="text-center pb-4">
        <Badge variant="outline" className="text-xs">
          🔗 WS1: User Management Integration Active
        </Badge>
      </div>
    </div>
  )
}

