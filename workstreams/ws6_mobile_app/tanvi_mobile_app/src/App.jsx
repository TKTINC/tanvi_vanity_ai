import { useState, useEffect } from 'react'
import { AuthProvider } from './hooks/useAuth'
import { usePWA } from './hooks/usePWA'

// Import all screen components
import HomeScreen from './components/HomeScreen'
import AuthScreen from './components/AuthScreen'
import ProfileScreen from './components/ProfileScreen'
import AIStyleScreen from './components/AIStyleScreen'
import CameraScreen from './components/CameraScreen'
import WardrobeScreen from './components/WardrobeScreen'
import SocialScreen from './components/SocialScreen'
import CommunityScreen from './components/CommunityScreen'
import ShopScreen from './components/ShopScreen'
import CartScreen from './components/CartScreen'
import CheckoutScreen from './components/CheckoutScreen'
import OrdersScreen from './components/OrdersScreen'
import AnalyticsScreen from './components/AnalyticsScreen'

// Icons
import { 
  Home, 
  Sparkles, 
  ShoppingBag, 
  Users, 
  User,
  Wifi,
  WifiOff,
  Download,
  X
} from 'lucide-react'

function App() {
  const [currentScreen, setCurrentScreen] = useState('home')
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [currentUser, setCurrentUser] = useState(null)
  const [showInstallPrompt, setShowInstallPrompt] = useState(false)
  
  // PWA functionality
  const { 
    isInstallable, 
    isInstalled, 
    isOnline, 
    installPWA, 
    shareContent,
    requestNotificationPermission 
  } = usePWA()

  // Mock user for demo
  useEffect(() => {
    const mockUser = {
      id: 1,
      name: 'Sarah Johnson',
      email: 'sarah@example.com',
      avatar: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face',
      preferences: {
        style: 'modern',
        market: 'US',
        notifications: true
      },
      stats: {
        stylingScore: 92,
        totalOutfits: 47,
        totalPurchases: 23,
        followers: 156,
        following: 89
      }
    }
    
    setCurrentUser(mockUser)
    setIsAuthenticated(true)
  }, [])

  // Show install prompt after delay
  useEffect(() => {
    if (isInstallable && !isInstalled) {
      const timer = setTimeout(() => {
        setShowInstallPrompt(true)
      }, 15000) // Show after 15 seconds
      
      return () => clearTimeout(timer)
    }
  }, [isInstallable, isInstalled])

  // Request notification permission on first visit
  useEffect(() => {
    const hasRequestedNotifications = localStorage.getItem('notificationsRequested')
    
    if (!hasRequestedNotifications && isAuthenticated) {
      setTimeout(async () => {
        const permission = await requestNotificationPermission()
        localStorage.setItem('notificationsRequested', 'true')
        
        if (permission === 'granted') {
          console.log('Notifications enabled')
        }
      }, 5000)
    }
  }, [isAuthenticated, requestNotificationPermission])

  const handleInstallPWA = async () => {
    const success = await installPWA()
    if (success) {
      setShowInstallPrompt(false)
    }
  }

  const handleShare = async (content) => {
    const shared = await shareContent(content)
    if (!shared) {
      // Fallback to copy to clipboard
      try {
        await navigator.clipboard.writeText(content.url || content.text)
        alert('Link copied to clipboard!')
      } catch (error) {
        console.error('Share failed:', error)
      }
    }
  }

  // Navigation items
  const navigationItems = [
    { id: 'home', label: 'Home', icon: Home, screen: 'home' },
    { id: 'style', label: 'Style', icon: Sparkles, screen: 'ai-style' },
    { id: 'shop', label: 'Shop', icon: ShoppingBag, screen: 'shop' },
    { id: 'social', label: 'Social', icon: Users, screen: 'social' },
    { id: 'profile', label: 'Profile', icon: User, screen: 'profile' }
  ]

  const renderScreen = () => {
    const screenProps = {
      currentUser,
      onNavigate: setCurrentScreen,
      onShare: handleShare
    }

    switch (currentScreen) {
      case 'home':
        return <HomeScreen {...screenProps} />
      case 'auth':
        return <AuthScreen {...screenProps} onLogin={setIsAuthenticated} />
      case 'profile':
        return <ProfileScreen {...screenProps} />
      case 'ai-style':
        return <AIStyleScreen {...screenProps} />
      case 'camera':
        return <CameraScreen {...screenProps} />
      case 'wardrobe':
        return <WardrobeScreen {...screenProps} />
      case 'social':
        return <SocialScreen {...screenProps} />
      case 'community':
        return <CommunityScreen {...screenProps} />
      case 'shop':
        return <ShopScreen {...screenProps} />
      case 'cart':
        return <CartScreen {...screenProps} />
      case 'checkout':
        return <CheckoutScreen {...screenProps} onBack={() => setCurrentScreen('cart')} />
      case 'orders':
        return <OrdersScreen {...screenProps} />
      case 'analytics':
        return <AnalyticsScreen {...screenProps} />
      default:
        return <HomeScreen {...screenProps} />
    }
  }

  if (!isAuthenticated) {
    return (
      <AuthProvider>
        <div className="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50">
          <AuthScreen 
            currentUser={currentUser}
            onNavigate={setCurrentScreen}
            onLogin={setIsAuthenticated}
          />
        </div>
      </AuthProvider>
    )
  }

  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50 pb-20">
        {/* Offline Indicator */}
        {!isOnline && (
          <div className="fixed top-0 left-0 right-0 bg-red-500 text-white text-center py-2 text-sm z-50">
            <WifiOff className="w-4 h-4 inline mr-2" />
            You're offline. Some features may be limited.
          </div>
        )}

        {/* PWA Install Prompt */}
        {showInstallPrompt && isInstallable && !isInstalled && (
          <div className="fixed bottom-24 left-4 right-4 bg-gradient-to-r from-pink-500 to-purple-600 text-white p-4 rounded-lg shadow-lg z-50">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <h3 className="font-semibold mb-1">Install Tanvi AI</h3>
                <p className="text-sm opacity-90">Add to home screen for the best experience</p>
              </div>
              <div className="flex items-center space-x-2 ml-4">
                <button
                  onClick={handleInstallPWA}
                  className="bg-white/20 hover:bg-white/30 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
                >
                  <Download className="w-4 h-4 inline mr-1" />
                  Install
                </button>
                <button
                  onClick={() => setShowInstallPrompt(false)}
                  className="p-2 hover:bg-white/20 rounded-lg transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Main Content */}
        <main className="min-h-screen">
          {renderScreen()}
        </main>

        {/* Bottom Navigation */}
        <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-2 z-40">
          <div className="flex items-center justify-around">
            {navigationItems.map((item) => {
              const IconComponent = item.icon
              const isActive = currentScreen === item.screen || 
                             (item.screen === 'home' && currentScreen === 'home')
              
              return (
                <button
                  key={item.id}
                  onClick={() => setCurrentScreen(item.screen)}
                  className={`flex flex-col items-center space-y-1 py-2 px-3 rounded-lg transition-colors ${
                    isActive 
                      ? 'text-pink-600 bg-pink-50' 
                      : 'text-gray-600 hover:text-gray-800'
                  }`}
                >
                  <IconComponent className={`w-5 h-5 ${isActive ? 'text-pink-600' : ''}`} />
                  <span className={`text-xs font-medium ${isActive ? 'text-pink-600' : ''}`}>
                    {item.label}
                  </span>
                </button>
              )
            })}
          </div>
        </nav>

        {/* PWA Status Indicator (Development) */}
        {process.env.NODE_ENV === 'development' && (
          <div className="fixed top-4 right-4 bg-black/80 text-white text-xs px-2 py-1 rounded z-50">
            PWA: {isInstalled ? 'Installed' : isInstallable ? 'Installable' : 'Not Ready'} | 
            {isOnline ? ' Online' : ' Offline'}
          </div>
        )}
      </div>
    </AuthProvider>
  )
}

export default App

