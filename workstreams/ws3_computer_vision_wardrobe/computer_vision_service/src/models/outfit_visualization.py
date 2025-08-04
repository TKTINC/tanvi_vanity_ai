"""
WS3-P3: Outfit Visualization & Virtual Try-On
Outfit Visualization Models for Tanvi Vanity Agent
"We girls have no time" - Instant outfit visualization and virtual try-on!
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

class OutfitComposition(db.Model):
    """
    Complete outfit compositions with multiple items
    "We girls have no time" - Smart outfit creation in seconds!
    """
    __tablename__ = 'outfit_compositions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Outfit information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    occasion = db.Column(db.String(100))  # work, casual, date, party, formal
    season = db.Column(db.String(50))  # spring, summer, fall, winter
    
    # Outfit composition
    top_item_id = db.Column(db.Integer)
    bottom_item_id = db.Column(db.Integer)
    dress_item_id = db.Column(db.Integer)
    outerwear_item_id = db.Column(db.Integer)
    shoes_item_id = db.Column(db.Integer)
    accessories = db.Column(db.Text)  # JSON array of accessory item IDs
    
    # Outfit metadata
    style_tags = db.Column(db.Text)  # JSON array of style tags
    color_palette = db.Column(db.Text)  # JSON array of colors
    formality_level = db.Column(db.Integer, default=5)  # 1-10 scale
    
    # User interaction
    favorite = db.Column(db.Boolean, default=False)
    wear_count = db.Column(db.Integer, default=0)
    last_worn = db.Column(db.DateTime)
    rating = db.Column(db.Float)  # User rating 1-5
    
    # AI analysis
    ai_confidence = db.Column(db.Float, default=0.0)  # AI confidence in outfit
    ai_style_score = db.Column(db.Float, default=0.0)  # Style coherence score
    ai_color_harmony = db.Column(db.Float, default=0.0)  # Color harmony score
    ai_occasion_fit = db.Column(db.Float, default=0.0)  # Occasion appropriateness
    
    # Visualization data
    visualization_url = db.Column(db.String(500))  # URL to generated visualization
    thumbnail_url = db.Column(db.String(500))  # URL to thumbnail
    layout_data = db.Column(db.Text)  # JSON layout information for visualization
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'outfit_info': {
                'name': self.name,
                'description': self.description,
                'occasion': self.occasion,
                'season': self.season
            },
            'composition': {
                'top_item_id': self.top_item_id,
                'bottom_item_id': self.bottom_item_id,
                'dress_item_id': self.dress_item_id,
                'outerwear_item_id': self.outerwear_item_id,
                'shoes_item_id': self.shoes_item_id,
                'accessories': json.loads(self.accessories) if self.accessories else []
            },
            'metadata': {
                'style_tags': json.loads(self.style_tags) if self.style_tags else [],
                'color_palette': json.loads(self.color_palette) if self.color_palette else [],
                'formality_level': self.formality_level
            },
            'user_interaction': {
                'favorite': self.favorite,
                'wear_count': self.wear_count,
                'last_worn': self.last_worn.isoformat() if self.last_worn else None,
                'rating': self.rating
            },
            'ai_analysis': {
                'confidence': self.ai_confidence,
                'style_score': self.ai_style_score,
                'color_harmony': self.ai_color_harmony,
                'occasion_fit': self.ai_occasion_fit
            },
            'visualization': {
                'url': self.visualization_url,
                'thumbnail': self.thumbnail_url,
                'layout': json.loads(self.layout_data) if self.layout_data else {}
            },
            'timestamps': {
                'created_at': self.created_at.isoformat(),
                'updated_at': self.updated_at.isoformat()
            }
        }

class VirtualTryOn(db.Model):
    """
    Virtual try-on sessions and results
    "We girls have no time" - Instant virtual try-on experience!
    """
    __tablename__ = 'virtual_try_ons'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Try-on session information
    session_name = db.Column(db.String(200))
    session_type = db.Column(db.String(50), default='single_item')  # single_item, outfit, comparison
    
    # Items being tried on
    primary_item_id = db.Column(db.Integer)
    outfit_composition_id = db.Column(db.Integer, db.ForeignKey('outfit_compositions.id'))
    comparison_items = db.Column(db.Text)  # JSON array of item IDs for comparison
    
    # User model/photo
    user_photo_url = db.Column(db.String(500))  # User's photo for try-on
    body_measurements = db.Column(db.Text)  # JSON object with measurements
    skin_tone = db.Column(db.String(50))
    hair_color = db.Column(db.String(50))
    
    # Try-on results
    result_image_url = db.Column(db.String(500))  # Generated try-on image
    result_thumbnail_url = db.Column(db.String(500))  # Thumbnail
    processing_time = db.Column(db.Float, default=0.0)  # Processing time in seconds
    
    # AI analysis of try-on
    fit_analysis = db.Column(db.Text)  # JSON object with fit analysis
    color_analysis = db.Column(db.Text)  # JSON object with color compatibility
    style_analysis = db.Column(db.Text)  # JSON object with style assessment
    overall_score = db.Column(db.Float, default=0.0)  # Overall try-on score
    
    # User feedback
    user_rating = db.Column(db.Float)  # User rating 1-5
    user_feedback = db.Column(db.Text)  # User comments
    would_purchase = db.Column(db.Boolean)  # Purchase intent
    
    # Session metadata
    device_type = db.Column(db.String(50))  # mobile, desktop, tablet
    session_duration = db.Column(db.Float)  # Session duration in seconds
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    outfit_composition = db.relationship('OutfitComposition', backref='try_on_sessions')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_info': {
                'name': self.session_name,
                'type': self.session_type,
                'device_type': self.device_type,
                'duration': self.session_duration
            },
            'try_on_items': {
                'primary_item_id': self.primary_item_id,
                'outfit_composition_id': self.outfit_composition_id,
                'comparison_items': json.loads(self.comparison_items) if self.comparison_items else []
            },
            'user_model': {
                'photo_url': self.user_photo_url,
                'measurements': json.loads(self.body_measurements) if self.body_measurements else {},
                'skin_tone': self.skin_tone,
                'hair_color': self.hair_color
            },
            'results': {
                'image_url': self.result_image_url,
                'thumbnail_url': self.result_thumbnail_url,
                'processing_time': self.processing_time
            },
            'ai_analysis': {
                'fit': json.loads(self.fit_analysis) if self.fit_analysis else {},
                'color': json.loads(self.color_analysis) if self.color_analysis else {},
                'style': json.loads(self.style_analysis) if self.style_analysis else {},
                'overall_score': self.overall_score
            },
            'user_feedback': {
                'rating': self.user_rating,
                'feedback': self.user_feedback,
                'would_purchase': self.would_purchase
            },
            'created_at': self.created_at.isoformat()
        }

class OutfitVisualizationTemplate(db.Model):
    """
    Templates for outfit visualization layouts
    "We girls have no time" - Pre-designed layouts for instant visualization!
    """
    __tablename__ = 'outfit_visualization_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Template information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    template_type = db.Column(db.String(50))  # flat_lay, model, hanger, grid
    
    # Template configuration
    layout_config = db.Column(db.Text, nullable=False)  # JSON layout configuration
    item_positions = db.Column(db.Text)  # JSON item positioning rules
    background_options = db.Column(db.Text)  # JSON background options
    
    # Template metadata
    category = db.Column(db.String(100))  # casual, formal, seasonal, etc.
    style_compatibility = db.Column(db.Text)  # JSON array of compatible styles
    occasion_compatibility = db.Column(db.Text)  # JSON array of compatible occasions
    
    # Usage statistics
    usage_count = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float, default=0.0)
    
    # Template assets
    preview_image_url = db.Column(db.String(500))  # Template preview
    template_file_url = db.Column(db.String(500))  # Template file
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'template_info': {
                'name': self.name,
                'description': self.description,
                'type': self.template_type,
                'category': self.category
            },
            'configuration': {
                'layout': json.loads(self.layout_config) if self.layout_config else {},
                'positions': json.loads(self.item_positions) if self.item_positions else {},
                'backgrounds': json.loads(self.background_options) if self.background_options else {}
            },
            'compatibility': {
                'styles': json.loads(self.style_compatibility) if self.style_compatibility else [],
                'occasions': json.loads(self.occasion_compatibility) if self.occasion_compatibility else []
            },
            'statistics': {
                'usage_count': self.usage_count,
                'average_rating': self.average_rating
            },
            'assets': {
                'preview_url': self.preview_image_url,
                'template_url': self.template_file_url
            },
            'timestamps': {
                'created_at': self.created_at.isoformat(),
                'updated_at': self.updated_at.isoformat()
            }
        }

class OutfitStylingSession(db.Model):
    """
    Interactive outfit styling sessions
    "We girls have no time" - Guided styling sessions for perfect outfits!
    """
    __tablename__ = 'outfit_styling_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Session information
    session_name = db.Column(db.String(200))
    session_goal = db.Column(db.String(200))  # "Find work outfit", "Date night look", etc.
    target_occasion = db.Column(db.String(100))
    target_style = db.Column(db.String(100))
    
    # Session parameters
    budget_range = db.Column(db.String(50))  # "low", "medium", "high", "unlimited"
    time_constraint = db.Column(db.String(50))  # "quick", "thorough", "detailed"
    style_preferences = db.Column(db.Text)  # JSON object with preferences
    
    # Session progress
    current_step = db.Column(db.String(100))  # Current step in styling process
    steps_completed = db.Column(db.Text)  # JSON array of completed steps
    total_steps = db.Column(db.Integer, default=5)
    progress_percentage = db.Column(db.Float, default=0.0)
    
    # Session results
    generated_outfits = db.Column(db.Text)  # JSON array of outfit composition IDs
    selected_outfit_id = db.Column(db.Integer, db.ForeignKey('outfit_compositions.id'))
    alternative_outfits = db.Column(db.Text)  # JSON array of alternative outfit IDs
    
    # AI assistance
    ai_suggestions = db.Column(db.Text)  # JSON array of AI suggestions
    ai_reasoning = db.Column(db.Text)  # JSON object with AI reasoning
    styling_tips = db.Column(db.Text)  # JSON array of styling tips
    
    # User interaction
    user_choices = db.Column(db.Text)  # JSON object with user choices throughout session
    user_feedback = db.Column(db.Text)  # JSON object with user feedback
    session_rating = db.Column(db.Float)  # Overall session rating
    
    # Session metadata
    session_duration = db.Column(db.Float)  # Total session duration in minutes
    device_type = db.Column(db.String(50))
    session_status = db.Column(db.String(50), default='active')  # active, completed, abandoned
    
    # Metadata
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationship
    selected_outfit = db.relationship('OutfitComposition', backref='styling_sessions')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_info': {
                'name': self.session_name,
                'goal': self.session_goal,
                'target_occasion': self.target_occasion,
                'target_style': self.target_style,
                'status': self.session_status
            },
            'parameters': {
                'budget_range': self.budget_range,
                'time_constraint': self.time_constraint,
                'preferences': json.loads(self.style_preferences) if self.style_preferences else {}
            },
            'progress': {
                'current_step': self.current_step,
                'completed_steps': json.loads(self.steps_completed) if self.steps_completed else [],
                'total_steps': self.total_steps,
                'percentage': self.progress_percentage
            },
            'results': {
                'generated_outfits': json.loads(self.generated_outfits) if self.generated_outfits else [],
                'selected_outfit_id': self.selected_outfit_id,
                'alternatives': json.loads(self.alternative_outfits) if self.alternative_outfits else []
            },
            'ai_assistance': {
                'suggestions': json.loads(self.ai_suggestions) if self.ai_suggestions else [],
                'reasoning': json.loads(self.ai_reasoning) if self.ai_reasoning else {},
                'tips': json.loads(self.styling_tips) if self.styling_tips else []
            },
            'user_interaction': {
                'choices': json.loads(self.user_choices) if self.user_choices else {},
                'feedback': json.loads(self.user_feedback) if self.user_feedback else {},
                'rating': self.session_rating
            },
            'session_metadata': {
                'duration': self.session_duration,
                'device_type': self.device_type,
                'started_at': self.started_at.isoformat(),
                'completed_at': self.completed_at.isoformat() if self.completed_at else None
            }
        }

class OutfitVisualizationJob(db.Model):
    """
    Background jobs for outfit visualization generation
    "We girls have no time" - Background processing for instant results!
    """
    __tablename__ = 'outfit_visualization_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    
    # Job information
    job_type = db.Column(db.String(100), nullable=False)  # outfit_visualization, virtual_try_on, batch_visualization
    outfit_composition_id = db.Column(db.Integer, db.ForeignKey('outfit_compositions.id'))
    template_id = db.Column(db.Integer, db.ForeignKey('outfit_visualization_templates.id'))
    
    # Job parameters
    job_parameters = db.Column(db.Text)  # JSON object with job-specific parameters
    visualization_options = db.Column(db.Text)  # JSON object with visualization options
    
    # Job status
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    progress_percentage = db.Column(db.Float, default=0.0)
    
    # Job results
    result_urls = db.Column(db.Text)  # JSON array of generated image URLs
    thumbnail_urls = db.Column(db.Text)  # JSON array of thumbnail URLs
    processing_time = db.Column(db.Float, default=0.0)
    
    # Error handling
    error_message = db.Column(db.Text)
    retry_count = db.Column(db.Integer, default=0)
    max_retries = db.Column(db.Integer, default=3)
    
    # Timing
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    estimated_completion = db.Column(db.DateTime)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    outfit_composition = db.relationship('OutfitComposition', backref='visualization_jobs')
    template = db.relationship('OutfitVisualizationTemplate', backref='visualization_jobs')
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_info': {
                'type': self.job_type,
                'outfit_composition_id': self.outfit_composition_id,
                'template_id': self.template_id
            },
            'parameters': {
                'job_params': json.loads(self.job_parameters) if self.job_parameters else {},
                'visualization_options': json.loads(self.visualization_options) if self.visualization_options else {}
            },
            'status': {
                'current': self.status,
                'progress': self.progress_percentage
            },
            'results': {
                'urls': json.loads(self.result_urls) if self.result_urls else [],
                'thumbnails': json.loads(self.thumbnail_urls) if self.thumbnail_urls else [],
                'processing_time': self.processing_time
            },
            'error_handling': {
                'error_message': self.error_message,
                'retry_count': self.retry_count,
                'max_retries': self.max_retries
            },
            'timing': {
                'created_at': self.created_at.isoformat(),
                'started_at': self.started_at.isoformat() if self.started_at else None,
                'completed_at': self.completed_at.isoformat() if self.completed_at else None,
                'estimated_completion': self.estimated_completion.isoformat() if self.estimated_completion else None,
                'updated_at': self.updated_at.isoformat()
            }
        }

