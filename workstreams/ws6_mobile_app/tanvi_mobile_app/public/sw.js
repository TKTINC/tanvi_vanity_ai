// Tanvi Vanity AI - Service Worker for PWA
// "We girls have no time" - Lightning-fast offline experience

const CACHE_NAME = 'tanvi-vanity-ai-v1.0.0'
const STATIC_CACHE_NAME = 'tanvi-static-v1.0.0'
const DYNAMIC_CACHE_NAME = 'tanvi-dynamic-v1.0.0'

// Static assets to cache immediately
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  // Core app shell
  '/static/js/main.js',
  '/static/css/main.css',
  // Fonts and essential assets
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
]

// API endpoints to cache for offline functionality
const API_CACHE_PATTERNS = [
  /\/api\/users\/profile/,
  /\/api\/ai-styling\/recommendations/,
  /\/api\/products\/search/,
  /\/api\/social\/feed/,
  /\/api\/ecommerce\/cart/
]

// Network-first patterns (always try network first)
const NETWORK_FIRST_PATTERNS = [
  /\/api\/auth\//,
  /\/api\/payments\//,
  /\/api\/orders\//,
  /\/api\/camera\/analyze/
]

// Cache-first patterns (serve from cache if available)
const CACHE_FIRST_PATTERNS = [
  /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
  /\.(?:css|js)$/,
  /\/icons\//,
  /\/screenshots\//
]

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('[SW] Installing Tanvi Vanity AI Service Worker...')
  
  event.waitUntil(
    caches.open(STATIC_CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Caching static assets')
        return cache.addAll(STATIC_ASSETS)
      })
      .then(() => {
        console.log('[SW] Static assets cached successfully')
        return self.skipWaiting()
      })
      .catch((error) => {
        console.error('[SW] Failed to cache static assets:', error)
      })
  )
})

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating Tanvi Vanity AI Service Worker...')
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE_NAME && 
                cacheName !== DYNAMIC_CACHE_NAME &&
                cacheName !== CACHE_NAME) {
              console.log('[SW] Deleting old cache:', cacheName)
              return caches.delete(cacheName)
            }
          })
        )
      })
      .then(() => {
        console.log('[SW] Service Worker activated successfully')
        return self.clients.claim()
      })
  )
})

// Fetch event - handle all network requests
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return
  }
  
  // Skip chrome-extension and other non-http requests
  if (!request.url.startsWith('http')) {
    return
  }
  
  event.respondWith(handleFetch(request))
})

async function handleFetch(request) {
  const url = new URL(request.url)
  
  try {
    // Network-first strategy for critical APIs
    if (NETWORK_FIRST_PATTERNS.some(pattern => pattern.test(request.url))) {
      return await networkFirst(request)
    }
    
    // Cache-first strategy for static assets
    if (CACHE_FIRST_PATTERNS.some(pattern => pattern.test(request.url))) {
      return await cacheFirst(request)
    }
    
    // API caching strategy
    if (API_CACHE_PATTERNS.some(pattern => pattern.test(request.url))) {
      return await staleWhileRevalidate(request)
    }
    
    // Default: Network with cache fallback
    return await networkWithCacheFallback(request)
    
  } catch (error) {
    console.error('[SW] Fetch error:', error)
    return await handleOfflineFallback(request)
  }
}

// Network-first strategy
async function networkFirst(request) {
  try {
    const networkResponse = await fetch(request)
    
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE_NAME)
      cache.put(request, networkResponse.clone())
    }
    
    return networkResponse
  } catch (error) {
    const cachedResponse = await caches.match(request)
    if (cachedResponse) {
      return cachedResponse
    }
    throw error
  }
}

// Cache-first strategy
async function cacheFirst(request) {
  const cachedResponse = await caches.match(request)
  
  if (cachedResponse) {
    return cachedResponse
  }
  
  try {
    const networkResponse = await fetch(request)
    
    if (networkResponse.ok) {
      const cache = await caches.open(STATIC_CACHE_NAME)
      cache.put(request, networkResponse.clone())
    }
    
    return networkResponse
  } catch (error) {
    throw error
  }
}

// Stale-while-revalidate strategy
async function staleWhileRevalidate(request) {
  const cachedResponse = await caches.match(request)
  
  const networkResponsePromise = fetch(request)
    .then((networkResponse) => {
      if (networkResponse.ok) {
        const cache = caches.open(DYNAMIC_CACHE_NAME)
        cache.then(c => c.put(request, networkResponse.clone()))
      }
      return networkResponse
    })
    .catch(() => null)
  
  return cachedResponse || await networkResponsePromise
}

