import time
import functools
import json
from datetime import datetime, timedelta
from flask import request, g
from src.models.user import db
from src.models.analytics import AnalyticsHelper
import logging

# Configure performance logging
performance_logger = logging.getLogger('performance')
performance_logger.setLevel(logging.INFO)

class PerformanceMonitor:
    """
    Performance monitoring and optimization utilities
    "We girls have no time" - Every millisecond counts!
    """
    
    @staticmethod
    def time_endpoint(f):
        """Decorator to time API endpoint execution"""
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = f(*args, **kwargs)
                execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                
                # Log slow endpoints (>500ms)
                if execution_time > 500:
                    performance_logger.warning(
                        f"Slow endpoint: {request.endpoint} took {execution_time:.2f}ms"
                    )
                
                # Add performance headers for debugging
                if hasattr(result, 'headers'):
                    result.headers['X-Response-Time'] = f"{execution_time:.2f}ms"
                    result.headers['X-Endpoint'] = request.endpoint
                
                return result
                
            except Exception as e:
                execution_time = (time.time() - start_time) * 1000
                performance_logger.error(
                    f"Error in {request.endpoint} after {execution_time:.2f}ms: {str(e)}"
                )
                raise
                
        return wrapper
    
    @staticmethod
    def cache_response(duration_minutes=5):
        """Simple response caching decorator"""
        def decorator(f):
            cache = {}
            
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                # Create cache key from function name and args
                cache_key = f"{f.__name__}:{hash(str(args) + str(kwargs))}"
                current_time = datetime.utcnow()
                
                # Check if cached response exists and is still valid
                if cache_key in cache:
                    cached_data, cached_time = cache[cache_key]
                    if current_time - cached_time < timedelta(minutes=duration_minutes):
                        return cached_data
                
                # Execute function and cache result
                result = f(*args, **kwargs)
                cache[cache_key] = (result, current_time)
                
                # Clean old cache entries (simple cleanup)
                if len(cache) > 100:  # Limit cache size
                    oldest_key = min(cache.keys(), key=lambda k: cache[k][1])
                    del cache[oldest_key]
                
                return result
                
            return wrapper
        return decorator
    
    @staticmethod
    def optimize_database_query(query, limit=100):
        """Optimize database queries with pagination and limits"""
        # Add default limit if not specified
        if not hasattr(query, '_limit') or query._limit is None:
            query = query.limit(limit)
        
        # Add performance hints
        query = query.options(db.joinedload('*'))  # Eager load relationships
        
        return query
    
    @staticmethod
    def batch_database_operations(operations, batch_size=50):
        """Batch database operations for better performance"""
        results = []
        
        for i in range(0, len(operations), batch_size):
            batch = operations[i:i + batch_size]
            
            try:
                # Execute batch
                for operation in batch:
                    if callable(operation):
                        result = operation()
                        results.append(result)
                    else:
                        db.session.add(operation)
                
                db.session.commit()
                
            except Exception as e:
                db.session.rollback()
                performance_logger.error(f"Batch operation failed: {str(e)}")
                raise
        
        return results
    
    @staticmethod
    def compress_json_response(data):
        """Compress JSON responses for faster transfer"""
        # Remove null values to reduce size
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if v is not None}
        elif isinstance(data, list):
            return [PerformanceMonitor.compress_json_response(item) for item in data]
        return data
    
    @staticmethod
    def get_performance_metrics():
        """Get current performance metrics"""
        return {
            'database_connections': db.engine.pool.size(),
            'active_connections': db.engine.pool.checkedout(),
            'timestamp': datetime.utcnow().isoformat()
        }


