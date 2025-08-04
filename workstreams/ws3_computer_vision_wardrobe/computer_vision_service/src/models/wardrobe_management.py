"""
WS3-P2: Wardrobe Management & Visual Cataloging
Enhanced Wardrobe Management Models for Tanvi Vanity Agent
"We girls have no time" - Smart wardrobe organization in seconds!
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

class WardrobeCollection(db.Model):
    """
    Wardrobe collections for organizing items
    "We girls have no time" - Smart collections for instant organization!
    """
    __tablename__ = 'wardrobe_collections'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Collection information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    collection_type = db.Column(db.String(50), default='custom')  # custom, smart, seasonal, occasion
    
    # Smart collection rules (for auto-generated collections)
    auto_rules = db.Column(db.Text)  # JSON rules for smart collections
    
    # Collection metadata
    item_count = db.Column(db.Integer, default=0)
    color_theme = db.Column(db.String(100))
    style_theme = db.Column(db.String(100))
    
    # Usage tracking
    access_count = db.Column(db.Integer, default=0)
    last_accessed = db.Column(db.DateTime)
    
    # Metadata
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
            'auto_rules': json.loads(self.auto_rules) if self.auto_rules else None,
            'metadata': {
                'item_count': self.item_count,
                'color_theme': self.color_theme,
                'style_theme': self.style_theme
            },
            'usage': {
                'access_count': self.access_count,
                'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None
            },
            'timestamps': {
                'created_at': self.created_at.isoformat(),
                'updated_at': self.updated_at.isoformat()
            }
        }

class WardrobeItemCollection(db.Model):
    """
    Many-to-many relationship between wardrobe items and collections
    "We girls have no time" - Flexible item organization!
    """
    __tablename__ = 'wardrobe_item_collections'
    
    id = db.Column(db.Integer, primary_key=True)
    wardrobe_item_id = db.Column(db.Integer, nullable=False, index=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('wardrobe_collections.id'), nullable=False)
    
    # Relationship metadata
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.String(50), default='user')  # user, auto, ai
    
    # Relationship
    collection = db.relationship('WardrobeCollection', backref='item_associations')

class WardrobeAnalytics(db.Model):
    """
    Comprehensive wardrobe analytics and insights
    "We girls have no time" - Instant wardrobe intelligence!
    """
    __tablename__ = 'wardrobe_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Analytics period
    analysis_date = db.Column(db.Date, default=datetime.utcnow().date)
    period_type = db.Column(db.String(20), default='monthly')  # daily, weekly, monthly, yearly
    
    # Wardrobe composition
    total_items = db.Column(db.Integer, default=0)
    category_breakdown = db.Column(db.Text)  # JSON object with category counts
    color_breakdown = db.Column(db.Text)  # JSON object with color distribution
    brand_breakdown = db.Column(db.Text)  # JSON object with brand distribution
    
    # Usage analytics
    most_worn_items = db.Column(db.Text)  # JSON array of most worn item IDs
    least_worn_items = db.Column(db.Text)  # JSON array of least worn item IDs
    unworn_items = db.Column(db.Text)  # JSON array of never worn item IDs
    average_wear_frequency = db.Column(db.Float, default=0.0)
    
    # Style analytics
    style_distribution = db.Column(db.Text)  # JSON object with style preferences
    formality_distribution = db.Column(db.Text)  # JSON object with formality levels
    seasonal_distribution = db.Column(db.Text)  # JSON object with seasonal items
    
    # Wardrobe health metrics
    versatility_score = db.Column(db.Float, default=0.0)  # How versatile the wardrobe is
    completeness_score = db.Column(db.Float, default=0.0)  # How complete the wardrobe is
    efficiency_score = db.Column(db.Float, default=0.0)  # How efficiently items are used
    style_coherence_score = db.Column(db.Float, default=0.0)  # How coherent the style is
    
    # Recommendations
    wardrobe_gaps = db.Column(db.Text)  # JSON array of missing item types
    duplicate_items = db.Column(db.Text)  # JSON array of potential duplicates
    underutilized_items = db.Column(db.Text)  # JSON array of underused items
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'analysis_info': {
                'date': self.analysis_date.isoformat(),
                'period_type': self.period_type
            },
            'wardrobe_composition': {
                'total_items': self.total_items,
                'categories': json.loads(self.category_breakdown) if self.category_breakdown else {},
                'colors': json.loads(self.color_breakdown) if self.color_breakdown else {},
                'brands': json.loads(self.brand_breakdown) if self.brand_breakdown else {}
            },
            'usage_analytics': {
                'most_worn': json.loads(self.most_worn_items) if self.most_worn_items else [],
                'least_worn': json.loads(self.least_worn_items) if self.least_worn_items else [],
                'unworn': json.loads(self.unworn_items) if self.unworn_items else [],
                'average_frequency': self.average_wear_frequency
            },
            'style_analytics': {
                'styles': json.loads(self.style_distribution) if self.style_distribution else {},
                'formality': json.loads(self.formality_distribution) if self.formality_distribution else {},
                'seasonal': json.loads(self.seasonal_distribution) if self.seasonal_distribution else {}
            },
            'health_metrics': {
                'versatility_score': self.versatility_score,
                'completeness_score': self.completeness_score,
                'efficiency_score': self.efficiency_score,
                'style_coherence_score': self.style_coherence_score
            },
            'recommendations': {
                'gaps': json.loads(self.wardrobe_gaps) if self.wardrobe_gaps else [],
                'duplicates': json.loads(self.duplicate_items) if self.duplicate_items else [],
                'underutilized': json.loads(self.underutilized_items) if self.underutilized_items else []
            },
            'created_at': self.created_at.isoformat()
        }

class BatchProcessingJob(db.Model):
    """
    Batch processing jobs for wardrobe operations
    "We girls have no time" - Bulk operations in the background!
    """
    __tablename__ = 'batch_processing_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Job information
    job_type = db.Column(db.String(100), nullable=False)  # analyze_images, organize_wardrobe, etc.
    job_name = db.Column(db.String(200))
    job_description = db.Column(db.Text)
    
    # Job parameters
    job_parameters = db.Column(db.Text)  # JSON object with job-specific parameters
    
    # Job status
    status = db.Column(db.String(50), default='pending')  # pending, running, completed, failed
    progress_percentage = db.Column(db.Float, default=0.0)
    
    # Job results
    total_items = db.Column(db.Integer, default=0)
    processed_items = db.Column(db.Integer, default=0)
    successful_items = db.Column(db.Integer, default=0)
    failed_items = db.Column(db.Integer, default=0)
    
    # Job output
    results = db.Column(db.Text)  # JSON object with job results
    error_log = db.Column(db.Text)  # JSON array of errors
    
    # Timing
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    estimated_completion = db.Column(db.DateTime)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_info': {
                'type': self.job_type,
                'name': self.job_name,
                'description': self.job_description,
                'parameters': json.loads(self.job_parameters) if self.job_parameters else {}
            },
            'status': {
                'current': self.status,
                'progress': self.progress_percentage
            },
            'metrics': {
                'total_items': self.total_items,
                'processed': self.processed_items,
                'successful': self.successful_items,
                'failed': self.failed_items
            },
            'output': {
                'results': json.loads(self.results) if self.results else {},
                'errors': json.loads(self.error_log) if self.error_log else []
            },
            'timing': {
                'created_at': self.created_at.isoformat(),
                'started_at': self.started_at.isoformat() if self.started_at else None,
                'completed_at': self.completed_at.isoformat() if self.completed_at else None,
                'estimated_completion': self.estimated_completion.isoformat() if self.estimated_completion else None,
                'updated_at': self.updated_at.isoformat()
            }
        }

class WardrobeTag(db.Model):
    """
    Flexible tagging system for wardrobe items
    "We girls have no time" - Smart tagging for instant organization!
    """
    __tablename__ = 'wardrobe_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Tag information
    name = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(50))  # style, occasion, season, color, etc.
    description = db.Column(db.Text)
    
    # Tag metadata
    usage_count = db.Column(db.Integer, default=0)
    auto_generated = db.Column(db.Boolean, default=False)
    
    # Tag styling
    color = db.Column(db.String(7))  # Hex color code
    icon = db.Column(db.String(50))  # Icon name or emoji
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'metadata': {
                'usage_count': self.usage_count,
                'auto_generated': self.auto_generated
            },
            'styling': {
                'color': self.color,
                'icon': self.icon
            },
            'timestamps': {
                'created_at': self.created_at.isoformat(),
                'last_used': self.last_used.isoformat() if self.last_used else None
            }
        }

class WardrobeItemTag(db.Model):
    """
    Many-to-many relationship between wardrobe items and tags
    "We girls have no time" - Flexible item tagging!
    """
    __tablename__ = 'wardrobe_item_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    wardrobe_item_id = db.Column(db.Integer, nullable=False, index=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('wardrobe_tags.id'), nullable=False)
    
    # Tagging metadata
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    added_by = db.Column(db.String(50), default='user')  # user, auto, ai
    confidence = db.Column(db.Float, default=1.0)  # Confidence for auto-generated tags
    
    # Relationship
    tag = db.relationship('WardrobeTag', backref='item_associations')

class WardrobeMaintenanceLog(db.Model):
    """
    Maintenance and care log for wardrobe items
    "We girls have no time" - Smart care tracking!
    """
    __tablename__ = 'wardrobe_maintenance_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    wardrobe_item_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Maintenance information
    maintenance_type = db.Column(db.String(100), nullable=False)  # wash, dry_clean, repair, etc.
    maintenance_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Maintenance details
    notes = db.Column(db.Text)
    cost = db.Column(db.Float)
    location = db.Column(db.String(200))  # Where maintenance was done
    
    # Care instructions
    care_instructions = db.Column(db.Text)
    next_maintenance_due = db.Column(db.DateTime)
    
    # Condition tracking
    condition_before = db.Column(db.String(50))  # excellent, good, fair, poor
    condition_after = db.Column(db.String(50))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'wardrobe_item_id': self.wardrobe_item_id,
            'maintenance_info': {
                'type': self.maintenance_type,
                'date': self.maintenance_date.isoformat(),
                'notes': self.notes,
                'cost': self.cost,
                'location': self.location
            },
            'care_info': {
                'instructions': self.care_instructions,
                'next_due': self.next_maintenance_due.isoformat() if self.next_maintenance_due else None
            },
            'condition': {
                'before': self.condition_before,
                'after': self.condition_after
            },
            'created_at': self.created_at.isoformat()
        }