// Network with cache fallback
async function networkWithCacheFallback(request) {
  try {
    const networkResponse = await fetch(request)
    
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE_NAME)
      cache.put(request, networkResponse.clone())
    }
    
    return networkResponse
  } catch (error) {
    const cachedResponse = await caches.match(request)
    if (cachedResponse) {
      return cachedResponse
    }
    throw error
  }
}

// Offline fallback handling
async function handleOfflineFallback(request) {
  const url = new URL(request.url)
  
  // Return cached page for navigation requests
  if (request.mode === 'navigate') {
    const cachedPage = await caches.match('/')
    if (cachedPage) {
      return cachedPage
    }
  }
  
  // Return offline page for API requests
  if (url.pathname.startsWith('/api/')) {
    return new Response(
      JSON.stringify({
        error: 'Offline',
        message: 'You are currently offline. Please check your connection.',
        offline: true
      }),
      {
        status: 503,
        statusText: 'Service Unavailable',
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )
  }
  
  // Return generic offline response
  return new Response(
    'You are currently offline. Please check your connection.',
    {
      status: 503,
      statusText: 'Service Unavailable',
      headers: {
        'Content-Type': 'text/plain'
      }
    }
  )
}

// Background sync for offline actions
self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync triggered:', event.tag)
  
  if (event.tag === 'background-sync-cart') {
    event.waitUntil(syncCart())
  }
  
  if (event.tag === 'background-sync-analytics') {
    event.waitUntil(syncAnalytics())
  }
})

// Sync cart data when back online
async function syncCart() {
  try {
    // Get pending cart actions from IndexedDB
    const pendingActions = await getPendingCartActions()
    
    for (const action of pendingActions) {
      try {
        await fetch('/api/ecommerce/cart', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${action.token}`
          },
          body: JSON.stringify(action.data)
        })
        
        // Remove from pending actions
        await removePendingCartAction(action.id)
      } catch (error) {
        console.error('[SW] Failed to sync cart action:', error)
      }
    }
  } catch (error) {
    console.error('[SW] Cart sync failed:', error)
  }
}

// Sync analytics data when back online
async function syncAnalytics() {
  try {
    // Get pending analytics events from IndexedDB
    const pendingEvents = await getPendingAnalyticsEvents()
    
    for (const event of pendingEvents) {
      try {
        await fetch('/api/analytics/events', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(event.data)
        })
        
        // Remove from pending events
        await removePendingAnalyticsEvent(event.id)
      } catch (error) {
        console.error('[SW] Failed to sync analytics event:', error)
      }
    }
  } catch (error) {
    console.error('[SW] Analytics sync failed:', error)
  }
}

// Push notification handling
self.addEventListener('push', (event) => {
  console.log('[SW] Push notification received')
  
  const options = {
    body: 'New style recommendations available!',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Explore Styles',
        icon: '/icons/action-explore.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/icons/action-close.png'
      }
    ]
  }
  
  if (event.data) {
    const data = event.data.json()
    options.body = data.body || options.body
    options.data = { ...options.data, ...data }
  }
  
  event.waitUntil(
    self.registration.showNotification('Tanvi Vanity AI', options)
  )
})

// Notification click handling
self.addEventListener('notificationclick', (event) => {
  console.log('[SW] Notification clicked:', event.action)
  
  event.notification.close()
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/ai-style')
    )
  } else if (event.action === 'close') {
    // Just close the notification
    return
  } else {
    // Default action - open the app
    event.waitUntil(
      clients.openWindow('/')
    )
  }
})

// Message handling from main app
self.addEventListener('message', (event) => {
  console.log('[SW] Message received:', event.data)
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting()
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME })
  }
})

// Utility functions for IndexedDB operations
async function getPendingCartActions() {
  // Implementation would use IndexedDB to store/retrieve pending actions
  return []
}

async function removePendingCartAction(id) {
  // Implementation would remove action from IndexedDB
}

async function getPendingAnalyticsEvents() {
  // Implementation would use IndexedDB to store/retrieve pending events
  return []
}

async function removePendingAnalyticsEvent(id) {
  // Implementation would remove event from IndexedDB
}

console.log('[SW] Tanvi Vanity AI Service Worker loaded successfully')

