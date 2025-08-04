from datetime import datetime
import json

# Import db from user module to avoid circular imports
from src.models.user import db

class StyleProfile(db.Model):
    """
    Enhanced style profile for personalized recommendations
    "We girls have no time" - Smart style profiling with minimal input
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Body type and measurements for quick fit recommendations
    body_type = db.Column(db.String(20), nullable=True)  # pear, apple, hourglass, rectangle, inverted_triangle
    height_range = db.Column(db.String(20), nullable=True)  # petite, average, tall
    measurements = db.Column(db.Text, nullable=True)  # JSON: bust, waist, hips, etc.
    
    # Style personality - "We girls have no time" for style quizzes
    style_personality = db.Column(db.String(30), nullable=True)  # minimalist, bohemian, classic, edgy, romantic
    lifestyle = db.Column(db.String(30), nullable=True)  # student, professional, creative, entrepreneur
    activity_level = db.Column(db.String(20), nullable=True)  # low, moderate, high
    
    # Color analysis for quick outfit coordination
    skin_tone = db.Column(db.String(20), nullable=True)  # warm, cool, neutral
    hair_color = db.Column(db.String(30), nullable=True)
    eye_color = db.Column(db.String(30), nullable=True)
    color_season = db.Column(db.String(20), nullable=True)  # spring, summer, autumn, winter
    
    # Quick preferences for AI styling
    favorite_colors = db.Column(db.Text, nullable=True)  # JSON array
    colors_to_avoid = db.Column(db.Text, nullable=True)  # JSON array
    preferred_fits = db.Column(db.Text, nullable=True)  # JSON: tight, loose, fitted, etc.
    style_goals = db.Column(db.Text, nullable=True)  # JSON: confidence, comfort, trendy, etc.
    
    # Occasion-based preferences
    work_style = db.Column(db.String(30), nullable=True)  # business, business_casual, creative, casual
    weekend_style = db.Column(db.String(30), nullable=True)  # sporty, casual, chic, bohemian
    evening_style = db.Column(db.String(30), nullable=True)  # elegant, edgy, romantic, minimalist
    
    # Quick setup completion tracking
    profile_completion = db.Column(db.Integer, default=0)  # Percentage 0-100
    last_style_quiz = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<StyleProfile {self.user_id}>'

    def calculate_completion(self):
        """Calculate profile completion percentage for quick overview"""
        total_fields = 15
        completed_fields = 0
        
        if self.body_type:
            completed_fields += 1
        if self.height_range:
            completed_fields += 1
        if self.measurements:
            completed_fields += 1
        if self.style_personality:
            completed_fields += 1
        if self.lifestyle:
            completed_fields += 1
        if self.skin_tone:
            completed_fields += 1
        if self.hair_color:
            completed_fields += 1
        if self.eye_color:
            completed_fields += 1
        if self.favorite_colors:
            completed_fields += 1
        if self.preferred_fits:
            completed_fields += 1
        if self.style_goals:
            completed_fields += 1
        if self.work_style:
            completed_fields += 1
        if self.weekend_style:
            completed_fields += 1
        if self.evening_style:
            completed_fields += 1
        if self.activity_level:
            completed_fields += 1
        
        self.profile_completion = int((completed_fields / total_fields) * 100)
        return self.profile_completion

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'body_type': self.body_type,
            'height_range': self.height_range,
            'measurements': json.loads(self.measurements) if self.measurements else None,
            'style_personality': self.style_personality,
            'lifestyle': self.lifestyle,
            'activity_level': self.activity_level,
            'skin_tone': self.skin_tone,
            'hair_color': self.hair_color,
            'eye_color': self.eye_color,
            'color_season': self.color_season,
            'favorite_colors': json.loads(self.favorite_colors) if self.favorite_colors else None,
            'colors_to_avoid': json.loads(self.colors_to_avoid) if self.colors_to_avoid else None,
            'preferred_fits': json.loads(self.preferred_fits) if self.preferred_fits else None,
            'style_goals': json.loads(self.style_goals) if self.style_goals else None,
            'work_style': self.work_style,
            'weekend_style': self.weekend_style,
            'evening_style': self.evening_style,
            'profile_completion': self.calculate_completion(),
            'last_style_quiz': self.last_style_quiz.isoformat() if self.last_style_quiz else None,
            'updated_at': self.updated_at.isoformat()
        }


class WardrobeItem(db.Model):
    """
    Individual wardrobe items for outfit planning
    "We girls have no time" - Quick item cataloging with smart categorization
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Basic item information
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(30), nullable=False)  # top, bottom, dress, outerwear, shoes, accessories
    subcategory = db.Column(db.String(30), nullable=True)  # blouse, jeans, sneakers, etc.
    brand = db.Column(db.String(50), nullable=True)
    
    # Visual attributes for AI matching
    primary_color = db.Column(db.String(30), nullable=True)
    secondary_colors = db.Column(db.Text, nullable=True)  # JSON array
    pattern = db.Column(db.String(30), nullable=True)  # solid, stripes, floral, geometric, etc.
    material = db.Column(db.String(50), nullable=True)  # cotton, denim, silk, leather, etc.
    
    # Fit and style attributes
    fit_type = db.Column(db.String(30), nullable=True)  # tight, fitted, loose, oversized
    style_tags = db.Column(db.Text, nullable=True)  # JSON: casual, formal, trendy, vintage, etc.
    season_appropriate = db.Column(db.Text, nullable=True)  # JSON: spring, summer, fall, winter
    
    # Usage tracking for smart recommendations
    purchase_date = db.Column(db.Date, nullable=True)
    last_worn = db.Column(db.Date, nullable=True)
    wear_count = db.Column(db.Integer, default=0)
    favorite = db.Column(db.Boolean, default=False)
    
    # Quick organization
    location = db.Column(db.String(50), nullable=True)  # closet, dresser, laundry, etc.
    condition = db.Column(db.String(20), default='good')  # excellent, good, fair, needs_repair
    
    # Image storage
    image_url = db.Column(db.String(255), nullable=True)
    thumbnail_url = db.Column(db.String(255), nullable=True)
    
    # AI analysis results
    ai_tags = db.Column(db.Text, nullable=True)  # JSON: AI-generated tags
    versatility_score = db.Column(db.Float, nullable=True)  # 0-10 how versatile the item is
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<WardrobeItem {self.name}>'

    def increment_wear_count(self):
        """Track when item is worn for usage analytics"""
        self.wear_count += 1
        self.last_worn = datetime.utcnow().date()
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'category': self.category,
            'subcategory': self.subcategory,
            'brand': self.brand,
            'primary_color': self.primary_color,
            'secondary_colors': json.loads(self.secondary_colors) if self.secondary_colors else None,
            'pattern': self.pattern,
            'material': self.material,
            'fit_type': self.fit_type,
            'style_tags': json.loads(self.style_tags) if self.style_tags else None,
            'season_appropriate': json.loads(self.season_appropriate) if self.season_appropriate else None,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'last_worn': self.last_worn.isoformat() if self.last_worn else None,
            'wear_count': self.wear_count,
            'favorite': self.favorite,
            'location': self.location,
            'condition': self.condition,
            'image_url': self.image_url,
            'thumbnail_url': self.thumbnail_url,
            'ai_tags': json.loads(self.ai_tags) if self.ai_tags else None,
            'versatility_score': self.versatility_score,
            'updated_at': self.updated_at.isoformat()
        }


