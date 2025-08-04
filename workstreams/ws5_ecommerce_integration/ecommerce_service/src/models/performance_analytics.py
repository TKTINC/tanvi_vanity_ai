from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json
import uuid
from src.models.ecommerce_models import db

class PerformanceMetric(db.Model):
    """Performance metrics and monitoring"""
    __tablename__ = 'performance_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Metric identification
    metric_name = db.Column(db.String(100), nullable=False)  # 'api_response_time', 'db_query_time', 'cache_hit_rate'
    metric_type = db.Column(db.String(50), nullable=False)   # 'latency', 'throughput', 'error_rate', 'resource_usage'
    
    # Metric value
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20))  # 'ms', 'seconds', 'percent', 'count'
    
    # Context information
    endpoint = db.Column(db.String(200))  # API endpoint
    method = db.Column(db.String(10))     # HTTP method
    user_id = db.Column(db.Integer)       # User context
    market_id = db.Column(db.Integer)     # Market context
    
    # Performance details
    request_id = db.Column(db.String(100))
    session_id = db.Column(db.String(100))
    
    # Additional metadata
    additional_data = db.Column(db.Text)  # JSON object with extra details
    
    # Status and categorization
    status = db.Column(db.String(20), default='normal')  # 'normal', 'warning', 'critical'
    category = db.Column(db.String(50))  # 'api', 'database', 'cache', 'payment', 'search'
    
    # Timestamps
    measured_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'metric_name': self.metric_name,
            'metric_type': self.metric_type,
            'value': self.value,
            'unit': self.unit,
            'endpoint': self.endpoint,
            'method': self.method,
            'user_id': self.user_id,
            'market_id': self.market_id,
            'request_id': self.request_id,
            'session_id': self.session_id,
            'additional_data': json.loads(self.additional_data) if self.additional_data else {},
            'status': self.status,
            'category': self.category,
            'measured_at': self.measured_at.isoformat(),
            'created_at': self.created_at.isoformat()
        }

