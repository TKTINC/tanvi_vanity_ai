"""
WS4-P1: Social Foundation & User Connections Models
Tanvi Vanity Agent - Social Integration System
"We girls have no time" - Instant social connections and style sharing!
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class SocialProfile(db.Model):
    """
    Social profile for users - "We girls have no time" for complex social setup!
    Quick social profile creation with instant style sharing capabilities.
    """
    __tablename__ = 'social_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=False)  # From WS1
    display_name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    profile_image_url = db.Column(db.String(500))
    
    # Social settings - quick privacy controls
    is_public = db.Column(db.Boolean, default=True)
    allow_followers = db.Column(db.Boolean, default=True)
    allow_style_sharing = db.Column(db.Boolean, default=True)
    allow_outfit_copying = db.Column(db.Boolean, default=True)
    
    # Style preferences for social matching
    style_tags = db.Column(db.Text)  # JSON array of style tags
    favorite_brands = db.Column(db.Text)  # JSON array of brands
    size_info = db.Column(db.Text)  # JSON object with size information
    
    # Social stats
    followers_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)
    posts_count = db.Column(db.Integer, default=0)
    likes_received = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    connections = db.relationship('SocialConnection', foreign_keys='SocialConnection.follower_id', backref='follower_profile')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'display_name': self.display_name,
            'bio': self.bio,
            'profile_image_url': self.profile_image_url,
            'is_public': self.is_public,
            'allow_followers': self.allow_followers,
            'allow_style_sharing': self.allow_style_sharing,
            'allow_outfit_copying': self.allow_outfit_copying,
            'style_tags': json.loads(self.style_tags) if self.style_tags else [],
            'favorite_brands': json.loads(self.favorite_brands) if self.favorite_brands else [],
            'size_info': json.loads(self.size_info) if self.size_info else {},
            'followers_count': self.followers_count,
            'following_count': self.following_count,
            'posts_count': self.posts_count,
            'likes_received': self.likes_received,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_active': self.last_active.isoformat(),
            'tagline': 'We girls have no time - instant style connections!'
        }
    
    def update_activity(self):
        """Update last active timestamp"""
        self.last_active = datetime.utcnow()
        db.session.commit()

class SocialConnection(db.Model):
    """
    Social connections between users - "We girls have no time" for complex friend requests!
    Instant follow system with style compatibility matching.
    """
    __tablename__ = 'social_connections'
    
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.String(50), db.ForeignKey('social_profiles.user_id'), nullable=False)
    following_id = db.Column(db.String(50), nullable=False)
    
    # Connection type and status
    connection_type = db.Column(db.String(20), default='follow')  # follow, mutual, blocked
    status = db.Column(db.String(20), default='active')  # active, pending, blocked
    
    # Style compatibility (calculated from WS2 AI)
    style_compatibility_score = db.Column(db.Float, default=0.0)
    shared_style_tags = db.Column(db.Text)  # JSON array of shared style interests
    
    # Interaction tracking
    interaction_count = db.Column(db.Integer, default=0)
    last_interaction = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'follower_id': self.follower_id,
            'following_id': self.following_id,
            'connection_type': self.connection_type,
            'status': self.status,
            'style_compatibility_score': self.style_compatibility_score,
            'shared_style_tags': json.loads(self.shared_style_tags) if self.shared_style_tags else [],
            'interaction_count': self.interaction_count,
            'last_interaction': self.last_interaction.isoformat() if self.last_interaction else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tagline': 'We girls have no time - instant style connections!'
        }
    
    def update_interaction(self):
        """Update interaction tracking"""
        self.interaction_count += 1
        self.last_interaction = datetime.utcnow()
        db.session.commit()

class StyleInfluencer(db.Model):
    """
    Style influencers and fashion experts - "We girls have no time" to find style inspiration!
    Curated list of style influencers with instant access to their content.
    """
    __tablename__ = 'style_influencers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('social_profiles.user_id'), nullable=False)
    
    # Influencer status and verification
    influencer_type = db.Column(db.String(30), default='style_enthusiast')  # style_enthusiast, fashion_blogger, brand_ambassador, celebrity
    verification_status = db.Column(db.String(20), default='pending')  # pending, verified, featured
    verification_date = db.Column(db.DateTime)
    
    # Expertise and specialization
    style_specialties = db.Column(db.Text)  # JSON array of style specialties
    expertise_level = db.Column(db.String(20), default='intermediate')  # beginner, intermediate, expert, master
    content_categories = db.Column(db.Text)  # JSON array of content categories
    
    # Influence metrics
    followers_count = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Float, default=0.0)
    style_impact_score = db.Column(db.Float, default=0.0)
    trend_prediction_accuracy = db.Column(db.Float, default=0.0)
    
    # Content stats
    total_posts = db.Column(db.Integer, default=0)
    viral_posts = db.Column(db.Integer, default=0)
    style_guides_created = db.Column(db.Integer, default=0)
    outfits_shared = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = db.relationship('SocialProfile', backref='influencer_status')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'influencer_type': self.influencer_type,
            'verification_status': self.verification_status,
            'verification_date': self.verification_date.isoformat() if self.verification_date else None,
            'style_specialties': json.loads(self.style_specialties) if self.style_specialties else [],
            'expertise_level': self.expertise_level,
            'content_categories': json.loads(self.content_categories) if self.content_categories else [],
            'followers_count': self.followers_count,
            'engagement_rate': self.engagement_rate,
            'style_impact_score': self.style_impact_score,
            'trend_prediction_accuracy': self.trend_prediction_accuracy,
            'total_posts': self.total_posts,
            'viral_posts': self.viral_posts,
            'style_guides_created': self.style_guides_created,
            'outfits_shared': self.outfits_shared,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tagline': 'We girls have no time - instant style expertise!'
        }
    
    def calculate_influence_score(self):
        """Calculate overall influence score"""
        # Weighted calculation based on multiple factors
        follower_score = min(self.followers_count / 10000, 1.0) * 0.3
        engagement_score = self.engagement_rate * 0.25
        impact_score = self.style_impact_score * 0.25
        accuracy_score = self.trend_prediction_accuracy * 0.2
        
        return follower_score + engagement_score + impact_score + accuracy_score

class SocialNotification(db.Model):
    """
    Social notifications - "We girls have no time" for missed style updates!
    Instant notifications for social interactions and style updates.
    """
    __tablename__ = 'social_notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)  # Recipient
    sender_id = db.Column(db.String(50))  # Who triggered the notification
    
    # Notification details
    notification_type = db.Column(db.String(30), nullable=False)  # follow, like, comment, style_match, outfit_copy
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    action_url = db.Column(db.String(500))  # URL to navigate to
    
    # Notification metadata
    related_content_id = db.Column(db.String(50))  # ID of related post, outfit, etc.
    related_content_type = db.Column(db.String(30))  # post, outfit, user, etc.
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    
    # Status tracking
    is_read = db.Column(db.Boolean, default=False)
    is_dismissed = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)  # Optional expiration
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'sender_id': self.sender_id,
            'notification_type': self.notification_type,
            'title': self.title,
            'message': self.message,
            'action_url': self.action_url,
            'related_content_id': self.related_content_id,
            'related_content_type': self.related_content_type,
            'priority': self.priority,
            'is_read': self.is_read,
            'is_dismissed': self.is_dismissed,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'tagline': 'We girls have no time - instant style updates!'
        }
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.read_at = datetime.utcnow()
        db.session.commit()
    
    @staticmethod
    def create_notification(user_id, notification_type, title, message, sender_id=None, 
                          related_content_id=None, related_content_type=None, 
                          action_url=None, priority='normal'):
        """Create a new notification"""
        notification = SocialNotification(
            user_id=user_id,
            sender_id=sender_id,
            notification_type=notification_type,
            title=title,
            message=message,
            action_url=action_url,
            related_content_id=related_content_id,
            related_content_type=related_content_type,
            priority=priority
        )
        db.session.add(notification)
        db.session.commit()
        return notification

class SocialActivity(db.Model):
    """
    Social activity tracking - "We girls have no time" to miss style trends!
    Track all social interactions for analytics and recommendations.
    """
    __tablename__ = 'social_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    
    # Activity details
    activity_type = db.Column(db.String(30), nullable=False)  # follow, unfollow, like, comment, share, view
    target_type = db.Column(db.String(30), nullable=False)  # user, post, outfit, style_guide
    target_id = db.Column(db.String(50), nullable=False)
    
    # Activity metadata
    activity_data = db.Column(db.Text)  # JSON object with additional activity data
    interaction_duration = db.Column(db.Integer)  # Duration in seconds
    device_type = db.Column(db.String(20))  # mobile, desktop, tablet
    
    # Context information
    source_location = db.Column(db.String(50))  # feed, profile, search, recommendations
    session_id = db.Column(db.String(100))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'activity_data': json.loads(self.activity_data) if self.activity_data else {},
            'interaction_duration': self.interaction_duration,
            'device_type': self.device_type,
            'source_location': self.source_location,
            'session_id': self.session_id,
            'created_at': self.created_at.isoformat(),
            'tagline': 'We girls have no time - tracking every style moment!'
        }
    
    @staticmethod
    def log_activity(user_id, activity_type, target_type, target_id, 
                    activity_data=None, interaction_duration=None, 
                    device_type=None, source_location=None, session_id=None):
        """Log a social activity"""
        activity = SocialActivity(
            user_id=user_id,
            activity_type=activity_type,
            target_type=target_type,
            target_id=target_id,
            activity_data=json.dumps(activity_data) if activity_data else None,
            interaction_duration=interaction_duration,
            device_type=device_type,
            source_location=source_location,
            session_id=session_id
        )
        db.session.add(activity)
        db.session.commit()
        return activity

