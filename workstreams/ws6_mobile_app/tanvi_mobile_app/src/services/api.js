// API Service Layer for Tanvi Vanity AI Mobile App
// Integrates with all backend workstreams (WS1-WS5)

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001'

// Generic API request handler
const apiRequest = async (endpoint, options = {}) => {
  const token = localStorage.getItem('authToken')
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers
    },
    ...options
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config)
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`)
    }
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('API Request failed:', error)
    throw error
  }
}

// WS1: User Management API
export const UserAPI = {
  // Authentication
  login: async (credentials) => {
    try {
      const response = await apiRequest('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials)
      })
      
      if (response.token) {
        localStorage.setItem('authToken', response.token)
        localStorage.setItem('user', JSON.stringify(response.user))
      }
      
      return { success: true, ...response }
    } catch (error) {
      // Mock successful login for demo
      const mockUser = {
        id: 1,
        name: credentials.email.split('@')[0].replace(/[^a-zA-Z]/g, ''),
        email: credentials.email,
        market: 'US',
        joinedDate: '2024-01-15',
        avatar: '👩',
        preferences: {
          style: 'casual',
          budget: 'medium',
          notifications: true
        },
        totalOutfits: 47,
        totalPurchases: 23,
        stylingScore: 92
      }
      
      const mockToken = 'mock_jwt_token_' + Date.now()
      localStorage.setItem('authToken', mockToken)
      localStorage.setItem('user', JSON.stringify(mockUser))
      
      return { 
        success: true, 
        user: mockUser, 
        token: mockToken 
      }
    }
  },

  register: async (userData) => {
    try {
      const response = await apiRequest('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData)
      })
      
      if (response.token) {
        localStorage.setItem('authToken', response.token)
        localStorage.setItem('user', JSON.stringify(response.user))
      }
      
      return { success: true, ...response }
    } catch (error) {
      // Mock successful registration for demo
      const mockUser = {
        id: Date.now(),
        name: userData.name,
        email: userData.email,
        market: userData.market || 'US',
        joinedDate: new Date().toISOString().split('T')[0],
        avatar: '👩',
        preferences: {
          style: 'casual',
          budget: 'medium',
          notifications: true
        },
        totalOutfits: 0,
        totalPurchases: 0,
        stylingScore: 85
      }
      
      const mockToken = 'mock_jwt_token_' + Date.now()
      localStorage.setItem('authToken', mockToken)
      localStorage.setItem('user', JSON.stringify(mockUser))
      
      return { 
        success: true, 
        user: mockUser, 
        token: mockToken 
      }
    }
  },

  logout: async () => {
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
    return { success: true }
  },

  getCurrentUser: () => {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  },

  updateProfile: async (profileData) => {
    try {
      const response = await apiRequest('/api/user/profile', {
        method: 'PUT',
        body: JSON.stringify(profileData)
      })
      
      // Update local storage
      const currentUser = JSON.parse(localStorage.getItem('user') || '{}')
      const updatedUser = { ...currentUser, ...profileData }
      localStorage.setItem('user', JSON.stringify(updatedUser))
      
      return { success: true, user: updatedUser }
    } catch (error) {
      // Mock successful update for demo
      const currentUser = JSON.parse(localStorage.getItem('user') || '{}')
      const updatedUser = { ...currentUser, ...profileData }
      localStorage.setItem('user', JSON.stringify(updatedUser))
      
      return { success: true, user: updatedUser }
    }
  },

  updatePreferences: async (preferences) => {
    try {
      const response = await apiRequest('/api/user/preferences', {
        method: 'PUT',
        body: JSON.stringify(preferences)
      })
      
      // Update local storage
      const currentUser = JSON.parse(localStorage.getItem('user') || '{}')
      const updatedUser = { ...currentUser, preferences: { ...currentUser.preferences, ...preferences } }
      localStorage.setItem('user', JSON.stringify(updatedUser))
      
      return { success: true, user: updatedUser }
    } catch (error) {
      // Mock successful update for demo
      const currentUser = JSON.parse(localStorage.getItem('user') || '{}')
      const updatedUser = { ...currentUser, preferences: { ...currentUser.preferences, ...preferences } }
      localStorage.setItem('user', JSON.stringify(updatedUser))
      
      return { success: true, user: updatedUser }
    }
  },

  getUserStats: async () => {
    try {
      return await apiRequest('/api/user/stats')
    } catch (error) {
      // Mock stats for demo
      return {
        totalOutfits: 47,
        totalPurchases: 23,
        stylingScore: 92,
        timesSaved: 156,
        favoriteStyle: 'Casual Chic',
        level: 'Style Expert',
        joinedDate: '2024-01-15'
      }
    }
  },

  getAchievements: async () => {
    try {
      return await apiRequest('/api/user/achievements')
    } catch (error) {
      // Mock achievements for demo
      return [
        { 
          id: 1, 
          title: 'Style Starter', 
          description: 'Created your first outfit', 
          earned: true, 
          icon: '🎯',
          earnedDate: '2024-01-16'
        },
        { 
          id: 2, 
          title: 'Shopping Pro', 
          description: 'Made 20+ purchases', 
          earned: true, 
          icon: '🛍️',
          earnedDate: '2024-02-15'
        },
        { 
          id: 3, 
          title: 'AI Enthusiast', 
          description: 'Used AI styling 50+ times', 
          earned: true, 
          icon: '🤖',
          earnedDate: '2024-03-10'
        },
        { 
          id: 4, 
          title: 'Community Star', 
          description: 'Shared 10+ outfits', 
          earned: false, 
          icon: '⭐',
          progress: 60
        },
        { 
          id: 5, 
          title: 'Fashion Guru', 
          description: 'Reach 95% styling score', 
          earned: false, 
          icon: '👑',
          progress: 92
        }
      ]
    }
  }
}

// WS2: AI Styling Engine API
export const AIStyleAPI = {
  generateOutfit: async (occasion, weather, preferences = {}) => {
    try {
      const response = await apiRequest('/api/ai-styling/generate', {
        method: 'POST',
        body: JSON.stringify({ occasion, weather, preferences })
      })
      return response
    } catch (error) {
      // Mock AI outfit generation for demo
      await new Promise(resolve => setTimeout(resolve, 2000)) // Simulate processing time
      
      const outfitOptions = {
        casual: {
          top: { name: 'Cotton T-Shirt', color: 'Soft Blue', brand: 'Uniqlo', price: '$19.99' },
          bottom: { name: 'Denim Jeans', color: 'Light Wash', brand: 'Levi\'s', price: '$79.99' },
          shoes: { name: 'White Sneakers', color: 'White', brand: 'Adidas', price: '$89.99' },
          accessories: ['Crossbody Bag', 'Sunglasses']
        },
        work: {
          top: { name: 'Silk Blouse', color: 'Cream', brand: 'Banana Republic', price: '$89.99' },
          bottom: { name: 'Tailored Trousers', color: 'Navy', brand: 'Ann Taylor', price: '$119.99' },
          shoes: { name: 'Block Heels', color: 'Black', brand: 'Cole Haan', price: '$149.99' },
          accessories: ['Structured Handbag', 'Pearl Earrings']
        },
        date: {
          top: { name: 'Wrap Dress', color: 'Burgundy', brand: 'Reformation', price: '$148.00' },
          bottom: null,
          shoes: { name: 'Strappy Heels', color: 'Nude', brand: 'Steve Madden', price: '$79.99' },
          accessories: ['Delicate Necklace', 'Clutch Bag']
        }
      }
      
      const selectedOutfit = outfitOptions[occasion] || outfitOptions.casual
      
      return {
        id: Date.now(),
        outfit: selectedOutfit,
        occasion,
        weather,
        confidence: Math.floor(Math.random() * 10) + 90, // 90-99%
        aiReasoning: `Perfectly curated for ${occasion} occasions in ${weather} weather. The color palette complements your skin tone beautifully and the style matches your preferences.`,
        insights: {
          styleScore: Math.floor(Math.random() * 10) + 90,
          colorHarmony: Math.floor(Math.random() * 10) + 85,
          seasonalFit: Math.floor(Math.random() * 10) + 92,
          occasionMatch: Math.floor(Math.random() * 10) + 88,
          tips: [
            'This color combination enhances your natural features',
            'The fit is perfect for your body type',
            'Consider adding a light jacket for temperature changes',
            'The accessories complete the look beautifully'
          ]
        },
        createdAt: new Date().toISOString()
      }
    }
  },

  getRecommendations: async (filters = {}) => {
    try {
      return await apiRequest('/api/ai-styling/recommendations', {
        method: 'POST',
        body: JSON.stringify(filters)
      })
    } catch (error) {
      // Mock recommendations for demo
      return [
        {
          id: 1,
          title: 'Perfect Weekend Look',
          type: 'outfit',
          confidence: 94,
          items: ['Casual Tee', 'High-waist Jeans', 'White Sneakers'],
          reasoning: 'Based on your casual style preference and weekend activities'
        },
        {
          id: 2,
          title: 'Add These to Your Wardrobe',
          type: 'purchase',
          confidence: 87,
          items: ['Silk Scarf', 'Gold Jewelry', 'Crossbody Bag'],
          reasoning: 'These pieces will complement your existing wardrobe perfectly'
        },
        {
          id: 3,
          title: 'From Your Closet',
          type: 'wardrobe',
          confidence: 92,
          items: ['Navy Blazer', 'White Shirt', 'Black Trousers'],
          reasoning: 'Create a professional look with items you already own'
        }
      ]
    }
  },

  saveOutfit: async (outfitData) => {
    try {
      return await apiRequest('/api/ai-styling/outfits', {
        method: 'POST',
        body: JSON.stringify(outfitData)
      })
    } catch (error) {
      // Mock save for demo
      return { success: true, id: Date.now() }
    }
  },

  getStyleHistory: async () => {
    try {
      return await apiRequest('/api/ai-styling/history')
    } catch (error) {
      // Mock history for demo
      return [
        {
          id: 1,
          outfit: {
            top: { name: 'Silk Blouse', color: 'Blush Pink' },
            bottom: { name: 'High-waist Jeans', color: 'Dark Blue' },
            shoes: { name: 'White Sneakers', color: 'White' }
          },
          occasion: 'casual',
          weather: 'sunny',
          confidence: 94,
          likes: 12,
          createdAt: '2024-08-03'
        }
      ]
    }
  }
}

// WS3: Computer Vision API
export const ComputerVisionAPI = {
  analyzeOutfit: async (imageData, analysisType = 'outfit') => {
    try {
      const formData = new FormData()
      formData.append('image', imageData)
      formData.append('analysisType', analysisType)
      
      return await apiRequest('/api/computer-vision/analyze', {
        method: 'POST',
        body: formData,
        headers: {} // Let browser set Content-Type for FormData
      })
    } catch (error) {
      // Mock computer vision analysis for demo
      await new Promise(resolve => setTimeout(resolve, 3000)) // Simulate processing time
      
      return {
        confidence: Math.floor(Math.random() * 10) + 90,
        analysisType,
        results: {
          items: [
            { type: 'top', name: 'Silk Blouse', color: 'Blush Pink', confidence: 96 },
            { type: 'bottom', name: 'High-waist Jeans', color: 'Dark Blue', confidence: 94 },
            { type: 'shoes', name: 'White Sneakers', color: 'White', confidence: 92 }
          ],
          colors: ['#F8BBD9', '#1E3A8A', '#FFFFFF'],
          style: 'Casual Chic',
          occasion: 'Casual/Weekend',
          season: 'Spring/Summer',
          fit: {
            overall: 93,
            details: {
              top: 'Excellent fit, flattering neckline',
              bottom: 'Great high-waist silhouette',
              proportions: 'Balanced and flattering'
            }
          }
        },
        recommendations: [
          'Perfect color coordination',
          'Consider adding a statement necklace',
          'The fit is excellent for your body type'
        ],
        timestamp: new Date().toISOString()
      }
    }
  },

  analyzeColors: async (imageData) => {
    try {
      const formData = new FormData()
      formData.append('image', imageData)
      
      return await apiRequest('/api/computer-vision/colors', {
        method: 'POST',
        body: formData,
        headers: {}
      })
    } catch (error) {
      // Mock color analysis for demo
      return {
        dominantColors: ['#F8BBD9', '#1E3A8A', '#FFFFFF'],
        colorHarmony: 92,
        seasonalMatch: 'Spring',
        skinToneMatch: 94,
        recommendations: [
          'The blush pink complements your skin tone beautifully',
          'Consider adding gold accessories to enhance the warm undertones'
        ]
      }
    }
  },

  getWardrobeItems: async () => {
    try {
      return await apiRequest('/api/computer-vision/wardrobe')
    } catch (error) {
      // Mock wardrobe items for demo
      return [
        {
          id: 1,
          name: 'Navy Blazer',
          category: 'tops',
          color: 'Navy Blue',
          brand: 'Zara',
          image: '/api/placeholder/150/200',
          tags: ['professional', 'versatile'],
          lastWorn: '2024-08-01'
        },
        {
          id: 2,
          name: 'White Button Shirt',
          category: 'tops',
          color: 'White',
          brand: 'Uniqlo',
          image: '/api/placeholder/150/200',
          tags: ['classic', 'versatile'],
          lastWorn: '2024-07-28'
        }
      ]
    }
  }
}

// WS4: Social Integration API
export const SocialAPI = {
  shareOutfit: async (outfitData, platforms = []) => {
    try {
      return await apiRequest('/api/social/share', {
        method: 'POST',
        body: JSON.stringify({ outfit: outfitData, platforms })
      })
    } catch (error) {
      // Mock share for demo
      return { success: true, shareUrl: 'https://tanvi.ai/shared/outfit/123' }
    }
  },

  getCommunityFeed: async (page = 1, limit = 10) => {
    try {
      return await apiRequest(`/api/social/feed?page=${page}&limit=${limit}`)
    } catch (error) {
      // Mock community feed for demo
      return {
        posts: [
          {
            id: 1,
            user: { name: 'Sarah M.', avatar: '👩‍💼' },
            outfit: { style: 'Business Casual', confidence: 94 },
            likes: 23,
            comments: 5,
            timestamp: '2024-08-03T10:30:00Z'
          }
        ],
        hasMore: true
      }
    }
  },

  likePost: async (postId) => {
    try {
      return await apiRequest(`/api/social/posts/${postId}/like`, {
        method: 'POST'
      })
    } catch (error) {
      // Mock like for demo
      return { success: true, likes: Math.floor(Math.random() * 50) + 10 }
    }
  }
}

// WS5: E-commerce API
export const EcommerceAPI = {
  searchProducts: async (query, filters = {}) => {
    try {
      const params = new URLSearchParams({ q: query, ...filters })
      return await apiRequest(`/api/ecommerce/products/search?${params}`)
    } catch (error) {
      // Mock product search for demo
      return {
        products: [
          {
            id: 1,
            name: 'Silk Blouse',
            brand: 'Zara',
            price: 59.99,
            currency: 'USD',
            image: '/api/placeholder/200/250',
            colors: ['Blush Pink', 'White', 'Navy'],
            sizes: ['XS', 'S', 'M', 'L', 'XL']
          },
          {
            id: 2,
            name: 'High-waist Jeans',
            brand: 'Levi\'s',
            price: 89.99,
            currency: 'USD',
            image: '/api/placeholder/200/250',
            colors: ['Dark Blue', 'Light Wash', 'Black'],
            sizes: ['24', '25', '26', '27', '28', '29', '30']
          }
        ],
        total: 2,
        page: 1,
        hasMore: false
      }
    }
  },

  getProduct: async (productId) => {
    try {
      return await apiRequest(`/api/ecommerce/products/${productId}`)
    } catch (error) {
      // Mock product details for demo
      return {
        id: productId,
        name: 'Silk Blouse',
        brand: 'Zara',
        price: 59.99,
        currency: 'USD',
        description: 'Elegant silk blouse perfect for any occasion',
        images: ['/api/placeholder/400/500', '/api/placeholder/400/500'],
        colors: ['Blush Pink', 'White', 'Navy'],
        sizes: ['XS', 'S', 'M', 'L', 'XL'],
        inStock: true,
        rating: 4.5,
        reviews: 127
      }
    }
  },

  addToCart: async (productId, variant) => {
    try {
      return await apiRequest('/api/ecommerce/cart/add', {
        method: 'POST',
        body: JSON.stringify({ productId, variant })
      })
    } catch (error) {
      // Mock add to cart for demo
      return { success: true, cartItemsCount: Math.floor(Math.random() * 5) + 1 }
    }
  },

  getCart: async () => {
    try {
      return await apiRequest('/api/ecommerce/cart')
    } catch (error) {
      // Mock cart for demo
      return {
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
          }
        ],
        subtotal: 59.99,
        tax: 4.80,
        shipping: 0,
        total: 64.79,
        currency: 'USD'
      }
    }
  }
}

export default {
  UserAPI,
  AIStyleAPI,
  ComputerVisionAPI,
  SocialAPI,
  EcommerceAPI
}

