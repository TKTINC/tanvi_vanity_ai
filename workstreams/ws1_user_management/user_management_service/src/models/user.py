from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import os

db = SQLAlchemy()

class User(db.Model):
    """
    User model for Tanvi Vanity Agent
    Tagline: "We girls have no time" - Quick registration and profile setup
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile information for quick styling
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    age_range = db.Column(db.String(20), nullable=True)  # 13-17, 18-22, 23-25
    
    # Quick style preferences - "We girls have no time" for complex setup
    style_preference = db.Column(db.String(50), nullable=True)  # casual, professional, trendy, classic
    color_preferences = db.Column(db.Text, nullable=True)  # JSON string of preferred colors
    size_info = db.Column(db.Text, nullable=True)  # JSON string of size information
    
    # Account management
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Privacy settings - quick setup for busy users
    privacy_level = db.Column(db.String(20), default='private')  # public, friends, private
    allow_social_sharing = db.Column(db.Boolean, default=False)
    marketing_consent = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Set password hash for secure authentication"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        """Generate JWT token for authentication - quick login for busy users"""
        payload = {
            'user_id': self.id,
            'username': self.username,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, os.environ.get('SECRET_KEY', 'dev-secret'), algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        """Verify JWT token and return user"""
        try:
            payload = jwt.decode(token, os.environ.get('SECRET_KEY', 'dev-secret'), algorithms=['HS256'])
            return User.query.get(payload['user_id'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary - optimized for quick API responses"""
        user_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email if include_sensitive else None,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age_range': self.age_range,
            'style_preference': self.style_preference,
            'color_preferences': self.color_preferences,
            'size_info': self.size_info,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'privacy_level': self.privacy_level,
            'allow_social_sharing': self.allow_social_sharing
        }
        
        # Remove None values for cleaner responses
        return {k: v for k, v in user_dict.items() if v is not None}

    def to_public_dict(self):
        """Public profile information - respecting privacy settings"""
        if self.privacy_level == 'private':
            return {
                'id': self.id,
                'username': self.username,
                'style_preference': self.style_preference
            }
        else:
            return {
                'id': self.id,
                'username': self.username,
                'first_name': self.first_name,
                'style_preference': self.style_preference,
                'age_range': self.age_range,
                'created_at': self.created_at.isoformat() if self.created_at else None
            }


class UserSession(db.Model):
    """
    User session tracking for security and analytics
    "We girls have no time" - Quick session management
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    device_info = db.Column(db.Text, nullable=True)  # JSON string of device information
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 or IPv6
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    user = db.relationship('User', backref=db.backref('sessions', lazy=True))

    def __repr__(self):
        return f'<UserSession {self.user_id}:{self.session_token[:8]}...>'

    def is_expired(self):
        """Check if session is expired"""
        return datetime.utcnow() > self.expires_at

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'device_info': self.device_info,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'is_active': self.is_active
        }


class UserPreference(db.Model):
    """
    Detailed user preferences for AI styling
    "We girls have no time" - Smart defaults with quick customization
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Quick setup preferences
    occasion_preferences = db.Column(db.Text, nullable=True)  # JSON: work, casual, party, date, etc.
    weather_sensitivity = db.Column(db.String(20), default='medium')  # low, medium, high
    comfort_priority = db.Column(db.Integer, default=7)  # 1-10 scale
    trend_following = db.Column(db.Integer, default=5)  # 1-10 scale
    
    # Shopping preferences for quick recommendations
    budget_range = db.Column(db.String(20), nullable=True)  # low, medium, high, luxury
    preferred_brands = db.Column(db.Text, nullable=True)  # JSON array of brand names
    shopping_frequency = db.Column(db.String(20), default='monthly')  # weekly, monthly, seasonal
    
    # AI interaction preferences
    conversation_style = db.Column(db.String(20), default='friendly')  # formal, friendly, casual
    notification_frequency = db.Column(db.String(20), default='daily')  # never, daily, weekly
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('preferences', uselist=False))

    def __repr__(self):
        return f'<UserPreference {self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'occasion_preferences': self.occasion_preferences,
            'weather_sensitivity': self.weather_sensitivity,
            'comfort_priority': self.comfort_priority,
            'trend_following': self.trend_following,
            'budget_range': self.budget_range,
            'preferred_brands': self.preferred_brands,
            'shopping_frequency': self.shopping_frequency,
            'conversation_style': self.conversation_style,
            'notification_frequency': self.notification_frequency,
            'updated_at': self.updated_at.isoformat()
        }