class ResponseOptimizer:
    """
    Response optimization utilities
    "We girls have no time" - Optimized responses for instant loading
    """
    
    @staticmethod
    def paginate_results(query, page=1, per_page=20, max_per_page=100):
        """Paginate query results efficiently"""
        per_page = min(per_page, max_per_page)  # Limit page size
        
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Get total count efficiently
        total = query.count()
        
        # Get paginated results
        items = query.offset(offset).limit(per_page).all()
        
        return {
            'items': [item.to_dict() if hasattr(item, 'to_dict') else item for item in items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page,
                'has_next': offset + per_page < total,
                'has_prev': page > 1
            }
        }
    
    @staticmethod
    def optimize_user_data(user_data, include_sensitive=False):
        """Optimize user data for API responses"""
        if not user_data:
            return None
        
        # Base optimized fields
        optimized = {
            'id': user_data.get('id'),
            'username': user_data.get('username'),
            'first_name': user_data.get('first_name'),
            'style_preference': user_data.get('style_preference'),
            'is_active': user_data.get('is_active', True)
        }
        
        # Add sensitive data only if requested
        if include_sensitive:
            optimized.update({
                'email': user_data.get('email'),
                'last_login': user_data.get('last_login'),
                'created_at': user_data.get('created_at')
            })
        
        return optimized
    
    @staticmethod
    def optimize_wardrobe_data(wardrobe_items):
        """Optimize wardrobe data for mobile responses"""
        if not wardrobe_items:
            return []
        
        optimized_items = []
        for item in wardrobe_items:
            optimized = {
                'id': item.get('id'),
                'name': item.get('name'),
                'category': item.get('category'),
                'primary_color': item.get('primary_color'),
                'favorite': item.get('favorite', False),
                'wear_count': item.get('wear_count', 0),
                'thumbnail_url': item.get('thumbnail_url')
            }
            optimized_items.append(optimized)
        
        return optimized_items
    
    @staticmethod
    def optimize_analytics_data(analytics_data):
        """Optimize analytics data for dashboard responses"""
        if not analytics_data:
            return {}
        
        return {
            'summary': {
                'total_sessions': analytics_data.get('total_sessions_week', 0),
                'total_time': analytics_data.get('total_time_minutes', 0),
                'personalization_score': round(analytics_data.get('personalization_score', 0), 1)
            },
            'insights_count': len(analytics_data.get('insights', [])),
            'patterns_count': len(analytics_data.get('usage_patterns', []))
        }


class CacheManager:
    """
    Simple in-memory cache for frequently accessed data
    "We girls have no time" - Cache everything that doesn't change often
    """
    
    _cache = {}
    _cache_timestamps = {}
    
    @classmethod
    def get(cls, key):
        """Get cached value if still valid"""
        if key in cls._cache:
            timestamp = cls._cache_timestamps.get(key)
            if timestamp and datetime.utcnow() - timestamp < timedelta(minutes=5):
                return cls._cache[key]
            else:
                # Remove expired cache
                cls.delete(key)
        return None
    
    @classmethod
    def set(cls, key, value, duration_minutes=5):
        """Set cache value with expiration"""
        cls._cache[key] = value
        cls._cache_timestamps[key] = datetime.utcnow()
        
        # Clean old cache entries
        cls._cleanup_cache()
    
    @classmethod
    def delete(cls, key):
        """Delete cache entry"""
        cls._cache.pop(key, None)
        cls._cache_timestamps.pop(key, None)
    
    @classmethod
    def clear(cls):
        """Clear all cache"""
        cls._cache.clear()
        cls._cache_timestamps.clear()
    
    @classmethod
    def _cleanup_cache(cls):
        """Remove expired cache entries"""
        current_time = datetime.utcnow()
        expired_keys = []
        
        for key, timestamp in cls._cache_timestamps.items():
            if current_time - timestamp > timedelta(minutes=10):  # Double the default duration
                expired_keys.append(key)
        
        for key in expired_keys:
            cls.delete(key)


