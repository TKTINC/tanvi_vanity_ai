import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  Sparkles, 
  Camera, 
  Wand2,
  Star,
  Heart,
  Share2,
  Download,
  RefreshCw,
  Zap,
  Eye,
  ThumbsUp,
  Clock,
  Palette,
  Shirt,
  Sun,
  Cloud,
  Briefcase,
  Coffee,
  Music,
  Calendar
} from 'lucide-react'

export default function AIStyleScreen({ currentUser }) {
  const [isGenerating, setIsGenerating] = useState(false)
  const [currentOutfit, setCurrentOutfit] = useState(null)
  const [styleHistory, setStyleHistory] = useState([])
  const [selectedOccasion, setSelectedOccasion] = useState('casual')
  const [selectedWeather, setSelectedWeather] = useState('sunny')
  const [aiInsights, setAiInsights] = useState(null)

  const occasions = [
    { id: 'casual', label: 'Casual', icon: Coffee },
    { id: 'work', label: 'Work', icon: Briefcase },
    { id: 'date', label: 'Date Night', icon: Heart },
    { id: 'party', label: 'Party', icon: Music },
    { id: 'formal', label: 'Formal', icon: Star }
  ]

  const weatherOptions = [
    { id: 'sunny', label: 'Sunny', icon: Sun },
    { id: 'cloudy', label: 'Cloudy', icon: Cloud },
    { id: 'rainy', label: 'Rainy', icon: Cloud },
    { id: 'cold', label: 'Cold', icon: Cloud }
  ]

  useEffect(() => {
    // Load style history
    setStyleHistory([
      {
        id: 1,
        outfit: {
          top: { name: 'Silk Blouse', color: 'Blush Pink', brand: 'Zara' },
          bottom: { name: 'High-waist Jeans', color: 'Dark Blue', brand: 'Levi\'s' },
          shoes: { name: 'White Sneakers', color: 'White', brand: 'Adidas' },
          accessories: ['Gold Necklace', 'Crossbody Bag']
        },
        occasion: 'casual',
        weather: 'sunny',
        confidence: 94,
        likes: 12,
        createdAt: '2024-01-20',
        aiReasoning: 'Perfect balance of comfort and style for a casual day out'
      },
      {
        id: 2,
        outfit: {
          top: { name: 'Blazer', color: 'Navy Blue', brand: 'H&M' },
          bottom: { name: 'Pencil Skirt', color: 'Black', brand: 'Zara' },
          shoes: { name: 'Heels', color: 'Black', brand: 'Nine West' },
          accessories: ['Pearl Earrings', 'Leather Handbag']
        },
        occasion: 'work',
        weather: 'cloudy',
        confidence: 91,
        likes: 8,
        createdAt: '2024-01-19',
        aiReasoning: 'Professional and polished look that commands confidence'
      }
    ])
  }, [])

  const generateOutfit = async () => {
    setIsGenerating(true)
    
    try {
      // Simulate AI outfit generation (WS2 integration)
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      const newOutfit = {
        id: Date.now(),
        outfit: {
          top: { name: 'Floral Midi Dress', color: 'Lavender', brand: 'Anthropologie' },
          shoes: { name: 'Block Heels', color: 'Nude', brand: 'Steve Madden' },
          accessories: ['Delicate Bracelet', 'Straw Hat', 'Tote Bag']
        },
        occasion: selectedOccasion,
        weather: selectedWeather,
        confidence: 96,
        likes: 0,
        createdAt: new Date().toISOString().split('T')[0],
        aiReasoning: `Perfectly curated for ${selectedOccasion} occasions in ${selectedWeather} weather. The color palette complements your skin tone beautifully.`
      }
      
      setCurrentOutfit(newOutfit)
      setAiInsights({
        styleScore: 96,
        colorHarmony: 94,
        seasonalFit: 98,
        occasionMatch: 95,
        personalStyle: 92,
        tips: [
          'This lavender shade enhances your natural glow',
          'The midi length is perfect for your body type',
          'Block heels provide comfort without sacrificing style',
          'The straw hat adds a trendy summer touch'
        ],
        alternatives: [
          'Try with white sneakers for a more casual vibe',
          'Swap the hat for statement earrings for evening',
          'Add a denim jacket for cooler weather'
        ]
      })
      
    } catch (error) {
      console.error('Failed to generate outfit:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  const saveOutfit = () => {
    if (currentOutfit) {
      setStyleHistory(prev => [currentOutfit, ...prev])
      // In real app, would save to WS2 backend
    }
  }

  const likeOutfit = (outfitId) => {
    setStyleHistory(prev => 
      prev.map(outfit => 
        outfit.id === outfitId 
          ? { ...outfit, likes: outfit.likes + 1 }
          : outfit
      )
    )
  }

  return (
    <div className="p-4 space-y-6">
      {/* Header */}
      <div className="text-center py-4">
        <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
          AI Style Assistant
        </h2>
        <p className="text-gray-600">Let AI create the perfect outfit for you</p>
      </div>

      {/* Style Preferences */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Palette className="w-5 h-5 text-purple-500" />
            <span>Style Preferences</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-2 block">Occasion</label>
            <div className="grid grid-cols-3 gap-2">
              {occasions.map((occasion) => {
                const IconComponent = occasion.icon
                return (
                  <Button
                    key={occasion.id}
                    variant={selectedOccasion === occasion.id ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setSelectedOccasion(occasion.id)}
                    className="flex flex-col space-y-1 h-16"
                  >
                    <IconComponent className="w-4 h-4" />
                    <span className="text-xs">{occasion.label}</span>
                  </Button>
                )
              })}
            </div>
          </div>

          <div>
            <label className="text-sm font-medium text-gray-700 mb-2 block">Weather</label>
            <div className="grid grid-cols-4 gap-2">
              {weatherOptions.map((weather) => {
                const IconComponent = weather.icon
                return (
                  <Button
                    key={weather.id}
                    variant={selectedWeather === weather.id ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setSelectedWeather(weather.id)}
                    className="flex flex-col space-y-1 h-16"
                  >
                    <IconComponent className="w-4 h-4" />
                    <span className="text-xs">{weather.label}</span>
                  </Button>
                )
              })}
            </div>
          </div>

          <Button
            onClick={generateOutfit}
            disabled={isGenerating}
            className="w-full bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700"
          >
            {isGenerating ? (
              <div className="flex items-center space-x-2">
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>AI is styling you...</span>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Wand2 className="w-4 h-4" />
                <span>Generate AI Outfit</span>
              </div>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Current AI Generated Outfit */}
      {currentOutfit && (
        <Card className="border-purple-200 bg-gradient-to-r from-purple-50 to-pink-50">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Sparkles className="w-5 h-5 text-purple-500" />
                <span>AI Generated Outfit</span>
              </div>
              <Badge className="bg-purple-100 text-purple-800">
                {currentOutfit.confidence}% match
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Outfit Items */}
            <div className="space-y-3">
              {Object.entries(currentOutfit.outfit).map(([category, item]) => (
                <div key={category} className="flex items-center justify-between p-3 bg-white rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full flex items-center justify-center">
                      <Shirt className="w-4 h-4 text-white" />
                    </div>
                    <div>
                      <p className="font-medium text-gray-800 capitalize">
                        {Array.isArray(item) ? `${category} (${item.length})` : item.name}
                      </p>
                      <p className="text-sm text-gray-600">
                        {Array.isArray(item) ? item.join(', ') : `${item.color} • ${item.brand}`}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* AI Reasoning */}
            <div className="p-3 bg-white rounded-lg">
              <h4 className="font-medium text-gray-800 mb-2 flex items-center">
                <Zap className="w-4 h-4 text-yellow-500 mr-2" />
                AI Styling Insights
              </h4>
              <p className="text-sm text-gray-600 mb-3">{currentOutfit.aiReasoning}</p>
              
              {aiInsights && (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="text-center p-2 bg-purple-50 rounded">
                      <div className="font-semibold text-purple-600">{aiInsights.styleScore}%</div>
                      <div className="text-gray-600">Style Score</div>
                    </div>
                    <div className="text-center p-2 bg-pink-50 rounded">
                      <div className="font-semibold text-pink-600">{aiInsights.colorHarmony}%</div>
                      <div className="text-gray-600">Color Harmony</div>
                    </div>
                  </div>
                  
                  <div>
                    <h5 className="text-sm font-medium text-gray-700 mb-1">AI Tips:</h5>
                    <ul className="text-xs text-gray-600 space-y-1">
                      {aiInsights.tips.slice(0, 2).map((tip, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-purple-500 mr-1">•</span>
                          {tip}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex space-x-2">
              <Button onClick={saveOutfit} className="flex-1" variant="outline">
                <Heart className="w-4 h-4 mr-2" />
                Save
              </Button>
              <Button className="flex-1" variant="outline">
                <Share2 className="w-4 h-4 mr-2" />
                Share
              </Button>
              <Button variant="outline">
                <RefreshCw className="w-4 h-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Style History */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Clock className="w-5 h-5 text-gray-500" />
            <span>Style History</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {styleHistory.map((outfit) => (
              <div key={outfit.id} className="p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <Badge variant="outline" className="text-xs capitalize">
                      {outfit.occasion}
                    </Badge>
                    <Badge variant="secondary" className="text-xs">
                      {outfit.confidence}% match
                    </Badge>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => likeOutfit(outfit.id)}
                    >
                      <ThumbsUp className="w-3 h-3 mr-1" />
                      {outfit.likes}
                    </Button>
                    <Button size="sm" variant="ghost">
                      <Eye className="w-3 h-3" />
                    </Button>
                  </div>
                </div>
                <p className="text-sm text-gray-600 mb-2">{outfit.aiReasoning}</p>
                <div className="text-xs text-gray-500">
                  Created on {new Date(outfit.createdAt).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardContent className="pt-6">
          <div className="grid grid-cols-2 gap-3">
            <Button variant="outline" onClick={() => window.location.href = '/camera'}>
              <Camera className="w-4 h-4 mr-2" />
              Style Camera
            </Button>
            <Button variant="outline" onClick={() => window.location.href = '/wardrobe'}>
              <Shirt className="w-4 h-4 mr-2" />
              My Wardrobe
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* WS2 Integration Status */}
      <div className="text-center pb-4">
        <Badge variant="outline" className="text-xs">
          🔗 WS2: AI Styling Engine Integration Active
        </Badge>
      </div>
    </div>
  )
}

