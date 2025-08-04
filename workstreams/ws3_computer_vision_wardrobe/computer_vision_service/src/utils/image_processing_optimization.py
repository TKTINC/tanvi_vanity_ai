"""
WS3-P5: Performance Optimization & Image Processing
Image Processing Optimization Utilities for Tanvi Vanity Agent
"We girls have no time" - Lightning-fast image processing for instant results!
"""

import time
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import threading
from collections import OrderedDict

class ImageProcessingCache:
    """
    High-performance image processing cache
    "We girls have no time" - Instant image analysis results!
    """
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache = OrderedDict()
        self.access_times = {}
        self.hit_count = 0
        self.miss_count = 0
        self.lock = threading.RLock()
    
    def _generate_key(self, image_path: str, analysis_type: str, params: Dict = None) -> str:
        """Generate cache key for image analysis"""
        key_data = {
            'image_path': image_path,
            'analysis_type': analysis_type,
            'params': params or {}
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _is_expired(self, timestamp: datetime) -> bool:
        """Check if cache entry is expired"""
        return datetime.utcnow() - timestamp > timedelta(seconds=self.ttl_seconds)
    
    def _cleanup_expired(self):
        """Remove expired entries"""
        current_time = datetime.utcnow()
        expired_keys = [
            key for key, (_, timestamp) in self.cache.items()
            if self._is_expired(timestamp)
        ]
        for key in expired_keys:
            del self.cache[key]
            if key in self.access_times:
                del self.access_times[key]
    
    def get(self, image_path: str, analysis_type: str, params: Dict = None) -> Optional[Any]:
        """Get cached analysis result"""
        with self.lock:
            key = self._generate_key(image_path, analysis_type, params)
            
            if key in self.cache:
                result, timestamp = self.cache[key]
                if not self._is_expired(timestamp):
                    # Move to end (most recently used)
                    self.cache.move_to_end(key)
                    self.access_times[key] = datetime.utcnow()
                    self.hit_count += 1
                    return result
                else:
                    # Remove expired entry
                    del self.cache[key]
                    if key in self.access_times:
                        del self.access_times[key]
            
            self.miss_count += 1
            return None
    
    def set(self, image_path: str, analysis_type: str, result: Any, params: Dict = None):
        """Cache analysis result"""
        with self.lock:
            key = self._generate_key(image_path, analysis_type, params)
            current_time = datetime.utcnow()
            
            # Remove oldest entries if cache is full
            while len(self.cache) >= self.max_size:
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
                if oldest_key in self.access_times:
                    del self.access_times[oldest_key]
            
            self.cache[key] = (result, current_time)
            self.access_times[key] = current_time
            
            # Periodic cleanup
            if len(self.cache) % 100 == 0:
                self._cleanup_expired()
    
    def invalidate_pattern(self, pattern: str):
        """Invalidate cache entries matching pattern"""
        with self.lock:
            keys_to_remove = [
                key for key in self.cache.keys()
                if pattern in key
            ]
            for key in keys_to_remove:
                del self.cache[key]
                if key in self.access_times:
                    del self.access_times[key]
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        with self.lock:
            total_requests = self.hit_count + self.miss_count
            hit_ratio = self.hit_count / total_requests if total_requests > 0 else 0
            
            return {
                'cache_size': len(self.cache),
                'max_size': self.max_size,
                'hit_count': self.hit_count,
                'miss_count': self.miss_count,
                'hit_ratio': hit_ratio,
                'ttl_seconds': self.ttl_seconds
            }
    
    def clear(self):
        """Clear all cache entries"""
        with self.lock:
            self.cache.clear()
            self.access_times.clear()
            self.hit_count = 0
            self.miss_count = 0

class ImageProcessingOptimizer:
    """
    Image processing performance optimizer
    "We girls have no time" - Optimized image processing for instant results!
    """
    
    def __init__(self):
        self.processing_times = []
        self.optimization_stats = {
            'total_processed': 0,
            'total_time': 0.0,
            'average_time': 0.0,
            'fastest_time': float('inf'),
            'slowest_time': 0.0
        }
        self.lock = threading.RLock()
    
    def optimize_image_size(self, image_path: str, target_size: Tuple[int, int] = (512, 512)) -> Dict:
        """
        Optimize image size for processing
        "We girls have no time" - Instant image optimization!
        """
        start_time = time.time()
        
        # Mock image optimization
        optimization_result = {
            'original_size': (1920, 1080),
            'optimized_size': target_size,
            'compression_ratio': 0.25,
            'size_reduction': '75%',
            'quality_retained': '95%',
            'processing_time': time.time() - start_time
        }
        
        return optimization_result
    
    def batch_optimize_images(self, image_paths: List[str], target_size: Tuple[int, int] = (512, 512)) -> Dict:
        """
        Batch optimize multiple images
        "We girls have no time" - Batch optimization for efficiency!
        """
        start_time = time.time()
        
        results = []
        for image_path in image_paths:
            result = self.optimize_image_size(image_path, target_size)
            results.append(result)
        
        total_time = time.time() - start_time
        
        return {
            'batch_size': len(image_paths),
            'total_processing_time': total_time,
            'average_time_per_image': total_time / len(image_paths) if image_paths else 0,
            'results': results,
            'efficiency_gain': f"{(len(image_paths) * 0.5 - total_time) / (len(image_paths) * 0.5) * 100:.1f}%"
        }
    
    def preprocess_for_analysis(self, image_path: str, analysis_type: str) -> Dict:
        """
        Preprocess image for specific analysis type
        "We girls have no time" - Optimized preprocessing for instant analysis!
        """
        start_time = time.time()
        
        # Mock preprocessing based on analysis type
        preprocessing_configs = {
            'color_analysis': {
                'resize': (256, 256),
                'color_space': 'RGB',
                'enhancement': 'color_boost',
                'processing_time': 0.3
            },
            'pattern_recognition': {
                'resize': (512, 512),
                'color_space': 'Grayscale',
                'enhancement': 'edge_detection',
                'processing_time': 0.5
            },
            'style_analysis': {
                'resize': (384, 384),
                'color_space': 'RGB',
                'enhancement': 'contrast_boost',
                'processing_time': 0.4
            },
            'similarity_analysis': {
                'resize': (224, 224),
                'color_space': 'RGB',
                'enhancement': 'normalization',
                'processing_time': 0.2
            }
        }
        
        config = preprocessing_configs.get(analysis_type, preprocessing_configs['style_analysis'])
        time.sleep(config['processing_time'])  # Simulate processing
        
        result = {
            'analysis_type': analysis_type,
            'preprocessing_config': config,
            'optimized_for_analysis': True,
            'processing_time': time.time() - start_time,
            'quality_score': 0.95
        }
        
        return result
    
    def track_processing_time(self, processing_time: float):
        """Track processing time for optimization"""
        with self.lock:
            self.processing_times.append(processing_time)
            
            # Keep only last 1000 entries
            if len(self.processing_times) > 1000:
                self.processing_times = self.processing_times[-1000:]
            
            # Update stats
            self.optimization_stats['total_processed'] += 1
            self.optimization_stats['total_time'] += processing_time
            self.optimization_stats['average_time'] = (
                self.optimization_stats['total_time'] / self.optimization_stats['total_processed']
            )
            self.optimization_stats['fastest_time'] = min(
                self.optimization_stats['fastest_time'], processing_time
            )
            self.optimization_stats['slowest_time'] = max(
                self.optimization_stats['slowest_time'], processing_time
            )
    
    def get_optimization_recommendations(self) -> List[str]:
        """Get optimization recommendations based on performance data"""
        recommendations = []
        
        if self.optimization_stats['average_time'] > 2.0:
            recommendations.append("Consider reducing image resolution for faster processing")
        
        if len(self.processing_times) > 10:
            recent_avg = sum(self.processing_times[-10:]) / 10
            if recent_avg > self.optimization_stats['average_time'] * 1.2:
                recommendations.append("Recent processing times are slower - check system resources")
        
        if self.optimization_stats['slowest_time'] > 5.0:
            recommendations.append("Some images take very long to process - implement timeout handling")
        
        if not recommendations:
            recommendations.append("Performance is optimal - no recommendations needed")
        
        return recommendations
    
    def get_performance_stats(self) -> Dict:
        """Get comprehensive performance statistics"""
        with self.lock:
            return {
                'processing_stats': self.optimization_stats.copy(),
                'recent_times': self.processing_times[-10:] if self.processing_times else [],
                'recommendations': self.get_optimization_recommendations(),
                'performance_grade': self._calculate_performance_grade()
            }
    
    def _calculate_performance_grade(self) -> str:
        """Calculate performance grade based on metrics"""
        avg_time = self.optimization_stats['average_time']
        
        if avg_time < 1.0:
            return 'A+'
        elif avg_time < 1.5:
            return 'A'
        elif avg_time < 2.0:
            return 'B+'
        elif avg_time < 3.0:
            return 'B'
        elif avg_time < 4.0:
            return 'C+'
        else:
            return 'C'

class PerformanceMonitor:
    """
    Comprehensive performance monitoring for image processing
    "We girls have no time" - Real-time performance insights!
    """
    
    def __init__(self):
        self.metrics = {
            'requests_processed': 0,
            'total_processing_time': 0.0,
            'cache_hits': 0,
            'cache_misses': 0,
            'errors': 0,
            'slow_requests': 0  # > 3 seconds
        }
        self.request_times = []
        self.error_log = []
        self.lock = threading.RLock()
    
    def record_request(self, processing_time: float, cache_hit: bool = False, error: bool = False):
        """Record request metrics"""
        with self.lock:
            self.metrics['requests_processed'] += 1
            self.metrics['total_processing_time'] += processing_time
            
            if cache_hit:
                self.metrics['cache_hits'] += 1
            else:
                self.metrics['cache_misses'] += 1
            
            if error:
                self.metrics['errors'] += 1
                self.error_log.append({
                    'timestamp': datetime.utcnow().isoformat(),
                    'processing_time': processing_time
                })
            
            if processing_time > 3.0:
                self.metrics['slow_requests'] += 1
            
            self.request_times.append(processing_time)
            
            # Keep only last 1000 requests
            if len(self.request_times) > 1000:
                self.request_times = self.request_times[-1000:]
            
            # Keep only last 100 errors
            if len(self.error_log) > 100:
                self.error_log = self.error_log[-100:]
    
    def get_performance_metrics(self) -> Dict:
        """Get comprehensive performance metrics"""
        with self.lock:
            if not self.request_times:
                return {
                    'status': 'no_data',
                    'message': 'No requests processed yet'
                }
            
            # Calculate percentiles
            sorted_times = sorted(self.request_times)
            n = len(sorted_times)
            
            p50 = sorted_times[int(n * 0.5)]
            p95 = sorted_times[int(n * 0.95)]
            p99 = sorted_times[int(n * 0.99)]
            
            avg_time = self.metrics['total_processing_time'] / self.metrics['requests_processed']
            cache_hit_ratio = self.metrics['cache_hits'] / (self.metrics['cache_hits'] + self.metrics['cache_misses'])
            error_rate = self.metrics['errors'] / self.metrics['requests_processed']
            
            return {
                'summary': {
                    'total_requests': self.metrics['requests_processed'],
                    'average_time': avg_time,
                    'cache_hit_ratio': cache_hit_ratio,
                    'error_rate': error_rate,
                    'slow_request_rate': self.metrics['slow_requests'] / self.metrics['requests_processed']
                },
                'response_times': {
                    'p50': p50,
                    'p95': p95,
                    'p99': p99,
                    'min': min(sorted_times),
                    'max': max(sorted_times)
                },
                'performance_grade': self._calculate_grade(avg_time, error_rate),
                'recommendations': self._get_recommendations(avg_time, cache_hit_ratio, error_rate),
                'recent_errors': self.error_log[-5:] if self.error_log else []
            }
    
    def _calculate_grade(self, avg_time: float, error_rate: float) -> str:
        """Calculate overall performance grade"""
        if error_rate > 0.05:  # > 5% error rate
            return 'D'
        elif avg_time < 1.0 and error_rate < 0.01:
            return 'A+'
        elif avg_time < 1.5 and error_rate < 0.02:
            return 'A'
        elif avg_time < 2.0 and error_rate < 0.03:
            return 'B+'
        elif avg_time < 3.0 and error_rate < 0.04:
            return 'B'
        else:
            return 'C'
    
    def _get_recommendations(self, avg_time: float, cache_hit_ratio: float, error_rate: float) -> List[str]:
        """Get performance recommendations"""
        recommendations = []
        
        if avg_time > 2.0:
            recommendations.append("Average response time is high - consider image optimization")
        
        if cache_hit_ratio < 0.7:
            recommendations.append("Cache hit ratio is low - review caching strategy")
        
        if error_rate > 0.02:
            recommendations.append("Error rate is elevated - investigate error causes")
        
        if self.metrics['slow_requests'] / self.metrics['requests_processed'] > 0.1:
            recommendations.append("High percentage of slow requests - implement timeout handling")
        
        if not recommendations:
            recommendations.append("Performance is excellent - no improvements needed")
        
        return recommendations

# Global instances
image_cache = ImageProcessingCache(max_size=1000, ttl_seconds=3600)
image_optimizer = ImageProcessingOptimizer()
performance_monitor = PerformanceMonitor()

def optimize_image_processing(func):
    """
    Decorator for optimizing image processing functions
    "We girls have no time" - Automatic optimization for all image processing!
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        cache_hit = False
        error = False
        
        try:
            # Try to get from cache first
            if 'image_path' in kwargs:
                cached_result = image_cache.get(
                    kwargs['image_path'], 
                    func.__name__, 
                    kwargs.get('params')
                )
                if cached_result is not None:
                    cache_hit = True
                    processing_time = time.time() - start_time
                    performance_monitor.record_request(processing_time, cache_hit)
                    return cached_result
            
            # Process and cache result
            result = func(*args, **kwargs)
            
            if 'image_path' in kwargs:
                image_cache.set(
                    kwargs['image_path'], 
                    func.__name__, 
                    result, 
                    kwargs.get('params')
                )
            
        except Exception as e:
            error = True
            raise e
        finally:
            processing_time = time.time() - start_time
            image_optimizer.track_processing_time(processing_time)
            performance_monitor.record_request(processing_time, cache_hit, error)
        
        return result
    
    return wrapper