class DatabaseOptimizer:
    """
    Database optimization utilities
    "We girls have no time" - Optimize every query
    """
    
    @staticmethod
    def optimize_user_queries():
        """Optimize common user-related queries"""
        # Add database indexes (would be done in migration)
        optimization_tips = {
            'indexes_needed': [
                'user.email',
                'user.username', 
                'user.created_at',
                'user_analytics.user_id',
                'user_analytics.date',
                'wardrobe_item.user_id',
                'wardrobe_item.category',
                'style_insights.user_id',
                'style_insights.expires_at',
                'security_audit_log.user_id',
                'security_audit_log.created_at'
            ],
            'query_optimizations': [
                'Use SELECT specific columns instead of SELECT *',
                'Add LIMIT clauses to prevent large result sets',
                'Use JOIN instead of multiple queries',
                'Cache frequently accessed user preferences',
                'Batch INSERT operations for analytics'
            ]
        }
        return optimization_tips
    
    @staticmethod
    def get_optimized_user_profile(user_id):
        """Get user profile with optimized queries"""
        cache_key = f"user_profile_{user_id}"
        cached_profile = CacheManager.get(cache_key)
        
        if cached_profile:
            return cached_profile
        
        # Optimized query with specific fields
        from src.models.user import User
        from src.models.profile import StyleProfile
        
        user = db.session.query(
            User.id, User.username, User.first_name, User.style_preference,
            User.is_active, User.created_at
        ).filter_by(id=user_id).first()
        
        if not user:
            return None
        
        # Get style profile if exists
        style_profile = StyleProfile.query.filter_by(user_id=user_id).first()
        
        profile_data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'style_preference': user.style_preference,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'has_style_profile': style_profile is not None,
            'profile_completion': style_profile.calculate_completion() if style_profile else 0
        }
        
        # Cache for 5 minutes
        CacheManager.set(cache_key, profile_data, 5)
        
        return profile_data
    
    @staticmethod
    def get_optimized_wardrobe_summary(user_id):
        """Get wardrobe summary with optimized queries"""
        cache_key = f"wardrobe_summary_{user_id}"
        cached_summary = CacheManager.get(cache_key)
        
        if cached_summary:
            return cached_summary
        
        from src.models.profile import WardrobeItem
        
        # Optimized aggregation query
        wardrobe_stats = db.session.query(
            WardrobeItem.category,
            db.func.count(WardrobeItem.id).label('count'),
            db.func.sum(WardrobeItem.wear_count).label('total_wears'),
            db.func.sum(db.case((WardrobeItem.favorite == True, 1), else_=0)).label('favorites')
        ).filter_by(user_id=user_id).group_by(WardrobeItem.category).all()
        
        summary = {
            'total_items': sum(stat.count for stat in wardrobe_stats),
            'total_wears': sum(stat.total_wears or 0 for stat in wardrobe_stats),
            'total_favorites': sum(stat.favorites for stat in wardrobe_stats),
            'categories': {stat.category: stat.count for stat in wardrobe_stats}
        }
        
        # Cache for 10 minutes (wardrobe changes less frequently)
        CacheManager.set(cache_key, summary, 10)
        
        return summary


class APIOptimizer:
    """
    API response optimization
    "We girls have no time" - Lightning-fast API responses
    """
    
    @staticmethod
    def create_fast_response(data, message, tagline=None, extra_data=None):
        """Create optimized API response"""
        response = {
            'message': message,
            'data': PerformanceMonitor.compress_json_response(data)
        }
        
        if tagline:
            response['tagline'] = tagline
        
        if extra_data:
            response.update(extra_data)
        
        # Add performance metadata
        response['_meta'] = {
            'response_time': f"{time.time() * 1000:.2f}ms",
            'cached': False,  # Would be set to True if from cache
            'optimized': True
        }
        
        return response
    
    @staticmethod
    def create_paginated_response(paginated_data, message, tagline=None):
        """Create optimized paginated response"""
        return {
            'message': message,
            'tagline': tagline or 'We girls have no time - here\'s your optimized data!',
            'data': paginated_data['items'],
            'pagination': paginated_data['pagination'],
            '_meta': {
                'optimized': True,
                'total_items': paginated_data['pagination']['total']
            }
        }
    
    @staticmethod
    def create_error_response(error_message, details=None):
        """Create optimized error response"""
        response = {
            'error': error_message,
            'tagline': 'We girls have no time - but something went wrong!'
        }
        
        if details:
            response['details'] = details
        
        return response


# Performance middleware
def setup_performance_monitoring(app):
    """Setup performance monitoring for Flask app"""
    
    @app.before_request
    def before_request():
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        # Add performance headers
        if hasattr(g, 'start_time'):
            duration = (time.time() - g.start_time) * 1000
            response.headers['X-Response-Time'] = f"{duration:.2f}ms"
        
        # Add cache headers for static content
        if request.endpoint and 'static' in request.endpoint:
            response.headers['Cache-Control'] = 'public, max-age=3600'
        
        # Add compression hint
        response.headers['X-Optimized'] = 'true'
        
        return response
    
    @app.route('/api/performance', methods=['GET'])
    def performance_metrics():
        """Get current performance metrics"""
        metrics = PerformanceMonitor.get_performance_metrics()
        cache_stats = {
            'cache_size': len(CacheManager._cache),
            'cache_hit_ratio': 'N/A'  # Would calculate in production
        }
        
        return {
            'message': 'Performance metrics retrieved',
            'tagline': 'We girls have no time - here\'s how fast we are!',
            'metrics': metrics,
            'cache': cache_stats,
            'optimizations': DatabaseOptimizer.optimize_user_queries()
        }

