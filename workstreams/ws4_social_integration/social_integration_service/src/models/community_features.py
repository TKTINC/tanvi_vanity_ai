"""
WS4-P3: Community Features & Engagement Models
Tanvi Vanity Agent - Social Integration System
"We girls have no time" - Instant community engagement and style discovery!
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

class StyleCommunity(db.Model):
    """
    Style communities and groups
    "We girls have no time" - instant style communities!
    """
    __tablename__ = 'style_communities'
    
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.String(50), nullable=False)
    
    # Community details
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    community_type = db.Column(db.String(30), default='style')  # style, brand, occasion, color, trend
    
    # Community metadata
    cover_image_url = db.Column(db.String(500))
    banner_image_url = db.Column(db.String(500))
    tags = db.Column(db.Text)  # JSON array of tags
    style_focus = db.Column(db.Text)  # JSON array of style focuses
    
    # Community settings
    is_public = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    requires_approval = db.Column(db.Boolean, default=False)
    allow_posts = db.Column(db.Boolean, default=True)
    allow_challenges = db.Column(db.Boolean, default=True)
    
    # Community stats
    members_count = db.Column(db.Integer, default=0)
    posts_count = db.Column(db.Integer, default=0)
    active_members_count = db.Column(db.Integer, default=0)
    engagement_score = db.Column(db.Float, default=0.0)
    
    # Community rules
    rules = db.Column(db.Text)  # JSON array of community rules
    guidelines = db.Column(db.Text)  # Community guidelines
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'name': self.name,
            'description': self.description,
            'community_type': self.community_type,
            'cover_image_url': self.cover_image_url,
            'banner_image_url': self.banner_image_url,
            'tags': json.loads(self.tags) if self.tags else [],
            'style_focus': json.loads(self.style_focus) if self.style_focus else [],
            'settings': {
                'is_public': self.is_public,
                'is_verified': self.is_verified,
                'requires_approval': self.requires_approval,
                'allow_posts': self.allow_posts,
                'allow_challenges': self.allow_challenges
            },
            'stats': {
                'members_count': self.members_count,
                'posts_count': self.posts_count,
                'active_members_count': self.active_members_count,
                'engagement_score': self.engagement_score
            },
            'rules': json.loads(self.rules) if self.rules else [],
            'guidelines': self.guidelines,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tagline': 'We girls have no time - instant style communities!'
        }
    
    def add_member(self):
        """Add a member to the community"""
        self.members_count += 1
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def add_post(self):
        """Add a post to the community"""
        self.posts_count += 1
        self.updated_at = datetime.utcnow()
        db.session.commit()

class CommunityMembership(db.Model):
    """
    Community membership tracking
    "We girls have no time" - instant community joining!
    """
    __tablename__ = 'community_memberships'
    
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('style_communities.id'), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    
    # Membership details
    role = db.Column(db.String(20), default='member')  # member, moderator, admin, creator
    status = db.Column(db.String(20), default='active')  # active, pending, banned, left
    
    # Membership metadata
    join_reason = db.Column(db.Text)
    introduction = db.Column(db.Text)
    
    # Activity tracking
    posts_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    likes_given = db.Column(db.Integer, default=0)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Timestamps
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    community = db.relationship('StyleCommunity', backref='memberships')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'community_id': self.community_id,
            'user_id': self.user_id,
            'role': self.role,
            'status': self.status,
            'join_reason': self.join_reason,
            'introduction': self.introduction,
            'activity': {
                'posts_count': self.posts_count,
                'comments_count': self.comments_count,
                'likes_given': self.likes_given,
                'last_active': self.last_active.isoformat()
            },
            'joined_at': self.joined_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tagline': 'We girls have no time - instant community joining!'
        }

class StyleEvent(db.Model):
    """
    Style events and meetups
    "We girls have no time" - instant style events!
    """
    __tablename__ = 'style_events'
    
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.String(50), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('style_communities.id'))
    
    # Event details
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(30), default='virtual')  # virtual, in_person, hybrid, challenge
    
    # Event metadata
    cover_image_url = db.Column(db.String(500))
    tags = db.Column(db.Text)  # JSON array of tags
    dress_code = db.Column(db.String(100))
    style_theme = db.Column(db.String(100))
    
    # Event timing
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    timezone = db.Column(db.String(50), default='UTC')
    duration_minutes = db.Column(db.Integer)
    
    # Event location (for in-person events)
    location_name = db.Column(db.String(200))
    location_address = db.Column(db.Text)
    location_coordinates = db.Column(db.String(100))  # lat,lng
    
    # Virtual event details
    meeting_url = db.Column(db.String(500))
    meeting_platform = db.Column(db.String(50))  # zoom, teams, discord, etc.
    meeting_id = db.Column(db.String(100))
    meeting_password = db.Column(db.String(100))
    
    # Event settings
    is_public = db.Column(db.Boolean, default=True)
    requires_rsvp = db.Column(db.Boolean, default=True)
    max_attendees = db.Column(db.Integer)
    allow_guests = db.Column(db.Boolean, default=False)
    
    # Event stats
    attendees_count = db.Column(db.Integer, default=0)
    interested_count = db.Column(db.Integer, default=0)
    rsvp_yes_count = db.Column(db.Integer, default=0)
    rsvp_maybe_count = db.Column(db.Integer, default=0)
    
    # Event status
    status = db.Column(db.String(20), default='upcoming')  # upcoming, live, completed, cancelled
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    community = db.relationship('StyleCommunity', backref='events')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'community_id': self.community_id,
            'title': self.title,
            'description': self.description,
            'event_type': self.event_type,
            'cover_image_url': self.cover_image_url,
            'tags': json.loads(self.tags) if self.tags else [],
            'dress_code': self.dress_code,
            'style_theme': self.style_theme,
            'timing': {
                'start_time': self.start_time.isoformat(),
                'end_time': self.end_time.isoformat() if self.end_time else None,
                'timezone': self.timezone,
                'duration_minutes': self.duration_minutes
            },
            'location': {
                'name': self.location_name,
                'address': self.location_address,
                'coordinates': self.location_coordinates
            },
            'virtual': {
                'meeting_url': self.meeting_url,
                'meeting_platform': self.meeting_platform,
                'meeting_id': self.meeting_id,
                'meeting_password': self.meeting_password
            },
            'settings': {
                'is_public': self.is_public,
                'requires_rsvp': self.requires_rsvp,
                'max_attendees': self.max_attendees,
                'allow_guests': self.allow_guests
            },
            'stats': {
                'attendees_count': self.attendees_count,
                'interested_count': self.interested_count,
                'rsvp_yes_count': self.rsvp_yes_count,
                'rsvp_maybe_count': self.rsvp_maybe_count
            },
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tagline': 'We girls have no time - instant style events!'
        }

class EventRSVP(db.Model):
    """
    Event RSVP tracking
    "We girls have no time" - instant event responses!
    """
    __tablename__ = 'event_rsvps'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('style_events.id'), nullable=False)
    user_id = db.Column(db.String(50), nullable=False)
    
    # RSVP details
    response = db.Column(db.String(20), default='yes')  # yes, no, maybe, interested
    guest_count = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    
    # Outfit planning
    planned_outfit_id = db.Column(db.String(50))  # Reference to WS3 outfit
    outfit_notes = db.Column(db.Text)
    
    # Timestamps
    rsvp_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    event = db.relationship('StyleEvent', backref='rsvps')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'event_id': self.event_id,
            'user_id': self.user_id,
            'response': self.response,
            'guest_count': self.guest_count,
            'notes': self.notes,
            'planned_outfit_id': self.planned_outfit_id,
            'outfit_notes': self.outfit_notes,
            'rsvp_at': self.rsvp_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tagline': 'We girls have no time - instant event responses!'
        }

class StyleMentor(db.Model):
    """
    Style mentors and coaching relationships
    "We girls have no time" - instant style mentoring!
    """
    __tablename__ = 'style_mentors'
    
    id = db.Column(db.Integer, primary_key=True)
    mentor_user_id = db.Column(db.String(50), nullable=False)
    
    # Mentor profile
    bio = db.Column(db.Text)
    specialties = db.Column(db.Text)  # JSON array of specialties
    experience_years = db.Column(db.Integer)
    style_philosophy = db.Column(db.Text)
    
    # Mentor credentials
    certifications = db.Column(db.Text)  # JSON array of certifications
    portfolio_url = db.Column(db.String(500))
    social_links = db.Column(db.Text)  # JSON object of social links
    
    # Mentor availability
    is_accepting_mentees = db.Column(db.Boolean, default=True)
    max_mentees = db.Column(db.Integer, default=10)
    current_mentees_count = db.Column(db.Integer, default=0)
    hourly_rate = db.Column(db.Float)
    currency = db.Column(db.String(10), default='USD')
    
    # Mentor stats
    total_sessions = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float, default=0.0)
    reviews_count = db.Column(db.Integer, default=0)
    response_time_hours = db.Column(db.Float, default=24.0)
    
    # Mentor settings
    is_verified = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='active')  # active, inactive, suspended
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'mentor_user_id': self.mentor_user_id,
            'bio': self.bio,
            'specialties': json.loads(self.specialties) if self.specialties else [],
            'experience_years': self.experience_years,
            'style_philosophy': self.style_philosophy,
            'credentials': {
                'certifications': json.loads(self.certifications) if self.certifications else [],
                'portfolio_url': self.portfolio_url,
                'social_links': json.loads(self.social_links) if self.social_links else {}
            },
            'availability': {
                'is_accepting_mentees': self.is_accepting_mentees,
                'max_mentees': self.max_mentees,
                'current_mentees_count': self.current_mentees_count,
                'hourly_rate': self.hourly_rate,
                'currency': self.currency
            },
            'stats': {
                'total_sessions': self.total_sessions,
                'average_rating': self.average_rating,
                'reviews_count': self.reviews_count,
                'response_time_hours': self.response_time_hours
            },
            'verification': {
                'is_verified': self.is_verified,
                'is_featured': self.is_featured,
                'status': self.status
            },
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tagline': 'We girls have no time - instant style mentoring!'
        }

class MentorshipRelationship(db.Model):
    """
    Mentorship relationships between mentors and mentees
    "We girls have no time" - instant mentoring connections!
    """
    __tablename__ = 'mentorship_relationships'
    
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('style_mentors.id'), nullable=False)
    mentee_user_id = db.Column(db.String(50), nullable=False)
    
    # Relationship details
    status = db.Column(db.String(20), default='pending')  # pending, active, completed, cancelled
    mentorship_type = db.Column(db.String(30), default='general')  # general, wardrobe_audit, style_transformation
    
    # Mentorship goals
    goals = db.Column(db.Text)  # JSON array of goals
    focus_areas = db.Column(db.Text)  # JSON array of focus areas
    timeline_weeks = db.Column(db.Integer, default=4)
    
    # Progress tracking
    sessions_completed = db.Column(db.Integer, default=0)
    sessions_planned = db.Column(db.Integer, default=4)
    progress_percentage = db.Column(db.Float, default=0.0)
    
    # Feedback and rating
    mentee_rating = db.Column(db.Float)
    mentee_review = db.Column(db.Text)
    mentor_notes = db.Column(db.Text)
    
    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    mentor = db.relationship('StyleMentor', backref='mentorships')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'mentor_id': self.mentor_id,
            'mentee_user_id': self.mentee_user_id,
            'status': self.status,
            'mentorship_type': self.mentorship_type,
            'goals': json.loads(self.goals) if self.goals else [],
            'focus_areas': json.loads(self.focus_areas) if self.focus_areas else [],
            'timeline_weeks': self.timeline_weeks,
            'progress': {
                'sessions_completed': self.sessions_completed,
                'sessions_planned': self.sessions_planned,
                'progress_percentage': self.progress_percentage
            },
            'feedback': {
                'mentee_rating': self.mentee_rating,
                'mentee_review': self.mentee_review,
                'mentor_notes': self.mentor_notes
            },
            'started_at': self.started_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'updated_at': self.updated_at.isoformat(),
            'tagline': 'We girls have no time - instant mentoring connections!'
        }

class StyleTip(db.Model):
    """
    Daily style tips and advice
    "We girls have no time" - instant style wisdom!
    """
    __tablename__ = 'style_tips'
    
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.String(50), nullable=False)
    
    # Tip content
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tip_type = db.Column(db.String(30), default='general')  # general, seasonal, occasion, color, body_type
    
    # Tip metadata
    difficulty_level = db.Column(db.String(20), default='easy')  # easy, medium, advanced
    time_to_implement = db.Column(db.String(30))  # "2 minutes", "5 minutes", etc.
    category = db.Column(db.String(50))  # styling, color, fit, accessories, etc.
    
    # Visual content
    image_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500))
    
    # Tip targeting
    target_audience = db.Column(db.Text)  # JSON array of target audience
    style_types = db.Column(db.Text)  # JSON array of applicable style types
    occasions = db.Column(db.Text)  # JSON array of applicable occasions
    
    # Engagement
    likes_count = db.Column(db.Integer, default=0)
    saves_count = db.Column(db.Integer, default=0)
    shares_count = db.Column(db.Integer, default=0)
    views_count = db.Column(db.Integer, default=0)
    
    # Tip status
    is_featured = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='published')  # draft, published, archived
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'title': self.title,
            'content': self.content,
            'tip_type': self.tip_type,
            'difficulty_level': self.difficulty_level,
            'time_to_implement': self.time_to_implement,
            'category': self.category,
            'media': {
                'image_url': self.image_url,
                'video_url': self.video_url
            },
            'targeting': {
                'target_audience': json.loads(self.target_audience) if self.target_audience else [],
                'style_types': json.loads(self.style_types) if self.style_types else [],
                'occasions': json.loads(self.occasions) if self.occasions else []
            },
            'engagement': {
                'likes_count': self.likes_count,
                'saves_count': self.saves_count,
                'shares_count': self.shares_count,
                'views_count': self.views_count
            },
            'verification': {
                'is_featured': self.is_featured,
                'is_verified': self.is_verified,
                'status': self.status
            },
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'tagline': 'We girls have no time - instant style wisdom!'
        }
    
    def increment_engagement(self, engagement_type):
        """Increment engagement metrics"""
        if engagement_type == 'like':
            self.likes_count += 1
        elif engagement_type == 'save':
            self.saves_count += 1
        elif engagement_type == 'share':
            self.shares_count += 1
        elif engagement_type == 'view':
            self.views_count += 1
        
        db.session.commit()

