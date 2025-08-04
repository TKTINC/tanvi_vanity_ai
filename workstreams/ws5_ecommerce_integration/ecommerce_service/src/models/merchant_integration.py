from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import requests
from src.models.ecommerce_models import db

class MerchantAPI(db.Model):
    """Merchant API configuration and credentials"""
    __tablename__ = 'merchant_apis'
    
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchants.id'), nullable=False)
    
    # API Configuration
    api_name = db.Column(db.String(100), nullable=False)  # 'REST API', 'GraphQL', 'Webhook'
    base_url = db.Column(db.String(300), nullable=False)
    api_version = db.Column(db.String(20))
    
    # Authentication
    auth_type = db.Column(db.String(50), nullable=False)  # 'api_key', 'oauth', 'basic', 'bearer'
    api_key = db.Column(db.String(500))
    api_secret = db.Column(db.String(500))
    access_token = db.Column(db.String(500))
    refresh_token = db.Column(db.String(500))
    token_expires_at = db.Column(db.DateTime)
    
    # API Capabilities
    supports_product_sync = db.Column(db.Boolean, default=False)
    supports_inventory_sync = db.Column(db.Boolean, default=False)
    supports_price_sync = db.Column(db.Boolean, default=False)
    supports_order_creation = db.Column(db.Boolean, default=False)
    supports_order_tracking = db.Column(db.Boolean, default=False)
    supports_webhooks = db.Column(db.Boolean, default=False)
    
    # Rate Limiting
    rate_limit_per_minute = db.Column(db.Integer, default=60)
    rate_limit_per_hour = db.Column(db.Integer, default=1000)
    
    # API Status
    is_active = db.Column(db.Boolean, default=True)
    last_successful_call = db.Column(db.DateTime)
    last_failed_call = db.Column(db.DateTime)
    consecutive_failures = db.Column(db.Integer, default=0)
    
    # Configuration
    custom_headers = db.Column(db.Text)  # JSON object
    custom_parameters = db.Column(db.Text)  # JSON object
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    merchant = db.relationship('Merchant', backref='api_configs')
    
    def to_dict(self):
        return {
            'id': self.id,
            'merchant_id': self.merchant_id,
            'merchant_name': self.merchant.name if self.merchant else None,
            'api_name': self.api_name,
            'base_url': self.base_url,
            'api_version': self.api_version,
            'auth_type': self.auth_type,
            'supports_product_sync': self.supports_product_sync,
            'supports_inventory_sync': self.supports_inventory_sync,
            'supports_price_sync': self.supports_price_sync,
            'supports_order_creation': self.supports_order_creation,
            'supports_order_tracking': self.supports_order_tracking,
            'supports_webhooks': self.supports_webhooks,
            'rate_limit_per_minute': self.rate_limit_per_minute,
            'rate_limit_per_hour': self.rate_limit_per_hour,
            'is_active': self.is_active,
            'last_successful_call': self.last_successful_call.isoformat() if self.last_successful_call else None,
            'last_failed_call': self.last_failed_call.isoformat() if self.last_failed_call else None,
            'consecutive_failures': self.consecutive_failures,
            'health_status': 'healthy' if self.consecutive_failures < 3 else 'degraded' if self.consecutive_failures < 10 else 'unhealthy',
            'custom_headers': json.loads(self.custom_headers) if self.custom_headers else {},
            'custom_parameters': json.loads(self.custom_parameters) if self.custom_parameters else {},
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ProductSync(db.Model):
    """Product synchronization tracking"""
    __tablename__ = 'product_syncs'
    
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchants.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    
    # Sync details
    sync_type = db.Column(db.String(50), nullable=False)  # 'full', 'incremental', 'single_product'
    sync_status = db.Column(db.String(30), default='pending')  # 'pending', 'running', 'completed', 'failed'
    
    # Sync metadata
    external_product_id = db.Column(db.String(100))  # Product ID in merchant system
    sync_direction = db.Column(db.String(20), default='import')  # 'import', 'export', 'bidirectional'
    
    # Sync results
    products_processed = db.Column(db.Integer, default=0)
    products_created = db.Column(db.Integer, default=0)
    products_updated = db.Column(db.Integer, default=0)
    products_failed = db.Column(db.Integer, default=0)
    
    # Error handling
    error_message = db.Column(db.Text)
    error_details = db.Column(db.Text)  # JSON object with detailed errors
    
    # Timing
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    duration_seconds = db.Column(db.Integer)
    
    # Next sync scheduling
    next_sync_at = db.Column(db.DateTime)
    sync_frequency = db.Column(db.String(20))  # 'hourly', 'daily', 'weekly', 'manual'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    merchant = db.relationship('Merchant', backref='product_syncs')
    product = db.relationship('Product', backref='sync_records')
    
    def to_dict(self):
        return {
            'id': self.id,
            'merchant_id': self.merchant_id,
            'merchant_name': self.merchant.name if self.merchant else None,
            'product_id': self.product_id,
            'sync_type': self.sync_type,
            'sync_status': self.sync_status,
            'external_product_id': self.external_product_id,
            'sync_direction': self.sync_direction,
            'products_processed': self.products_processed,
            'products_created': self.products_created,
            'products_updated': self.products_updated,
            'products_failed': self.products_failed,
            'success_rate': (self.products_created + self.products_updated) / max(self.products_processed, 1) if self.products_processed > 0 else 0,
            'error_message': self.error_message,
            'error_details': json.loads(self.error_details) if self.error_details else {},
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration_seconds': self.duration_seconds,
            'next_sync_at': self.next_sync_at.isoformat() if self.next_sync_at else None,
            'sync_frequency': self.sync_frequency,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class MerchantWebhook(db.Model):
    """Webhook configuration for real-time merchant updates"""
    __tablename__ = 'merchant_webhooks'
    
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchants.id'), nullable=False)
    
    # Webhook configuration
    webhook_url = db.Column(db.String(300), nullable=False)  # Our endpoint URL
    merchant_webhook_id = db.Column(db.String(100))  # Webhook ID in merchant system
    
    # Event types
    event_types = db.Column(db.Text)  # JSON array: ['product.created', 'product.updated', 'inventory.changed']
    
    # Security
    secret_key = db.Column(db.String(200))
    signature_header = db.Column(db.String(100))  # Header name for signature verification
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    last_received = db.Column(db.DateTime)
    total_received = db.Column(db.Integer, default=0)
    total_processed = db.Column(db.Integer, default=0)
    total_failed = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    merchant = db.relationship('Merchant', backref='webhooks')
    
    def to_dict(self):
        return {
            'id': self.id,
            'merchant_id': self.merchant_id,
            'merchant_name': self.merchant.name if self.merchant else None,
            'webhook_url': self.webhook_url,
            'merchant_webhook_id': self.merchant_webhook_id,
            'event_types': json.loads(self.event_types) if self.event_types else [],
            'secret_key': '***' if self.secret_key else None,
            'signature_header': self.signature_header,
            'is_active': self.is_active,
            'last_received': self.last_received.isoformat() if self.last_received else None,
            'total_received': self.total_received,
            'total_processed': self.total_processed,
            'total_failed': self.total_failed,
            'success_rate': self.total_processed / max(self.total_received, 1) if self.total_received > 0 else 0,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class MerchantAdapter:
    """Base class for merchant API adapters"""
    
    def __init__(self, merchant_api):
        self.merchant_api = merchant_api
        self.merchant = merchant_api.merchant
        self.session = requests.Session()
        self._setup_authentication()
    
    def _setup_authentication(self):
        """Setup authentication for API calls"""
        if self.merchant_api.auth_type == 'api_key':
            self.session.headers.update({
                'X-API-Key': self.merchant_api.api_key
            })
        elif self.merchant_api.auth_type == 'bearer':
            self.session.headers.update({
                'Authorization': f'Bearer {self.merchant_api.access_token}'
            })
        elif self.merchant_api.auth_type == 'basic':
            self.session.auth = (self.merchant_api.api_key, self.merchant_api.api_secret)
        
        # Add custom headers
        if self.merchant_api.custom_headers:
            custom_headers = json.loads(self.merchant_api.custom_headers)
            self.session.headers.update(custom_headers)
    
    def _make_request(self, method, endpoint, **kwargs):
        """Make authenticated API request with error handling"""
        url = f"{self.merchant_api.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Update success timestamp
            self.merchant_api.last_successful_call = datetime.utcnow()
            self.merchant_api.consecutive_failures = 0
            db.session.commit()
            
            response.raise_for_status()
            return response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            # Update failure tracking
            self.merchant_api.last_failed_call = datetime.utcnow()
            self.merchant_api.consecutive_failures += 1
            db.session.commit()
            
            raise Exception(f"API request failed: {str(e)}")
    
    def get_products(self, limit=100, offset=0):
        """Get products from merchant API"""
        raise NotImplementedError("Subclasses must implement get_products")
    
    def get_product(self, external_id):
        """Get single product from merchant API"""
        raise NotImplementedError("Subclasses must implement get_product")
    
    def update_inventory(self, external_id, quantity):
        """Update product inventory"""
        raise NotImplementedError("Subclasses must implement update_inventory")
    
    def create_order(self, order_data):
        """Create order in merchant system"""
        raise NotImplementedError("Subclasses must implement create_order")
    
    def get_order_status(self, external_order_id):
        """Get order status from merchant system"""
        raise NotImplementedError("Subclasses must implement get_order_status")

class ZaraUSAdapter(MerchantAdapter):
    """Zara US API adapter (simulated)"""
    
    def get_products(self, limit=100, offset=0):
        """Get products from Zara US (simulated)"""
        # This would be actual Zara API call
        # For now, return simulated data
        return {
            "products": [
                {
                    "id": "ZARA-US-001",
                    "name": "Black Midi Dress",
                    "description": "Elegant black midi dress perfect for work or evening",
                    "price": 79.90,
                    "currency": "USD",
                    "category": "dresses",
                    "brand": "Zara",
                    "colors": ["black", "navy"],
                    "sizes": ["XS", "S", "M", "L", "XL"],
                    "images": ["https://static.zara.net/photos/dress1.jpg"],
                    "stock": 25,
                    "url": "https://www.zara.com/us/en/dress-001.html"
                }
            ],
            "total": 1,
            "limit": limit,
            "offset": offset
        }
    
    def get_product(self, external_id):
        """Get single product from Zara US"""
        return {
            "id": external_id,
            "name": "Black Midi Dress",
            "description": "Elegant black midi dress perfect for work or evening",
            "price": 79.90,
            "currency": "USD",
            "category": "dresses",
            "brand": "Zara",
            "colors": ["black", "navy"],
            "sizes": ["XS", "S", "M", "L", "XL"],
            "images": ["https://static.zara.net/photos/dress1.jpg"],
            "stock": 25,
            "url": "https://www.zara.com/us/en/dress-001.html"
        }

class MyntraAdapter(MerchantAdapter):
    """Myntra API adapter (simulated)"""
    
    def get_products(self, limit=100, offset=0):
        """Get products from Myntra (simulated)"""
        return {
            "products": [
                {
                    "id": "MYNTRA-001",
                    "name": "Cotton Anarkali Kurta",
                    "description": "Beautiful cotton anarkali kurta with embroidered details",
                    "price": 999.0,
                    "original_price": 1299.0,
                    "currency": "INR",
                    "category": "ethnic-wear",
                    "brand": "Libas",
                    "colors": ["pink", "blue", "white"],
                    "sizes": ["S", "M", "L", "XL", "XXL"],
                    "images": ["https://assets.myntra.com/kurta1.jpg"],
                    "stock": 50,
                    "url": "https://www.myntra.com/kurta-001"
                }
            ],
            "total": 1,
            "limit": limit,
            "offset": offset
        }
    
    def get_product(self, external_id):
        """Get single product from Myntra"""
        return {
            "id": external_id,
            "name": "Cotton Anarkali Kurta",
            "description": "Beautiful cotton anarkali kurta with embroidered details",
            "price": 999.0,
            "original_price": 1299.0,
            "currency": "INR",
            "category": "ethnic-wear",
            "brand": "Libas",
            "colors": ["pink", "blue", "white"],
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "images": ["https://assets.myntra.com/kurta1.jpg"],
            "stock": 50,
            "url": "https://www.myntra.com/kurta-001"
        }

def get_merchant_adapter(merchant_code):
    """Factory function to get appropriate merchant adapter"""
    from src.models.ecommerce_models import Merchant
    
    merchant = Merchant.query.filter_by(code=merchant_code, is_active=True).first()
    if not merchant:
        raise ValueError(f"Merchant {merchant_code} not found")
    
    # Get API configuration
    api_config = MerchantAPI.query.filter_by(merchant_id=merchant.id, is_active=True).first()
    if not api_config:
        raise ValueError(f"No API configuration found for merchant {merchant_code}")
    
    # Return appropriate adapter
    if merchant_code == 'zara_us':
        return ZaraUSAdapter(api_config)
    elif merchant_code == 'myntra':
        return MyntraAdapter(api_config)
    else:
        # Return generic adapter for other merchants
        return MerchantAdapter(api_config)

