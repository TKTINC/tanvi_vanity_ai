"""
WS3-P1: Computer Vision Foundation & Item Recognition
Computer Vision Models for Tanvi Vanity Agent
"We girls have no time" - Instant visual wardrobe intelligence!
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class WardrobeItem(db.Model):
    """
    Core wardrobe item model with computer vision capabilities
    "We girls have no time" - Quick visual item recognition!
    """
    __tablename__ = 'wardrobe_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Basic item information
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False, index=True)
    subcategory = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    color_primary = db.Column(db.String(50), nullable=False, index=True)
    color_secondary = db.Column(db.String(50))
    
    # Visual analysis results
    image_url = db.Column(db.String(500))
    image_hash = db.Column(db.String(64), unique=True, index=True)
    
    # Computer vision analysis
    cv_confidence = db.Column(db.Float, default=0.0)  # CV analysis confidence
    cv_category = db.Column(db.String(100))  # CV detected category
    cv_colors = db.Column(db.Text)  # JSON array of detected colors
    cv_patterns = db.Column(db.Text)  # JSON array of detected patterns
    cv_materials = db.Column(db.Text)  # JSON array of detected materials
    cv_style_tags = db.Column(db.Text)  # JSON array of style tags
    
    # Item attributes
    size = db.Column(db.String(20))
    fit_type = db.Column(db.String(50))  # slim, regular, loose, oversized
    occasion_tags = db.Column(db.Text)  # JSON array of occasions
    season_tags = db.Column(db.Text)  # JSON array of seasons
    
    # Usage tracking
    wear_count = db.Column(db.Integer, default=0)
    last_worn = db.Column(db.DateTime)
    favorite = db.Column(db.Boolean, default=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'category': self.category,
            'subcategory': self.subcategory,
            'brand': self.brand,
            'color_primary': self.color_primary,
            'color_secondary': self.color_secondary,
            'image_url': self.image_url,
            'image_hash': self.image_hash,
            'cv_analysis': {
                'confidence': self.cv_confidence,
                'category': self.cv_category,
                'colors': json.loads(self.cv_colors) if self.cv_colors else [],
                'patterns': json.loads(self.cv_patterns) if self.cv_patterns else [],
                'materials': json.loads(self.cv_materials) if self.cv_materials else [],
                'style_tags': json.loads(self.cv_style_tags) if self.cv_style_tags else []
            },
            'attributes': {
                'size': self.size,
                'fit_type': self.fit_type,
                'occasion_tags': json.loads(self.occasion_tags) if self.occasion_tags else [],
                'season_tags': json.loads(self.season_tags) if self.season_tags else []
            },
            'usage': {
                'wear_count': self.wear_count,
                'last_worn': self.last_worn.isoformat() if self.last_worn else None,
                'favorite': self.favorite
            },
            'metadata': {
                'created_at': self.created_at.isoformat(),
                'updated_at': self.updated_at.isoformat()
            }
        }

class ImageAnalysis(db.Model):
    """
    Detailed image analysis results for wardrobe items
    "We girls have no time" - Comprehensive visual analysis in seconds!
    """
    __tablename__ = 'image_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    wardrobe_item_id = db.Column(db.Integer, db.ForeignKey('wardrobe_items.id'), nullable=False)
    
    # Image processing metadata
    image_url = db.Column(db.String(500), nullable=False)
    image_hash = db.Column(db.String(64), nullable=False, index=True)
    image_size = db.Column(db.String(20))  # "1024x768"
    file_size = db.Column(db.Integer)  # bytes
    
    # Computer vision analysis
    analysis_version = db.Column(db.String(20), default="1.0")
    processing_time = db.Column(db.Float)  # seconds
    confidence_score = db.Column(db.Float, nullable=False)
    
    # Visual features
    dominant_colors = db.Column(db.Text)  # JSON array with hex codes and percentages
    color_palette = db.Column(db.Text)  # JSON array of color analysis
    patterns_detected = db.Column(db.Text)  # JSON array of patterns
    textures_detected = db.Column(db.Text)  # JSON array of textures
    
    # Item classification
    category_predictions = db.Column(db.Text)  # JSON array with confidence scores
    style_predictions = db.Column(db.Text)  # JSON array with confidence scores
    material_predictions = db.Column(db.Text)  # JSON array with confidence scores
    
    # Advanced features
    silhouette_analysis = db.Column(db.Text)  # JSON object with silhouette data
    fit_analysis = db.Column(db.Text)  # JSON object with fit characteristics
    quality_assessment = db.Column(db.Text)  # JSON object with quality metrics
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    wardrobe_item = db.relationship('WardrobeItem', backref='image_analyses')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'wardrobe_item_id': self.wardrobe_item_id,
            'image_metadata': {
                'url': self.image_url,
                'hash': self.image_hash,
                'size': self.image_size,
                'file_size': self.file_size
            },
            'analysis_metadata': {
                'version': self.analysis_version,
                'processing_time': self.processing_time,
                'confidence_score': self.confidence_score
            },
            'visual_features': {
                'dominant_colors': json.loads(self.dominant_colors) if self.dominant_colors else [],
                'color_palette': json.loads(self.color_palette) if self.color_palette else [],
                'patterns': json.loads(self.patterns_detected) if self.patterns_detected else [],
                'textures': json.loads(self.textures_detected) if self.textures_detected else []
            },
            'predictions': {
                'categories': json.loads(self.category_predictions) if self.category_predictions else [],
                'styles': json.loads(self.style_predictions) if self.style_predictions else [],
                'materials': json.loads(self.material_predictions) if self.material_predictions else []
            },
            'advanced_analysis': {
                'silhouette': json.loads(self.silhouette_analysis) if self.silhouette_analysis else {},
                'fit': json.loads(self.fit_analysis) if self.fit_analysis else {},
                'quality': json.loads(self.quality_assessment) if self.quality_assessment else {}
            },
            'created_at': self.created_at.isoformat()
        }

class OutfitVisualization(db.Model):
    """
    Outfit visualization and virtual try-on data
    "We girls have no time" - Instant outfit visualization!
    """
    __tablename__ = 'outfit_visualizations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Outfit composition
    outfit_name = db.Column(db.String(200))
    wardrobe_item_ids = db.Column(db.Text, nullable=False)  # JSON array of item IDs
    
    # Visualization data
    visualization_url = db.Column(db.String(500))
    thumbnail_url = db.Column(db.String(500))
    visualization_type = db.Column(db.String(50), default='flat_lay')  # flat_lay, mannequin, model
    
    # Styling information
    occasion = db.Column(db.String(100))
    season = db.Column(db.String(50))
    style_theme = db.Column(db.String(100))
    color_harmony = db.Column(db.String(100))
    
    # AI analysis
    style_score = db.Column(db.Float)  # Overall style compatibility score
    color_score = db.Column(db.Float)  # Color harmony score
    occasion_score = db.Column(db.Float)  # Occasion appropriateness score
    overall_score = db.Column(db.Float)  # Combined score
    
    # User interaction
    user_rating = db.Column(db.Integer)  # 1-5 stars
    worn_count = db.Column(db.Integer, default=0)
    last_worn = db.Column(db.DateTime)
    favorite = db.Column(db.Boolean, default=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'outfit_info': {
                'name': self.outfit_name,
                'item_ids': json.loads(self.wardrobe_item_ids) if self.wardrobe_item_ids else [],
                'occasion': self.occasion,
                'season': self.season,
                'style_theme': self.style_theme,
                'color_harmony': self.color_harmony
            },
            'visualization': {
                'url': self.visualization_url,
                'thumbnail': self.thumbnail_url,
                'type': self.visualization_type
            },
            'ai_scores': {
                'style_score': self.style_score,
                'color_score': self.color_score,
                'occasion_score': self.occasion_score,
                'overall_score': self.overall_score
            },
            'user_data': {
                'rating': self.user_rating,
                'worn_count': self.worn_count,
                'last_worn': self.last_worn.isoformat() if self.last_worn else None,
                'favorite': self.favorite
            },
            'metadata': {
                'created_at': self.created_at.isoformat(),
                'updated_at': self.updated_at.isoformat()
            }
        }

class StyleDetection(db.Model):
    """
    Advanced style detection and analysis
    "We girls have no time" - Instant style recognition!
    """
    __tablename__ = 'style_detections'
    
    id = db.Column(db.Integer, primary_key=True)
    wardrobe_item_id = db.Column(db.Integer, db.ForeignKey('wardrobe_items.id'))
    outfit_visualization_id = db.Column(db.Integer, db.ForeignKey('outfit_visualizations.id'))
    
    # Style analysis
    style_category = db.Column(db.String(100), nullable=False)  # casual, formal, bohemian, etc.
    style_subcategory = db.Column(db.String(100))
    confidence_score = db.Column(db.Float, nullable=False)
    
    # Style attributes
    formality_level = db.Column(db.Integer)  # 1-10 scale
    trendiness_score = db.Column(db.Float)  # 0-1 scale
    versatility_score = db.Column(db.Float)  # 0-1 scale
    uniqueness_score = db.Column(db.Float)  # 0-1 scale
    
    # Style tags and descriptors
    style_tags = db.Column(db.Text)  # JSON array of style descriptors
    aesthetic_tags = db.Column(db.Text)  # JSON array of aesthetic descriptors
    mood_tags = db.Column(db.Text)  # JSON array of mood descriptors
    
    # Trend analysis
    trend_alignment = db.Column(db.Float)  # How well it aligns with current trends
    trend_categories = db.Column(db.Text)  # JSON array of trend categories
    seasonal_relevance = db.Column(db.Float)  # Seasonal appropriateness
    
    # Metadata
    analysis_version = db.Column(db.String(20), default="1.0")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    wardrobe_item = db.relationship('WardrobeItem', backref='style_detections')
    outfit_visualization = db.relationship('OutfitVisualization', backref='style_detections')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'wardrobe_item_id': self.wardrobe_item_id,
            'outfit_visualization_id': self.outfit_visualization_id,
            'style_analysis': {
                'category': self.style_category,
                'subcategory': self.style_subcategory,
                'confidence': self.confidence_score
            },
            'style_metrics': {
                'formality_level': self.formality_level,
                'trendiness_score': self.trendiness_score,
                'versatility_score': self.versatility_score,
                'uniqueness_score': self.uniqueness_score
            },
            'style_descriptors': {
                'style_tags': json.loads(self.style_tags) if self.style_tags else [],
                'aesthetic_tags': json.loads(self.aesthetic_tags) if self.aesthetic_tags else [],
                'mood_tags': json.loads(self.mood_tags) if self.mood_tags else []
            },
            'trend_analysis': {
                'trend_alignment': self.trend_alignment,
                'trend_categories': json.loads(self.trend_categories) if self.trend_categories else [],
                'seasonal_relevance': self.seasonal_relevance
            },
            'metadata': {
                'analysis_version': self.analysis_version,
                'created_at': self.created_at.isoformat()
            }
        }

class VisualSimilarity(db.Model):
    """
    Visual similarity analysis between wardrobe items
    "We girls have no time" - Find similar items instantly!
    """
    __tablename__ = 'visual_similarities'
    
    id = db.Column(db.Integer, primary_key=True)
    item1_id = db.Column(db.Integer, db.ForeignKey('wardrobe_items.id'), nullable=False)
    item2_id = db.Column(db.Integer, db.ForeignKey('wardrobe_items.id'), nullable=False)
    
    # Similarity scores
    overall_similarity = db.Column(db.Float, nullable=False)  # 0-1 overall similarity
    color_similarity = db.Column(db.Float)  # Color similarity
    pattern_similarity = db.Column(db.Float)  # Pattern similarity
    style_similarity = db.Column(db.Float)  # Style similarity
    silhouette_similarity = db.Column(db.Float)  # Silhouette similarity
    
    # Similarity analysis
    similarity_reasons = db.Column(db.Text)  # JSON array of similarity reasons
    difference_reasons = db.Column(db.Text)  # JSON array of difference reasons
    
    # Metadata
    analysis_version = db.Column(db.String(20), default="1.0")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    item1 = db.relationship('WardrobeItem', foreign_keys=[item1_id], backref='similarities_as_item1')
    item2 = db.relationship('WardrobeItem', foreign_keys=[item2_id], backref='similarities_as_item2')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'item1_id': self.item1_id,
            'item2_id': self.item2_id,
            'similarity_scores': {
                'overall': self.overall_similarity,
                'color': self.color_similarity,
                'pattern': self.pattern_similarity,
                'style': self.style_similarity,
                'silhouette': self.silhouette_similarity
            },
            'analysis': {
                'similarity_reasons': json.loads(self.similarity_reasons) if self.similarity_reasons else [],
                'difference_reasons': json.loads(self.difference_reasons) if self.difference_reasons else []
            },
            'metadata': {
                'analysis_version': self.analysis_version,
                'created_at': self.created_at.isoformat()
            }
        }

