from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import uuid
from src.models.ecommerce_models import db

class ShippingAddress(db.Model):
    """User shipping addresses"""
    __tablename__ = 'shipping_addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Reference to WS1 user
    
    # Address details
    label = db.Column(db.String(100))  # 'Home', 'Work', 'Mom\'s House'
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(200))
    
    # Address fields
    address_line_1 = db.Column(db.String(300), nullable=False)
    address_line_2 = db.Column(db.String(300))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    
    # Contact information
    phone = db.Column(db.String(20))
    email = db.Column(db.String(200))
    
    # Address preferences
    is_default = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Delivery instructions
    delivery_instructions = db.Column(db.Text)
    
    # Usage tracking
    last_used_at = db.Column(db.DateTime)
    usage_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'label': self.label,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'company': self.company,
            'address_line_1': self.address_line_1,
            'address_line_2': self.address_line_2,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'phone': self.phone,
            'email': self.email,
            'is_default': self.is_default,
            'is_verified': self.is_verified,
            'delivery_instructions': self.delivery_instructions,
            'full_name': f"{self.first_name} {self.last_name}",
            'full_address': f"{self.address_line_1}, {self.city}, {self.state} {self.postal_code}, {self.country}",
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'usage_count': self.usage_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ShippingMethod(db.Model):
    """Available shipping methods by market"""
    __tablename__ = 'shipping_methods'
    
    id = db.Column(db.Integer, primary_key=True)
    market_id = db.Column(db.Integer, db.ForeignKey('markets.id'), nullable=False)
    
    # Shipping method details
    name = db.Column(db.String(100), nullable=False)  # 'Standard', 'Express', 'Same-day'
    code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    
    # Pricing
    base_cost = db.Column(db.Float, nullable=False)
    cost_per_kg = db.Column(db.Float, default=0.0)
    free_shipping_threshold = db.Column(db.Float)  # Free above this amount
    
    # Delivery timeframes
    min_delivery_days = db.Column(db.Integer, nullable=False)
    max_delivery_days = db.Column(db.Integer, nullable=False)
    
    # Shipping method capabilities
    supports_cod = db.Column(db.Boolean, default=False)
    supports_tracking = db.Column(db.Boolean, default=True)
    supports_insurance = db.Column(db.Boolean, default=False)
    requires_signature = db.Column(db.Boolean, default=False)
    
    # Availability
    is_active = db.Column(db.Boolean, default=True)
    is_express = db.Column(db.Boolean, default=False)
    
    # Service provider
    carrier = db.Column(db.String(100))  # 'FedEx', 'UPS', 'BlueDart', 'Delhivery'
    carrier_service_code = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    market = db.relationship('Market', backref='shipping_methods')
    
    def to_dict(self):
        return {
            'id': self.id,
            'market_id': self.market_id,
            'market_name': self.market.name if self.market else None,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'base_cost': self.base_cost,
            'cost_per_kg': self.cost_per_kg,
            'free_shipping_threshold': self.free_shipping_threshold,
            'min_delivery_days': self.min_delivery_days,
            'max_delivery_days': self.max_delivery_days,
            'delivery_estimate': f"{self.min_delivery_days}-{self.max_delivery_days} days" if self.min_delivery_days != self.max_delivery_days else f"{self.min_delivery_days} days",
            'supports_cod': self.supports_cod,
            'supports_tracking': self.supports_tracking,
            'supports_insurance': self.supports_insurance,
            'requires_signature': self.requires_signature,
            'is_active': self.is_active,
            'is_express': self.is_express,
            'carrier': self.carrier,
            'carrier_service_code': self.carrier_service_code,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Coupon(db.Model):
    """Discount coupons and promotional codes"""
    __tablename__ = 'coupons'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    
    # Coupon details
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Discount configuration
    discount_type = db.Column(db.String(20), nullable=False)  # 'percentage', 'fixed_amount'
    discount_value = db.Column(db.Float, nullable=False)  # 10 (for 10%) or 50 (for $50)
    
    # Usage constraints
    minimum_order_amount = db.Column(db.Float, default=0.0)
    maximum_discount_amount = db.Column(db.Float)  # Cap for percentage discounts
    
    # Validity
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_until = db.Column(db.DateTime, nullable=False)
    
    # Usage limits
    usage_limit = db.Column(db.Integer)  # Total usage limit
    usage_limit_per_user = db.Column(db.Integer, default=1)
    current_usage_count = db.Column(db.Integer, default=0)
    
    # Targeting
    applicable_markets = db.Column(db.Text)  # JSON array of market codes
    applicable_categories = db.Column(db.Text)  # JSON array of categories
    applicable_brands = db.Column(db.Text)  # JSON array of brands
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_public = db.Column(db.Boolean, default=True)  # False for targeted campaigns
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'discount_type': self.discount_type,
            'discount_value': self.discount_value,
            'discount_display': f"{self.discount_value}%" if self.discount_type == 'percentage' else f"${self.discount_value}",
            'minimum_order_amount': self.minimum_order_amount,
            'maximum_discount_amount': self.maximum_discount_amount,
            'valid_from': self.valid_from.isoformat(),
            'valid_until': self.valid_until.isoformat(),
            'usage_limit': self.usage_limit,
            'usage_limit_per_user': self.usage_limit_per_user,
            'current_usage_count': self.current_usage_count,
            'remaining_uses': (self.usage_limit - self.current_usage_count) if self.usage_limit else None,
            'applicable_markets': json.loads(self.applicable_markets) if self.applicable_markets else [],
            'applicable_categories': json.loads(self.applicable_categories) if self.applicable_categories else [],
            'applicable_brands': json.loads(self.applicable_brands) if self.applicable_brands else [],
            'is_active': self.is_active,
            'is_public': self.is_public,
            'is_valid': self.is_active and self.valid_from <= datetime.utcnow() <= self.valid_until,
            'is_expired': datetime.utcnow() > self.valid_until,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class CouponUsage(db.Model):
    """Track coupon usage by users"""
    __tablename__ = 'coupon_usage'
    
    id = db.Column(db.Integer, primary_key=True)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    
    # Usage details
    discount_amount = db.Column(db.Float, nullable=False)
    order_amount = db.Column(db.Float, nullable=False)
    
    used_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    coupon = db.relationship('Coupon', backref='usage_records')
    order = db.relationship('Order', backref='coupon_usage')
    
    def to_dict(self):
        return {
            'id': self.id,
            'coupon_id': self.coupon_id,
            'coupon_code': self.coupon.code if self.coupon else None,
            'user_id': self.user_id,
            'order_id': self.order_id,
            'discount_amount': self.discount_amount,
            'order_amount': self.order_amount,
            'savings_percentage': (self.discount_amount / self.order_amount) * 100 if self.order_amount > 0 else 0,
            'used_at': self.used_at.isoformat()
        }

class CheckoutSession(db.Model):
    """Checkout session management"""
    __tablename__ = 'checkout_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    
    # User and cart association
    user_id = db.Column(db.Integer, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('shopping_carts.id'), nullable=False)
    
    # Checkout progress
    step = db.Column(db.String(50), default='cart_review')  # cart_review, shipping, payment, confirmation
    
    # Selected options
    shipping_address_id = db.Column(db.Integer, db.ForeignKey('shipping_addresses.id'))
    shipping_method_id = db.Column(db.Integer, db.ForeignKey('shipping_methods.id'))
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'))
    
    # Applied discounts
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.id'))
    
    # Checkout totals (calculated)
    subtotal = db.Column(db.Float, default=0.0)
    shipping_cost = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    
    # Session metadata
    browser_info = db.Column(db.Text)  # JSON object
    device_info = db.Column(db.Text)  # JSON object
    
    # Session status
    status = db.Column(db.String(30), default='active')  # active, completed, abandoned, expired
    
    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)  # Session expiration
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cart = db.relationship('ShoppingCart', backref='checkout_sessions')
    shipping_address = db.relationship('ShippingAddress', backref='checkout_sessions')
    shipping_method = db.relationship('ShippingMethod', backref='checkout_sessions')
    coupon = db.relationship('Coupon', backref='checkout_sessions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'cart_id': self.cart_id,
            'step': self.step,
            'shipping_address_id': self.shipping_address_id,
            'shipping_address': self.shipping_address.to_dict() if self.shipping_address else None,
            'shipping_method_id': self.shipping_method_id,
            'shipping_method': self.shipping_method.to_dict() if self.shipping_method else None,
            'payment_method_id': self.payment_method_id,
            'coupon_id': self.coupon_id,
            'coupon': self.coupon.to_dict() if self.coupon else None,
            'subtotal': self.subtotal,
            'shipping_cost': self.shipping_cost,
            'tax_amount': self.tax_amount,
            'discount_amount': self.discount_amount,
            'total_amount': self.total_amount,
            'browser_info': json.loads(self.browser_info) if self.browser_info else {},
            'device_info': json.loads(self.device_info) if self.device_info else {},
            'status': self.status,
            'started_at': self.started_at.isoformat(),
            'last_activity_at': self.last_activity_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_expired': self.expires_at < datetime.utcnow() if self.expires_at else False,
            'duration_minutes': int((datetime.utcnow() - self.started_at).total_seconds() / 60),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class OrderNotification(db.Model):
    """Order-related notifications and communications"""
    __tablename__ = 'order_notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    
    # Notification details
    notification_type = db.Column(db.String(50), nullable=False)  # 'order_confirmed', 'payment_received', 'shipped', 'delivered'
    channel = db.Column(db.String(20), nullable=False)  # 'email', 'sms', 'push', 'in_app'
    
    # Message content
    subject = db.Column(db.String(300))
    message = db.Column(db.Text, nullable=False)
    
    # Delivery status
    status = db.Column(db.String(20), default='pending')  # pending, sent, delivered, failed
    
    # Delivery details
    recipient = db.Column(db.String(300))  # email address or phone number
    sent_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    
    # Error handling
    error_message = db.Column(db.Text)
    retry_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', backref='notifications')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'notification_type': self.notification_type,
            'channel': self.channel,
            'subject': self.subject,
            'message': self.message,
            'status': self.status,
            'recipient': self.recipient,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'error_message': self.error_message,
            'retry_count': self.retry_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

