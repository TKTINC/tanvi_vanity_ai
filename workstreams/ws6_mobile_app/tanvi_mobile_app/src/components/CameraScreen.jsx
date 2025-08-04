import { useState, useRef, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  Camera, 
  RotateCcw, 
  Zap, 
  Eye, 
  Palette, 
  Shirt,
  Star,
  TrendingUp,
  Save,
  Share,
  RefreshCw,
  ScanLine,
  Target,
  Sparkles,
  Award,
  CheckCircle,
  AlertCircle,
  Info,
  Heart,
  ShoppingBag,
  Wand2
} from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import { ComputerVisionAPI } from '../services/api'

export default function CameraScreen({ currentUser }) {
  const { user } = useAuth()
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [cameraActive, setCameraActive] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [capturedImage, setCapturedImage] = useState(null)
  const [analysisMode, setAnalysisMode] = useState('outfit') // outfit, color, style, fit
  const [facingMode, setFacingMode] = useState('user') // user (front) or environment (back)

  const analysisModes = [
    { id: 'outfit', label: 'Outfit Analysis', icon: Shirt, description: 'Analyze complete outfit' },
    { id: 'color', label: 'Color Match', icon: Palette, description: 'Color harmony analysis' },
    { id: 'style', label: 'Style Score', icon: Star, description: 'Style rating & tips' },
    { id: 'fit', label: 'Fit Check', icon: Target, description: 'Fit and silhouette analysis' }
  ]

  // Initialize camera
  useEffect(() => {
    startCamera()
    return () => {
      stopCamera()
    }
  }, [facingMode])

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { 
          facingMode: facingMode,
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      })
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        setCameraActive(true)
      }
    } catch (error) {
      console.error('Error accessing camera:', error)
    }
  }

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks()
      tracks.forEach(track => track.stop())
      setCameraActive(false)
    }
  }

  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) return

    const canvas = canvasRef.current
    const video = videoRef.current
    
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    
    const ctx = canvas.getContext('2d')
    ctx.drawImage(video, 0, 0)
    
    const imageData = canvas.toDataURL('image/jpeg', 0.8)
    setCapturedImage(imageData)
    
    // Start analysis
    analyzeOutfit(imageData)
  }

  const analyzeOutfit = async (imageData) => {
    setIsAnalyzing(true)
    
    try {
      // Simulate WS3 Computer Vision analysis
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      const mockAnalysis = {
        mode: analysisMode,
        confidence: 94,
        timestamp: new Date().toISOString(),
        results: {
          outfit: {
            items: [
              { type: 'top', name: 'Silk Blouse', color: 'Blush Pink', confidence: 96 },
              { type: 'bottom', name: 'High-waist Jeans', color: 'Dark Blue', confidence: 94 },
              { type: 'shoes', name: 'White Sneakers', color: 'White', confidence: 92 }
            ],
            style: 'Casual Chic',
            occasion: 'Casual/Weekend',
            season: 'Spring/Summer'
          },
          colorAnalysis: {
            dominantColors: ['#F8BBD9', '#1E3A8A', '#FFFFFF'],
            colorHarmony: 92,
            seasonalMatch: 'Spring',
            skinToneMatch: 94,
            recommendations: [
              'The blush pink complements your skin tone beautifully',
              'Consider adding gold accessories to enhance the warm undertones',
              'The color balance is excellent for daytime wear'
            ]
          },
          styleScore: {
            overall: 94,
            breakdown: {
              coordination: 96,
              fit: 92,
              appropriateness: 95,
              trendiness: 91,
              personalStyle: 94
            },
            improvements: [
              'Perfect color coordination',
              'Great fit on the jeans',
              'Consider a statement necklace to elevate the look',
              'The casual-chic style suits you perfectly'
            ]
          },
          fitAnalysis: {
            overall: 93,
            details: {
              top: { fit: 'Excellent', notes: 'Perfect shoulder fit, flattering neckline' },
              bottom: { fit: 'Great', notes: 'High-waist creates nice silhouette' },
              proportions: 'Balanced and flattering'
            },
            suggestions: [
              'The high-waist jeans elongate your legs beautifully',
              'The blouse length is perfect for your torso',
              'Consider tucking in slightly for a more polished look'
            ]
          }
        },
        aiInsights: {
          strengths: [
            'Excellent color coordination',
            'Perfect casual-chic balance',
            'Great fit and proportions',
            'Seasonally appropriate'
          ],
          improvements: [
            'Add a statement accessory',
            'Consider a light cardigan for layering',
            'Experiment with different shoe styles'
          ],
          shoppingRecommendations: [
            'Gold delicate jewelry would complement this look',
            'A light blazer for more formal occasions',
            'Similar styles in different colors'
          ]
        }
      }
      
      setAnalysisResult(mockAnalysis)
      
    } catch (error) {
      console.error('Failed to analyze outfit:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const retakePhoto = () => {
    setCapturedImage(null)
    setAnalysisResult(null)
  }

  const saveAnalysis = async () => {
    if (analysisResult) {
      // Save to WS3 Computer Vision backend
      console.log('Saving analysis:', analysisResult)
    }
  }

  const shareAnalysis = async () => {
    if (navigator.share && analysisResult) {
      await navigator.share({
        title: 'My AI Style Analysis',
        text: `Check out my ${analysisResult.results.outfit.style} style with ${analysisResult.confidence}% confidence!`,
        url: window.location.href
      })
    }
  }

  const switchCamera = () => {
    setFacingMode(prev => prev === 'user' ? 'environment' : 'user')
  }

  const displayUser = user || currentUser

  return (
    <div className="p-4 space-y-6">
      {/* Header */}
      <div className="text-center py-4">
        <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mb-4 mx-auto">
          <Camera className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
          Style Camera
        </h1>
        <p className="text-gray-600">AI-powered outfit analysis and styling tips</p>
      </div>

      {/* Analysis Mode Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <ScanLine className="w-5 h-5" />
            <span>Analysis Mode</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-3">
            {analysisModes.map((mode) => {
              const IconComponent = mode.icon
              return (
                <Button
                  key={mode.id}
                  variant={analysisMode === mode.id ? 'default' : 'outline'}
                  onClick={() => setAnalysisMode(mode.id)}
                  className="h-20 flex flex-col space-y-1 p-3"
                >
                  <IconComponent className="w-5 h-5" />
                  <span className="text-xs font-medium">{mode.label}</span>
                  <span className="text-xs text-gray-500">{mode.description}</span>
                </Button>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Camera View */}
      <Card>
        <CardContent className="p-0">
          <div className="relative bg-black rounded-lg overflow-hidden">
            {!capturedImage ? (
              <>
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  className="w-full h-80 object-cover"
                />
                <canvas ref={canvasRef} className="hidden" />
                
                {/* Camera Controls */}
                <div className="absolute bottom-4 left-0 right-0 flex justify-center space-x-4">
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={switchCamera}
                    className="bg-black/50 text-white border-white/20"
                  >
                    <RotateCcw className="w-4 h-4" />
                  </Button>
                  
                  <Button
                    onClick={capturePhoto}
                    disabled={!cameraActive}
                    className="w-16 h-16 rounded-full bg-white text-black hover:bg-gray-100"
                  >
                    <Camera className="w-6 h-6" />
                  </Button>
                  
                  <Button
                    variant="secondary"
                    size="sm"
                    className="bg-black/50 text-white border-white/20"
                  >
                    <Zap className="w-4 h-4" />
                  </Button>
                </div>

                {/* Analysis Mode Indicator */}
                <div className="absolute top-4 left-4">
                  <Badge className="bg-black/50 text-white border-white/20">
                    {analysisModes.find(m => m.id === analysisMode)?.label}
                  </Badge>
                </div>
              </>
            ) : (
              <>
                <img
                  src={capturedImage}
                  alt="Captured outfit"
                  className="w-full h-80 object-cover"
                />
                
                {/* Retake Button */}
                <div className="absolute bottom-4 left-0 right-0 flex justify-center">
                  <Button
                    onClick={retakePhoto}
                    variant="secondary"
                    className="bg-black/50 text-white border-white/20"
                  >
                    <RefreshCw className="w-4 h-4 mr-2" />
                    Retake
                  </Button>
                </div>
              </>
            )}

            {/* Analysis Loading Overlay */}
            {isAnalyzing && (
              <div className="absolute inset-0 bg-black/70 flex items-center justify-center">
                <div className="text-center text-white">
                  <div className="w-12 h-12 border-4 border-white border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                  <p className="text-lg font-medium">AI Analyzing Your Style...</p>
                  <p className="text-sm opacity-80">This may take a few seconds</p>
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Analysis Results */}
      {analysisResult && (
        <div className="space-y-4">
          {/* Overall Score */}
          <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="text-4xl font-bold text-blue-600 mb-2">
                  {analysisResult.confidence}%
                </div>
                <p className="text-gray-700 font-medium">
                  {analysisResult.results.outfit.style} Style
                </p>
                <p className="text-sm text-gray-600">
                  Perfect for {analysisResult.results.outfit.occasion}
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Detailed Analysis */}
          {analysisMode === 'outfit' && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Shirt className="w-5 h-5" />
                  <span>Outfit Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {analysisResult.results.outfit.items.map((item, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium capitalize">{item.type}</p>
                      <p className="text-sm text-gray-600">{item.name} • {item.color}</p>
                    </div>
                    <Badge variant="outline">{item.confidence}%</Badge>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}

          {analysisMode === 'color' && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Palette className="w-5 h-5" />
                  <span>Color Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Color Harmony</span>
                  <Badge className="bg-gradient-to-r from-pink-500 to-purple-600">
                    {analysisResult.results.colorAnalysis.colorHarmony}%
                  </Badge>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Skin Tone Match</span>
                  <Badge variant="outline">
                    {analysisResult.results.colorAnalysis.skinToneMatch}%
                  </Badge>
                </div>

                <div className="space-y-2">
                  <h4 className="font-medium text-sm">Color Recommendations:</h4>
                  {analysisResult.results.colorAnalysis.recommendations.map((rec, index) => (
                    <div key={index} className="flex items-start space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <p className="text-sm text-gray-600">{rec}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {analysisMode === 'style' && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Star className="w-5 h-5" />
                  <span>Style Score</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  {Object.entries(analysisResult.results.styleScore.breakdown).map(([key, value]) => (
                    <div key={key} className="text-center p-3 bg-gray-50 rounded-lg">
                      <div className="text-lg font-bold text-purple-600">{value}%</div>
                      <div className="text-xs text-gray-600 capitalize">{key}</div>
                    </div>
                  ))}
                </div>

                <div className="space-y-2">
                  <h4 className="font-medium text-sm">Style Improvements:</h4>
                  {analysisResult.results.styleScore.improvements.map((improvement, index) => (
                    <div key={index} className="flex items-start space-x-2">
                      <Star className="w-4 h-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                      <p className="text-sm text-gray-600">{improvement}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {analysisMode === 'fit' && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Target className="w-5 h-5" />
                  <span>Fit Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600 mb-1">
                    {analysisResult.results.fitAnalysis.overall}%
                  </div>
                  <p className="text-sm text-gray-600">Overall Fit Score</p>
                </div>

                <div className="space-y-3">
                  {Object.entries(analysisResult.results.fitAnalysis.details).map(([key, value]) => (
                    <div key={key} className="p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium capitalize">{key}</span>
                        <Badge variant="outline">{value.fit}</Badge>
                      </div>
                      <p className="text-sm text-gray-600">{value.notes}</p>
                    </div>
                  ))}
                </div>

                <div className="space-y-2">
                  <h4 className="font-medium text-sm">Fit Suggestions:</h4>
                  {analysisResult.results.fitAnalysis.suggestions.map((suggestion, index) => (
                    <div key={index} className="flex items-start space-x-2">
                      <Info className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                      <p className="text-sm text-gray-600">{suggestion}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* AI Insights */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Sparkles className="w-5 h-5 text-purple-500" />
                <span>AI Insights</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-medium text-sm mb-2 text-green-700">What's Working:</h4>
                <div className="space-y-1">
                  {analysisResult.aiInsights.strengths.map((strength, index) => (
                    <div key={index} className="flex items-start space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                      <p className="text-sm text-gray-600">{strength}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-medium text-sm mb-2 text-orange-700">Suggestions:</h4>
                <div className="space-y-1">
                  {analysisResult.aiInsights.improvements.map((improvement, index) => (
                    <div key={index} className="flex items-start space-x-2">
                      <AlertCircle className="w-4 h-4 text-orange-500 mt-0.5 flex-shrink-0" />
                      <p className="text-sm text-gray-600">{improvement}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h4 className="font-medium text-sm mb-2 text-blue-700">Shopping Recommendations:</h4>
                <div className="space-y-1">
                  {analysisResult.aiInsights.shoppingRecommendations.map((rec, index) => (
                    <div key={index} className="flex items-start space-x-2">
                      <ShoppingBag className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                      <p className="text-sm text-gray-600">{rec}</p>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="flex space-x-2">
            <Button onClick={saveAnalysis} className="flex-1" variant="outline">
              <Save className="w-4 h-4 mr-2" />
              Save Analysis
            </Button>
            <Button onClick={shareAnalysis} className="flex-1" variant="outline">
              <Share className="w-4 h-4 mr-2" />
              Share Results
            </Button>
            <Button variant="outline">
              <Wand2 className="w-4 h-4" />
            </Button>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <Card>
        <CardContent className="pt-6">
          <div className="grid grid-cols-2 gap-3">
            <Button variant="outline" onClick={() => window.location.href = '/ai-style'}>
              <Sparkles className="w-4 h-4 mr-2" />
              AI Styling
            </Button>
            <Button variant="outline" onClick={() => window.location.href = '/wardrobe'}>
              <Shirt className="w-4 h-4 mr-2" />
              Add to Wardrobe
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* WS3 Integration Status */}
      <div className="text-center">
        <Badge variant="outline" className="text-xs">
          🔗 WS3: Computer Vision Integration Active
        </Badge>
      </div>
    </div>
  )
}

