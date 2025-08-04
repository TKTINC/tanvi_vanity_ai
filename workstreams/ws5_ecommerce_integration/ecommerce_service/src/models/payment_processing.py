from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import uuid
from src.models.ecommerce_models import db

class PaymentGateway(db.Model):
    """Payment gateway configuration for different markets"""
    __tablename__ = 'payment_gateways'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # 'Stripe', 'Razorpay', 'PayPal'
    code = db.Column(db.String(50), unique=True, nullable=False)
    
    # Market association
    market_id = db.Column(db.Integer, db.ForeignKey('markets.id'), nullable=False)
    
    # Gateway configuration
    api_key = db.Column(db.String(500))
    api_secret = db.Column(db.String(500))
    webhook_secret = db.Column(db.String(500))
    base_url = db.Column(db.String(300))
    
    # Gateway capabilities
    supports_cards = db.Column(db.Boolean, default=True)
    supports_wallets = db.Column(db.Boolean, default=False)
    supports_bank_transfer = db.Column(db.Boolean, default=False)
    supports_upi = db.Column(db.Boolean, default=False)
    supports_cod = db.Column(db.Boolean, default=False)
    supports_bnpl = db.Column(db.Boolean, default=False)  # Buy Now Pay Later
    supports_subscriptions = db.Column(db.Boolean, default=False)
    
    # Processing fees
    transaction_fee_percentage = db.Column(db.Float, default=2.9)  # 2.9%
    transaction_fee_fixed = db.Column(db.Float, default=0.30)  # $0.30
    
    # Gateway settings
    currency = db.Column(db.String(3), nullable=False)  # USD, INR
    min_amount = db.Column(db.Float, default=1.0)
    max_amount = db.Column(db.Float, default=999999.0)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_test_mode = db.Column(db.Boolean, default=True)
    
    # Performance metrics
    success_rate = db.Column(db.Float, default=0.0)
    average_processing_time = db.Column(db.Float, default=0.0)  # seconds
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    market = db.relationship('Market', backref='payment_gateways')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'market_id': self.market_id,
            'market_name': self.market.name if self.market else None,
            'market_currency': self.market.currency if self.market else None,
            'supports_cards': self.supports_cards,
            'supports_wallets': self.supports_wallets,
            'supports_bank_transfer': self.supports_bank_transfer,
            'supports_upi': self.supports_upi,
            'supports_cod': self.supports_cod,
            'supports_bnpl': self.supports_bnpl,
            'supports_subscriptions': self.supports_subscriptions,
            'transaction_fee_percentage': self.transaction_fee_percentage,
            'transaction_fee_fixed': self.transaction_fee_fixed,
            'currency': self.currency,
            'min_amount': self.min_amount,
            'max_amount': self.max_amount,
            'is_active': self.is_active,
            'is_test_mode': self.is_test_mode,
            'success_rate': self.success_rate,
            'average_processing_time': self.average_processing_time,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class PaymentMethod(db.Model):
    """User's saved payment methods"""
    __tablename__ = 'payment_methods'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Reference to WS1 user
    
    # Payment method details
    method_type = db.Column(db.String(50), nullable=False)  # 'card', 'wallet', 'upi', 'bank_account'
    provider = db.Column(db.String(100))  # 'visa', 'mastercard', 'paytm', 'gpay'
    
    # Tokenized payment data (never store actual card numbers)
    gateway_token = db.Column(db.String(500))  # Token from payment gateway
    last_four_digits = db.Column(db.String(4))  # Last 4 digits for display
    
    # Card-specific fields
    card_brand = db.Column(db.String(50))  # 'visa', 'mastercard', 'amex'
    expiry_month = db.Column(db.Integer)
    expiry_year = db.Column(db.Integer)
    cardholder_name = db.Column(db.String(200))
    
    # UPI-specific fields
    upi_id = db.Column(db.String(100))  # user@paytm, user@gpay
    
    # Bank account fields
    bank_name = db.Column(db.String(200))
    account_type = db.Column(db.String(50))  # 'savings', 'current'
    
    # Billing address
    billing_address = db.Column(db.Text)  # JSON object
    
    # Status and preferences
    is_default = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Usage tracking
    last_used_at = db.Column(db.DateTime)
    usage_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'method_type': self.method_type,
            'provider': self.provider,
            'last_four_digits': self.last_four_digits,
            'card_brand': self.card_brand,
            'expiry_month': self.expiry_month,
            'expiry_year': self.expiry_year,
            'cardholder_name': self.cardholder_name,
            'upi_id': self.upi_id,
            'bank_name': self.bank_name,
            'account_type': self.account_type,
            'billing_address': json.loads(self.billing_address) if self.billing_address else {},
            'is_default': self.is_default,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'usage_count': self.usage_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class PaymentTransaction(db.Model):
    """Payment transaction records"""
    __tablename__ = 'payment_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    
    # Order and user association
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    
    # Payment gateway
    gateway_id = db.Column(db.Integer, db.ForeignKey('payment_gateways.id'), nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'))
    
    # Transaction details
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    
    # Gateway-specific IDs
    gateway_transaction_id = db.Column(db.String(200))  # ID from payment gateway
    gateway_payment_intent_id = db.Column(db.String(200))  # Payment intent ID
    
    # Transaction status
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed, cancelled, refunded
    
    # Transaction metadata
    transaction_type = db.Column(db.String(50), default='payment')  # payment, refund, partial_refund
    payment_method_type = db.Column(db.String(50))  # card, wallet, upi, cod, bnpl
    
    # Fees and charges
    gateway_fee = db.Column(db.Float, default=0.0)
    processing_fee = db.Column(db.Float, default=0.0)
    net_amount = db.Column(db.Float)  # Amount after fees
    
    # Fraud detection
    risk_score = db.Column(db.Float, default=0.0)  # 0.0 to 1.0
    fraud_check_status = db.Column(db.String(50), default='pending')  # pending, passed, flagged, failed
    
    # Error handling
    error_code = db.Column(db.String(100))
    error_message = db.Column(db.Text)
    
    # Timing
    initiated_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    processing_time_seconds = db.Column(db.Float)
    
    # Additional data
    gateway_response = db.Column(db.Text)  # JSON response from gateway
    transaction_metadata = db.Column(db.Text)  # Additional transaction metadata
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', backref='payment_transactions')
    gateway = db.relationship('PaymentGateway', backref='transactions')
    payment_method = db.relationship('PaymentMethod', backref='transactions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'gateway_id': self.gateway_id,
            'gateway_name': self.gateway.name if self.gateway else None,
            'payment_method_id': self.payment_method_id,
            'amount': self.amount,
            'currency': self.currency,
            'gateway_transaction_id': self.gateway_transaction_id,
            'gateway_payment_intent_id': self.gateway_payment_intent_id,
            'status': self.status,
            'transaction_type': self.transaction_type,
            'payment_method_type': self.payment_method_type,
            'gateway_fee': self.gateway_fee,
            'processing_fee': self.processing_fee,
            'net_amount': self.net_amount,
            'risk_score': self.risk_score,
            'fraud_check_status': self.fraud_check_status,
            'error_code': self.error_code,
            'error_message': self.error_message,
            'initiated_at': self.initiated_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'processing_time_seconds': self.processing_time_seconds,
            'gateway_response': json.loads(self.gateway_response) if self.gateway_response else {},
            'transaction_metadata': json.loads(self.transaction_metadata) if self.transaction_metadata else {},
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class CurrencyExchange(db.Model):
    """Currency exchange rates for multi-market support"""
    __tablename__ = 'currency_exchanges'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Currency pair
    from_currency = db.Column(db.String(3), nullable=False)  # USD
    to_currency = db.Column(db.String(3), nullable=False)    # INR
    
    # Exchange rate
    exchange_rate = db.Column(db.Float, nullable=False)  # 1 USD = 83.50 INR
    
    # Rate metadata
    source = db.Column(db.String(100))  # 'xe.com', 'fixer.io', 'manual'
    rate_type = db.Column(db.String(50), default='mid')  # 'buy', 'sell', 'mid'
    
    # Validity
    valid_from = db.Column(db.DateTime, default=datetime.utcnow)
    valid_until = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Usage tracking
    last_used_at = db.Column(db.DateTime)
    usage_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'from_currency': self.from_currency,
            'to_currency': self.to_currency,
            'exchange_rate': self.exchange_rate,
            'source': self.source,
            'rate_type': self.rate_type,
            'valid_from': self.valid_from.isoformat(),
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'is_active': self.is_active,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'usage_count': self.usage_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class PaymentSubscription(db.Model):
    """Subscription and recurring payment management"""
    __tablename__ = 'payment_subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.String(100), unique=True, nullable=False)
    
    # User and payment method
    user_id = db.Column(db.Integer, nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'), nullable=False)
    gateway_id = db.Column(db.Integer, db.ForeignKey('payment_gateways.id'), nullable=False)
    
    # Subscription details
    subscription_type = db.Column(db.String(100), nullable=False)  # 'premium_styling', 'vip_access'
    plan_name = db.Column(db.String(200))
    
    # Billing
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    billing_cycle = db.Column(db.String(50), nullable=False)  # 'monthly', 'quarterly', 'yearly'
    
    # Gateway subscription ID
    gateway_subscription_id = db.Column(db.String(200))
    
    # Status
    status = db.Column(db.String(50), default='active')  # active, paused, cancelled, expired
    
    # Billing dates
    start_date = db.Column(db.DateTime, nullable=False)
    next_billing_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    
    # Trial period
    trial_start_date = db.Column(db.DateTime)
    trial_end_date = db.Column(db.DateTime)
    is_trial_active = db.Column(db.Boolean, default=False)
    
    # Billing history
    successful_payments = db.Column(db.Integer, default=0)
    failed_payments = db.Column(db.Integer, default=0)
    total_amount_paid = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payment_method = db.relationship('PaymentMethod', backref='subscriptions')
    gateway = db.relationship('PaymentGateway', backref='subscriptions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'subscription_id': self.subscription_id,
            'user_id': self.user_id,
            'payment_method_id': self.payment_method_id,
            'gateway_id': self.gateway_id,
            'gateway_name': self.gateway.name if self.gateway else None,
            'subscription_type': self.subscription_type,
            'plan_name': self.plan_name,
            'amount': self.amount,
            'currency': self.currency,
            'billing_cycle': self.billing_cycle,
            'gateway_subscription_id': self.gateway_subscription_id,
            'status': self.status,
            'start_date': self.start_date.isoformat(),
            'next_billing_date': self.next_billing_date.isoformat() if self.next_billing_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'trial_start_date': self.trial_start_date.isoformat() if self.trial_start_date else None,
            'trial_end_date': self.trial_end_date.isoformat() if self.trial_end_date else None,
            'is_trial_active': self.is_trial_active,
            'successful_payments': self.successful_payments,
            'failed_payments': self.failed_payments,
            'total_amount_paid': self.total_amount_paid,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class FraudDetection(db.Model):
    """Fraud detection and risk assessment"""
    __tablename__ = 'fraud_detections'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('payment_transactions.id'), nullable=False)
    
    # Risk assessment
    risk_score = db.Column(db.Float, nullable=False)  # 0.0 to 1.0
    risk_level = db.Column(db.String(50))  # 'low', 'medium', 'high', 'critical'
    
    # Risk factors
    risk_factors = db.Column(db.Text)  # JSON array of risk factors
    
    # Fraud rules triggered
    rules_triggered = db.Column(db.Text)  # JSON array of rule IDs
    
    # Device and location analysis
    device_fingerprint = db.Column(db.String(500))
    ip_address = db.Column(db.String(45))
    geolocation = db.Column(db.Text)  # JSON object
    
    # Behavioral analysis
    velocity_check = db.Column(db.String(50))  # 'passed', 'flagged', 'failed'
    pattern_analysis = db.Column(db.String(50))  # 'normal', 'suspicious', 'anomalous'
    
    # Decision
    decision = db.Column(db.String(50), nullable=False)  # 'approve', 'review', 'decline'
    decision_reason = db.Column(db.Text)
    
    # Manual review
    requires_manual_review = db.Column(db.Boolean, default=False)
    reviewed_by = db.Column(db.Integer)  # Admin user ID
    review_decision = db.Column(db.String(50))  # 'approve', 'decline'
    review_notes = db.Column(db.Text)
    reviewed_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transaction = db.relationship('PaymentTransaction', backref='fraud_detection')
    
    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'risk_score': self.risk_score,
            'risk_level': self.risk_level,
            'risk_factors': json.loads(self.risk_factors) if self.risk_factors else [],
            'rules_triggered': json.loads(self.rules_triggered) if self.rules_triggered else [],
            'device_fingerprint': self.device_fingerprint,
            'ip_address': self.ip_address,
            'geolocation': json.loads(self.geolocation) if self.geolocation else {},
            'velocity_check': self.velocity_check,
            'pattern_analysis': self.pattern_analysis,
            'decision': self.decision,
            'decision_reason': self.decision_reason,
            'requires_manual_review': self.requires_manual_review,
            'reviewed_by': self.reviewed_by,
            'review_decision': self.review_decision,
            'review_notes': self.review_notes,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

