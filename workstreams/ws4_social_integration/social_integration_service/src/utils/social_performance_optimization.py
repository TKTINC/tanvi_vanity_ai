"""
WS4-P5: Social Performance Optimization & Analytics Utilities
Tanvi Vanity Agent - Social Integration System
"We girls have no time" - Lightning-fast social performance!
"""

import time
import json
import hashlib
from datetime import datetime, timedelta
from collections import defaultdict, OrderedDict
from typing import Dict, List, Any, Optional
import threading

class SocialPerformanceCache:
    """High-performance caching system for social data"""
    
    def __init__(self, max_size: int = 10000, default_ttl: int = 300):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache = OrderedDict()
        self.expiry_times = {}
        self.hit_count = 0
        self.miss_count = 0
        self.lock = threading.RLock()
        
    def _generate_key(self, prefix: str, **kwargs) -> str:
        """Generate cache key from parameters"""
        key_data = f"{prefix}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _is_expired(self, key: str) -> bool:
        """Check if cache entry is expired"""
        if key not in self.expiry_times:
            return True
        return datetime.utcnow() > self.expiry_times[key]
    
    def _cleanup_expired(self):
        """Remove expired entries"""
        current_time = datetime.utcnow()
        expired_keys = [
            key for key, expiry in self.expiry_times.items()
            if current_time > expiry
        ]
        for key in expired_keys:
            self.cache.pop(key, None)
            self.expiry_times.pop(key, None)
    
    def get(self, prefix: str, **kwargs) -> Optional[Any]:
        """Get cached data"""
        with self.lock:
            key = self._generate_key(prefix, **kwargs)
            
            if key in self.cache and not self._is_expired(key):
                # Move to end (LRU)
                self.cache.move_to_end(key)
                self.hit_count += 1
                return self.cache[key]
            
            self.miss_count += 1
            return None
    
    def set(self, prefix: str, data: Any, ttl: Optional[int] = None, **kwargs):
        """Set cached data"""
        with self.lock:
            key = self._generate_key(prefix, **kwargs)
            ttl = ttl or self.default_ttl
            
            # Remove oldest entries if at capacity
            while len(self.cache) >= self.max_size:
                oldest_key = next(iter(self.cache))
                self.cache.pop(oldest_key)
                self.expiry_times.pop(oldest_key, None)
            
            self.cache[key] = data
            self.expiry_times[key] = datetime.utcnow() + timedelta(seconds=ttl)
            
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
                self.cache.pop(key, None)
                self.expiry_times.pop(key, None)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self.lock:
            total_requests = self.hit_count + self.miss_count
            hit_ratio = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'cache_size': len(self.cache),
                'max_size': self.max_size,
                'hit_count': self.hit_count,
                'miss_count': self.miss_count,
                'hit_ratio': round(hit_ratio, 2),
                'expired_entries': len([
                    key for key in self.expiry_times.keys()
                    if self._is_expired(key)
                ])
            }

