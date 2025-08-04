from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from src.models.ecommerce_models import db

class ProductCategory(db.Model):
    """Product category hierarchy for better organization"""
    __tablename__ = 'product_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    
    # Category metadata
    description = db.Column(db.Text)
    image_url = db.Column(db.String(300))
    sort_order = db.Column(db.Integer, default=0)
    
    # SEO and display
    display_name = db.Column(db.String(100))
    meta_description = db.Column(db.Text)
    
    # Category attributes for filtering
    attributes = db.Column(db.Text)  # JSON: size_types, color_families, etc.
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    parent = db.relationship('ProductCategory', remote_side=[id], backref='children')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'parent_id': self.parent_id,
            'parent': self.parent.to_dict() if self.parent else None,
            'description': self.description,
            'image_url': self.image_url,
            'sort_order': self.sort_order,
            'display_name': self.display_name,
            'meta_description': self.meta_description,
            'attributes': json.loads(self.attributes) if self.attributes else {},
            'is_active': self.is_active,
            'children_count': len(self.children),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ProductBrand(db.Model):
    """Brand information for products"""
    __tablename__ = 'product_brands'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    
    # Brand details
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(300))
    website_url = db.Column(db.String(200))
    
    # Brand positioning
    price_range = db.Column(db.String(20))  # 'budget', 'mid-range', 'premium', 'luxury'
    target_demographic = db.Column(db.String(100))  # 'teens', 'young-adults', 'professionals'
    style_category = db.Column(db.String(100))  # 'fast-fashion', 'sustainable', 'luxury'
    
    # Brand metrics
    popularity_score = db.Column(db.Float, default=0.0)
    quality_rating = db.Column(db.Float, default=0.0)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'logo_url': self.logo_url,
            'website_url': self.website_url,
            'price_range': self.price_range,
            'target_demographic': self.target_demographic,
            'style_category': self.style_category,
            'popularity_score': self.popularity_score,
            'quality_rating': self.quality_rating,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ProductReview(db.Model):
    """Product reviews and ratings"""
    __tablename__ = 'product_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)  # Reference to WS1 user
    
    # Review content
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    title = db.Column(db.String(200))
    review_text = db.Column(db.Text)
    
    # Review metadata
    verified_purchase = db.Column(db.Boolean, default=False)
    helpful_votes = db.Column(db.Integer, default=0)
    total_votes = db.Column(db.Integer, default=0)
    
    # Detailed ratings
    fit_rating = db.Column(db.Integer)  # 1-5 for clothing fit
    quality_rating = db.Column(db.Integer)  # 1-5 for material quality
    value_rating = db.Column(db.Integer)  # 1-5 for value for money
    
    # Review attributes
    size_purchased = db.Column(db.String(20))
    color_purchased = db.Column(db.String(50))
    
    # Status
    is_approved = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref='reviews')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'title': self.title,
            'review_text': self.review_text,
            'verified_purchase': self.verified_purchase,
            'helpful_votes': self.helpful_votes,
            'total_votes': self.total_votes,
            'helpfulness_ratio': self.helpful_votes / max(self.total_votes, 1),
            'fit_rating': self.fit_rating,
            'quality_rating': self.quality_rating,
            'value_rating': self.value_rating,
            'size_purchased': self.size_purchased,
            'color_purchased': self.color_purchased,
            'is_approved': self.is_approved,
            'is_featured': self.is_featured,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ProductInventory(db.Model):
    """Detailed inventory tracking for products"""
    __tablename__ = 'product_inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Variant details
    color = db.Column(db.String(50))
    size = db.Column(db.String(20))
    sku_variant = db.Column(db.String(100), unique=True)  # Unique SKU for this variant
    
    # Inventory levels
    quantity_available = db.Column(db.Integer, default=0)
    quantity_reserved = db.Column(db.Integer, default=0)  # In carts but not purchased
    quantity_sold = db.Column(db.Integer, default=0)
    
    # Inventory thresholds
    low_stock_threshold = db.Column(db.Integer, default=5)
    reorder_point = db.Column(db.Integer, default=10)
    max_stock_level = db.Column(db.Integer, default=100)
    
    # Pricing for this variant
    variant_price_adjustment = db.Column(db.Float, default=0.0)  # +/- from base price
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_backorderable = db.Column(db.Boolean, default=False)
    
    # Timestamps
    last_restocked = db.Column(db.DateTime)
    last_sold = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref='inventory_variants')
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'color': self.color,
            'size': self.size,
            'sku_variant': self.sku_variant,
            'quantity_available': self.quantity_available,
            'quantity_reserved': self.quantity_reserved,
            'quantity_sold': self.quantity_sold,
            'total_quantity': self.quantity_available + self.quantity_reserved,
            'low_stock_threshold': self.low_stock_threshold,
            'reorder_point': self.reorder_point,
            'max_stock_level': self.max_stock_level,
            'variant_price_adjustment': self.variant_price_adjustment,
            'is_active': self.is_active,
            'is_backorderable': self.is_backorderable,
            'is_low_stock': self.quantity_available <= self.low_stock_threshold,
            'needs_reorder': self.quantity_available <= self.reorder_point,
            'last_restocked': self.last_restocked.isoformat() if self.last_restocked else None,
            'last_sold': self.last_sold.isoformat() if self.last_sold else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ProductRecommendation(db.Model):
    """AI-powered product recommendations"""
    __tablename__ = 'product_recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Reference to WS1 user
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Recommendation metadata
    recommendation_type = db.Column(db.String(50), nullable=False)  # 'ai_styling', 'similar_items', 'trending', 'personalized'
    confidence_score = db.Column(db.Float, default=0.0)  # 0.0 - 1.0
    
    # Recommendation context
    context = db.Column(db.Text)  # JSON: occasion, weather, style_preference, etc.
    reasoning = db.Column(db.Text)  # Why this was recommended
    
    # Recommendation performance
    shown_count = db.Column(db.Integer, default=0)
    clicked_count = db.Column(db.Integer, default=0)
    purchased_count = db.Column(db.Integer, default=0)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    expires_at = db.Column(db.DateTime)  # When recommendation expires
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref='recommendations')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'recommendation_type': self.recommendation_type,
            'confidence_score': self.confidence_score,
            'context': json.loads(self.context) if self.context else {},
            'reasoning': self.reasoning,
            'shown_count': self.shown_count,
            'clicked_count': self.clicked_count,
            'purchased_count': self.purchased_count,
            'click_through_rate': self.clicked_count / max(self.shown_count, 1),
            'conversion_rate': self.purchased_count / max(self.clicked_count, 1),
            'is_active': self.is_active,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_expired': self.expires_at < datetime.utcnow() if self.expires_at else False,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ProductCollection(db.Model):
    """Curated product collections (e.g., "Summer Essentials", "Work Wardrobe")"""
    __tablename__ = 'product_collections'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    
    # Collection details
    description = db.Column(db.Text)
    image_url = db.Column(db.String(300))
    banner_image_url = db.Column(db.String(300))
    
    # Collection metadata
    collection_type = db.Column(db.String(50))  # 'seasonal', 'occasion', 'style', 'trending'
    target_market = db.Column(db.String(10))  # 'US', 'IN', 'ALL'
    
    # Collection attributes
    tags = db.Column(db.Text)  # JSON array of tags
    style_attributes = db.Column(db.Text)  # JSON: target_age, style_type, etc.
    
    # Collection status
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    
    # Time-based collections
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'image_url': self.image_url,
            'banner_image_url': self.banner_image_url,
            'collection_type': self.collection_type,
            'target_market': self.target_market,
            'tags': json.loads(self.tags) if self.tags else [],
            'style_attributes': json.loads(self.style_attributes) if self.style_attributes else {},
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'sort_order': self.sort_order,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_current': (
                (not self.start_date or self.start_date <= datetime.utcnow()) and
                (not self.end_date or self.end_date >= datetime.utcnow())
            ) if self.is_active else False,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class CollectionProduct(db.Model):
    """Many-to-many relationship between collections and products"""
    __tablename__ = 'collection_products'
    
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('product_collections.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Product position in collection
    sort_order = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    
    # Collection-specific product metadata
    collection_notes = db.Column(db.Text)  # Why this product is in this collection
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    collection = db.relationship('ProductCollection', backref='collection_products')
    product = db.relationship('Product', backref='product_collections')
    
    def to_dict(self):
        return {
            'id': self.id,
            'collection_id': self.collection_id,
            'product_id': self.product_id,
            'collection': self.collection.to_dict() if self.collection else None,
            'product': self.product.to_dict() if self.product else None,
            'sort_order': self.sort_order,
            'is_featured': self.is_featured,
            'collection_notes': self.collection_notes,
            'created_at': self.created_at.isoformat()
        }

