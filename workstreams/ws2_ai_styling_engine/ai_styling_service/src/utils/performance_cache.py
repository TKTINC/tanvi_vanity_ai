import time
import json
import hashlib
from datetime import datetime, timedelta
from functools import wraps
from collections import defaultdict, OrderedDict
import threading
from typing import Dict, Any, Optional, Callable
import pickle
import os

class PerformanceCache:
    """
    Advanced caching system for AI styling engine
    "We girls have no time" - Lightning-fast AI with intelligent caching!
    """
    
    def __init__(self, max_size=1000, default_ttl=3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache = OrderedDict()
        self.access_times = {}
        self.hit_counts = defaultdict(int)
        self.miss_counts = defaultdict(int)
        self.lock = threading.RLock()
        self.start_time = time.time()
        
        # Performance metrics
        self.total_requests = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_response_time = 0.0
        self.slow_queries = []
        
    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate cache key from function name and arguments"""
        key_data = {
            'func': func_name,
            'args': args,
            'kwargs': sorted(kwargs.items()) if kwargs else {}
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _is_expired(self, entry: dict) -> bool:
        """Check if cache entry is expired"""
        if 'expires_at' not in entry:
            return False
        return datetime.utcnow() > entry['expires_at']
    
    def _evict_expired(self):
        """Remove expired entries from cache"""
        with self.lock:
            expired_keys = [
                key for key, entry in self.cache.items()
                if self._is_expired(entry)
            ]
            for key in expired_keys:
                del self.cache[key]
                if key in self.access_times:
                    del self.access_times[key]
    
    def _evict_lru(self):
        """Evict least recently used entries if cache is full"""
        with self.lock:
            while len(self.cache) >= self.max_size:
                # Remove oldest entry
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
                if oldest_key in self.access_times:
                    del self.access_times[oldest_key]
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        with self.lock:
            if key not in self.cache:
                self.cache_misses += 1
                self.miss_counts[key] += 1
                return None
            
            entry = self.cache[key]
            if self._is_expired(entry):
                del self.cache[key]
                if key in self.access_times:
                    del self.access_times[key]
                self.cache_misses += 1
                self.miss_counts[key] += 1
                return None
            
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            self.access_times[key] = time.time()
            self.cache_hits += 1
            self.hit_counts[key] += 1
            
            return entry['value']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        with self.lock:
            # Clean up expired entries
            self._evict_expired()
            
            # Evict LRU if necessary
            self._evict_lru()
            
            expires_at = None
            if ttl is not None:
                expires_at = datetime.utcnow() + timedelta(seconds=ttl)
            elif self.default_ttl:
                expires_at = datetime.utcnow() + timedelta(seconds=self.default_ttl)
            
            entry = {
                'value': value,
                'created_at': datetime.utcnow(),
                'expires_at': expires_at,
                'access_count': 0
            }
            
            self.cache[key] = entry
            self.access_times[key] = time.time()
    
    def invalidate(self, pattern: str = None) -> int:
        """Invalidate cache entries matching pattern"""
        with self.lock:
            if pattern is None:
                # Clear all
                count = len(self.cache)
                self.cache.clear()
                self.access_times.clear()
                return count
            
            # Pattern matching
            keys_to_remove = [
                key for key in self.cache.keys()
                if pattern in key
            ]
            
            for key in keys_to_remove:
                del self.cache[key]
                if key in self.access_times:
                    del self.access_times[key]
            
            return len(keys_to_remove)
    
    def get_stats(self) -> dict:
        """Get cache performance statistics"""
        with self.lock:
            total_requests = self.cache_hits + self.cache_misses
            hit_ratio = (self.cache_hits / total_requests) if total_requests > 0 else 0
            
            # Calculate average response time
            avg_response_time = (self.total_response_time / self.total_requests) if self.total_requests > 0 else 0
            
            return {
                'cache_size': len(self.cache),
                'max_size': self.max_size,
                'hit_ratio': hit_ratio,
                'cache_hits': self.cache_hits,
                'cache_misses': self.cache_misses,
                'total_requests': total_requests,
                'uptime_seconds': time.time() - self.start_time,
                'average_response_time': avg_response_time,
                'slow_queries_count': len(self.slow_queries),
                'memory_usage_estimate': len(self.cache) * 1024,  # Rough estimate
                'top_hit_keys': sorted(self.hit_counts.items(), key=lambda x: x[1], reverse=True)[:5],
                'top_miss_keys': sorted(self.miss_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            }

# Global cache instance
ai_cache = PerformanceCache(max_size=2000, default_ttl=1800)  # 30 minutes default TTL

class PerformanceMonitor:
    """
    Performance monitoring and optimization
    "We girls have no time" - Monitor and optimize every millisecond!
    """
    
    def __init__(self):
        self.request_times = []
        self.slow_threshold = 2.0  # 2 seconds
        self.slow_requests = []
        self.endpoint_stats = defaultdict(lambda: {
            'count': 0,
            'total_time': 0.0,
            'min_time': float('inf'),
            'max_time': 0.0,
            'errors': 0
        })
        self.lock = threading.RLock()
    
    def record_request(self, endpoint: str, duration: float, success: bool = True):
        """Record request performance metrics"""
        with self.lock:
            self.request_times.append(duration)
            
            # Keep only last 1000 requests
            if len(self.request_times) > 1000:
                self.request_times = self.request_times[-1000:]
            
            # Track slow requests
            if duration > self.slow_threshold:
                self.slow_requests.append({
                    'endpoint': endpoint,
                    'duration': duration,
                    'timestamp': datetime.utcnow().isoformat(),
                    'success': success
                })
                
                # Keep only last 50 slow requests
                if len(self.slow_requests) > 50:
                    self.slow_requests = self.slow_requests[-50:]
            
            # Update endpoint statistics
            stats = self.endpoint_stats[endpoint]
            stats['count'] += 1
            stats['total_time'] += duration
            stats['min_time'] = min(stats['min_time'], duration)
            stats['max_time'] = max(stats['max_time'], duration)
            
            if not success:
                stats['errors'] += 1
    
    def get_performance_stats(self) -> dict:
        """Get comprehensive performance statistics"""
        with self.lock:
            if not self.request_times:
                return {
                    'status': 'no_data',
                    'message': 'No performance data available yet'
                }
            
            # Calculate percentiles
            sorted_times = sorted(self.request_times)
            count = len(sorted_times)
            
            p50 = sorted_times[int(count * 0.5)]
            p95 = sorted_times[int(count * 0.95)]
            p99 = sorted_times[int(count * 0.99)]
            
            # Calculate endpoint averages
            endpoint_averages = {}
            for endpoint, stats in self.endpoint_stats.items():
                if stats['count'] > 0:
                    endpoint_averages[endpoint] = {
                        'average_time': stats['total_time'] / stats['count'],
                        'min_time': stats['min_time'],
                        'max_time': stats['max_time'],
                        'request_count': stats['count'],
                        'error_rate': stats['errors'] / stats['count'],
                        'success_rate': 1 - (stats['errors'] / stats['count'])
                    }
            
            return {
                'overall_performance': {
                    'average_response_time': sum(self.request_times) / len(self.request_times),
                    'median_response_time': p50,
                    'p95_response_time': p95,
                    'p99_response_time': p99,
                    'min_response_time': min(self.request_times),
                    'max_response_time': max(self.request_times),
                    'total_requests': len(self.request_times),
                    'slow_requests': len(self.slow_requests),
                    'slow_request_rate': len(self.slow_requests) / len(self.request_times)
                },
                'endpoint_performance': endpoint_averages,
                'recent_slow_requests': self.slow_requests[-10:],  # Last 10 slow requests
                'performance_grade': self._calculate_performance_grade(p95),
                'optimization_suggestions': self._get_optimization_suggestions(p95, endpoint_averages)
            }
    
    def _calculate_performance_grade(self, p95_time: float) -> str:
        """Calculate performance grade based on P95 response time"""
        if p95_time < 0.5:
            return 'A+'
        elif p95_time < 1.0:
            return 'A'
        elif p95_time < 2.0:
            return 'B'
        elif p95_time < 3.0:
            return 'C'
        else:
            return 'D'
    
    def _get_optimization_suggestions(self, p95_time: float, endpoint_stats: dict) -> list:
        """Generate optimization suggestions based on performance data"""
        suggestions = []
        
        if p95_time > 2.0:
            suggestions.append("Consider implementing more aggressive caching")
            suggestions.append("Review database query optimization")
        
        if p95_time > 1.0:
            suggestions.append("Implement response compression")
            suggestions.append("Consider async processing for heavy operations")
        
        # Check for slow endpoints
        slow_endpoints = [
            endpoint for endpoint, stats in endpoint_stats.items()
            if stats['average_time'] > 1.5
        ]
        
        if slow_endpoints:
            suggestions.append(f"Optimize slow endpoints: {', '.join(slow_endpoints)}")
        
        # Check error rates
        high_error_endpoints = [
            endpoint for endpoint, stats in endpoint_stats.items()
            if stats['error_rate'] > 0.05  # 5% error rate
        ]
        
        if high_error_endpoints:
            suggestions.append(f"Investigate high error rates in: {', '.join(high_error_endpoints)}")
        
        return suggestions

# Global performance monitor
performance_monitor = PerformanceMonitor()

def cached(ttl: int = 1800, key_prefix: str = ""):
    """
    Decorator for caching function results
    "We girls have no time" - Cache everything for speed!
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            func_name = f"{key_prefix}{func.__name__}" if key_prefix else func.__name__
            cache_key = ai_cache._generate_key(func_name, args, kwargs)
            
            # Try to get from cache
            cached_result = ai_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                ai_cache.set(cache_key, result, ttl)
                return result
            finally:
                duration = time.time() - start_time
                performance_monitor.record_request(func_name, duration, True)
        
        return wrapper
    return decorator

def performance_tracked(endpoint_name: str = None):
    """
    Decorator for tracking performance metrics
    "We girls have no time" - Track every millisecond!
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                raise
            finally:
                duration = time.time() - start_time
                name = endpoint_name or func.__name__
                performance_monitor.record_request(name, duration, success)
        
        return wrapper
    return decorator

class ResponseOptimizer:
    """
    Response optimization utilities
    "We girls have no time" - Optimize every byte!
    """
    
    @staticmethod
    def compress_response(data: dict, compression_level: str = 'medium') -> dict:
        """Compress response data for faster transfer"""
        if compression_level == 'high':
            # Aggressive compression - remove optional fields
            return ResponseOptimizer._aggressive_compress(data)
        elif compression_level == 'medium':
            # Moderate compression - optimize field names and values
            return ResponseOptimizer._moderate_compress(data)
        else:
            # Light compression - just clean up
            return ResponseOptimizer._light_compress(data)
    
    @staticmethod
    def _aggressive_compress(data: dict) -> dict:
        """Aggressive compression - remove non-essential data"""
        if isinstance(data, dict):
            compressed = {}
            
            # Essential fields to keep
            essential_fields = {
                'status', 'message', 'data', 'results', 'recommendations',
                'outfit', 'style', 'confidence', 'score', 'items', 'id',
                'name', 'category', 'color', 'occasion', 'weather'
            }
            
            for key, value in data.items():
                if key in essential_fields or key.endswith('_score') or key.endswith('_id'):
                    if isinstance(value, (dict, list)):
                        compressed[key] = ResponseOptimizer._aggressive_compress(value)
                    else:
                        compressed[key] = value
            
            return compressed
        elif isinstance(data, list):
            return [ResponseOptimizer._aggressive_compress(item) for item in data]
        else:
            return data
    
    @staticmethod
    def _moderate_compress(data: dict) -> dict:
        """Moderate compression - optimize field names and values"""
        if isinstance(data, dict):
            compressed = {}
            
            # Field name mappings for shorter names
            field_mappings = {
                'recommendation': 'rec',
                'confidence_score': 'conf',
                'compatibility': 'compat',
                'description': 'desc',
                'suggestions': 'sugg',
                'analysis_date': 'date',
                'created_at': 'created',
                'updated_at': 'updated'
            }
            
            for key, value in data.items():
                # Use shorter field name if available
                short_key = field_mappings.get(key, key)
                
                if isinstance(value, (dict, list)):
                    compressed[short_key] = ResponseOptimizer._moderate_compress(value)
                elif isinstance(value, str) and len(value) > 100:
                    # Truncate very long strings
                    compressed[short_key] = value[:100] + "..."
                else:
                    compressed[short_key] = value
            
            return compressed
        elif isinstance(data, list):
            return [ResponseOptimizer._moderate_compress(item) for item in data]
        else:
            return data
    
    @staticmethod
    def _light_compress(data: dict) -> dict:
        """Light compression - just clean up"""
        if isinstance(data, dict):
            compressed = {}
            
            for key, value in data.items():
                if value is not None and value != "":
                    if isinstance(value, (dict, list)):
                        compressed_value = ResponseOptimizer._light_compress(value)
                        if compressed_value:  # Only include non-empty structures
                            compressed[key] = compressed_value
                    else:
                        compressed[key] = value
            
            return compressed
        elif isinstance(data, list):
            return [ResponseOptimizer._light_compress(item) for item in data if item]
        else:
            return data
    
    @staticmethod
    def paginate_response(data: list, page: int = 1, per_page: int = 20) -> dict:
        """Paginate large response data"""
        total_items = len(data)
        total_pages = (total_items + per_page - 1) // per_page
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_data = data[start_idx:end_idx]
        
        return {
            'data': paginated_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_items': total_items,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1,
                'next_page': page + 1 if page < total_pages else None,
                'prev_page': page - 1 if page > 1 else None
            }
        }

class AIModelCache:
    """
    Specialized caching for AI model results
    "We girls have no time" - Cache AI intelligence!
    """
    
    def __init__(self):
        self.style_analysis_cache = {}
        self.outfit_recommendation_cache = {}
        self.trend_forecast_cache = {}
        self.wardrobe_optimization_cache = {}
        
        # Cache TTLs (in seconds)
        self.cache_ttls = {
            'style_analysis': 3600,      # 1 hour
            'outfit_recommendation': 1800, # 30 minutes
            'trend_forecast': 86400,     # 24 hours
            'wardrobe_optimization': 7200, # 2 hours
            'style_compatibility': 3600,  # 1 hour
            'predictive_recommendations': 1800  # 30 minutes
        }
    
    def get_style_analysis(self, user_id: int, style_data_hash: str) -> Optional[dict]:
        """Get cached style analysis"""
        cache_key = f"{user_id}_{style_data_hash}"
        return self._get_cached_result('style_analysis', cache_key)
    
    def set_style_analysis(self, user_id: int, style_data_hash: str, result: dict):
        """Cache style analysis result"""
        cache_key = f"{user_id}_{style_data_hash}"
        self._set_cached_result('style_analysis', cache_key, result)
    
    def get_outfit_recommendation(self, user_id: int, context_hash: str) -> Optional[dict]:
        """Get cached outfit recommendation"""
        cache_key = f"{user_id}_{context_hash}"
        return self._get_cached_result('outfit_recommendation', cache_key)
    
    def set_outfit_recommendation(self, user_id: int, context_hash: str, result: dict):
        """Cache outfit recommendation result"""
        cache_key = f"{user_id}_{context_hash}"
        self._set_cached_result('outfit_recommendation', cache_key, result)
    
    def get_trend_forecast(self, forecast_type: str) -> Optional[dict]:
        """Get cached trend forecast"""
        return self._get_cached_result('trend_forecast', forecast_type)
    
    def set_trend_forecast(self, forecast_type: str, result: dict):
        """Cache trend forecast result"""
        self._set_cached_result('trend_forecast', forecast_type, result)
    
    def get_wardrobe_optimization(self, user_id: int, wardrobe_hash: str) -> Optional[dict]:
        """Get cached wardrobe optimization"""
        cache_key = f"{user_id}_{wardrobe_hash}"
        return self._get_cached_result('wardrobe_optimization', cache_key)
    
    def set_wardrobe_optimization(self, user_id: int, wardrobe_hash: str, result: dict):
        """Cache wardrobe optimization result"""
        cache_key = f"{user_id}_{wardrobe_hash}"
        self._set_cached_result('wardrobe_optimization', cache_key, result)
    
    def _get_cached_result(self, cache_type: str, key: str) -> Optional[dict]:
        """Get result from specific cache"""
        cache = getattr(self, f"{cache_type}_cache", {})
        
        if key not in cache:
            return None
        
        entry = cache[key]
        if self._is_expired(entry, cache_type):
            del cache[key]
            return None
        
        return entry['result']
    
    def _set_cached_result(self, cache_type: str, key: str, result: dict):
        """Set result in specific cache"""
        cache = getattr(self, f"{cache_type}_cache", {})
        ttl = self.cache_ttls.get(cache_type, 1800)
        
        cache[key] = {
            'result': result,
            'cached_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(seconds=ttl)
        }
    
    def _is_expired(self, entry: dict, cache_type: str) -> bool:
        """Check if cache entry is expired"""
        return datetime.utcnow() > entry['expires_at']
    
    def invalidate_user_cache(self, user_id: int):
        """Invalidate all cache entries for a specific user"""
        caches = [
            self.style_analysis_cache,
            self.outfit_recommendation_cache,
            self.wardrobe_optimization_cache
        ]
        
        for cache in caches:
            keys_to_remove = [
                key for key in cache.keys()
                if key.startswith(f"{user_id}_")
            ]
            for key in keys_to_remove:
                del cache[key]
    
    def get_cache_stats(self) -> dict:
        """Get AI model cache statistics"""
        stats = {}
        
        for cache_type in ['style_analysis', 'outfit_recommendation', 'trend_forecast', 'wardrobe_optimization']:
            cache = getattr(self, f"{cache_type}_cache", {})
            
            # Count expired entries
            expired_count = sum(
                1 for entry in cache.values()
                if self._is_expired(entry, cache_type)
            )
            
            stats[cache_type] = {
                'total_entries': len(cache),
                'expired_entries': expired_count,
                'active_entries': len(cache) - expired_count,
                'cache_ttl': self.cache_ttls.get(cache_type, 1800)
            }
        
        return stats

# Global AI model cache
ai_model_cache = AIModelCache()