class SocialAnalyticsEngine:
    """Advanced social analytics and metrics tracking"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.user_analytics = defaultdict(dict)
        self.content_analytics = defaultdict(dict)
        self.engagement_patterns = defaultdict(list)
        self.lock = threading.RLock()
    
    def track_user_activity(self, user_id: str, activity_type: str, metadata: Dict[str, Any] = None):
        """Track user activity for analytics"""
        with self.lock:
            activity_data = {
                'user_id': user_id,
                'activity_type': activity_type,
                'metadata': metadata or {},
                'timestamp': datetime.utcnow().isoformat(),
                'hour_of_day': datetime.utcnow().hour,
                'day_of_week': datetime.utcnow().weekday()
            }
            
            self.metrics['user_activities'].append(activity_data)
            
            # Update user analytics
            if user_id not in self.user_analytics:
                self.user_analytics[user_id] = {
                    'total_activities': 0,
                    'activity_types': defaultdict(int),
                    'peak_hours': defaultdict(int),
                    'engagement_score': 0.0,
                    'last_active': None
                }
            
            user_stats = self.user_analytics[user_id]
            user_stats['total_activities'] += 1
            user_stats['activity_types'][activity_type] += 1
            user_stats['peak_hours'][activity_data['hour_of_day']] += 1
            user_stats['last_active'] = activity_data['timestamp']
    
    def track_content_engagement(self, content_id: str, engagement_type: str, user_id: str, metadata: Dict[str, Any] = None):
        """Track content engagement for analytics"""
        with self.lock:
            engagement_data = {
                'content_id': content_id,
                'engagement_type': engagement_type,
                'user_id': user_id,
                'metadata': metadata or {},
                'timestamp': datetime.utcnow().isoformat()
            }
            
            self.metrics['content_engagements'].append(engagement_data)
            self.engagement_patterns[content_id].append(engagement_data)
            
            # Update content analytics
            if content_id not in self.content_analytics:
                self.content_analytics[content_id] = {
                    'total_engagements': 0,
                    'engagement_types': defaultdict(int),
                    'unique_users': set(),
                    'engagement_rate': 0.0,
                    'viral_score': 0.0
                }
            
            content_stats = self.content_analytics[content_id]
            content_stats['total_engagements'] += 1
            content_stats['engagement_types'][engagement_type] += 1
            content_stats['unique_users'].add(user_id)
    
    def calculate_engagement_score(self, user_id: str) -> float:
        """Calculate user engagement score"""
        if user_id not in self.user_analytics:
            return 0.0
        
        user_stats = self.user_analytics[user_id]
        
        # Base score from activity count
        activity_score = min(user_stats['total_activities'] / 100, 1.0) * 40
        
        # Diversity score from activity types
        diversity_score = min(len(user_stats['activity_types']) / 10, 1.0) * 30
        
        # Consistency score from regular activity
        peak_hour_count = max(user_stats['peak_hours'].values()) if user_stats['peak_hours'] else 0
        consistency_score = min(peak_hour_count / 20, 1.0) * 30
        
        total_score = activity_score + diversity_score + consistency_score
        
        # Update cached score
        self.user_analytics[user_id]['engagement_score'] = round(total_score, 2)
        
        return round(total_score, 2)
    
    def calculate_viral_score(self, content_id: str) -> float:
        """Calculate content viral score"""
        if content_id not in self.content_analytics:
            return 0.0
        
        content_stats = self.content_analytics[content_id]
        
        # Base score from total engagements
        engagement_score = min(content_stats['total_engagements'] / 1000, 1.0) * 40
        
        # Reach score from unique users
        reach_score = min(len(content_stats['unique_users']) / 500, 1.0) * 35
        
        # Diversity score from engagement types
        diversity_score = min(len(content_stats['engagement_types']) / 5, 1.0) * 25
        
        total_score = engagement_score + reach_score + diversity_score
        
        # Update cached score
        self.content_analytics[content_id]['viral_score'] = round(total_score, 2)
        
        return round(total_score, 2)
    
    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user insights"""
        if user_id not in self.user_analytics:
            return {'error': 'User not found in analytics'}
        
        user_stats = self.user_analytics[user_id]
        engagement_score = self.calculate_engagement_score(user_id)
        
        # Find peak activity hour
        peak_hour = max(user_stats['peak_hours'].items(), key=lambda x: x[1])[0] if user_stats['peak_hours'] else 0
        
        # Activity patterns
        activity_patterns = []
        for activity_type, count in user_stats['activity_types'].items():
            percentage = (count / user_stats['total_activities']) * 100
            activity_patterns.append({
                'activity_type': activity_type,
                'count': count,
                'percentage': round(percentage, 1)
            })
        
        return {
            'user_id': user_id,
            'engagement_score': engagement_score,
            'total_activities': user_stats['total_activities'],
            'peak_activity_hour': f"{peak_hour}:00",
            'activity_patterns': sorted(activity_patterns, key=lambda x: x['count'], reverse=True),
            'last_active': user_stats['last_active'],
            'engagement_level': self._get_engagement_level(engagement_score),
            'recommendations': self._get_user_recommendations(user_stats, engagement_score)
        }
    
    def get_content_insights(self, content_id: str) -> Dict[str, Any]:
        """Get comprehensive content insights"""
        if content_id not in self.content_analytics:
            return {'error': 'Content not found in analytics'}
        
        content_stats = self.content_analytics[content_id]
        viral_score = self.calculate_viral_score(content_id)
        
        # Engagement breakdown
        engagement_breakdown = []
        for engagement_type, count in content_stats['engagement_types'].items():
            percentage = (count / content_stats['total_engagements']) * 100
            engagement_breakdown.append({
                'engagement_type': engagement_type,
                'count': count,
                'percentage': round(percentage, 1)
            })
        
        # Calculate engagement rate
        unique_users_count = len(content_stats['unique_users'])
        engagement_rate = (content_stats['total_engagements'] / max(unique_users_count, 1)) * 100
        
        return {
            'content_id': content_id,
            'viral_score': viral_score,
            'total_engagements': content_stats['total_engagements'],
            'unique_users': unique_users_count,
            'engagement_rate': round(engagement_rate, 2),
            'engagement_breakdown': sorted(engagement_breakdown, key=lambda x: x['count'], reverse=True),
            'viral_level': self._get_viral_level(viral_score),
            'performance_insights': self._get_content_recommendations(content_stats, viral_score)
        }
    
    def get_platform_analytics(self) -> Dict[str, Any]:
        """Get overall platform analytics"""
        with self.lock:
            total_users = len(self.user_analytics)
            total_content = len(self.content_analytics)
            total_activities = len(self.metrics['user_activities'])
            total_engagements = len(self.metrics['content_engagements'])
            
            # Calculate averages
            avg_engagement_score = 0.0
            if total_users > 0:
                total_engagement = sum(
                    self.calculate_engagement_score(user_id)
                    for user_id in self.user_analytics.keys()
                )
                avg_engagement_score = total_engagement / total_users
            
            avg_viral_score = 0.0
            if total_content > 0:
                total_viral = sum(
                    self.calculate_viral_score(content_id)
                    for content_id in self.content_analytics.keys()
                )
                avg_viral_score = total_viral / total_content
            
            return {
                'platform_overview': {
                    'total_users': total_users,
                    'total_content': total_content,
                    'total_activities': total_activities,
                    'total_engagements': total_engagements
                },
                'performance_metrics': {
                    'avg_engagement_score': round(avg_engagement_score, 2),
                    'avg_viral_score': round(avg_viral_score, 2),
                    'activity_per_user': round(total_activities / max(total_users, 1), 2),
                    'engagement_per_content': round(total_engagements / max(total_content, 1), 2)
                },
                'growth_insights': {
                    'active_users_24h': self._count_recent_users(24),
                    'new_content_24h': self._count_recent_content(24),
                    'trending_activities': self._get_trending_activities(),
                    'top_engagement_types': self._get_top_engagement_types()
                }
            }
    
    def _get_engagement_level(self, score: float) -> str:
        """Get engagement level description"""
        if score >= 80:
            return 'Highly Engaged'
        elif score >= 60:
            return 'Engaged'
        elif score >= 40:
            return 'Moderately Engaged'
        elif score >= 20:
            return 'Low Engagement'
        else:
            return 'Inactive'
    
    def _get_viral_level(self, score: float) -> str:
        """Get viral level description"""
        if score >= 80:
            return 'Viral'
        elif score >= 60:
            return 'High Performance'
        elif score >= 40:
            return 'Good Performance'
        elif score >= 20:
            return 'Average Performance'
        else:
            return 'Low Performance'
    
    def _get_user_recommendations(self, user_stats: Dict, engagement_score: float) -> List[str]:
        """Get personalized user recommendations"""
        recommendations = []
        
        if engagement_score < 40:
            recommendations.append("Try posting more style content to increase engagement")
            recommendations.append("Follow more users with similar style preferences")
        
        if len(user_stats['activity_types']) < 3:
            recommendations.append("Explore different types of activities (posts, comments, likes)")
        
        if user_stats['total_activities'] < 10:
            recommendations.append("Stay active with daily style interactions")
        
        return recommendations
    
    def _get_content_recommendations(self, content_stats: Dict, viral_score: float) -> List[str]:
        """Get content performance recommendations"""
        recommendations = []
        
        if viral_score < 40:
            recommendations.append("Add trending hashtags to increase discoverability")
            recommendations.append("Post during peak engagement hours")
        
        if len(content_stats['engagement_types']) < 3:
            recommendations.append("Encourage diverse engagement (likes, comments, shares)")
        
        if len(content_stats['unique_users']) < 50:
            recommendations.append("Share in relevant style communities")
        
        return recommendations
    
    def _count_recent_users(self, hours: int) -> int:
        """Count users active in recent hours"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        recent_users = set()
        
        for activity in self.metrics['user_activities']:
            activity_time = datetime.fromisoformat(activity['timestamp'])
            if activity_time > cutoff_time:
                recent_users.add(activity['user_id'])
        
        return len(recent_users)
    
    def _count_recent_content(self, hours: int) -> int:
        """Count content created in recent hours"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        recent_content = set()
        
        for engagement in self.metrics['content_engagements']:
            engagement_time = datetime.fromisoformat(engagement['timestamp'])
            if engagement_time > cutoff_time:
                recent_content.add(engagement['content_id'])
        
        return len(recent_content)
    
    def _get_trending_activities(self) -> List[Dict[str, Any]]:
        """Get trending activity types"""
        activity_counts = defaultdict(int)
        
        # Count activities in last 24 hours
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        for activity in self.metrics['user_activities']:
            activity_time = datetime.fromisoformat(activity['timestamp'])
            if activity_time > cutoff_time:
                activity_counts[activity['activity_type']] += 1
        
        # Sort by count and return top 5
        trending = sorted(activity_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return [
            {'activity_type': activity_type, 'count': count}
            for activity_type, count in trending
        ]
    
    def _get_top_engagement_types(self) -> List[Dict[str, Any]]:
        """Get top engagement types"""
        engagement_counts = defaultdict(int)
        
        # Count engagements in last 24 hours
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        for engagement in self.metrics['content_engagements']:
            engagement_time = datetime.fromisoformat(engagement['timestamp'])
            if engagement_time > cutoff_time:
                engagement_counts[engagement['engagement_type']] += 1
        
        # Sort by count and return top 5
        top_engagements = sorted(engagement_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return [
            {'engagement_type': engagement_type, 'count': count}
            for engagement_type, count in top_engagements
        ]

class SocialPerformanceMonitor:
    """Real-time social performance monitoring"""
    
    def __init__(self):
        self.request_times = []
        self.error_counts = defaultdict(int)
        self.endpoint_stats = defaultdict(list)
        self.lock = threading.RLock()
    
    def track_request(self, endpoint: str, response_time: float, status_code: int):
        """Track API request performance"""
        with self.lock:
            request_data = {
                'endpoint': endpoint,
                'response_time': response_time,
                'status_code': status_code,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            self.request_times.append(request_data)
            self.endpoint_stats[endpoint].append(request_data)
            
            if status_code >= 400:
                self.error_counts[endpoint] += 1
            
            # Keep only last 1000 requests
            if len(self.request_times) > 1000:
                self.request_times = self.request_times[-1000:]
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        with self.lock:
            if not self.request_times:
                return {'message': 'No performance data available'}
            
            # Calculate overall statistics
            response_times = [req['response_time'] for req in self.request_times]
            
            stats = {
                'overall_performance': {
                    'total_requests': len(self.request_times),
                    'avg_response_time': round(sum(response_times) / len(response_times), 3),
                    'min_response_time': round(min(response_times), 3),
                    'max_response_time': round(max(response_times), 3),
                    'p95_response_time': round(self._calculate_percentile(response_times, 95), 3),
                    'p99_response_time': round(self._calculate_percentile(response_times, 99), 3)
                },
                'error_analysis': {
                    'total_errors': sum(self.error_counts.values()),
                    'error_rate': round(sum(self.error_counts.values()) / len(self.request_times) * 100, 2),
                    'errors_by_endpoint': dict(self.error_counts)
                },
                'endpoint_performance': self._get_endpoint_performance(),
                'performance_grade': self._calculate_performance_grade(response_times),
                'recommendations': self._get_performance_recommendations(response_times)
            }
            
            return stats
    
    def _calculate_percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile of data"""
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    def _get_endpoint_performance(self) -> Dict[str, Any]:
        """Get performance stats by endpoint"""
        endpoint_performance = {}
        
        for endpoint, requests in self.endpoint_stats.items():
            if not requests:
                continue
                
            response_times = [req['response_time'] for req in requests]
            error_count = sum(1 for req in requests if req['status_code'] >= 400)
            
            endpoint_performance[endpoint] = {
                'request_count': len(requests),
                'avg_response_time': round(sum(response_times) / len(response_times), 3),
                'error_count': error_count,
                'error_rate': round(error_count / len(requests) * 100, 2),
                'performance_grade': self._calculate_performance_grade(response_times)
            }
        
        return endpoint_performance
    
    def _calculate_performance_grade(self, response_times: List[float]) -> str:
        """Calculate performance grade based on response times"""
        if not response_times:
            return 'N/A'
        
        avg_time = sum(response_times) / len(response_times)
        p95_time = self._calculate_percentile(response_times, 95)
        
        if avg_time < 0.1 and p95_time < 0.2:
            return 'A+'
        elif avg_time < 0.2 and p95_time < 0.5:
            return 'A'
        elif avg_time < 0.5 and p95_time < 1.0:
            return 'B'
        elif avg_time < 1.0 and p95_time < 2.0:
            return 'C'
        else:
            return 'D'
    
    def _get_performance_recommendations(self, response_times: List[float]) -> List[str]:
        """Get performance improvement recommendations"""
        recommendations = []
        
        if not response_times:
            return recommendations
        
        avg_time = sum(response_times) / len(response_times)
        p95_time = self._calculate_percentile(response_times, 95)
        
        if avg_time > 1.0:
            recommendations.append("Consider implementing caching for frequently accessed data")
            recommendations.append("Optimize database queries and add indexes")
        
        if p95_time > 2.0:
            recommendations.append("Investigate slow endpoints and optimize bottlenecks")
            recommendations.append("Consider implementing request queuing for heavy operations")
        
        if sum(self.error_counts.values()) / len(self.request_times) > 0.05:
            recommendations.append("Review error handling and improve system reliability")
        
        return recommendations

# Global instances
social_cache = SocialPerformanceCache()
social_analytics = SocialAnalyticsEngine()
social_monitor = SocialPerformanceMonitor()

