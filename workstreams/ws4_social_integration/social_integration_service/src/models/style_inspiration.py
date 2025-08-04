"""
WS4-P4: Style Inspiration & Discovery Models
Tanvi Vanity Agent - Social Integration System
"We girls have no time" - Instant style inspiration and discovery!
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

class StyleInspiration(db.Model):
    """Style inspiration posts and content"""
    __tablename__ = 'style_inspirations'
    
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    inspiration_type = db.Column(db.String(30), default='outfit')
    primary_image_url = db.Column(db.String(500), nullable=False)
    style_tags = db.Column(db.Text)
    ai_style_score = db.Column(db.Float, default=0.0)
    views_count = db.Column(db.Integer, default=0)
    likes_count = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'title': self.title,
            'description': self.description,
            'inspiration_type': self.inspiration_type,
            'primary_image_url': self.primary_image_url,
            'style_tags': json.loads(self.style_tags) if self.style_tags else [],
            'ai_style_score': self.ai_style_score,
            'views_count': self.views_count,
            'likes_count': self.likes_count,
            'is_featured': self.is_featured,
            'created_at': self.created_at.isoformat(),
            'tagline': 'We girls have no time - instant style inspiration!'
        }

class TrendAnalysis(db.Model):
    """Fashion trend analysis and tracking"""
    __tablename__ = 'trend_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    trend_name = db.Column(db.String(100), nullable=False)
    trend_category = db.Column(db.String(50), default='style')
    trend_description = db.Column(db.Text)
    lifecycle_stage = db.Column(db.String(30), default='emerging')
    confidence_score = db.Column(db.Float, default=0.0)
    mention_count = db.Column(db.Integer, default=0)
    ai_trend_score = db.Column(db.Float, default=0.0)
    is_verified = db.Column(db.Boolean, default=False)
    first_detected = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'trend_name': self.trend_name,
            'trend_category': self.trend_category,
            'trend_description': self.trend_description,
            'lifecycle_stage': self.lifecycle_stage,
            'confidence_score': self.confidence_score,
            'mention_count': self.mention_count,
            'ai_trend_score': self.ai_trend_score,
            'is_verified': self.is_verified,
            'first_detected': self.first_detected.isoformat(),
            'tagline': 'We girls have no time - instant trend insights!'
        }

class PersonalizedFeed(db.Model):
    """Personalized style inspiration feeds"""
    __tablename__ = 'personalized_feeds'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    feed_type = db.Column(db.String(30), default='main')
    feed_name = db.Column(db.String(100))
    style_preferences = db.Column(db.Text)
    personalization_strength = db.Column(db.Float, default=0.7)
    engagement_rate = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'feed_type': self.feed_type,
            'feed_name': self.feed_name,
            'style_preferences': json.loads(self.style_preferences) if self.style_preferences else [],
            'personalization_strength': self.personalization_strength,
            'engagement_rate': self.engagement_rate,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'tagline': 'We girls have no time - instant personalized discovery!'
        }

class StyleMoodboard(db.Model):
    """User-created style moodboards"""
    __tablename__ = 'style_moodboards'
    
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    mood_type = db.Column(db.String(30), default='inspiration')
    inspiration_ids = db.Column(db.Text)
    color_palette = db.Column(db.Text)
    ai_mood_score = db.Column(db.Float, default=0.0)
    is_public = db.Column(db.Boolean, default=False)
    views_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'title': self.title,
            'description': self.description,
            'mood_type': self.mood_type,
            'inspiration_ids': json.loads(self.inspiration_ids) if self.inspiration_ids else [],
            'color_palette': json.loads(self.color_palette) if self.color_palette else [],
            'ai_mood_score': self.ai_mood_score,
            'is_public': self.is_public,
            'views_count': self.views_count,
            'created_at': self.created_at.isoformat(),
            'tagline': 'We girls have no time - instant mood creation!'
        }

class StyleRecommendation(db.Model):
    """AI-generated style recommendations"""
    __tablename__ = 'style_recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    recommendation_type = db.Column(db.String(30), default='inspiration')
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    ai_confidence_score = db.Column(db.Float, default=0.0)
    user_rating = db.Column(db.Float)
    is_saved = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recommendation_type': self.recommendation_type,
            'title': self.title,
            'description': self.description,
            'ai_confidence_score': self.ai_confidence_score,
            'user_rating': self.user_rating,
            'is_saved': self.is_saved,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'tagline': 'We girls have no time - instant style recommendations!'
        }

