import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Input } from '@/components/ui/input.jsx'
import { 
  ShoppingBag, 
  Search, 
  Filter, 
  Heart,
  Star,
  Plus,
  Minus,
  ShoppingCart,
  Zap,
  TrendingUp,
  Tag,
  Truck,
  Shield,
  CreditCard,
  MapPin,
  Clock,
  Sparkles,
  Eye,
  Share,
  Bookmark,
  ArrowRight,
  Grid,
  List,
  SlidersHorizontal,
  Package,
  Percent
} from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import { EcommerceAPI } from '../services/api'

export default function ShopScreen({ currentUser }) {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState('discover')
  const [searchQuery, setSearchQuery] = useState('')
  const [products, setProducts] = useState([])
  const [featuredProducts, setFeaturedProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [cart, setCart] = useState({ items: [], total: 0 })
  const [wishlist, setWishlist] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [viewMode, setViewMode] = useState('grid') // grid or list
  const [filters, setFilters] = useState({
    priceRange: [0, 500],
    category: '',
    brand: '',
    size: '',
    color: '',
    rating: 0
  })

  const tabs = [
    { id: 'discover', label: 'Discover', icon: Sparkles },
    { id: 'categories', label: 'Categories', icon: Grid },
    { id: 'cart', label: 'Cart', icon: ShoppingCart },
    { id: 'wishlist', label: 'Wishlist', icon: Heart }
  ]

  // Load shopping data
  useEffect(() => {
    loadShoppingData()
    loadCart()
  }, [activeTab])

  const loadShoppingData = async () => {
    setIsLoading(true)
    try {
      switch (activeTab) {
        case 'discover':
          await loadFeaturedProducts()
          break
        case 'categories':
          await loadCategories()
          break
        case 'cart':
          await loadCart()
          break
        case 'wishlist':
          await loadWishlist()
          break
      }
    } catch (error) {
      console.error('Failed to load shopping data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const loadFeaturedProducts = async () => {
    try {
      const result = await EcommerceAPI.searchProducts('featured')
      setFeaturedProducts(result.products || [])
    } catch (error) {
      // Mock featured products for demo
      setFeaturedProducts([
        {
          id: 1,
          name: 'Silk Blouse',
          brand: 'Zara',
          price: 59.99,
          originalPrice: 79.99,
          currency: 'USD',
          image: '/api/placeholder/200/250',
          rating: 4.5,
          reviews: 127,
          colors: ['Blush Pink', 'White', 'Navy'],
          sizes: ['XS', 'S', 'M', 'L', 'XL'],
          isNew: true,
          isSale: true,
          discount: 25,
          inStock: true,
          fastShipping: true,
          tags: ['trending', 'workwear', 'versatile']
        },
        {
          id: 2,
          name: 'High-waist Jeans',
          brand: 'Levi\'s',
          price: 89.99,
          currency: 'USD',
          image: '/api/placeholder/200/250',
          rating: 4.7,
          reviews: 203,
          colors: ['Dark Blue', 'Light Wash', 'Black'],
          sizes: ['24', '25', '26', '27', '28', '29', '30'],
          isNew: false,
          isSale: false,
          inStock: true,
          fastShipping: true,
          tags: ['classic', 'denim', 'flattering']
        },
        {
          id: 3,
          name: 'Floral Midi Dress',
          brand: 'Anthropologie',
          price: 148.00,
          currency: 'USD',
          image: '/api/placeholder/200/250',
          rating: 4.3,
          reviews: 89,
          colors: ['Lavender', 'Coral', 'Sage Green'],
          sizes: ['XS', 'S', 'M', 'L'],
          isNew: true,
          isSale: false,
          inStock: true,
          fastShipping: false,
          tags: ['romantic', 'spring', 'feminine']
        },
        {
          id: 4,
          name: 'White Sneakers',
          brand: 'Adidas',
          price: 89.99,
          currency: 'USD',
          image: '/api/placeholder/200/250',
          rating: 4.6,
          reviews: 156,
          colors: ['White', 'Off-White', 'Cream'],
          sizes: ['6', '6.5', '7', '7.5', '8', '8.5', '9'],
          isNew: false,
          isSale: false,
          inStock: true,
          fastShipping: true,
          tags: ['casual', 'comfortable', 'versatile']
        }
      ])
    }
  }

  const loadCategories = async () => {
    // Mock categories for demo
    setCategories([
      {
        id: 1,
        name: 'Tops',
        count: 156,
        image: '/api/placeholder/150/150',
        subcategories: ['Blouses', 'T-Shirts', 'Sweaters', 'Tank Tops']
      },
      {
        id: 2,
        name: 'Bottoms',
        count: 89,
        image: '/api/placeholder/150/150',
        subcategories: ['Jeans', 'Trousers', 'Skirts', 'Shorts']
      },
      {
        id: 3,
        name: 'Dresses',
        count: 67,
        image: '/api/placeholder/150/150',
        subcategories: ['Casual', 'Formal', 'Midi', 'Maxi']
      },
      {
        id: 4,
        name: 'Shoes',
        count: 123,
        image: '/api/placeholder/150/150',
        subcategories: ['Sneakers', 'Heels', 'Flats', 'Boots']
      },
      {
        id: 5,
        name: 'Accessories',
        count: 234,
        image: '/api/placeholder/150/150',
        subcategories: ['Bags', 'Jewelry', 'Scarves', 'Belts']
      },
      {
        id: 6,
        name: 'Outerwear',
        count: 45,
        image: '/api/placeholder/150/150',
        subcategories: ['Jackets', 'Coats', 'Blazers', 'Cardigans']
      }
    ])
  }

  const loadCart = async () => {
    try {
      const cartData = await EcommerceAPI.getCart()
      setCart(cartData)
    } catch (error) {
      // Mock cart for demo
      setCart({
        items: [
          {
            id: 1,
            product: {
              id: 1,
              name: 'Silk Blouse',
              brand: 'Zara',
              price: 59.99,
              image: '/api/placeholder/100/125'
            },
            variant: { color: 'Blush Pink', size: 'M' },
            quantity: 1
          },
          {
            id: 2,
            product: {
              id: 2,
              name: 'High-waist Jeans',
              brand: 'Levi\'s',
              price: 89.99,
              image: '/api/placeholder/100/125'
            },
            variant: { color: 'Dark Blue', size: '27' },
            quantity: 1
          }
        ],
        subtotal: 149.98,
        tax: 12.00,
        shipping: 0,
        total: 161.98,
        currency: 'USD',
        freeShippingThreshold: 50,
        estimatedDelivery: '2-3 business days'
      })
    }
  }

  const loadWishlist = async () => {
    // Mock wishlist for demo
    setWishlist([
      {
        id: 3,
        name: 'Floral Midi Dress',
        brand: 'Anthropologie',
        price: 148.00,
        currency: 'USD',
        image: '/api/placeholder/150/200',
        inStock: true,
        priceDropped: false
      },
      {
        id: 5,
        name: 'Leather Handbag',
        brand: 'Coach',
        price: 295.00,
        originalPrice: 350.00,
        currency: 'USD',
        image: '/api/placeholder/150/200',
        inStock: true,
        priceDropped: true,
        discount: 16
      }
    ])
  }

  const handleSearch = async (query) => {
    if (!query.trim()) return
    
    setIsLoading(true)
    try {
      const result = await EcommerceAPI.searchProducts(query, filters)
      setProducts(result.products || [])
    } catch (error) {
      console.error('Search failed:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const addToCart = async (product, variant = {}) => {
    try {
      const result = await EcommerceAPI.addToCart(product.id, variant)
      
      // Update local cart state
      setCart(prev => ({
        ...prev,
        items: [...prev.items, {
          id: Date.now(),
          product,
          variant,
          quantity: 1
        }],
        total: prev.total + product.price
      }))
      
    } catch (error) {
      console.error('Failed to add to cart:', error)
    }
  }

  const addToWishlist = (product) => {
    setWishlist(prev => {
      const exists = prev.find(item => item.id === product.id)
      if (exists) {
        return prev.filter(item => item.id !== product.id)
      } else {
        return [...prev, product]
      }
    })
  }

  const updateCartQuantity = (itemId, newQuantity) => {
    if (newQuantity <= 0) {
      setCart(prev => ({
        ...prev,
        items: prev.items.filter(item => item.id !== itemId)
      }))
    } else {
      setCart(prev => ({
        ...prev,
        items: prev.items.map(item =>
          item.id === itemId ? { ...item, quantity: newQuantity } : item
        )
      }))
    }
  }

  const displayUser = user || currentUser
  const cartItemsCount = cart.items.reduce((sum, item) => sum + item.quantity, 0)

  return (
    <div className="p-4 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Shop
          </h1>
          <p className="text-gray-600">Discover your perfect style</p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="sm">
            <Search className="w-4 h-4" />
          </Button>
          <Button variant="ghost" size="sm" className="relative">
            <ShoppingCart className="w-4 h-4" />
            {cartItemsCount > 0 && (
              <Badge className="absolute -top-2 -right-2 w-5 h-5 rounded-full p-0 flex items-center justify-center text-xs">
                {cartItemsCount}
              </Badge>
            )}
          </Button>
        </div>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
        <Input
          placeholder="Search for clothes, brands, styles..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch(searchQuery)}
          className="pl-10 pr-12"
        />
        <Button
          variant="ghost"
          size="sm"
          className="absolute right-1 top-1/2 transform -translate-y-1/2"
        >
          <Filter className="w-4 h-4" />
        </Button>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 bg-gray-100 rounded-lg p-1">
        {tabs.map((tab) => {
          const IconComponent = tab.icon
          return (
            <Button
              key={tab.id}
              variant={activeTab === tab.id ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setActiveTab(tab.id)}
              className="flex-1 flex items-center space-x-2 relative"
            >
              <IconComponent className="w-4 h-4" />
              <span className="text-xs">{tab.label}</span>
              {tab.id === 'cart' && cartItemsCount > 0 && (
                <Badge className="absolute -top-1 -right-1 w-4 h-4 rounded-full p-0 flex items-center justify-center text-xs">
                  {cartItemsCount}
                </Badge>
              )}
              {tab.id === 'wishlist' && wishlist.length > 0 && (
                <Badge variant="outline" className="absolute -top-1 -right-1 w-4 h-4 rounded-full p-0 flex items-center justify-center text-xs">
                  {wishlist.length}
                </Badge>
              )}
            </Button>
          )
        })}
      </div>

      {/* Discover Tab */}
      {activeTab === 'discover' && (
        <div className="space-y-6">
          {/* AI Recommendations Banner */}
          <Card className="bg-gradient-to-r from-pink-50 to-purple-50 border-pink-200">
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                  <h3 className="font-medium text-gray-800">AI Styling Recommendations</h3>
                  <p className="text-sm text-gray-600">Personalized picks based on your style</p>
                </div>
                <Button size="sm" className="bg-gradient-to-r from-pink-500 to-purple-600">
                  View All
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Flash Sale Banner */}
          <Card className="bg-gradient-to-r from-red-50 to-orange-50 border-red-200">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Zap className="w-6 h-6 text-red-500" />
                  <div>
                    <h3 className="font-medium text-red-800">Flash Sale</h3>
                    <p className="text-sm text-red-600">Up to 50% off selected items</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-red-600">Ends in</p>
                  <p className="font-bold text-red-800">2h 34m</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Featured Products */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Featured Products</h3>
              <div className="flex space-x-2">
                <Button
                  variant={viewMode === 'grid' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setViewMode('grid')}
                >
                  <Grid className="w-4 h-4" />
                </Button>
                <Button
                  variant={viewMode === 'list' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setViewMode('list')}
                >
                  <List className="w-4 h-4" />
                </Button>
              </div>
            </div>

            <div className={viewMode === 'grid' ? 'grid grid-cols-2 gap-4' : 'space-y-4'}>
              {featuredProducts.map((product) => (
                <Card key={product.id} className="overflow-hidden">
                  <div className="relative">
                    <div className="w-full h-48 bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
                      <Package className="w-12 h-12 text-gray-400" />
                    </div>
                    
                    {/* Product Badges */}
                    <div className="absolute top-2 left-2 space-y-1">
                      {product.isNew && (
                        <Badge className="bg-green-500 text-white text-xs">NEW</Badge>
                      )}
                      {product.isSale && (
                        <Badge className="bg-red-500 text-white text-xs">
                          -{product.discount}%
                        </Badge>
                      )}
                    </div>

                    {/* Wishlist Button */}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => addToWishlist(product)}
                      className="absolute top-2 right-2 w-8 h-8 rounded-full bg-white/80 hover:bg-white"
                    >
                      <Heart className={`w-4 h-4 ${wishlist.find(item => item.id === product.id) ? 'fill-current text-red-500' : ''}`} />
                    </Button>

                    {/* Quick Actions */}
                    <div className="absolute bottom-2 right-2 space-y-1">
                      <Button variant="ghost" size="sm" className="w-8 h-8 rounded-full bg-white/80 hover:bg-white">
                        <Eye className="w-4 h-4" />
                      </Button>
                      <Button variant="ghost" size="sm" className="w-8 h-8 rounded-full bg-white/80 hover:bg-white">
                        <Share className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>

                  <CardContent className="p-3">
                    <div className="mb-2">
                      <h4 className="font-medium text-sm text-gray-800 line-clamp-1">{product.name}</h4>
                      <p className="text-xs text-gray-500">{product.brand}</p>
                    </div>

                    <div className="flex items-center space-x-1 mb-2">
                      <div className="flex items-center">
                        {[1, 2, 3, 4, 5].map((star) => (
                          <Star
                            key={star}
                            className={`w-3 h-3 ${
                              star <= Math.floor(product.rating)
                                ? 'text-yellow-400 fill-current'
                                : 'text-gray-300'
                            }`}
                          />
                        ))}
                      </div>
                      <span className="text-xs text-gray-500">({product.reviews})</span>
                    </div>

                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-2">
                        <span className="font-bold text-gray-800">${product.price}</span>
                        {product.originalPrice && (
                          <span className="text-xs text-gray-500 line-through">
                            ${product.originalPrice}
                          </span>
                        )}
                      </div>
                      {product.fastShipping && (
                        <Badge variant="outline" className="text-xs">
                          <Truck className="w-3 h-3 mr-1" />
                          Fast
                        </Badge>
                      )}
                    </div>

                    {/* Color Options */}
                    <div className="flex items-center space-x-1 mb-3">
                      {product.colors.slice(0, 3).map((color, index) => (
                        <div
                          key={index}
                          className="w-4 h-4 rounded-full border border-gray-300"
                          style={{ backgroundColor: color.toLowerCase().replace(' ', '') }}
                          title={color}
                        />
                      ))}
                      {product.colors.length > 3 && (
                        <span className="text-xs text-gray-500">+{product.colors.length - 3}</span>
                      )}
                    </div>

                    <Button
                      onClick={() => addToCart(product)}
                      disabled={!product.inStock}
                      className="w-full h-8 text-xs bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700"
                    >
                      {product.inStock ? (
                        <>
                          <Plus className="w-3 h-3 mr-1" />
                          Add to Cart
                        </>
                      ) : (
                        'Out of Stock'
                      )}
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Categories Tab */}
      {activeTab === 'categories' && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            {categories.map((category) => (
              <Card key={category.id} className="cursor-pointer hover:shadow-md transition-shadow">
                <CardContent className="p-4 text-center">
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-purple-100 rounded-lg mx-auto mb-3 flex items-center justify-center">
                    <Package className="w-8 h-8 text-purple-500" />
                  </div>
                  <h3 className="font-medium text-gray-800 mb-1">{category.name}</h3>
                  <p className="text-xs text-gray-500">{category.count} items</p>
                  
                  <div className="mt-3 space-y-1">
                    {category.subcategories.slice(0, 2).map((sub, index) => (
                      <Badge key={index} variant="outline" className="text-xs mr-1">
                        {sub}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Cart Tab */}
      {activeTab === 'cart' && (
        <div className="space-y-4">
          {cart.items.length === 0 ? (
            <div className="text-center py-12">
              <ShoppingCart className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-600 mb-2">Your cart is empty</h3>
              <p className="text-gray-500 mb-4">Add some items to get started</p>
              <Button onClick={() => setActiveTab('discover')}>
                Start Shopping
              </Button>
            </div>
          ) : (
            <>
              {/* Cart Items */}
              <div className="space-y-3">
                {cart.items.map((item) => (
                  <Card key={item.id}>
                    <CardContent className="p-4">
                      <div className="flex items-center space-x-4">
                        <div className="w-16 h-20 bg-gray-100 rounded-lg flex items-center justify-center">
                          <Package className="w-6 h-6 text-gray-400" />
                        </div>
                        <div className="flex-1">
                          <h4 className="font-medium text-gray-800">{item.product.name}</h4>
                          <p className="text-sm text-gray-500">{item.product.brand}</p>
                          <div className="flex items-center space-x-2 text-xs text-gray-500 mt-1">
                            <span>{item.variant.color}</span>
                            <span>•</span>
                            <span>Size {item.variant.size}</span>
                          </div>
                          <p className="font-bold text-gray-800 mt-1">${item.product.price}</p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => updateCartQuantity(item.id, item.quantity - 1)}
                            className="w-8 h-8 p-0"
                          >
                            <Minus className="w-3 h-3" />
                          </Button>
                          <span className="w-8 text-center">{item.quantity}</span>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => updateCartQuantity(item.id, item.quantity + 1)}
                            className="w-8 h-8 p-0"
                          >
                            <Plus className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {/* Cart Summary */}
              <Card>
                <CardContent className="p-4">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between text-sm">
                      <span>Subtotal</span>
                      <span>${cart.subtotal}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span>Tax</span>
                      <span>${cart.tax}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span>Shipping</span>
                      <span className="text-green-600">
                        {cart.shipping === 0 ? 'FREE' : `$${cart.shipping}`}
                      </span>
                    </div>
                    <div className="border-t pt-3">
                      <div className="flex items-center justify-between font-bold">
                        <span>Total</span>
                        <span>${cart.total}</span>
                      </div>
                    </div>
                    
                    {cart.shipping === 0 && (
                      <div className="flex items-center space-x-2 text-sm text-green-600">
                        <Truck className="w-4 h-4" />
                        <span>Free shipping on orders over ${cart.freeShippingThreshold}</span>
                      </div>
                    )}
                    
                    <div className="flex items-center space-x-2 text-sm text-gray-500">
                      <Clock className="w-4 h-4" />
                      <span>Estimated delivery: {cart.estimatedDelivery}</span>
                    </div>
                  </div>

                  <Button className="w-full mt-4 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
                    <CreditCard className="w-4 h-4 mr-2" />
                    Proceed to Checkout
                  </Button>
                </CardContent>
              </Card>
            </>
          )}
        </div>
      )}

      {/* Wishlist Tab */}
      {activeTab === 'wishlist' && (
        <div className="space-y-4">
          {wishlist.length === 0 ? (
            <div className="text-center py-12">
              <Heart className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-600 mb-2">Your wishlist is empty</h3>
              <p className="text-gray-500 mb-4">Save items you love for later</p>
              <Button onClick={() => setActiveTab('discover')}>
                Discover Products
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-4">
              {wishlist.map((item) => (
                <Card key={item.id}>
                  <div className="relative">
                    <div className="w-full h-40 bg-gray-100 flex items-center justify-center">
                      <Package className="w-8 h-8 text-gray-400" />
                    </div>
                    
                    {item.priceDropped && (
                      <Badge className="absolute top-2 left-2 bg-green-500 text-white text-xs">
                        <Percent className="w-3 h-3 mr-1" />
                        Price Drop!
                      </Badge>
                    )}
                    
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => addToWishlist(item)}
                      className="absolute top-2 right-2 w-8 h-8 rounded-full bg-white/80 hover:bg-white"
                    >
                      <Heart className="w-4 h-4 fill-current text-red-500" />
                    </Button>
                  </div>

                  <CardContent className="p-3">
                    <h4 className="font-medium text-sm text-gray-800 mb-1">{item.name}</h4>
                    <p className="text-xs text-gray-500 mb-2">{item.brand}</p>
                    
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-2">
                        <span className="font-bold text-gray-800">${item.price}</span>
                        {item.originalPrice && (
                          <span className="text-xs text-gray-500 line-through">
                            ${item.originalPrice}
                          </span>
                        )}
                      </div>
                      {item.priceDropped && (
                        <Badge variant="outline" className="text-xs text-green-600">
                          -{item.discount}%
                        </Badge>
                      )}
                    </div>

                    <Button
                      onClick={() => addToCart(item)}
                      disabled={!item.inStock}
                      className="w-full h-8 text-xs"
                    >
                      {item.inStock ? 'Add to Cart' : 'Out of Stock'}
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
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
            <Button variant="outline" onClick={() => setActiveTab('categories')}>
              <Grid className="w-4 h-4 mr-2" />
              Browse All
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* WS5 Integration Status */}
      <div className="text-center">
        <Badge variant="outline" className="text-xs">
          🔗 WS5: E-commerce Integration Active
        </Badge>
      </div>
    </div>
  )
}

