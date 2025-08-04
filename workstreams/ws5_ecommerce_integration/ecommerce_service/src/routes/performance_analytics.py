from flask import Blueprint, request, jsonify
from src.models.ecommerce_models import db, Market, Product, Order, ShoppingCart
from src.models.performance_analytics import (
    PerformanceMetric, EcommerceAnalytics, CacheMetrics, 
    UserBehaviorAnalytics, SystemAlert, DatabaseOptimization
)
from src.models.payment_processing import PaymentTransaction
import json
import uuid
import hashlib
from datetime import datetime, timedelta
from collections import defaultdict

performance_analytics_bp = Blueprint('performance_analytics', __name__)

# ============================================================================
# PERFORMANCE & ANALYTICS HEALTH
# ============================================================================

@performance_analytics_bp.route('/analytics/health', methods=['GET'])
def analytics_health_check():
    """Health check for performance optimization and analytics service"""
    # Get system performance overview
    recent_metrics = PerformanceMetric.query.filter(
        PerformanceMetric.created_at >= datetime.utcnow() - timedelta(hours=1)
    ).count()
    
    active_alerts = SystemAlert.query.filter_by(status='active').count()
    critical_alerts = SystemAlert.query.filter_by(status='active', severity='critical').count()
    
    # Get cache performance
    latest_cache_metrics = CacheMetrics.query.order_by(CacheMetrics.created_at.desc()).first()
    avg_cache_hit_rate = latest_cache_metrics.hit_rate if latest_cache_metrics else 0
    
    return jsonify({
        "status": "healthy",
        "service": "WS5: Performance Optimization & Analytics",
        "version": "5.0.0",
        "tagline": "We girls have no time",
        "philosophy": "Lightning-fast performance with intelligent insights",
        "system_health": {
            "metrics_collected_1h": recent_metrics,
            "active_alerts": active_alerts,
            "critical_alerts": critical_alerts,
            "cache_hit_rate": f"{avg_cache_hit_rate:.1f}%" if avg_cache_hit_rate else "N/A",
            "system_status": "critical" if critical_alerts > 0 else "warning" if active_alerts > 0 else "healthy"
        },
        "features": [
            "Real-time performance monitoring",
            "E-commerce business analytics",
            "Cache optimization and metrics",
            "User behavior tracking",
            "Automated alerting system",
            "Database query optimization",
            "API response time monitoring",
            "Conversion funnel analysis"
        ],
        "monitoring_categories": [
            "API Performance",
            "Database Optimization", 
            "Cache Efficiency",
            "User Experience",
            "Business KPIs",
            "System Health"
        ],
        "message": "Performance optimization and analytics system monitoring all aspects!"
    })

# ============================================================================
# PERFORMANCE METRICS
# ============================================================================

