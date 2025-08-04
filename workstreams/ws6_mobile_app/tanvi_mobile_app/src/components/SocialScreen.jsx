import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  Users, 
  Heart, 
  MessageCircle, 
  Share, 
  TrendingUp,
  Star,
  Crown,
  Trophy,
  Camera,
  Plus,
  Search,
  Filter,
  Bell,
  UserPlus,
  Eye,
  ThumbsUp,
  Bookmark,
  Send,
  MoreHorizontal,
  Sparkles,
  Award,
  Target,
  Zap,
  Globe,
  MapPin,
  Clock,
  ShoppingBag
} from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import { SocialAPI } from '../services/api'

export default function SocialScreen({ currentUser }) {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState('feed')
  const [communityFeed, setCommunityFeed] = useState([])
  const [trendingOutfits, setTrendingOutfits] = useState([])
  const [challenges, setChallenges] = useState([])
  const [following, setFollowing] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [showCreatePost, setShowCreatePost] = useState(false)

  const tabs = [
    { id: 'feed', label: 'Feed', icon: Users },
    { id: 'trending', label: 'Trending', icon: TrendingUp },
    { id: 'challenges', label: 'Challenges', icon: Trophy },
    { id: 'following', label: 'Following', icon: UserPlus }
  ]

  // Load social data
  useEffect(() => {
    loadSocialData()
  }, [activeTab])

  const loadSocialData = async () => {
    setIsLoading(true)
    try {
      switch (activeTab) {
        case 'feed':
          await loadCommunityFeed()
          break
        case 'trending':
          await loadTrendingOutfits()
          break
        case 'challenges':
          await loadChallenges()
          break
        case 'following':
          await loadFollowing()
          break
      }
    } catch (error) {
      console.error('Failed to load social data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const loadCommunityFeed = async () => {
    try {
      const feed = await SocialAPI.getCommunityFeed()
      setCommunityFeed(feed.posts || [])
    } catch (error) {
      // Mock community feed for demo
      setCommunityFeed([
        {
          id: 1,
          user: { 
            name: 'Sarah M.', 
            avatar: '👩‍💼', 
            location: 'New York', 
            followers: 1247,
            isFollowing: false
          },
          outfit: { 
            style: 'Business Casual', 
            confidence: 94,
            occasion: 'Work Meeting',
            items: ['Navy Blazer', 'White Shirt', 'Black Trousers']
          },
          image: '/api/placeholder/300/400',
          caption: 'Perfect outfit for today\'s client presentation! The AI styling suggestions were spot on 💼✨',
          likes: 23,
          comments: 5,
          shares: 2,
          timestamp: '2024-08-03T10:30:00Z',
          isLiked: false,
          isBookmarked: false,
          tags: ['workwear', 'professional', 'aiStyled']
        },
        {
          id: 2,
          user: { 
            name: 'Emma K.', 
            avatar: '👩‍🎨', 
            location: 'Los Angeles', 
            followers: 892,
            isFollowing: true
          },
          outfit: { 
            style: 'Casual Chic', 
            confidence: 96,
            occasion: 'Weekend Brunch',
            items: ['Floral Dress', 'Denim Jacket', 'White Sneakers']
          },
          image: '/api/placeholder/300/400',
          caption: 'Sunday brunch vibes! Love how the AI picked this perfect spring combination 🌸',
          likes: 45,
          comments: 12,
          shares: 8,
          timestamp: '2024-08-03T09:15:00Z',
          isLiked: true,
          isBookmarked: true,
          tags: ['casual', 'brunch', 'spring']
        },
        {
          id: 3,
          user: { 
            name: 'Priya S.', 
            avatar: '👩‍💻', 
            location: 'Mumbai', 
            followers: 2156,
            isFollowing: false
          },
          outfit: { 
            style: 'Indo-Western', 
            confidence: 92,
            occasion: 'Festival',
            items: ['Kurta Top', 'Palazzo Pants', 'Statement Jewelry']
          },
          image: '/api/placeholder/300/400',
          caption: 'Festival ready! Mixing traditional and modern styles with AI help 🎉',
          likes: 67,
          comments: 18,
          shares: 15,
          timestamp: '2024-08-02T18:45:00Z',
          isLiked: false,
          isBookmarked: false,
          tags: ['festival', 'traditional', 'indowestern']
        }
      ])
    }
  }

  const loadTrendingOutfits = async () => {
    // Mock trending outfits for demo
    setTrendingOutfits([
      {
        id: 1,
        style: 'Cottagecore Chic',
        popularity: 94,
        posts: 156,
        growth: '+23%',
        description: 'Romantic, nature-inspired looks with flowing fabrics',
        image: '/api/placeholder/200/250',
        tags: ['romantic', 'nature', 'flowing']
      },
      {
        id: 2,
        style: 'Y2K Revival',
        popularity: 89,
        posts: 203,
        growth: '+45%',
        description: 'Early 2000s fashion making a bold comeback',
        image: '/api/placeholder/200/250',
        tags: ['retro', 'bold', 'nostalgic']
      },
      {
        id: 3,
        style: 'Minimalist Luxe',
        popularity: 87,
        posts: 98,
        growth: '+12%',
        description: 'Clean lines, neutral colors, premium fabrics',
        image: '/api/placeholder/200/250',
        tags: ['minimal', 'luxury', 'clean']
      }
    ])
  }

  const loadChallenges = async () => {
    // Mock challenges for demo
    setChallenges([
      {
        id: 1,
        title: '30-Day Style Challenge',
        description: 'Create a new outfit every day for 30 days',
        participants: 1247,
        prize: '$500 Shopping Spree',
        endDate: '2024-08-31',
        progress: 12,
        totalDays: 30,
        isParticipating: true,
        difficulty: 'Medium',
        category: 'Daily Style'
      },
      {
        id: 2,
        title: 'Sustainable Fashion Week',
        description: 'Style outfits using only sustainable brands',
        participants: 892,
        prize: 'Eco-Friendly Wardrobe',
        endDate: '2024-08-15',
        progress: 0,
        totalDays: 7,
        isParticipating: false,
        difficulty: 'Easy',
        category: 'Sustainability'
      },
      {
        id: 3,
        title: 'Color Pop Challenge',
        description: 'Incorporate bold colors into everyday looks',
        participants: 2156,
        prize: 'Featured on Homepage',
        endDate: '2024-09-10',
        progress: 0,
        totalDays: 14,
        isParticipating: false,
        difficulty: 'Hard',
        category: 'Color Theory'
      }
    ])
  }

  const loadFollowing = async () => {
    // Mock following list for demo
    setFollowing([
      {
        id: 1,
        name: 'Fashion Guru Maya',
        avatar: '👑',
        followers: 15420,
        posts: 342,
        specialty: 'Professional Wear',
        isFollowing: true,
        recentPost: 'Just shared 5 power blazer looks!'
      },
      {
        id: 2,
        name: 'Style Influencer Zoe',
        avatar: '✨',
        followers: 8765,
        posts: 189,
        specialty: 'Casual Chic',
        isFollowing: true,
        recentPost: 'Weekend outfit inspiration is here!'
      },
      {
        id: 3,
        name: 'AI Style Expert',
        avatar: '🤖',
        followers: 25680,
        posts: 567,
        specialty: 'AI Styling Tips',
        isFollowing: true,
        recentPost: 'New AI styling algorithm update!'
      }
    ])
  }

  const handleLike = async (postId) => {
    try {
      const result = await SocialAPI.likePost(postId)
      setCommunityFeed(prev => 
        prev.map(post => 
          post.id === postId 
            ? { 
                ...post, 
                isLiked: !post.isLiked,
                likes: post.isLiked ? post.likes - 1 : post.likes + 1
              }
            : post
        )
      )
    } catch (error) {
      console.error('Failed to like post:', error)
    }
  }

  const handleBookmark = (postId) => {
    setCommunityFeed(prev => 
      prev.map(post => 
        post.id === postId 
          ? { ...post, isBookmarked: !post.isBookmarked }
          : post
      )
    )
  }

  const handleFollow = (userId) => {
    setCommunityFeed(prev => 
      prev.map(post => 
        post.user.id === userId 
          ? { 
              ...post, 
              user: { 
                ...post.user, 
                isFollowing: !post.user.isFollowing,
                followers: post.user.isFollowing 
                  ? post.user.followers - 1 
                  : post.user.followers + 1
              }
            }
          : post
      )
    )
  }

  const joinChallenge = (challengeId) => {
    setChallenges(prev => 
      prev.map(challenge => 
        challenge.id === challengeId 
          ? { 
              ...challenge, 
              isParticipating: true,
              participants: challenge.participants + 1
            }
          : challenge
      )
    )
  }

  const formatTimeAgo = (timestamp) => {
    const now = new Date()
    const postTime = new Date(timestamp)
    const diffInHours = Math.floor((now - postTime) / (1000 * 60 * 60))
    
    if (diffInHours < 1) return 'Just now'
    if (diffInHours < 24) return `${diffInHours}h ago`
    return `${Math.floor(diffInHours / 24)}d ago`
  }

  const displayUser = user || currentUser

  return (
    <div className="p-4 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent">
            Style Community
          </h1>
          <p className="text-gray-600">Connect, share, and get inspired</p>
        </div>
        <div className="flex space-x-2">
          <Button variant="ghost" size="sm">
            <Bell className="w-4 h-4" />
          </Button>
          <Button variant="ghost" size="sm">
            <Search className="w-4 h-4" />
          </Button>
        </div>
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
              className="flex-1 flex items-center space-x-2"
            >
              <IconComponent className="w-4 h-4" />
              <span className="text-xs">{tab.label}</span>
            </Button>
          )
        })}
      </div>

      {/* Create Post Button */}
      {activeTab === 'feed' && (
        <Button
          onClick={() => setShowCreatePost(true)}
          className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700"
        >
          <Plus className="w-4 h-4 mr-2" />
          Share Your Style
        </Button>
      )}

      {/* Feed Tab */}
      {activeTab === 'feed' && (
        <div className="space-y-6">
          {communityFeed.map((post) => (
            <Card key={post.id} className="overflow-hidden">
              {/* Post Header */}
              <div className="p-4 pb-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-pink-400 to-purple-500 rounded-full flex items-center justify-center text-lg">
                      {post.user.avatar}
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <p className="font-medium text-gray-800">{post.user.name}</p>
                        {!post.user.isFollowing && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleFollow(post.user.id)}
                            className="h-6 px-2 text-xs"
                          >
                            Follow
                          </Button>
                        )}
                      </div>
                      <div className="flex items-center space-x-2 text-xs text-gray-500">
                        <MapPin className="w-3 h-3" />
                        <span>{post.user.location}</span>
                        <span>•</span>
                        <span>{formatTimeAgo(post.timestamp)}</span>
                      </div>
                    </div>
                  </div>
                  <Button variant="ghost" size="sm">
                    <MoreHorizontal className="w-4 h-4" />
                  </Button>
                </div>
              </div>

              {/* Post Image */}
              <div className="relative">
                <div className="w-full h-80 bg-gradient-to-br from-pink-100 to-purple-100 flex items-center justify-center">
                  <div className="text-center">
                    <Camera className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-500">Outfit Photo</p>
                  </div>
                </div>
                
                {/* AI Confidence Badge */}
                <div className="absolute top-3 right-3">
                  <Badge className="bg-gradient-to-r from-pink-500 to-purple-600">
                    <Sparkles className="w-3 h-3 mr-1" />
                    {post.outfit.confidence}% AI Match
                  </Badge>
                </div>
              </div>

              {/* Post Content */}
              <div className="p-4">
                {/* Outfit Details */}
                <div className="mb-3">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-medium text-gray-800">{post.outfit.style}</h3>
                    <Badge variant="outline" className="text-xs">
                      {post.outfit.occasion}
                    </Badge>
                  </div>
                  <div className="flex flex-wrap gap-1 mb-2">
                    {post.outfit.items.map((item, index) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {item}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Caption */}
                <p className="text-gray-700 text-sm mb-3">{post.caption}</p>

                {/* Tags */}
                <div className="flex flex-wrap gap-1 mb-3">
                  {post.tags.map((tag, index) => (
                    <span key={index} className="text-xs text-blue-600 hover:underline cursor-pointer">
                      #{tag}
                    </span>
                  ))}
                </div>

                {/* Engagement Stats */}
                <div className="flex items-center justify-between text-sm text-gray-500 mb-3">
                  <div className="flex items-center space-x-4">
                    <span>{post.likes} likes</span>
                    <span>{post.comments} comments</span>
                    <span>{post.shares} shares</span>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex items-center justify-between pt-3 border-t">
                  <div className="flex space-x-1">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleLike(post.id)}
                      className={post.isLiked ? 'text-red-500' : ''}
                    >
                      <Heart className={`w-4 h-4 mr-1 ${post.isLiked ? 'fill-current' : ''}`} />
                      Like
                    </Button>
                    <Button variant="ghost" size="sm">
                      <MessageCircle className="w-4 h-4 mr-1" />
                      Comment
                    </Button>
                    <Button variant="ghost" size="sm">
                      <Share className="w-4 h-4 mr-1" />
                      Share
                    </Button>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleBookmark(post.id)}
                    className={post.isBookmarked ? 'text-blue-500' : ''}
                  >
                    <Bookmark className={`w-4 h-4 ${post.isBookmarked ? 'fill-current' : ''}`} />
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Trending Tab */}
      {activeTab === 'trending' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Trending Styles</h3>
            <Button variant="ghost" size="sm">
              <Filter className="w-4 h-4" />
            </Button>
          </div>
          
          {trendingOutfits.map((trend) => (
            <Card key={trend.id}>
              <CardContent className="p-4">
                <div className="flex items-center space-x-4">
                  <div className="w-16 h-20 bg-gradient-to-br from-pink-100 to-purple-100 rounded-lg flex items-center justify-center">
                    <Sparkles className="w-6 h-6 text-purple-500" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="font-medium">{trend.style}</h4>
                      <Badge className="bg-gradient-to-r from-green-500 to-blue-500">
                        {trend.growth}
                      </Badge>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{trend.description}</p>
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>{trend.posts} posts</span>
                      <div className="flex items-center space-x-1">
                        <TrendingUp className="w-3 h-3" />
                        <span>{trend.popularity}% popularity</span>
                      </div>
                    </div>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {trend.tags.map((tag, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Challenges Tab */}
      {activeTab === 'challenges' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Style Challenges</h3>
            <Badge variant="outline">{challenges.length} active</Badge>
          </div>
          
          {challenges.map((challenge) => (
            <Card key={challenge.id}>
              <CardContent className="p-4">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <h4 className="font-medium">{challenge.title}</h4>
                      <Badge variant="outline" className="text-xs">
                        {challenge.difficulty}
                      </Badge>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{challenge.description}</p>
                    <div className="flex items-center space-x-4 text-xs text-gray-500">
                      <div className="flex items-center space-x-1">
                        <Users className="w-3 h-3" />
                        <span>{challenge.participants} participants</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Clock className="w-3 h-3" />
                        <span>Ends {challenge.endDate}</span>
                      </div>
                    </div>
                  </div>
                  <Trophy className="w-6 h-6 text-yellow-500" />
                </div>

                {challenge.isParticipating && (
                  <div className="mb-3">
                    <div className="flex items-center justify-between text-sm mb-1">
                      <span>Progress</span>
                      <span>{challenge.progress}/{challenge.totalDays} days</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-pink-500 to-purple-600 h-2 rounded-full" 
                        style={{ width: `${(challenge.progress / challenge.totalDays) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                )}

                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-green-600">Prize: {challenge.prize}</p>
                    <p className="text-xs text-gray-500">{challenge.category}</p>
                  </div>
                  {!challenge.isParticipating ? (
                    <Button
                      size="sm"
                      onClick={() => joinChallenge(challenge.id)}
                      className="bg-gradient-to-r from-pink-500 to-purple-600"
                    >
                      Join Challenge
                    </Button>
                  ) : (
                    <Badge className="bg-green-100 text-green-800">
                      Participating
                    </Badge>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Following Tab */}
      {activeTab === 'following' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Following</h3>
            <Badge variant="outline">{following.length} people</Badge>
          </div>
          
          {following.map((person) => (
            <Card key={person.id}>
              <CardContent className="p-4">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-pink-400 to-purple-500 rounded-full flex items-center justify-center text-xl">
                    {person.avatar}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="font-medium">{person.name}</h4>
                      <Button variant="outline" size="sm">
                        Following
                      </Button>
                    </div>
                    <p className="text-sm text-gray-600 mb-1">{person.specialty}</p>
                    <div className="flex items-center space-x-4 text-xs text-gray-500 mb-2">
                      <span>{person.followers.toLocaleString()} followers</span>
                      <span>{person.posts} posts</span>
                    </div>
                    <p className="text-xs text-blue-600">{person.recentPost}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Quick Actions */}
      <Card>
        <CardContent className="pt-6">
          <div className="grid grid-cols-2 gap-3">
            <Button variant="outline" onClick={() => window.location.href = '/camera'}>
              <Camera className="w-4 h-4 mr-2" />
              Share Outfit
            </Button>
            <Button variant="outline" onClick={() => window.location.href = '/ai-style'}>
              <Sparkles className="w-4 h-4 mr-2" />
              Get AI Styled
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* WS4 Integration Status */}
      <div className="text-center">
        <Badge variant="outline" className="text-xs">
          🔗 WS4: Social Integration Active
        </Badge>
      </div>
    </div>
  )
}

