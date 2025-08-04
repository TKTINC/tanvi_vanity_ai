from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Market(db.Model):
    """Market configuration for US and India"""
    __tablename__ = 'markets'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), unique=True, nullable=False)  # 'US', 'IN'
    name = db.Column(db.String(50), nullable=False)  # 'United States', 'India'
    currency = db.Column(db.String(5), nullable=False)  # 'USD', 'INR'
    currency_symbol = db.Column(db.String(5), nullable=False)  # '$', '₹'
    
    # Market-specific configuration
    tax_rate = db.Column(db.Float, default=0.0)
    shipping_base_cost = db.Column(db.Float, default=0.0)
    free_shipping_threshold = db.Column(db.Float, default=0.0)
    
    # Payment methods available in this market
    payment_methods = db.Column(db.Text)  # JSON string
    
    # Shipping options
    shipping_options = db.Column(db.Text)  # JSON string
    
    # Market preferences
    preferences = db.Column(db.Text)  # JSON string for market-specific settings
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'currency': self.currency,
            'currency_symbol': self.currency_symbol,
            'tax_rate': self.tax_rate,
            'shipping_base_cost': self.shipping_base_cost,
            'free_shipping_threshold': self.free_shipping_threshold,
            'payment_methods': json.loads(self.payment_methods) if self.payment_methods else [],
            'shipping_options': json.loads(self.shipping_options) if self.shipping_options else [],
            'preferences': json.loads(self.preferences) if self.preferences else {},
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Merchant(db.Model):
    """Merchant/retailer information"""
    __tablename__ = 'merchants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)  # 'zara', 'myntra'
    market_id = db.Column(db.Integer, db.ForeignKey('markets.id'), nullable=False)
    
    # Merchant details
    website_url = db.Column(db.String(200))
    logo_url = db.Column(db.String(200))
    description = db.Column(db.Text)
    
    # Integration details
    api_endpoint = db.Column(db.String(200))
    api_key = db.Column(db.String(200))
    integration_type = db.Column(db.String(50))  # 'api', 'affiliate', 'scraping'
    
    # Merchant capabilities
    supports_real_time_inventory = db.Column(db.Boolean, default=False)
    supports_price_updates = db.Column(db.Boolean, default=False)
    supports_order_tracking = db.Column(db.Boolean, default=False)
    
    # Commission and fees
    commission_rate = db.Column(db.Float, default=0.0)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    market = db.relationship('Market', backref='merchants')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'market_id': self.market_id,
            'market': self.market.to_dict() if self.market else None,
            'website_url': self.website_url,
            'logo_url': self.logo_url,
            'description': self.description,
            'integration_type': self.integration_type,
            'supports_real_time_inventory': self.supports_real_time_inventory,
            'supports_price_updates': self.supports_price_updates,
            'supports_order_tracking': self.supports_order_tracking,
            'commission_rate': self.commission_rate,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Product(db.Model):
    """Product catalog with multi-market support"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchants.id'), nullable=False)
    
    # Product identification
    sku = db.Column(db.String(100), nullable=False)
    merchant_product_id = db.Column(db.String(100))  # ID from merchant system
    
    # Basic product info
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    brand = db.Column(db.String(100))
    
    # Product categorization
    category = db.Column(db.String(100))  # 'tops', 'bottoms', 'dresses', etc.
    subcategory = db.Column(db.String(100))  # 'blouses', 'jeans', 'casual-dresses'
    tags = db.Column(db.Text)  # JSON array of tags
    
    # Pricing
    original_price = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float)
    currency = db.Column(db.String(5), nullable=False)
    
    # Product attributes
    colors = db.Column(db.Text)  # JSON array of available colors
    sizes = db.Column(db.Text)  # JSON array of available sizes
    materials = db.Column(db.Text)  # JSON array of materials
    care_instructions = db.Column(db.Text)
    
    # Images and media
    primary_image_url = db.Column(db.String(300))
    additional_images = db.Column(db.Text)  # JSON array of image URLs
    
    # Inventory and availability
    stock_quantity = db.Column(db.Integer, default=0)
    is_in_stock = db.Column(db.Boolean, default=True)
    low_stock_threshold = db.Column(db.Integer, default=5)
    
    # SEO and search
    search_keywords = db.Column(db.Text)  # JSON array of keywords
    
    # Product URLs
    product_url = db.Column(db.String(300))  # Direct link to product on merchant site
    affiliate_url = db.Column(db.String(300))  # Affiliate tracking URL
    
    # AI and styling data
    style_tags = db.Column(db.Text)  # JSON array: ['casual', 'work', 'date-night']
    occasion_tags = db.Column(db.Text)  # JSON array: ['office', 'party', 'weekend']
    season_tags = db.Column(db.Text)  # JSON array: ['spring', 'summer', 'fall', 'winter']
    
    # Status and metadata
    is_active = db.Column(db.Boolean, default=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    merchant = db.relationship('Merchant', backref='products')
    
    def to_dict(self):
        return {
            'id': self.id,
            'merchant_id': self.merchant_id,
            'merchant': self.merchant.to_dict() if self.merchant else None,
            'sku': self.sku,
            'merchant_product_id': self.merchant_product_id,
            'name': self.name,
            'description': self.description,
            'brand': self.brand,
            'category': self.category,
            'subcategory': self.subcategory,
            'tags': json.loads(self.tags) if self.tags else [],
            'original_price': self.original_price,
            'sale_price': self.sale_price,
            'current_price': self.sale_price if self.sale_price else self.original_price,
            'currency': self.currency,
            'colors': json.loads(self.colors) if self.colors else [],
            'sizes': json.loads(self.sizes) if self.sizes else [],
            'materials': json.loads(self.materials) if self.materials else [],
            'care_instructions': self.care_instructions,
            'primary_image_url': self.primary_image_url,
            'additional_images': json.loads(self.additional_images) if self.additional_images else [],
            'stock_quantity': self.stock_quantity,
            'is_in_stock': self.is_in_stock,
            'low_stock_threshold': self.low_stock_threshold,
            'search_keywords': json.loads(self.search_keywords) if self.search_keywords else [],
            'product_url': self.product_url,
            'affiliate_url': self.affiliate_url,
            'style_tags': json.loads(self.style_tags) if self.style_tags else [],
            'occasion_tags': json.loads(self.occasion_tags) if self.occasion_tags else [],
            'season_tags': json.loads(self.season_tags) if self.season_tags else [],
            'is_active': self.is_active,
            'last_updated': self.last_updated.isoformat(),
            'created_at': self.created_at.isoformat()
        }

class ShoppingCart(db.Model):
    """Shopping cart for users"""
    __tablename__ = 'shopping_carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Reference to WS1 user
    market_id = db.Column(db.Integer, db.ForeignKey('markets.id'), nullable=False)
    
    # Cart metadata
    session_id = db.Column(db.String(100))  # For anonymous users
    
    # Cart totals (calculated)
    subtotal = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    shipping_cost = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    
    # Cart status
    status = db.Column(db.String(20), default='active')  # 'active', 'abandoned', 'converted'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    market = db.relationship('Market', backref='shopping_carts')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'market_id': self.market_id,
            'market': self.market.to_dict() if self.market else None,
            'session_id': self.session_id,
            'subtotal': self.subtotal,
            'tax_amount': self.tax_amount,
            'shipping_cost': self.shipping_cost,
            'discount_amount': self.discount_amount,
            'total_amount': self.total_amount,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class CartItem(db.Model):
    """Items in shopping cart"""
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('shopping_carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Item details
    quantity = db.Column(db.Integer, default=1)
    selected_color = db.Column(db.String(50))
    selected_size = db.Column(db.String(20))
    
    # Pricing at time of adding to cart
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    
    # Special offers or discounts applied
    discount_applied = db.Column(db.Float, default=0.0)
    
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cart = db.relationship('ShoppingCart', backref='items')
    product = db.relationship('Product', backref='cart_items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'selected_color': self.selected_color,
            'selected_size': self.selected_size,
            'unit_price': self.unit_price,
            'total_price': self.total_price,
            'discount_applied': self.discount_applied,
            'added_at': self.added_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Order(db.Model):
    """Order management"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)  # Reference to WS1 user
    market_id = db.Column(db.Integer, db.ForeignKey('markets.id'), nullable=False)
    
    # Order totals
    subtotal = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, default=0.0)
    shipping_cost = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, nullable=False)
    
    # Order status
    status = db.Column(db.String(30), default='pending')  # 'pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled', 'returned'
    
    # Shipping information
    shipping_address = db.Column(db.Text)  # JSON object
    billing_address = db.Column(db.Text)  # JSON object
    shipping_method = db.Column(db.String(50))
    tracking_number = db.Column(db.String(100))
    
    # Payment information
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(30), default='pending')  # 'pending', 'completed', 'failed', 'refunded'
    payment_reference = db.Column(db.String(100))
    
    # Timestamps
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    shipped_date = db.Column(db.DateTime)
    delivered_date = db.Column(db.DateTime)
    
    # Special instructions
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    market = db.relationship('Market', backref='orders')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'market_id': self.market_id,
            'market': self.market.to_dict() if self.market else None,
            'subtotal': self.subtotal,
            'tax_amount': self.tax_amount,
            'shipping_cost': self.shipping_cost,
            'discount_amount': self.discount_amount,
            'total_amount': self.total_amount,
            'status': self.status,
            'shipping_address': json.loads(self.shipping_address) if self.shipping_address else {},
            'billing_address': json.loads(self.billing_address) if self.billing_address else {},
            'shipping_method': self.shipping_method,
            'tracking_number': self.tracking_number,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'payment_reference': self.payment_reference,
            'order_date': self.order_date.isoformat(),
            'shipped_date': self.shipped_date.isoformat() if self.shipped_date else None,
            'delivered_date': self.delivered_date.isoformat() if self.delivered_date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class OrderItem(db.Model):
    """Items in an order"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Item details at time of purchase
    quantity = db.Column(db.Integer, nullable=False)
    selected_color = db.Column(db.String(50))
    selected_size = db.Column(db.String(20))
    
    # Pricing at time of purchase
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    discount_applied = db.Column(db.Float, default=0.0)
    
    # Item status (for partial shipments)
    status = db.Column(db.String(30), default='pending')  # 'pending', 'processing', 'shipped', 'delivered', 'cancelled', 'returned'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', backref='items')
    product = db.relationship('Product', backref='order_items')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'selected_color': self.selected_color,
            'selected_size': self.selected_size,
            'unit_price': self.unit_price,
            'total_price': self.total_price,
            'discount_applied': self.discount_applied,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

