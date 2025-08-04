import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  Home, 
  User, 
  Camera, 
  Heart, 
  ShoppingBag, 
  Search,
  Menu,
  Bell,
  Settings,
  Sparkles,
  Users,
  CreditCard,
  Package,
  BarChart3,
  Smartphone
} from 'lucide-react'
import './App.css'

// Import authentication provider and hook
import { AuthProvider, useAuth } from './hooks/useAuth'

// Import all phase components
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

function AppContent() {
  const { user, isLoading, isAuthenticated } = useAuth()
  const [currentMarket, setCurrentMarket] = useState('US')
  const [activeTab, setActiveTab] = useState('home')

  // Update market when user changes
  useEffect(() => {
    if (user && user.market) {
      setCurrentMarket(user.market)
    }
  }, [user])

  if (isLoading) {
    return <LoadingScreen />
  }

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-indigo-50">
        {/* App Header */}
        <header className="bg-white/80 backdrop-blur-md border-b border-pink-200 sticky top-0 z-50">
          <div className="max-w-md mx-auto px-4 py-3 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent">
                  Tanvi
                </h1>
                <p className="text-xs text-gray-500">We girls have no time</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant="outline" className="text-xs">
                {currentMarket === 'US' ? '🇺🇸 USA' : '🇮🇳 India'}
              </Badge>
              {isAuthenticated && (
                <Button variant="ghost" size="sm">
                  <Bell className="w-4 h-4" />
                </Button>
              )}
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-md mx-auto pb-20">
          <Routes>
            <Route path="/" element={
              isAuthenticated ? 
                <HomeScreen currentUser={user} currentMarket={currentMarket} /> : 
                <Navigate to="/auth" replace />
            } />
            <Route path="/auth" element={
              !isAuthenticated ? 
                <AuthScreen /> : 
                <Navigate to="/" replace />
            } />
            <Route path="/profile" element={
              isAuthenticated ? 
                <ProfileScreen currentUser={user} /> : 
                <Navigate to="/auth" replace />
            } />
            <Route path="/ai-style" element={
              isAuthenticated ? 
                <AIStyleScreen currentUser={user} /> : 
                <Navigate to="/auth" replace />
            } />
            <Route path="/camera" element={
              isAuthenticated ? 
                <CameraScreen currentUser={user} /> : 
                <Navigate to="/auth" replace />
            } />
            <Route path="/wardrobe" element={
              isAuthenticated ? 
                <WardrobeScreen currentUser={user} /> : 
                <Navigate to="/auth" replace />
            } />
            <Route path="/social" element={
              isAuthenticated ? 
                <SocialScreen currentUser={user} /> : 
                <Navigate to="/auth" replace />
            } />
            <Route path="/community" element={
              isAuthenticated ? 
                <CommunityScreen currentUser={user} /> : 
                <Navigate to="/auth" replace />
            } />
            <Route path="/shop" element={
              isAuthenticated ? 
                <ShopScreen currentMarket={currentMarket} /> : 
                <Navigate to="/auth" replace />
            } />
            <Route path="/cart" element={
              isAuthenticated ? 
                <CartScreen currentUser={user} /> : 
                <Navigate to="/auth" replace />
            } />
            <Route path="/checkout" element={
              isAuthenticated ? 
                <CheckoutScreen currentUser={user} /> : 
                <Navigate to="/auth" replace />
            } />
            <Route path="/orders" element={
              isAuthenticated ? 
                <OrdersScreen currentUser={user} /> : 
                <Navigate to="/auth" replace />
            } />
            <Route path="/analytics" element={
              isAuthenticated ? 
                <AnalyticsScreen /> : 
                <Navigate to="/auth" replace />
            } />
          </Routes>
        </main>

        {/* Bottom Navigation - Only show when authenticated */}
        {isAuthenticated && (
          <nav className="fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-md border-t border-pink-200">
            <div className="max-w-md mx-auto px-4 py-2">
              <div className="flex justify-around">
                <NavButton 
                  icon={Home} 
                  label="Home" 
                  isActive={activeTab === 'home'}
                  onClick={() => setActiveTab('home')}
                  to="/"
                />
                <NavButton 
                  icon={Camera} 
                  label="Style" 
                  isActive={activeTab === 'style'}
                  onClick={() => setActiveTab('style')}
                  to="/ai-style"
                />
                <NavButton 
                  icon={ShoppingBag} 
                  label="Shop" 
                  isActive={activeTab === 'shop'}
                  onClick={() => setActiveTab('shop')}
                  to="/shop"
                />
                <NavButton 
                  icon={Users} 
                  label="Social" 
                  isActive={activeTab === 'social'}
                  onClick={() => setActiveTab('social')}
                  to="/social"
                />
                <NavButton 
                  icon={User} 
                  label="Profile" 
                  isActive={activeTab === 'profile'}
                  onClick={() => setActiveTab('profile')}
                  to="/profile"
                />
              </div>
            </div>
          </nav>
        )}
      </div>
    </Router>
  )
}

function LoadingScreen() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-indigo-50 flex items-center justify-center">
      <div className="text-center">
        <div className="w-16 h-16 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full flex items-center justify-center mb-4 mx-auto animate-pulse">
          <Sparkles className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent mb-2">
          Tanvi Vanity AI
        </h1>
        <p className="text-gray-600 mb-4">We girls have no time</p>
        <div className="flex items-center justify-center space-x-1">
          <div className="w-2 h-2 bg-pink-500 rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
          <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
        </div>
      </div>
    </div>
  )
}

function NavButton({ icon: Icon, label, isActive, onClick, to }) {
  return (
    <a href={to} onClick={(e) => { e.preventDefault(); onClick(); window.history.pushState({}, '', to); }}>
      <div className={`flex flex-col items-center p-2 rounded-lg transition-colors ${
        isActive 
          ? 'text-pink-600 bg-pink-50' 
          : 'text-gray-500 hover:text-pink-600 hover:bg-pink-50'
      }`}>
        <Icon className="w-5 h-5 mb-1" />
        <span className="text-xs font-medium">{label}</span>
      </div>
    </a>
  )
}

// Main App component with AuthProvider
function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App