@performance_analytics_bp.route('/analytics/performance/metrics', methods=['GET'])
def get_performance_metrics():
    """Get performance metrics with filtering"""
    # Query parameters
    metric_type = request.args.get('metric_type')  # 'latency', 'throughput', 'error_rate'
    category = request.args.get('category')        # 'api', 'database', 'cache'
    endpoint = request.args.get('endpoint')
    hours = int(request.args.get('hours', 24))
    
    # Build query
    query = PerformanceMetric.query.filter(
        PerformanceMetric.created_at >= datetime.utcnow() - timedelta(hours=hours)
    )
    
    if metric_type:
        query = query.filter_by(metric_type=metric_type)
    if category:
        query = query.filter_by(category=category)
    if endpoint:
        query = query.filter_by(endpoint=endpoint)
    
    metrics = query.order_by(PerformanceMetric.created_at.desc()).limit(1000).all()
    
    # Calculate aggregated statistics
    if metrics:
        values = [m.value for m in metrics]
        avg_value = sum(values) / len(values)
        min_value = min(values)
        max_value = max(values)
        
        # Calculate percentiles
        sorted_values = sorted(values)
        p50 = sorted_values[len(sorted_values) // 2]
        p95 = sorted_values[int(len(sorted_values) * 0.95)]
        p99 = sorted_values[int(len(sorted_values) * 0.99)]
    else:
        avg_value = min_value = max_value = p50 = p95 = p99 = 0
    
    return jsonify({
        "metrics": [metric.to_dict() for metric in metrics],
        "total_metrics": len(metrics),
        "time_range_hours": hours,
        "aggregated_stats": {
            "average": round(avg_value, 2),
            "minimum": min_value,
            "maximum": max_value,
            "p50_median": p50,
            "p95": p95,
            "p99": p99
        },
        "filters": {
            "metric_type": metric_type,
            "category": category,
            "endpoint": endpoint
        },
        "message": f"Performance metrics for last {hours} hours"
    })

@performance_analytics_bp.route('/analytics/performance/record', methods=['POST'])
def record_performance_metric():
    """Record a new performance metric"""
    data = request.get_json()
    
    try:
        metric = PerformanceMetric(
            metric_name=data['metric_name'],
            metric_type=data['metric_type'],
            value=float(data['value']),
            unit=data.get('unit'),
            endpoint=data.get('endpoint'),
            method=data.get('method'),
            user_id=data.get('user_id'),
            market_id=data.get('market_id'),
            request_id=data.get('request_id'),
            session_id=data.get('session_id'),
            additional_data=json.dumps(data.get('additional_data', {})),
            category=data.get('category'),
            status=data.get('status', 'normal')
        )
        
        db.session.add(metric)
        db.session.commit()
        
        # Check for performance alerts
        _check_performance_alerts(metric)
        
        return jsonify({
            "success": True,
            "metric": metric.to_dict(),
            "message": "Performance metric recorded"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# ============================================================================
# E-COMMERCE ANALYTICS
# ============================================================================

@performance_analytics_bp.route('/analytics/ecommerce/dashboard', methods=['GET'])
def get_ecommerce_dashboard():
    """Get e-commerce analytics dashboard"""
    period = request.args.get('period', 'daily')  # 'hourly', 'daily', 'weekly', 'monthly'
    market_code = request.args.get('market')
    
    # Calculate date range
    if period == 'hourly':
        start_date = datetime.utcnow() - timedelta(hours=24)
    elif period == 'daily':
        start_date = datetime.utcnow() - timedelta(days=30)
    elif period == 'weekly':
        start_date = datetime.utcnow() - timedelta(weeks=12)
    else:  # monthly
        start_date = datetime.utcnow() - timedelta(days=365)
    
    # Build query
    query = EcommerceAnalytics.query.filter(
        EcommerceAnalytics.period_start >= start_date,
        EcommerceAnalytics.period_type == period
    )
    
    if market_code:
        market = Market.query.filter_by(code=market_code.upper()).first()
        if market:
            query = query.filter_by(market_id=market.id)
    
    analytics = query.order_by(EcommerceAnalytics.period_start.desc()).all()
    
    # Group by metric category
    metrics_by_category = defaultdict(list)
    for analytic in analytics:
        metrics_by_category[analytic.metric_category].append(analytic.to_dict())
    
    # Calculate key performance indicators
    kpis = _calculate_kpis(period, market_code)
    
    return jsonify({
        "dashboard": dict(metrics_by_category),
        "kpis": kpis,
        "period": period,
        "market": market_code,
        "date_range": {
            "start": start_date.isoformat(),
            "end": datetime.utcnow().isoformat()
        },
        "total_metrics": len(analytics),
        "message": f"E-commerce analytics dashboard for {period} period"
    })

@performance_analytics_bp.route('/analytics/ecommerce/conversion-funnel', methods=['GET'])
def get_conversion_funnel():
    """Get conversion funnel analysis"""
    days = int(request.args.get('days', 7))
    market_code = request.args.get('market')
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get funnel data from user behavior analytics
    query = UserBehaviorAnalytics.query.filter(
        UserBehaviorAnalytics.event_timestamp >= start_date
    )
    
    if market_code:
        market = Market.query.filter_by(code=market_code.upper()).first()
        if market:
            query = query.filter_by(market_id=market.id)
    
    behaviors = query.all()
    
    # Calculate funnel steps
    funnel_data = _calculate_conversion_funnel(behaviors)
    
    return jsonify({
        "conversion_funnel": funnel_data,
        "date_range": {
            "start": start_date.isoformat(),
            "end": datetime.utcnow().isoformat(),
            "days": days
        },
        "market": market_code,
        "total_events": len(behaviors),
        "message": f"Conversion funnel analysis for last {days} days"
    })

# ============================================================================
# CACHE METRICS
# ============================================================================

@performance_analytics_bp.route('/analytics/cache/metrics', methods=['GET'])
def get_cache_metrics():
    """Get cache performance metrics"""
    cache_name = request.args.get('cache_name')
    hours = int(request.args.get('hours', 24))
    
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    query = CacheMetrics.query.filter(
        CacheMetrics.period_start >= start_time
    )
    
    if cache_name:
        query = query.filter_by(cache_name=cache_name)
    
    cache_metrics = query.order_by(CacheMetrics.created_at.desc()).all()
    
    # Calculate overall cache performance
    if cache_metrics:
        total_hits = sum(m.hit_count for m in cache_metrics)
        total_misses = sum(m.miss_count for m in cache_metrics)
        overall_hit_rate = (total_hits / (total_hits + total_misses)) * 100 if (total_hits + total_misses) > 0 else 0
        avg_response_time = sum(m.avg_response_time_ms for m in cache_metrics if m.avg_response_time_ms) / len([m for m in cache_metrics if m.avg_response_time_ms])
    else:
        overall_hit_rate = avg_response_time = 0
    
    return jsonify({
        "cache_metrics": [metric.to_dict() for metric in cache_metrics],
        "overall_performance": {
            "hit_rate": round(overall_hit_rate, 2),
            "avg_response_time_ms": round(avg_response_time, 2) if avg_response_time else 0,
            "efficiency_rating": "excellent" if overall_hit_rate > 90 else "good" if overall_hit_rate > 75 else "needs_improvement"
        },
        "time_range_hours": hours,
        "cache_filter": cache_name,
        "total_metrics": len(cache_metrics),
        "message": f"Cache performance metrics for last {hours} hours"
    })

@performance_analytics_bp.route('/analytics/cache/record', methods=['POST'])
def record_cache_metrics():
    """Record cache performance metrics"""
    data = request.get_json()
    
    try:
        # Calculate hit rate
        hit_count = data.get('hit_count', 0)
        miss_count = data.get('miss_count', 0)
        hit_rate = (hit_count / (hit_count + miss_count)) * 100 if (hit_count + miss_count) > 0 else 0
        
        # Calculate cache utilization
        cache_size = data.get('cache_size_mb', 0)
        max_cache_size = data.get('max_cache_size_mb', 0)
        utilization = (cache_size / max_cache_size) * 100 if max_cache_size > 0 else 0
        
        cache_metric = CacheMetrics(
            cache_name=data['cache_name'],
            cache_type=data.get('cache_type', 'redis'),
            hit_count=hit_count,
            miss_count=miss_count,
            hit_rate=hit_rate,
            avg_response_time_ms=data.get('avg_response_time_ms'),
            total_requests=hit_count + miss_count,
            cache_size_mb=cache_size,
            max_cache_size_mb=max_cache_size,
            cache_utilization=utilization,
            evictions=data.get('evictions', 0),
            expirations=data.get('expirations', 0),
            period_start=datetime.fromisoformat(data['period_start']) if 'period_start' in data else datetime.utcnow() - timedelta(hours=1),
            period_end=datetime.fromisoformat(data['period_end']) if 'period_end' in data else datetime.utcnow()
        )
        
        db.session.add(cache_metric)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "cache_metric": cache_metric.to_dict(),
            "message": "Cache metrics recorded"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# ============================================================================
# USER BEHAVIOR ANALYTICS
# ============================================================================

@performance_analytics_bp.route('/analytics/behavior/track', methods=['POST'])
def track_user_behavior():
    """Track user behavior event"""
    data = request.get_json()
    
    try:
        behavior = UserBehaviorAnalytics(
            user_id=data.get('user_id'),
            session_id=data.get('session_id'),
            event_type=data['event_type'],
            event_category=data.get('event_category'),
            page_url=data.get('page_url'),
            product_id=data.get('product_id'),
            category=data.get('category'),
            market_id=data.get('market_id'),
            device_type=data.get('device_type'),
            browser=data.get('browser'),
            os=data.get('os'),
            time_spent_seconds=data.get('time_spent_seconds'),
            scroll_depth=data.get('scroll_depth'),
            clicks=data.get('clicks', 0),
            conversion_value=data.get('conversion_value'),
            conversion_type=data.get('conversion_type'),
            country=data.get('country'),
            city=data.get('city'),
            referrer=data.get('referrer'),
            utm_source=data.get('utm_source'),
            utm_medium=data.get('utm_medium'),
            utm_campaign=data.get('utm_campaign')
        )
        
        db.session.add(behavior)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "behavior_id": behavior.id,
            "message": "User behavior tracked"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@performance_analytics_bp.route('/analytics/behavior/insights', methods=['GET'])
def get_behavior_insights():
    """Get user behavior insights"""
    days = int(request.args.get('days', 7))
    event_type = request.args.get('event_type')
    market_code = request.args.get('market')
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = UserBehaviorAnalytics.query.filter(
        UserBehaviorAnalytics.event_timestamp >= start_date
    )
    
    if event_type:
        query = query.filter_by(event_type=event_type)
    
    if market_code:
        market = Market.query.filter_by(code=market_code.upper()).first()
        if market:
            query = query.filter_by(market_id=market.id)
    
    behaviors = query.all()
    
    # Generate insights
    insights = _generate_behavior_insights(behaviors)
    
    return jsonify({
        "insights": insights,
        "total_events": len(behaviors),
        "date_range": {
            "start": start_date.isoformat(),
            "end": datetime.utcnow().isoformat(),
            "days": days
        },
        "filters": {
            "event_type": event_type,
            "market": market_code
        },
        "message": f"User behavior insights for last {days} days"
    })

# ============================================================================
# SYSTEM ALERTS
# ============================================================================

@performance_analytics_bp.route('/analytics/alerts', methods=['GET'])
def get_system_alerts():
    """Get system alerts"""
    status = request.args.get('status', 'active')
    severity = request.args.get('severity')
    alert_type = request.args.get('alert_type')
    
    query = SystemAlert.query
    
    if status:
        query = query.filter_by(status=status)
    if severity:
        query = query.filter_by(severity=severity)
    if alert_type:
        query = query.filter_by(alert_type=alert_type)
    
    alerts = query.order_by(SystemAlert.created_at.desc()).limit(100).all()
    
    # Group by severity
    alerts_by_severity = defaultdict(list)
    for alert in alerts:
        alerts_by_severity[alert.severity].append(alert.to_dict())
    
    return jsonify({
        "alerts": [alert.to_dict() for alert in alerts],
        "alerts_by_severity": dict(alerts_by_severity),
        "total_alerts": len(alerts),
        "filters": {
            "status": status,
            "severity": severity,
            "alert_type": alert_type
        },
        "message": f"System alerts with status: {status}"
    })

@performance_analytics_bp.route('/analytics/alerts/create', methods=['POST'])
def create_system_alert():
    """Create a new system alert"""
    data = request.get_json()
    
    try:
        alert = SystemAlert(
            alert_id=f"ALERT_{uuid.uuid4().hex[:12].upper()}",
            alert_type=data['alert_type'],
            severity=data['severity'],
            title=data['title'],
            message=data['message'],
            component=data.get('component'),
            metric_name=data.get('metric_name'),
            threshold_value=data.get('threshold_value'),
            current_value=data.get('current_value'),
            additional_data=json.dumps(data.get('additional_data', {}))
        )
        
        db.session.add(alert)
        db.session.commit()
        
        # Send notifications if critical
        if alert.severity == 'critical':
            _send_alert_notifications(alert)
        
        return jsonify({
            "success": True,
            "alert": alert.to_dict(),
            "message": "System alert created"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# ============================================================================
# DATABASE OPTIMIZATION
# ============================================================================

@performance_analytics_bp.route('/analytics/database/optimization', methods=['GET'])
def get_database_optimization():
    """Get database optimization insights"""
    hours = int(request.args.get('hours', 24))
    query_type = request.args.get('query_type')
    
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    query = DatabaseOptimization.query.filter(
        DatabaseOptimization.last_executed >= start_time
    )
    
    if query_type:
        query = query.filter_by(query_type=query_type)
    
    optimizations = query.order_by(DatabaseOptimization.execution_time_ms.desc()).all()
    
    # Find slow queries
    slow_queries = [opt for opt in optimizations if opt.execution_time_ms > 100]
    
    # Find queries needing indexes
    index_needed = [opt for opt in optimizations if not opt.uses_index and opt.full_table_scan]
    
    return jsonify({
        "optimizations": [opt.to_dict() for opt in optimizations[:50]],
        "slow_queries": [opt.to_dict() for opt in slow_queries[:20]],
        "index_recommendations": [opt.to_dict() for opt in index_needed[:10]],
        "summary": {
            "total_queries_analyzed": len(optimizations),
            "slow_queries_count": len(slow_queries),
            "queries_needing_indexes": len(index_needed),
            "avg_execution_time": sum(opt.execution_time_ms for opt in optimizations) / len(optimizations) if optimizations else 0
        },
        "time_range_hours": hours,
        "message": f"Database optimization analysis for last {hours} hours"
    })

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _check_performance_alerts(metric):
    """Check if performance metric triggers any alerts"""
    # Define alert thresholds
    thresholds = {
        'api_response_time': {'warning': 500, 'critical': 1000},  # ms
        'db_query_time': {'warning': 100, 'critical': 500},      # ms
        'error_rate': {'warning': 5, 'critical': 10},            # %
        'cache_hit_rate': {'warning': 75, 'critical': 50}        # %
    }
    
    if metric.metric_name in thresholds:
        threshold = thresholds[metric.metric_name]
        
        if metric.value > threshold['critical']:
            severity = 'critical'
        elif metric.value > threshold['warning']:
            severity = 'high'
        else:
            return  # No alert needed
        
        # Create alert
        alert = SystemAlert(
            alert_id=f"PERF_{uuid.uuid4().hex[:12].upper()}",
            alert_type='performance',
            severity=severity,
            title=f"Performance Alert: {metric.metric_name}",
            message=f"{metric.metric_name} is {metric.value}{metric.unit}, exceeding threshold of {threshold['warning']}{metric.unit}",
            component=metric.category,
            metric_name=metric.metric_name,
            threshold_value=threshold['warning'],
            current_value=metric.value
        )
        
        db.session.add(alert)

def _calculate_kpis(period, market_code):
    """Calculate key performance indicators"""
    # This would integrate with actual business data
    # For now, return simulated KPIs
    return {
        "conversion_rate": {
            "value": 3.2,
            "change": "+0.5%",
            "trend": "up"
        },
        "average_order_value": {
            "value": 127.50,
            "change": "+$12.30",
            "trend": "up"
        },
        "cart_abandonment_rate": {
            "value": 68.5,
            "change": "-2.1%",
            "trend": "down"
        },
        "customer_lifetime_value": {
            "value": 285.00,
            "change": "+$23.50",
            "trend": "up"
        }
    }

def _calculate_conversion_funnel(behaviors):
    """Calculate conversion funnel from user behaviors"""
    # Group events by session
    sessions = defaultdict(list)
    for behavior in behaviors:
        sessions[behavior.session_id].append(behavior)
    
    # Count funnel steps
    funnel_steps = {
        "page_views": 0,
        "product_views": 0,
        "add_to_cart": 0,
        "checkout_start": 0,
        "purchase_complete": 0
    }
    
    for session_id, events in sessions.items():
        event_types = [event.event_type for event in events]
        
        if any(event_type in ['page_view', 'product_view'] for event_type in event_types):
            funnel_steps["page_views"] += 1
        
        if 'product_view' in event_types:
            funnel_steps["product_views"] += 1
        
        if 'add_to_cart' in event_types:
            funnel_steps["add_to_cart"] += 1
        
        if 'checkout_start' in event_types:
            funnel_steps["checkout_start"] += 1
        
        if 'purchase_complete' in event_types:
            funnel_steps["purchase_complete"] += 1
    
    # Calculate conversion rates
    total_sessions = len(sessions)
    if total_sessions > 0:
        conversion_rates = {
            step: (count / total_sessions) * 100
            for step, count in funnel_steps.items()
        }
    else:
        conversion_rates = {step: 0 for step in funnel_steps.keys()}
    
    return {
        "steps": funnel_steps,
        "conversion_rates": conversion_rates,
        "total_sessions": total_sessions
    }

def _generate_behavior_insights(behaviors):
    """Generate insights from user behavior data"""
    if not behaviors:
        return {}
    
    # Device type distribution
    device_counts = defaultdict(int)
    for behavior in behaviors:
        if behavior.device_type:
            device_counts[behavior.device_type] += 1
    
    # Most popular pages
    page_counts = defaultdict(int)
    for behavior in behaviors:
        if behavior.page_url:
            page_counts[behavior.page_url] += 1
    
    # Average engagement metrics
    engagement_times = [b.time_spent_seconds for b in behaviors if b.time_spent_seconds]
    avg_engagement = sum(engagement_times) / len(engagement_times) if engagement_times else 0
    
    return {
        "device_distribution": dict(device_counts),
        "popular_pages": dict(sorted(page_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
        "average_engagement_seconds": round(avg_engagement, 2),
        "total_unique_sessions": len(set(b.session_id for b in behaviors if b.session_id)),
        "conversion_events": len([b for b in behaviors if b.conversion_value and b.conversion_value > 0])
    }

def _send_alert_notifications(alert):
    """Send alert notifications (simulated)"""
    # This would integrate with notification services
    alert.notification_sent = True
    alert.notification_channels = json.dumps(['email', 'slack', 'sms'])
    return True

