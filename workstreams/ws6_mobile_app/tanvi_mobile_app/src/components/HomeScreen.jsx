import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  Sparkles, 
  Camera, 
  ShoppingBag, 
  Users, 
  TrendingUp,
  Clock,
  Star,
  Heart,
  Eye,
  Zap
} from 'lucide-react'

export default function HomeScreen({ currentUser, currentMarket }) {
  const [quickStats, setQuickStats] = useState({
    outfitsCreated: 0,
    itemsPurchased: 0,
    stylingScore: 0,
    timesSaved: 0
  })

  const [trendingItems, setTrendingItems] = useState([])
  const [aiRecommendations, setAiRecommendations] = useState([])

  useEffect(() => {
    // Simulate loading user stats and recommendations
    setTimeout(() => {
      setQuickStats({
        outfitsCreated: 47,
        itemsPurchased: 23,
        stylingScore: 92,
        timesSaved: 156 // minutes
      })

      setTrendingItems([
        { id: 1, name: 'Summer Floral Dress', price: '$89', image: '👗', trend: '+23%' },
        { id: 2, name: 'Denim Jacket', price: '$65', image: '🧥', trend: '+18%' },
        { id: 3, name: 'White Sneakers', price: '$120', image: '👟', trend: '+15%' }
      ])

      setAiRecommendations([
        { id: 1, type: 'outfit', title: 'Perfect for your meeting today', confidence: 94 },
        { id: 2, type: 'purchase', title: 'This dress matches your style', confidence: 89 },
        { id: 3, type: 'wardrobe', title: 'Mix & match suggestion', confidence: 87 }
      ])
    }, 1000)
  }, [])

  return (
    <div className="p-4 space-y-6">
      {/* Welcome Section */}
      <div className="text-center py-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          {currentUser ? `Welcome back, ${currentUser.name}!` : 'Welcome to Tanvi!'}
        </h2>
        <p className="text-gray-600 mb-4">
          Your AI-powered fashion assistant is ready
        </p>
        <div className="flex items-center justify-center space-x-2 text-sm text-gray-500">
          <Clock className="w-4 h-4" />
          <span>Saved {quickStats.timesSaved} minutes this month</span>
        </div>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Zap className="w-5 h-5 text-yellow-500" />
            <span>Quick Actions</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-3">
            <Button 
              className="h-20 flex-col space-y-2 bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700"
              onClick={() => window.location.href = '/camera'}
            >
              <Camera className="w-6 h-6" />
              <span className="text-sm">Style Me</span>
            </Button>
            <Button 
              variant="outline" 
              className="h-20 flex-col space-y-2 border-pink-200 hover:bg-pink-50"
              onClick={() => window.location.href = '/shop'}
            >
              <ShoppingBag className="w-6 h-6 text-pink-600" />
              <span className="text-sm">Shop Now</span>
            </Button>
            <Button 
              variant="outline" 
              className="h-20 flex-col space-y-2 border-purple-200 hover:bg-purple-50"
              onClick={() => window.location.href = '/wardrobe'}
            >
              <Sparkles className="w-6 h-6 text-purple-600" />
              <span className="text-sm">My Wardrobe</span>
            </Button>
            <Button 
              variant="outline" 
              className="h-20 flex-col space-y-2 border-indigo-200 hover:bg-indigo-50"
              onClick={() => window.location.href = '/social'}
            >
              <Users className="w-6 h-6 text-indigo-600" />
              <span className="text-sm">Community</span>
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* User Stats */}
      {currentUser && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="w-5 h-5 text-green-500" />
              <span>Your Fashion Journey</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-3 bg-pink-50 rounded-lg">
                <div className="text-2xl font-bold text-pink-600">{quickStats.outfitsCreated}</div>
                <div className="text-sm text-gray-600">Outfits Created</div>
              </div>
              <div className="text-center p-3 bg-purple-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">{quickStats.itemsPurchased}</div>
                <div className="text-sm text-gray-600">Items Purchased</div>
              </div>
              <div className="text-center p-3 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">{quickStats.stylingScore}%</div>
                <div className="text-sm text-gray-600">Style Score</div>
              </div>
              <div className="text-center p-3 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{quickStats.timesSaved}m</div>
                <div className="text-sm text-gray-600">Time Saved</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* AI Recommendations */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Sparkles className="w-5 h-5 text-purple-500" />
            <span>AI Recommendations</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {aiRecommendations.map((rec) => (
              <div key={rec.id} className="flex items-center justify-between p-3 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg">
                <div className="flex-1">
                  <p className="font-medium text-gray-800">{rec.title}</p>
                  <div className="flex items-center space-x-2 mt-1">
                    <Badge variant="secondary" className="text-xs">
                      {rec.confidence}% confidence
                    </Badge>
                    <span className="text-xs text-gray-500 capitalize">{rec.type}</span>
                  </div>
                </div>
                <Button size="sm" variant="ghost">
                  <Eye className="w-4 h-4" />
                </Button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Trending Items */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="w-5 h-5 text-orange-500" />
            <span>Trending in {currentMarket === 'US' ? 'USA' : 'India'}</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {trendingItems.map((item) => (
              <div key={item.id} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="text-2xl">{item.image}</div>
                <div className="flex-1">
                  <p className="font-medium text-gray-800">{item.name}</p>
                  <p className="text-sm text-gray-600">{item.price}</p>
                </div>
                <div className="text-right">
                  <Badge variant="outline" className="text-green-600 border-green-200">
                    {item.trend}
                  </Badge>
                  <Button size="sm" variant="ghost" className="ml-2">
                    <Heart className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Market Indicator */}
      <div className="text-center py-4">
        <Badge variant="outline" className="text-sm">
          {currentMarket === 'US' ? '🇺🇸 Shopping in USA' : '🇮🇳 Shopping in India'}
        </Badge>
        <p className="text-xs text-gray-500 mt-1">
          {currentMarket === 'US' ? 'Prices in USD • Free shipping over $50' : 'Prices in INR • Free shipping over ₹999'}
        </p>
      </div>
    </div>
  )
}

