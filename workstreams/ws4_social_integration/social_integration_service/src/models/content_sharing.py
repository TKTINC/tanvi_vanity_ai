"""
WS4-P2: Content Sharing & Style Posts Models
Tanvi Vanity Agent - Social Integration System
"We girls have no time" - Instant style content creation and sharing!
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class StylePost(db.Model):
    """
    Style posts for sharing outfits and fashion content
    "We girls have no time" - instant style sharing!
    """
    __tablename__ = 'style_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)  # From WS1
    
    # Post content
    title = db.Column(db.String(200))
    caption = db.Column(db.Text)
    post_type = db.Column(db.String(30), default='outfit')  # outfit, style_tip, inspiration, review
    
    # Visual content
    image_urls = db.Column(db.Text)  # JSON array of image URLs
    outfit_id = db.Column(db.String(50))  # Reference to WS3 outfit
    wardrobe_items = db.Column(db.Text)  # JSON array of wardrobe item IDs
    
    # Style metadata
    style_tags = db.Column(db.Text)  # JSON array of style tags
    occasion = db.Column(db.String(50))
    season = db.Column(db.String(20))
    weather = db.Column(db.String(30))
    formality_level = db.Column(db.String(20))  # casual, business_casual, formal, black_tie
    
    # Brand and shopping info
    brands_featured = db.Column(db.Text)  # JSON array of brands
    price_range = db.Column(db.String(20))  # budget, mid_range, luxury, mixed
    shopping_links = db.Column(db.Text)  # JSON array of shopping links
    
    # Engagement metrics
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    shares_count = db.Column(db.Integer, default=0)
    saves_count = db.Column(db.Integer, default=0)
    views_count = db.Column(db.Integer, default=0)
    
    # Post settings
    is_public = db.Column(db.Boolean, default=True)
    allow_comments = db.Column(db.Boolean, default=True)
    allow_sharing = db.Column(db.Boolean, default=True)
    allow_outfit_copying = db.Column(db.Boolean, default=True)
    
    # AI analysis
    ai_style_score = db.Column(db.Float, default=0.0)
    ai_trend_relevance = db.Column(db.Float, default=0.0)
    ai_color_harmony = db.Column(db.Float, default=0.0)
    ai_occasion_fit = db.Column(db.Float, default=0.0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # Status
    status = db.Column(db.String(20), default='published')  # draft, published, archived, deleted
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'caption': self.caption,
            'post_type': self.post_type,
            'image_urls': json.loads(self.image_urls) if self.image_urls else [],
            'outfit_id': self.outfit_id,
            'wardrobe_items': json.loads(self.wardrobe_items) if self.wardrobe_items else [],
            'style_tags': json.loads(self.style_tags) if self.style_tags else [],
            'occasion': self.occasion,
            'season': self.season,
            'weather': self.weather,
            'formality_level': self.formality_level,
            'brands_featured': json.loads(self.brands_featured) if self.brands_featured else [],
            'price_range': self.price_range,
            'shopping_links': json.loads(self.shopping_links) if self.shopping_links else [],
            'engagement': {
                'likes_count': self.likes_count,
                'comments_count': self.comments_count,
                'shares_count': self.shares_count,
                'saves_count': self.saves_count,
                'views_count': self.views_count
            },
            'settings': {
                'is_public': self.is_public,
                'allow_comments': self.allow_comments,
                'allow_sharing': self.allow_sharing,
                'allow_outfit_copying': self.allow_outfit_copying
            },
            'ai_analysis': {
                'style_score': self.ai_style_score,
                'trend_relevance': self.ai_trend_relevance,
                'color_harmony': self.ai_color_harmony,
                'occasion_fit': self.ai_occasion_fit
            },
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'status': self.status,
            'tagline': 'We girls have no time - instant style sharing!'
        }
    
    def increment_engagement(self, engagement_type):
        """Increment engagement metrics"""
        if engagement_type == 'like':
            self.likes_count += 1
        elif engagement_type == 'comment':
            self.comments_count += 1
        elif engagement_type == 'share':
            self.shares_count += 1
        elif engagement_type == 'save':
            self.saves_count += 1
        elif engagement_type == 'view':
            self.views_count += 1
        
        db.session.commit()

class PostComment(db.Model):
    """
    Comments on style posts
    "We girls have no time" - instant style feedback!
    """
    __tablename__ = 'post_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('style_posts.id'), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('post_comments.id'))  # For replies
    
    # Comment content
    content = db.Column(db.Text, nullable=False)
    comment_type = db.Column(db.String(20), default='text')  # text, emoji, style_tip
    
    # Engagement
    likes_count = db.Column(db.Integer, default=0)
    replies_count = db.Column(db.Integer, default=0)
    
    # Status
    is_edited = db.Column(db.Boolean, default=False)
    is_pinned = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='active')  # active, hidden, deleted
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    post = db.relationship('StylePost', backref='comments')
    replies = db.relationship('PostComment', backref=db.backref('parent', remote_side=[id]))
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'parent_comment_id': self.parent_comment_id,
            'content': self.content,
            'comment_type': self.comment_type,
            'likes_count': self.likes_count,
            'replies_count': self.replies_count,
            'is_edited': self.is_edited,
            'is_pinned': self.is_pinned,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tagline': 'We girls have no time - instant style feedback!'
        }

class PostLike(db.Model):
    """
    Likes on style posts and comments
    "We girls have no time" - instant style appreciation!
    """
    __tablename__ = 'post_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('style_posts.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('post_comments.id'))
    
    # Like metadata
    like_type = db.Column(db.String(20), default='like')  # like, love, fire, style_goals
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    post = db.relationship('StylePost', backref='likes')
    comment = db.relationship('PostComment', backref='likes')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'comment_id': self.comment_id,
            'like_type': self.like_type,
            'created_at': self.created_at.isoformat(),
            'tagline': 'We girls have no time - instant style appreciation!'
        }

class PostShare(db.Model):
    """
    Shares of style posts
    "We girls have no time" - instant style inspiration spreading!
    """
    __tablename__ = 'post_shares'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('style_posts.id'), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)  # User who shared
    
    # Share details
    share_type = db.Column(db.String(30), default='repost')  # repost, story, direct_message, external
    share_caption = db.Column(db.Text)
    share_platform = db.Column(db.String(30))  # internal, instagram, tiktok, pinterest
    
    # Share metadata
    recipient_user_id = db.Column(db.String(50))  # For direct messages
    external_url = db.Column(db.String(500))  # For external shares
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    post = db.relationship('StylePost', backref='shares')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'share_type': self.share_type,
            'share_caption': self.share_caption,
            'share_platform': self.share_platform,
            'recipient_user_id': self.recipient_user_id,
            'external_url': self.external_url,
            'created_at': self.created_at.isoformat(),
            'tagline': 'We girls have no time - instant style inspiration spreading!'
        }

class PostSave(db.Model):
    """
    Saved style posts for later reference
    "We girls have no time" - instant style bookmarking!
    """
    __tablename__ = 'post_saves'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('style_posts.id'), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    
    # Save organization
    collection_name = db.Column(db.String(100))  # Custom collection name
    save_reason = db.Column(db.String(50))  # outfit_inspiration, shopping_list, color_ideas, etc.
    notes = db.Column(db.Text)  # Personal notes about the save
    
    # Save metadata
    is_private = db.Column(db.Boolean, default=True)
    reminder_date = db.Column(db.DateTime)  # Optional reminder
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    post = db.relationship('StylePost', backref='saves')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'collection_name': self.collection_name,
            'save_reason': self.save_reason,
            'notes': self.notes,
            'is_private': self.is_private,
            'reminder_date': self.reminder_date.isoformat() if self.reminder_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tagline': 'We girls have no time - instant style bookmarking!'
        }

class StyleChallenge(db.Model):
    """
    Style challenges and trends
    "We girls have no time" - instant style challenges!
    """
    __tablename__ = 'style_challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.String(50), nullable=False)
    
    # Challenge details
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    challenge_type = db.Column(db.String(30), default='style')  # style, color, theme, brand, season
    
    # Challenge parameters
    rules = db.Column(db.Text)  # JSON object with challenge rules
    required_items = db.Column(db.Text)  # JSON array of required items/categories
    style_constraints = db.Column(db.Text)  # JSON object with style constraints
    
    # Challenge metadata
    hashtag = db.Column(db.String(100))
    difficulty_level = db.Column(db.String(20), default='medium')  # easy, medium, hard, expert
    estimated_time = db.Column(db.String(30))  # "5 minutes", "1 hour", etc.
    
    # Participation tracking
    participants_count = db.Column(db.Integer, default=0)
    posts_count = db.Column(db.Integer, default=0)
    completion_rate = db.Column(db.Float, default=0.0)
    
    # Challenge timing
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Rewards and recognition
    has_prizes = db.Column(db.Boolean, default=False)
    prize_description = db.Column(db.Text)
    featured_submissions = db.Column(db.Text)  # JSON array of featured post IDs
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'title': self.title,
            'description': self.description,
            'challenge_type': self.challenge_type,
            'rules': json.loads(self.rules) if self.rules else {},
            'required_items': json.loads(self.required_items) if self.required_items else [],
            'style_constraints': json.loads(self.style_constraints) if self.style_constraints else {},
            'hashtag': self.hashtag,
            'difficulty_level': self.difficulty_level,
            'estimated_time': self.estimated_time,
            'participation': {
                'participants_count': self.participants_count,
                'posts_count': self.posts_count,
                'completion_rate': self.completion_rate
            },
            'timing': {
                'start_date': self.start_date.isoformat(),
                'end_date': self.end_date.isoformat() if self.end_date else None,
                'is_active': self.is_active
            },
            'rewards': {
                'has_prizes': self.has_prizes,
                'prize_description': self.prize_description,
                'featured_submissions': json.loads(self.featured_submissions) if self.featured_submissions else []
            },
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tagline': 'We girls have no time - instant style challenges!'
        }
    
    def add_participant(self):
        """Add a participant to the challenge"""
        self.participants_count += 1
        db.session.commit()
    
    def add_post(self):
        """Add a post to the challenge"""
        self.posts_count += 1
        # Update completion rate (posts/participants)
        if self.participants_count > 0:
            self.completion_rate = self.posts_count / self.participants_count
        db.session.commit()

class ContentCollection(db.Model):
    """
    User-created collections of style content
    "We girls have no time" - instant style organization!
    """
    __tablename__ = 'content_collections'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    
    # Collection details
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    collection_type = db.Column(db.String(30), default='custom')  # custom, seasonal, occasion, color, brand
    
    # Collection metadata
    cover_image_url = db.Column(db.String(500))
    tags = db.Column(db.Text)  # JSON array of tags
    color_theme = db.Column(db.String(50))
    
    # Collection settings
    is_public = db.Column(db.Boolean, default=False)
    is_collaborative = db.Column(db.Boolean, default=False)
    allow_contributions = db.Column(db.Boolean, default=False)
    
    # Collection stats
    items_count = db.Column(db.Integer, default=0)
    followers_count = db.Column(db.Integer, default=0)
    views_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'collection_type': self.collection_type,
            'cover_image_url': self.cover_image_url,
            'tags': json.loads(self.tags) if self.tags else [],
            'color_theme': self.color_theme,
            'settings': {
                'is_public': self.is_public,
                'is_collaborative': self.is_collaborative,
                'allow_contributions': self.allow_contributions
            },
            'stats': {
                'items_count': self.items_count,
                'followers_count': self.followers_count,
                'views_count': self.views_count
            },
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tagline': 'We girls have no time - instant style organization!'
        }
    
    def add_item(self):
        """Add an item to the collection"""
        self.items_count += 1
        self.updated_at = datetime.utcnow()
        db.session.commit()

class CollectionItem(db.Model):
    """
    Items within content collections
    "We girls have no time" - instant collection management!
    """
    __tablename__ = 'collection_items'
    
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('content_collections.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('style_posts.id'), nullable=False)
    added_by_user_id = db.Column(db.String(50), nullable=False)
    
    # Item metadata
    order_index = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    
    # Timestamps
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    collection = db.relationship('ContentCollection', backref='items')
    post = db.relationship('StylePost', backref='collection_items')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'collection_id': self.collection_id,
            'post_id': self.post_id,
            'added_by_user_id': self.added_by_user_id,
            'order_index': self.order_index,
            'notes': self.notes,
            'added_at': self.added_at.isoformat(),
            'tagline': 'We girls have no time - instant collection management!'
        }