class EcommerceAnalytics(db.Model):
    """E-commerce business analytics and KPIs"""
    __tablename__ = 'ecommerce_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Analytics identification
    metric_name = db.Column(db.String(100), nullable=False)  # 'conversion_rate', 'cart_abandonment', 'avg_order_value'
    metric_category = db.Column(db.String(50), nullable=False)  # 'sales', 'user_behavior', 'product_performance'
    
    # Metric value and calculation
    value = db.Column(db.Float, nullable=False)
    previous_value = db.Column(db.Float)  # For comparison
    percentage_change = db.Column(db.Float)  # Change from previous period
    
    # Time period
    period_type = db.Column(db.String(20), nullable=False)  # 'hourly', 'daily', 'weekly', 'monthly'
    period_start = db.Column(db.DateTime, nullable=False)
    period_end = db.Column(db.DateTime, nullable=False)
    
    # Segmentation
    market_id = db.Column(db.Integer, db.ForeignKey('markets.id'))
    user_segment = db.Column(db.String(50))  # 'new_users', 'returning_users', 'vip_users'
    product_category = db.Column(db.String(100))
    
    # Calculation details
    numerator = db.Column(db.Float)    # For rate calculations
    denominator = db.Column(db.Float)  # For rate calculations
    sample_size = db.Column(db.Integer)
    
    # Metadata
    calculation_method = db.Column(db.String(100))
    data_sources = db.Column(db.Text)  # JSON array of data sources
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    market = db.relationship('Market', backref='analytics')
    
    def to_dict(self):
        return {
            'id': self.id,
            'metric_name': self.metric_name,
            'metric_category': self.metric_category,
            'value': self.value,
            'previous_value': self.previous_value,
            'percentage_change': self.percentage_change,
            'trend': 'up' if self.percentage_change and self.percentage_change > 0 else 'down' if self.percentage_change and self.percentage_change < 0 else 'stable',
            'period_type': self.period_type,
            'period_start': self.period_start.isoformat(),
            'period_end': self.period_end.isoformat(),
            'market_id': self.market_id,
            'market_name': self.market.name if self.market else None,
            'user_segment': self.user_segment,
            'product_category': self.product_category,
            'numerator': self.numerator,
            'denominator': self.denominator,
            'sample_size': self.sample_size,
            'calculation_method': self.calculation_method,
            'data_sources': json.loads(self.data_sources) if self.data_sources else [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class CacheMetrics(db.Model):
    """Cache performance metrics"""
    __tablename__ = 'cache_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Cache identification
    cache_name = db.Column(db.String(100), nullable=False)  # 'product_catalog', 'user_sessions', 'payment_methods'
    cache_type = db.Column(db.String(50), nullable=False)   # 'redis', 'memcached', 'in_memory'
    
    # Cache metrics
    hit_count = db.Column(db.Integer, default=0)
    miss_count = db.Column(db.Integer, default=0)
    hit_rate = db.Column(db.Float)  # Calculated hit rate percentage
    
    # Performance metrics
    avg_response_time_ms = db.Column(db.Float)
    total_requests = db.Column(db.Integer, default=0)
    
    # Cache size metrics
    cache_size_mb = db.Column(db.Float)
    max_cache_size_mb = db.Column(db.Float)
    cache_utilization = db.Column(db.Float)  # Percentage
    
    # Cache operations
    evictions = db.Column(db.Integer, default=0)
    expirations = db.Column(db.Integer, default=0)
    
    # Time period
    period_start = db.Column(db.DateTime, nullable=False)
    period_end = db.Column(db.DateTime, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cache_name': self.cache_name,
            'cache_type': self.cache_type,
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'hit_rate': self.hit_rate,
            'avg_response_time_ms': self.avg_response_time_ms,
            'total_requests': self.total_requests,
            'cache_size_mb': self.cache_size_mb,
            'max_cache_size_mb': self.max_cache_size_mb,
            'cache_utilization': self.cache_utilization,
            'evictions': self.evictions,
            'expirations': self.expirations,
            'period_start': self.period_start.isoformat(),
            'period_end': self.period_end.isoformat(),
            'efficiency': 'excellent' if self.hit_rate and self.hit_rate > 90 else 'good' if self.hit_rate and self.hit_rate > 75 else 'needs_improvement',
            'created_at': self.created_at.isoformat()
        }

class UserBehaviorAnalytics(db.Model):
    """User behavior tracking and analytics"""
    __tablename__ = 'user_behavior_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # User identification
    user_id = db.Column(db.Integer)  # Can be null for anonymous users
    session_id = db.Column(db.String(100))
    
    # Behavior tracking
    event_type = db.Column(db.String(50), nullable=False)  # 'page_view', 'product_view', 'add_to_cart', 'checkout_start'
    event_category = db.Column(db.String(50))  # 'navigation', 'product_interaction', 'purchase_funnel'
    
    # Event details
    page_url = db.Column(db.String(500))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    category = db.Column(db.String(100))
    
    # User context
    market_id = db.Column(db.Integer, db.ForeignKey('markets.id'))
    device_type = db.Column(db.String(20))  # 'mobile', 'tablet', 'desktop'
    browser = db.Column(db.String(50))
    os = db.Column(db.String(50))
    
    # Engagement metrics
    time_spent_seconds = db.Column(db.Integer)
    scroll_depth = db.Column(db.Float)  # Percentage of page scrolled
    clicks = db.Column(db.Integer, default=0)
    
    # Conversion tracking
    conversion_value = db.Column(db.Float)  # Value of conversion if applicable
    conversion_type = db.Column(db.String(50))  # 'purchase', 'signup', 'newsletter'
    
    # Geographic data
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    
    # Referral information
    referrer = db.Column(db.String(500))
    utm_source = db.Column(db.String(100))
    utm_medium = db.Column(db.String(100))
    utm_campaign = db.Column(db.String(100))
    
    event_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref='behavior_analytics')
    market = db.relationship('Market', backref='user_behaviors')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'event_type': self.event_type,
            'event_category': self.event_category,
            'page_url': self.page_url,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'category': self.category,
            'market_id': self.market_id,
            'market_name': self.market.name if self.market else None,
            'device_type': self.device_type,
            'browser': self.browser,
            'os': self.os,
            'time_spent_seconds': self.time_spent_seconds,
            'scroll_depth': self.scroll_depth,
            'clicks': self.clicks,
            'conversion_value': self.conversion_value,
            'conversion_type': self.conversion_type,
            'country': self.country,
            'city': self.city,
            'referrer': self.referrer,
            'utm_source': self.utm_source,
            'utm_medium': self.utm_medium,
            'utm_campaign': self.utm_campaign,
            'event_timestamp': self.event_timestamp.isoformat(),
            'created_at': self.created_at.isoformat()
        }

