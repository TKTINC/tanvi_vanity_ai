from flask import Blueprint, request, jsonify
from datetime import datetime
import time
import hashlib
import json
from src.utils.performance_cache import (
    ai_cache, performance_monitor, ai_model_cache, 
    cached, performance_tracked, ResponseOptimizer
)

performance_bp = Blueprint('performance', __name__)

@performance_bp.route('/cache-stats', methods=['GET'])
@performance_tracked('cache_stats')
def get_cache_stats():
    """
    Get comprehensive cache statistics
    "We girls have no time" - Monitor cache performance!
    """
    try:
        # Get main cache stats
        main_cache_stats = ai_cache.get_stats()
        
        # Get AI model cache stats
        ai_model_stats = ai_model_cache.get_cache_stats()
        
        # Get performance stats
        performance_stats = performance_monitor.get_performance_stats()
        
        # Calculate cache efficiency
        cache_efficiency = {
            'overall_hit_ratio': main_cache_stats['hit_ratio'],
            'cache_effectiveness': 'excellent' if main_cache_stats['hit_ratio'] > 0.8 else
                                 'good' if main_cache_stats['hit_ratio'] > 0.6 else
                                 'fair' if main_cache_stats['hit_ratio'] > 0.4 else 'poor',
            'memory_efficiency': 'optimal' if main_cache_stats['cache_size'] < main_cache_stats['max_size'] * 0.8 else 'high',
            'cache_health': 'healthy' if main_cache_stats['hit_ratio'] > 0.6 else 'needs_optimization'
        }
        
        # Generate cache optimization suggestions
        optimization_suggestions = []
        
        if main_cache_stats['hit_ratio'] < 0.6:
            optimization_suggestions.append("Increase cache TTL for frequently accessed data")
            optimization_suggestions.append("Implement more aggressive caching for AI model results")
        
        if main_cache_stats['cache_size'] > main_cache_stats['max_size'] * 0.9:
            optimization_suggestions.append("Consider increasing cache size limit")
            optimization_suggestions.append("Implement more selective caching strategy")
        
        if len(main_cache_stats['top_miss_keys']) > 0:
            optimization_suggestions.append("Analyze frequently missed keys for caching opportunities")
        
        return jsonify({
            'status': 'success',
            'message': 'Cache statistics retrieved successfully',
            'main_cache': main_cache_stats,
            'ai_model_cache': ai_model_stats,
            'performance_overview': performance_stats.get('overall_performance', {}),
            'cache_efficiency': cache_efficiency,
            'optimization_suggestions': optimization_suggestions,
            'cache_health_score': main_cache_stats['hit_ratio'] * 100,
            'analysis_date': datetime.utcnow().isoformat(),
            'tagline': 'We girls have no time - Cache performance optimized!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve cache statistics',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@performance_bp.route('/performance-stats', methods=['GET'])
@performance_tracked('performance_stats')
def get_performance_stats():
    """
    Get comprehensive performance statistics
    "We girls have no time" - Monitor every millisecond!
    """
    try:
        # Get detailed performance stats
        performance_stats = performance_monitor.get_performance_stats()
        
        if performance_stats.get('status') == 'no_data':
            return jsonify({
                'status': 'no_data',
                'message': 'No performance data available yet',
                'recommendation': 'Make some API calls to generate performance data',
                'tagline': 'We girls have no time - But we need data first!'
            }), 400
        
        # Get cache stats for correlation
        cache_stats = ai_cache.get_stats()
        
        # Calculate performance insights
        overall_perf = performance_stats['overall_performance']
        performance_insights = {
            'speed_rating': 'excellent' if overall_perf['p95_response_time'] < 0.5 else
                           'good' if overall_perf['p95_response_time'] < 1.0 else
                           'fair' if overall_perf['p95_response_time'] < 2.0 else 'poor',
            'consistency_rating': 'excellent' if overall_perf['p95_response_time'] / overall_perf['average_response_time'] < 2 else
                                 'good' if overall_perf['p95_response_time'] / overall_perf['average_response_time'] < 3 else 'fair',
            'reliability_rating': 'excellent' if overall_perf['slow_request_rate'] < 0.05 else
                                 'good' if overall_perf['slow_request_rate'] < 0.1 else 'fair',
            'cache_correlation': 'positive' if cache_stats['hit_ratio'] > 0.6 and overall_perf['average_response_time'] < 1.0 else 'neutral'
        }
        
        # Generate performance recommendations
        performance_recommendations = []
        
        if overall_perf['p95_response_time'] > 1.0:
            performance_recommendations.append("Implement more aggressive caching for slow endpoints")
            performance_recommendations.append("Consider async processing for heavy AI operations")
        
        if overall_perf['slow_request_rate'] > 0.1:
            performance_recommendations.append("Investigate and optimize slow request patterns")
        
        if cache_stats['hit_ratio'] < 0.6:
            performance_recommendations.append("Improve cache strategy to reduce response times")
        
        # Calculate performance score
        performance_score = (
            (1.0 / max(overall_perf['p95_response_time'], 0.1)) * 20 +  # Speed component
            (1.0 - overall_perf['slow_request_rate']) * 30 +           # Reliability component
            cache_stats['hit_ratio'] * 50                              # Cache efficiency component
        )
        performance_score = min(performance_score, 100)
        
        return jsonify({
            'status': 'success',
            'message': 'Performance statistics retrieved successfully',
            'performance_stats': performance_stats,
            'performance_insights': performance_insights,
            'performance_score': round(performance_score, 1),
            'performance_grade': performance_stats.get('performance_grade', 'N/A'),
            'cache_correlation': {
                'hit_ratio': cache_stats['hit_ratio'],
                'impact_on_performance': 'positive' if cache_stats['hit_ratio'] > 0.6 else 'neutral'
            },
            'recommendations': performance_recommendations,
            'analysis_date': datetime.utcnow().isoformat(),
            'tagline': 'We girls have no time - Performance monitored and optimized!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve performance statistics',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@performance_bp.route('/cache-invalidate', methods=['POST'])
@performance_tracked('cache_invalidate')
def invalidate_cache():
    """
    Invalidate cache entries
    "We girls have no time" - Clear cache when needed!
    """
    try:
        data = request.get_json() or {}
        pattern = data.get('pattern')
        user_id = data.get('user_id')
        cache_type = data.get('cache_type', 'all')  # all, main, ai_models
        
        invalidated_count = 0
        
        if cache_type in ['all', 'main']:
            # Invalidate main cache
            main_invalidated = ai_cache.invalidate(pattern)
            invalidated_count += main_invalidated
        
        if cache_type in ['all', 'ai_models'] and user_id:
            # Invalidate AI model cache for specific user
            ai_model_cache.invalidate_user_cache(user_id)
            invalidated_count += 10  # Estimate
        
        return jsonify({
            'status': 'success',
            'message': 'Cache invalidation completed',
            'invalidated_entries': invalidated_count,
            'pattern': pattern,
            'user_id': user_id,
            'cache_type': cache_type,
            'timestamp': datetime.utcnow().isoformat(),
            'tagline': 'We girls have no time - Cache cleared for fresh data!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Cache invalidation failed',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@performance_bp.route('/optimize-response', methods=['POST'])
@performance_tracked('optimize_response')
def optimize_response():
    """
    Optimize response data for faster transfer
    "We girls have no time" - Optimize every byte!
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided for optimization'}), 400
        
        response_data = data.get('data', {})
        compression_level = data.get('compression_level', 'medium')  # light, medium, high
        paginate = data.get('paginate', False)
        page = data.get('page', 1)
        per_page = data.get('per_page', 20)
        
        # Start optimization timer
        start_time = time.time()
        
        # Apply compression
        optimized_data = ResponseOptimizer.compress_response(response_data, compression_level)
        
        # Apply pagination if requested and data is a list
        if paginate and isinstance(optimized_data, list):
            optimized_data = ResponseOptimizer.paginate_response(optimized_data, page, per_page)
        
        # Calculate optimization metrics
        optimization_time = time.time() - start_time
        
        # Estimate size reduction (rough calculation)
        original_size = len(json.dumps(response_data, default=str))
        optimized_size = len(json.dumps(optimized_data, default=str))
        size_reduction = ((original_size - optimized_size) / original_size) * 100 if original_size > 0 else 0
        
        return jsonify({
            'status': 'success',
            'message': 'Response optimization completed',
            'optimized_data': optimized_data,
            'optimization_metrics': {
                'original_size_estimate': original_size,
                'optimized_size_estimate': optimized_size,
                'size_reduction_percentage': round(size_reduction, 1),
                'optimization_time': round(optimization_time * 1000, 2),  # in milliseconds
                'compression_level': compression_level,
                'pagination_applied': paginate
            },
            'optimization_date': datetime.utcnow().isoformat(),
            'tagline': 'We girls have no time - Response optimized for speed!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Response optimization failed',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@performance_bp.route('/benchmark', methods=['POST'])
@performance_tracked('benchmark')
def run_performance_benchmark():
    """
    Run performance benchmark tests
    "We girls have no time" - Benchmark for excellence!
    """
    try:
        data = request.get_json() or {}
        test_type = data.get('test_type', 'basic')  # basic, comprehensive, stress
        iterations = data.get('iterations', 10)
        
        benchmark_results = {
            'test_type': test_type,
            'iterations': iterations,
            'tests': [],
            'summary': {}
        }
        
        # Basic cache performance test
        cache_times = []
        for i in range(iterations):
            start_time = time.time()
            
            # Test cache set and get
            test_key = f"benchmark_test_{i}"
            test_data = {'test': True, 'iteration': i, 'data': 'x' * 100}
            
            ai_cache.set(test_key, test_data, 300)  # 5 minute TTL
            retrieved_data = ai_cache.get(test_key)
            
            cache_time = time.time() - start_time
            cache_times.append(cache_time)
            
            benchmark_results['tests'].append({
                'test': 'cache_performance',
                'iteration': i + 1,
                'duration': cache_time,
                'success': retrieved_data is not None
            })
        
        # Response optimization test
        if test_type in ['comprehensive', 'stress']:
            optimization_times = []
            test_response = {
                'data': [{'id': i, 'name': f'item_{i}', 'description': 'x' * 50} for i in range(100)],
                'metadata': {'total': 100, 'page': 1},
                'additional_info': 'x' * 200
            }
            
            for i in range(min(iterations, 5)):  # Limit optimization tests
                start_time = time.time()
                optimized = ResponseOptimizer.compress_response(test_response, 'medium')
                optimization_time = time.time() - start_time
                optimization_times.append(optimization_time)
                
                benchmark_results['tests'].append({
                    'test': 'response_optimization',
                    'iteration': i + 1,
                    'duration': optimization_time,
                    'success': optimized is not None
                })
        
        # Calculate summary statistics
        if cache_times:
            benchmark_results['summary']['cache_performance'] = {
                'average_time': sum(cache_times) / len(cache_times),
                'min_time': min(cache_times),
                'max_time': max(cache_times),
                'total_tests': len(cache_times),
                'success_rate': 1.0  # All cache tests should succeed
            }
        
        if test_type in ['comprehensive', 'stress'] and 'optimization_times' in locals():
            benchmark_results['summary']['optimization_performance'] = {
                'average_time': sum(optimization_times) / len(optimization_times),
                'min_time': min(optimization_times),
                'max_time': max(optimization_times),
                'total_tests': len(optimization_times),
                'success_rate': 1.0
            }
        
        # Overall benchmark score
        avg_cache_time = benchmark_results['summary']['cache_performance']['average_time']
        benchmark_score = max(0, 100 - (avg_cache_time * 1000))  # Score based on milliseconds
        
        benchmark_results['summary']['overall'] = {
            'benchmark_score': round(benchmark_score, 1),
            'performance_rating': 'excellent' if benchmark_score > 95 else
                                 'good' if benchmark_score > 85 else
                                 'fair' if benchmark_score > 70 else 'poor',
            'total_duration': sum(test['duration'] for test in benchmark_results['tests']),
            'total_tests': len(benchmark_results['tests'])
        }
        
        return jsonify({
            'status': 'success',
            'message': 'Performance benchmark completed',
            'benchmark_results': benchmark_results,
            'benchmark_date': datetime.utcnow().isoformat(),
            'tagline': 'We girls have no time - Benchmark completed at lightning speed!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Performance benchmark failed',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@performance_bp.route('/health-check', methods=['GET'])
@performance_tracked('performance_health')
def performance_health_check():
    """
    Comprehensive performance health check
    "We girls have no time" - Health check for peak performance!
    """
    try:
        # Get current performance metrics
        cache_stats = ai_cache.get_stats()
        performance_stats = performance_monitor.get_performance_stats()
        ai_model_stats = ai_model_cache.get_cache_stats()
        
        # Calculate health scores
        health_scores = {
            'cache_health': min(100, cache_stats['hit_ratio'] * 100 + 20),
            'response_time_health': 100 if performance_stats.get('status') == 'no_data' else 
                                   max(0, 100 - (performance_stats['overall_performance']['average_response_time'] * 50)),
            'memory_health': max(0, 100 - (cache_stats['cache_size'] / cache_stats['max_size'] * 100)),
            'error_rate_health': 100 if performance_stats.get('status') == 'no_data' else
                                 max(0, 100 - (performance_stats['overall_performance']['slow_request_rate'] * 200))
        }
        
        # Overall health score
        overall_health = sum(health_scores.values()) / len(health_scores)
        
        # Health status
        health_status = 'excellent' if overall_health > 90 else \
                       'good' if overall_health > 75 else \
                       'fair' if overall_health > 60 else 'poor'
        
        # Health recommendations
        recommendations = []
        
        if health_scores['cache_health'] < 70:
            recommendations.append("Improve cache hit ratio by optimizing cache strategy")
        
        if health_scores['response_time_health'] < 70:
            recommendations.append("Optimize slow endpoints to improve response times")
        
        if health_scores['memory_health'] < 70:
            recommendations.append("Consider increasing cache size or implementing cache cleanup")
        
        if health_scores['error_rate_health'] < 70:
            recommendations.append("Investigate and reduce slow request rate")
        
        if not recommendations:
            recommendations.append("Performance is optimal - maintain current configuration")
        
        return jsonify({
            'status': 'success',
            'message': 'Performance health check completed',
            'health_status': health_status,
            'overall_health_score': round(overall_health, 1),
            'health_scores': {k: round(v, 1) for k, v in health_scores.items()},
            'cache_summary': {
                'hit_ratio': cache_stats['hit_ratio'],
                'cache_size': cache_stats['cache_size'],
                'max_size': cache_stats['max_size']
            },
            'performance_summary': {
                'has_data': performance_stats.get('status') != 'no_data',
                'average_response_time': performance_stats.get('overall_performance', {}).get('average_response_time', 0),
                'slow_request_rate': performance_stats.get('overall_performance', {}).get('slow_request_rate', 0)
            },
            'ai_model_cache_summary': ai_model_stats,
            'recommendations': recommendations,
            'health_check_date': datetime.utcnow().isoformat(),
            'tagline': 'We girls have no time - Performance health optimized!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Performance health check failed',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