class OutfitHistory(db.Model):
    """
    Track outfit combinations and their success
    "We girls have no time" - Learn from past outfits for quick future recommendations
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Outfit composition
    outfit_name = db.Column(db.String(100), nullable=True)
    item_ids = db.Column(db.Text, nullable=False)  # JSON array of wardrobe item IDs
    
    # Context when worn
    occasion = db.Column(db.String(50), nullable=True)  # work, casual, date, party, etc.
    weather = db.Column(db.String(30), nullable=True)  # sunny, rainy, cold, hot, etc.
    season = db.Column(db.String(20), nullable=True)  # spring, summer, fall, winter
    location = db.Column(db.String(100), nullable=True)  # office, home, restaurant, etc.
    
    # User feedback for learning
    user_rating = db.Column(db.Integer, nullable=True)  # 1-5 stars
    comfort_level = db.Column(db.Integer, nullable=True)  # 1-5 scale
    confidence_level = db.Column(db.Integer, nullable=True)  # 1-5 scale
    received_compliments = db.Column(db.Boolean, default=False)
    
    # Social sharing
    shared_on_social = db.Column(db.Boolean, default=False)
    social_engagement = db.Column(db.Integer, default=0)  # likes, comments, etc.
    
    # Photo storage
    outfit_photo_url = db.Column(db.String(255), nullable=True)
    
    # AI analysis
    ai_style_score = db.Column(db.Float, nullable=True)  # AI assessment of outfit
    color_harmony_score = db.Column(db.Float, nullable=True)
    
    worn_date = db.Column(db.Date, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<OutfitHistory {self.id}>'

    def get_items(self):
        """Get the actual wardrobe items in this outfit"""
        if not self.item_ids:
            return []
        
        item_ids = json.loads(self.item_ids)
        return WardrobeItem.query.filter(WardrobeItem.id.in_(item_ids)).all()

    def calculate_success_score(self):
        """Calculate overall outfit success for learning"""
        scores = []
        
        if self.user_rating:
            scores.append(self.user_rating)
        if self.comfort_level:
            scores.append(self.comfort_level)
        if self.confidence_level:
            scores.append(self.confidence_level)
        if self.received_compliments:
            scores.append(5)
        if self.ai_style_score:
            scores.append(self.ai_style_score)
        
        return sum(scores) / len(scores) if scores else 0

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'outfit_name': self.outfit_name,
            'item_ids': json.loads(self.item_ids) if self.item_ids else [],
            'occasion': self.occasion,
            'weather': self.weather,
            'season': self.season,
            'location': self.location,
            'user_rating': self.user_rating,
            'comfort_level': self.comfort_level,
            'confidence_level': self.confidence_level,
            'received_compliments': self.received_compliments,
            'shared_on_social': self.shared_on_social,
            'social_engagement': self.social_engagement,
            'outfit_photo_url': self.outfit_photo_url,
            'ai_style_score': self.ai_style_score,
            'color_harmony_score': self.color_harmony_score,
            'success_score': self.calculate_success_score(),
            'worn_date': self.worn_date.isoformat(),
            'created_at': self.created_at.isoformat()
        }


class QuickStyleQuiz(db.Model):
    """
    Quick style assessment for rapid personalization
    "We girls have no time" - 2-minute style quiz for instant AI training
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Quiz metadata
    quiz_version = db.Column(db.String(10), default='1.0')
    completion_time = db.Column(db.Integer, nullable=True)  # seconds
    
    # Quick style questions (JSON responses)
    style_inspiration = db.Column(db.Text, nullable=True)  # JSON: celebrity, influencer, etc.
    shopping_frequency = db.Column(db.String(20), nullable=True)
    budget_comfort = db.Column(db.String(20), nullable=True)
    style_risk_level = db.Column(db.Integer, nullable=True)  # 1-5 scale
    
    # Image-based preferences (quick visual selection)
    preferred_outfits = db.Column(db.Text, nullable=True)  # JSON: outfit image IDs
    disliked_outfits = db.Column(db.Text, nullable=True)  # JSON: outfit image IDs
    
    # Lifestyle questions
    daily_activities = db.Column(db.Text, nullable=True)  # JSON array
    special_occasions = db.Column(db.Text, nullable=True)  # JSON array
    climate_location = db.Column(db.String(50), nullable=True)
    
    # Results and recommendations
    style_personality_result = db.Column(db.String(30), nullable=True)
    confidence_score = db.Column(db.Float, nullable=True)  # AI confidence in results
    recommendations = db.Column(db.Text, nullable=True)  # JSON: immediate recommendations
    
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<QuickStyleQuiz {self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'quiz_version': self.quiz_version,
            'completion_time': self.completion_time,
            'style_inspiration': json.loads(self.style_inspiration) if self.style_inspiration else None,
            'shopping_frequency': self.shopping_frequency,
            'budget_comfort': self.budget_comfort,
            'style_risk_level': self.style_risk_level,
            'preferred_outfits': json.loads(self.preferred_outfits) if self.preferred_outfits else None,
            'disliked_outfits': json.loads(self.disliked_outfits) if self.disliked_outfits else None,
            'daily_activities': json.loads(self.daily_activities) if self.daily_activities else None,
            'special_occasions': json.loads(self.special_occasions) if self.special_occasions else None,
            'climate_location': self.climate_location,
            'style_personality_result': self.style_personality_result,
            'confidence_score': self.confidence_score,
            'recommendations': json.loads(self.recommendations) if self.recommendations else None,
            'completed_at': self.completed_at.isoformat()
        }