class SystemAlert(db.Model):
    """System alerts and monitoring notifications"""
    __tablename__ = 'system_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.String(100), unique=True, nullable=False)
    
    # Alert details
    alert_type = db.Column(db.String(50), nullable=False)  # 'performance', 'error', 'security', 'business'
    severity = db.Column(db.String(20), nullable=False)    # 'low', 'medium', 'high', 'critical'
    
    # Alert content
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    # Alert context
    component = db.Column(db.String(100))  # 'payment_gateway', 'product_catalog', 'user_auth'
    metric_name = db.Column(db.String(100))
    threshold_value = db.Column(db.Float)
    current_value = db.Column(db.Float)
    
    # Alert status
    status = db.Column(db.String(20), default='active')  # 'active', 'acknowledged', 'resolved', 'suppressed'
    
    # Resolution tracking
    acknowledged_by = db.Column(db.Integer)  # Admin user ID
    acknowledged_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer)      # Admin user ID
    resolved_at = db.Column(db.DateTime)
    resolution_notes = db.Column(db.Text)
    
    # Notification tracking
    notification_sent = db.Column(db.Boolean, default=False)
    notification_channels = db.Column(db.Text)  # JSON array of channels used
    
    # Alert metadata
    additional_data = db.Column(db.Text)  # JSON object with extra context
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'alert_id': self.alert_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'title': self.title,
            'message': self.message,
            'component': self.component,
            'metric_name': self.metric_name,
            'threshold_value': self.threshold_value,
            'current_value': self.current_value,
            'status': self.status,
            'acknowledged_by': self.acknowledged_by,
            'acknowledged_at': self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            'resolved_by': self.resolved_by,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolution_notes': self.resolution_notes,
            'notification_sent': self.notification_sent,
            'notification_channels': json.loads(self.notification_channels) if self.notification_channels else [],
            'additional_data': json.loads(self.additional_data) if self.additional_data else {},
            'age_minutes': int((datetime.utcnow() - self.created_at).total_seconds() / 60),
            'is_recent': (datetime.utcnow() - self.created_at) < timedelta(hours=1),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class DatabaseOptimization(db.Model):
    """Database query optimization tracking"""
    __tablename__ = 'database_optimizations'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Query identification
    query_hash = db.Column(db.String(64), nullable=False)  # MD5 hash of normalized query
    query_type = db.Column(db.String(20), nullable=False)  # 'SELECT', 'INSERT', 'UPDATE', 'DELETE'
    table_name = db.Column(db.String(100))
    
    # Performance metrics
    execution_time_ms = db.Column(db.Float, nullable=False)
    rows_examined = db.Column(db.Integer)
    rows_returned = db.Column(db.Integer)
    
    # Query analysis
    uses_index = db.Column(db.Boolean, default=False)
    full_table_scan = db.Column(db.Boolean, default=False)
    query_complexity = db.Column(db.String(20))  # 'simple', 'moderate', 'complex'
    
    # Optimization suggestions
    optimization_suggestions = db.Column(db.Text)  # JSON array of suggestions
    index_suggestions = db.Column(db.Text)         # JSON array of index suggestions
    
    # Frequency tracking
    execution_count = db.Column(db.Integer, default=1)
    last_executed = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Query details
    query_pattern = db.Column(db.Text)  # Normalized query pattern
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'query_hash': self.query_hash,
            'query_type': self.query_type,
            'table_name': self.table_name,
            'execution_time_ms': self.execution_time_ms,
            'rows_examined': self.rows_examined,
            'rows_returned': self.rows_returned,
            'efficiency_ratio': (self.rows_returned / max(self.rows_examined, 1)) if self.rows_examined else 1.0,
            'uses_index': self.uses_index,
            'full_table_scan': self.full_table_scan,
            'query_complexity': self.query_complexity,
            'optimization_suggestions': json.loads(self.optimization_suggestions) if self.optimization_suggestions else [],
            'index_suggestions': json.loads(self.index_suggestions) if self.index_suggestions else [],
            'execution_count': self.execution_count,
            'last_executed': self.last_executed.isoformat(),
            'query_pattern': self.query_pattern,
            'performance_rating': 'excellent' if self.execution_time_ms < 10 else 'good' if self.execution_time_ms < 50 else 'needs_optimization',
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

