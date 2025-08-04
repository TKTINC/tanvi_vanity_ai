from datetime import datetime, date, timedelta
import json
import math
import random
from collections import defaultdict, Counter
from src.models.user import db
from src.models.ai_models import StyleAnalysis, OutfitRecommendation, AIInsight
from src.models.enhanced_recommendations import OutfitFeedback, WeatherOutfitRule, SeasonalRecommendation
from src.models.personalization import UserStyleProfile

class TrendForecast(db.Model):
    """
    AI-powered trend forecasting and prediction
    "We girls have no time" - Know what's trending before it's trending!
    """
    __tablename__ = 'trend_forecast'
    
    id = db.Column(db.Integer, primary_key=True)
    trend_name = db.Column(db.String(100), nullable=False)
    trend_category = db.Column(db.String(50), nullable=False)  # color, style, pattern, fabric, etc.
    
    # Trend timing and lifecycle
    forecast_date = db.Column(db.DateTime, default=datetime.utcnow)
    trend_start_date = db.Column(db.Date, nullable=True)  # When trend is expected to start
    trend_peak_date = db.Column(db.Date, nullable=True)   # When trend reaches peak popularity
    trend_end_date = db.Column(db.Date, nullable=True)    # When trend is expected to decline
    
    # Trend strength and confidence
    confidence_score = db.Column(db.Float, default=0.5)  # How confident we are in this forecast (0-1)
    trend_strength = db.Column(db.Float, default=0.5)    # How strong/popular the trend will be (0-1)
    adoption_speed = db.Column(db.String(20), default='medium')  # slow, medium, fast
    
    # Trend characteristics
    target_demographics = db.Column(db.Text, nullable=True)  # JSON: age groups, style personalities, etc.
    style_compatibility = db.Column(db.Text, nullable=True)  # JSON: which styles this trend works with
    seasonal_relevance = db.Column(db.Text, nullable=True)   # JSON: which seasons this trend is relevant
    
    # Trend details
    description = db.Column(db.Text, nullable=True)
    styling_tips = db.Column(db.Text, nullable=True)  # JSON: how to style this trend
    color_palette = db.Column(db.Text, nullable=True)  # JSON: associated colors
    
    # Market and adoption data
    market_penetration = db.Column(db.Float, default=0.0)  # Current market penetration (0-1)
    influencer_adoption = db.Column(db.Float, default=0.0)  # Influencer adoption rate (0-1)
    retail_availability = db.Column(db.Float, default=0.0)  # Retail availability (0-1)
    
    # Trend status
    status = db.Column(db.String(20), default='predicted')  # predicted, emerging, trending, peak, declining, ended
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TrendForecast {self.trend_name}:{self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'trend_name': self.trend_name,
            'trend_category': self.trend_category,
            'forecast_date': self.forecast_date.isoformat() if self.forecast_date else None,
            'trend_start_date': self.trend_start_date.isoformat() if self.trend_start_date else None,
            'trend_peak_date': self.trend_peak_date.isoformat() if self.trend_peak_date else None,
            'trend_end_date': self.trend_end_date.isoformat() if self.trend_end_date else None,
            'confidence_score': self.confidence_score,
            'trend_strength': self.trend_strength,
            'adoption_speed': self.adoption_speed,
            'target_demographics': json.loads(self.target_demographics) if self.target_demographics else {},
            'style_compatibility': json.loads(self.style_compatibility) if self.style_compatibility else {},
            'seasonal_relevance': json.loads(self.seasonal_relevance) if self.seasonal_relevance else {},
            'description': self.description,
            'styling_tips': json.loads(self.styling_tips) if self.styling_tips else [],
            'color_palette': json.loads(self.color_palette) if self.color_palette else [],
            'market_penetration': self.market_penetration,
            'influencer_adoption': self.influencer_adoption,
            'retail_availability': self.retail_availability,
            'status': self.status,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
    
    @staticmethod
    def get_current_trends(limit=10):
        """Get currently trending items"""
        return TrendForecast.query.filter(
            TrendForecast.status.in_(['trending', 'peak'])
        ).order_by(TrendForecast.trend_strength.desc()).limit(limit).all()
    
    @staticmethod
    def get_emerging_trends(limit=5):
        """Get emerging trends to watch"""
        return TrendForecast.query.filter(
            TrendForecast.status == 'emerging'
        ).order_by(TrendForecast.confidence_score.desc()).limit(limit).all()
    
    @staticmethod
    def get_predicted_trends(limit=5):
        """Get predicted future trends"""
        return TrendForecast.query.filter(
            TrendForecast.status == 'predicted'
        ).order_by(TrendForecast.confidence_score.desc()).limit(limit).all()


class WardrobeOptimization(db.Model):
    """
    Advanced wardrobe optimization and gap analysis
    "We girls have no time" - Optimize your wardrobe intelligently!
    """
    __tablename__ = 'wardrobe_optimization'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Wardrobe composition analysis
    total_items = db.Column(db.Integer, default=0)
    category_distribution = db.Column(db.Text, nullable=True)  # JSON: category breakdown
    color_distribution = db.Column(db.Text, nullable=True)     # JSON: color breakdown
    style_distribution = db.Column(db.Text, nullable=True)     # JSON: style breakdown
    
    # Optimization scores
    versatility_score = db.Column(db.Float, default=0.5)      # How versatile the wardrobe is (0-1)
    completeness_score = db.Column(db.Float, default=0.5)     # How complete the wardrobe is (0-1)
    efficiency_score = db.Column(db.Float, default=0.5)       # How efficiently items are used (0-1)
    style_coherence_score = db.Column(db.Float, default=0.5)  # How coherent the style is (0-1)
    
    # Gap analysis
    missing_essentials = db.Column(db.Text, nullable=True)     # JSON: essential items missing
    underrepresented_categories = db.Column(db.Text, nullable=True)  # JSON: categories needing more items
    color_gaps = db.Column(db.Text, nullable=True)            # JSON: missing colors for better coordination
    style_gaps = db.Column(db.Text, nullable=True)            # JSON: style elements missing
    
    # Optimization recommendations
    items_to_add = db.Column(db.Text, nullable=True)          # JSON: specific items to add
    items_to_remove = db.Column(db.Text, nullable=True)       # JSON: items that could be removed
    styling_opportunities = db.Column(db.Text, nullable=True)  # JSON: new styling combinations possible
    
    # Usage analysis
    high_usage_items = db.Column(db.Text, nullable=True)      # JSON: most worn items
    low_usage_items = db.Column(db.Text, nullable=True)       # JSON: rarely worn items
    seasonal_gaps = db.Column(db.Text, nullable=True)         # JSON: seasonal wardrobe gaps
    
    # Budget and priority analysis
    priority_purchases = db.Column(db.Text, nullable=True)    # JSON: prioritized shopping list
    budget_allocation = db.Column(db.Text, nullable=True)     # JSON: suggested budget allocation
    cost_per_wear_analysis = db.Column(db.Text, nullable=True)  # JSON: cost efficiency analysis
    
    def __repr__(self):
        return f'<WardrobeOptimization {self.user_id}:{self.analysis_date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'total_items': self.total_items,
            'category_distribution': json.loads(self.category_distribution) if self.category_distribution else {},
            'color_distribution': json.loads(self.color_distribution) if self.color_distribution else {},
            'style_distribution': json.loads(self.style_distribution) if self.style_distribution else {},
            'versatility_score': self.versatility_score,
            'completeness_score': self.completeness_score,
            'efficiency_score': self.efficiency_score,
            'style_coherence_score': self.style_coherence_score,
            'missing_essentials': json.loads(self.missing_essentials) if self.missing_essentials else [],
            'underrepresented_categories': json.loads(self.underrepresented_categories) if self.underrepresented_categories else [],
            'color_gaps': json.loads(self.color_gaps) if self.color_gaps else [],
            'style_gaps': json.loads(self.style_gaps) if self.style_gaps else [],
            'items_to_add': json.loads(self.items_to_add) if self.items_to_add else [],
            'items_to_remove': json.loads(self.items_to_remove) if self.items_to_remove else [],
            'styling_opportunities': json.loads(self.styling_opportunities) if self.styling_opportunities else [],
            'high_usage_items': json.loads(self.high_usage_items) if self.high_usage_items else [],
            'low_usage_items': json.loads(self.low_usage_items) if self.low_usage_items else [],
            'seasonal_gaps': json.loads(self.seasonal_gaps) if self.seasonal_gaps else [],
            'priority_purchases': json.loads(self.priority_purchases) if self.priority_purchases else [],
            'budget_allocation': json.loads(self.budget_allocation) if self.budget_allocation else {},
            'cost_per_wear_analysis': json.loads(self.cost_per_wear_analysis) if self.cost_per_wear_analysis else {}
        }


class StyleCompatibility(db.Model):
    """
    Advanced style compatibility and matching analysis
    "We girls have no time" - Perfect style matching every time!
    """
    __tablename__ = 'style_compatibility'
    
    id = db.Column(db.Integer, primary_key=True)
    item1_id = db.Column(db.String(50), nullable=False)  # First item identifier
    item2_id = db.Column(db.String(50), nullable=False)  # Second item identifier
    
    # Compatibility scores
    overall_compatibility = db.Column(db.Float, default=0.5)  # Overall compatibility (0-1)
    color_compatibility = db.Column(db.Float, default=0.5)    # Color harmony (0-1)
    style_compatibility = db.Column(db.Float, default=0.5)    # Style matching (0-1)
    formality_compatibility = db.Column(db.Float, default=0.5)  # Formality level matching (0-1)
    seasonal_compatibility = db.Column(db.Float, default=0.5)   # Seasonal appropriateness (0-1)
    
    # Compatibility factors
    compatibility_reasons = db.Column(db.Text, nullable=True)  # JSON: why items work together
    incompatibility_reasons = db.Column(db.Text, nullable=True)  # JSON: potential issues
    styling_suggestions = db.Column(db.Text, nullable=True)    # JSON: how to style together
    
    # Context and occasions
    suitable_occasions = db.Column(db.Text, nullable=True)     # JSON: occasions where this combo works
    unsuitable_occasions = db.Column(db.Text, nullable=True)   # JSON: occasions to avoid this combo
    styling_difficulty = db.Column(db.String(20), default='easy')  # easy, medium, advanced
    
    # Analysis metadata
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    confidence_score = db.Column(db.Float, default=0.5)        # Confidence in analysis (0-1)
    user_feedback_score = db.Column(db.Float, nullable=True)   # User feedback on this combination
    
    def __repr__(self):
        return f'<StyleCompatibility {self.item1_id}+{self.item2_id}:{self.overall_compatibility}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'item1_id': self.item1_id,
            'item2_id': self.item2_id,
            'overall_compatibility': self.overall_compatibility,
            'color_compatibility': self.color_compatibility,
            'style_compatibility': self.style_compatibility,
            'formality_compatibility': self.formality_compatibility,
            'seasonal_compatibility': self.seasonal_compatibility,
            'compatibility_reasons': json.loads(self.compatibility_reasons) if self.compatibility_reasons else [],
            'incompatibility_reasons': json.loads(self.incompatibility_reasons) if self.incompatibility_reasons else [],
            'styling_suggestions': json.loads(self.styling_suggestions) if self.styling_suggestions else [],
            'suitable_occasions': json.loads(self.suitable_occasions) if self.suitable_occasions else [],
            'unsuitable_occasions': json.loads(self.unsuitable_occasions) if self.unsuitable_occasions else [],
            'styling_difficulty': self.styling_difficulty,
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'confidence_score': self.confidence_score,
            'user_feedback_score': self.user_feedback_score
        }


class PredictiveRecommendation(db.Model):
    """
    Predictive AI recommendations based on trends, behavior, and context
    "We girls have no time" - AI that predicts what you'll love!
    """
    __tablename__ = 'predictive_recommendation'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    recommendation_type = db.Column(db.String(50), nullable=False)  # outfit, item, style, trend
    
    # Prediction details
    predicted_item_ids = db.Column(db.Text, nullable=True)     # JSON: predicted items/outfits
    prediction_confidence = db.Column(db.Float, default=0.5)   # Confidence in prediction (0-1)
    prediction_reasoning = db.Column(db.Text, nullable=True)   # JSON: why this was predicted
    
    # Context and timing
    predicted_for_date = db.Column(db.Date, nullable=True)     # When this will be relevant
    predicted_occasion = db.Column(db.String(50), nullable=True)  # Predicted occasion
    predicted_context = db.Column(db.Text, nullable=True)      # JSON: weather, season, etc.
    
    # Prediction factors
    trend_influence = db.Column(db.Float, default=0.0)         # How much trends influenced this (0-1)
    personal_style_influence = db.Column(db.Float, default=0.0)  # How much personal style influenced (0-1)
    behavioral_influence = db.Column(db.Float, default=0.0)    # How much past behavior influenced (0-1)
    seasonal_influence = db.Column(db.Float, default=0.0)      # How much season influenced (0-1)
    
    # Prediction metadata
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    expires_date = db.Column(db.DateTime, nullable=True)       # When prediction becomes irrelevant
    status = db.Column(db.String(20), default='active')       # active, fulfilled, expired, rejected
    
    # Validation and feedback
    user_interaction = db.Column(db.String(20), nullable=True)  # viewed, liked, disliked, used
    accuracy_score = db.Column(db.Float, nullable=True)        # How accurate the prediction was (0-1)
    feedback_date = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<PredictiveRecommendation {self.user_id}:{self.recommendation_type}:{self.prediction_confidence}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recommendation_type': self.recommendation_type,
            'predicted_item_ids': json.loads(self.predicted_item_ids) if self.predicted_item_ids else [],
            'prediction_confidence': self.prediction_confidence,
            'prediction_reasoning': json.loads(self.prediction_reasoning) if self.prediction_reasoning else [],
            'predicted_for_date': self.predicted_for_date.isoformat() if self.predicted_for_date else None,
            'predicted_occasion': self.predicted_occasion,
            'predicted_context': json.loads(self.predicted_context) if self.predicted_context else {},
            'trend_influence': self.trend_influence,
            'personal_style_influence': self.personal_style_influence,
            'behavioral_influence': self.behavioral_influence,
            'seasonal_influence': self.seasonal_influence,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'expires_date': self.expires_date.isoformat() if self.expires_date else None,
            'status': self.status,
            'user_interaction': self.user_interaction,
            'accuracy_score': self.accuracy_score,
            'feedback_date': self.feedback_date.isoformat() if self.feedback_date else None
        }


class AdvancedAIEngine:
    """
    Advanced AI engine with predictive capabilities and trend analysis
    "We girls have no time" - Next-generation AI styling intelligence!
    """
    
    @staticmethod
    def generate_trend_forecast(trend_data=None):
        """
        Generate AI-powered trend forecasts
        "We girls have no time" - Know trends before they happen!
        """
        # Sample trend forecasts (in production, this would use real trend data)
        sample_trends = [
            {
                'trend_name': 'Oversized Blazers',
                'trend_category': 'style',
                'confidence_score': 0.85,
                'trend_strength': 0.9,
                'adoption_speed': 'fast',
                'description': 'Oversized blazers continue to dominate professional and casual styling',
                'styling_tips': ['Pair with fitted bottoms', 'Roll sleeves for casual look', 'Layer over dresses'],
                'color_palette': ['navy', 'black', 'cream', 'camel'],
                'target_demographics': {'age_groups': ['25-35', '35-45'], 'styles': ['minimalist', 'classic']},
                'style_compatibility': {'classic': 0.9, 'minimalist': 0.8, 'edgy': 0.6},
                'seasonal_relevance': {'fall': 0.9, 'winter': 0.8, 'spring': 0.7},
                'status': 'trending'
            },
            {
                'trend_name': 'Earth Tone Palettes',
                'trend_category': 'color',
                'confidence_score': 0.78,
                'trend_strength': 0.75,
                'adoption_speed': 'medium',
                'description': 'Warm earth tones creating sophisticated, grounded looks',
                'styling_tips': ['Mix different earth tones', 'Add texture for interest', 'Pair with gold accessories'],
                'color_palette': ['terracotta', 'sage green', 'warm brown', 'cream'],
                'target_demographics': {'age_groups': ['25-45'], 'styles': ['bohemian', 'minimalist']},
                'style_compatibility': {'bohemian': 0.9, 'minimalist': 0.8, 'romantic': 0.7},
                'seasonal_relevance': {'fall': 0.9, 'winter': 0.7, 'spring': 0.6},
                'status': 'emerging'
            },
            {
                'trend_name': 'Statement Sleeves',
                'trend_category': 'style',
                'confidence_score': 0.72,
                'trend_strength': 0.65,
                'adoption_speed': 'medium',
                'description': 'Dramatic sleeves adding interest to simple silhouettes',
                'styling_tips': ['Keep rest of outfit simple', 'Choose fitted bottoms', 'Minimal accessories'],
                'color_palette': ['white', 'black', 'jewel tones'],
                'target_demographics': {'age_groups': ['20-35'], 'styles': ['romantic', 'trendy']},
                'style_compatibility': {'romantic': 0.9, 'trendy': 0.8, 'classic': 0.5},
                'seasonal_relevance': {'spring': 0.8, 'summer': 0.7, 'fall': 0.6},
                'status': 'predicted'
            }
        ]
        
        # Create or update trend forecasts
        forecasts = []
        for trend_data in sample_trends:
            # Check if trend already exists
            existing_trend = TrendForecast.query.filter_by(trend_name=trend_data['trend_name']).first()
            
            if existing_trend:
                # Update existing trend
                existing_trend.confidence_score = trend_data['confidence_score']
                existing_trend.trend_strength = trend_data['trend_strength']
                existing_trend.status = trend_data['status']
                existing_trend.last_updated = datetime.utcnow()
                forecasts.append(existing_trend)
            else:
                # Create new trend forecast
                new_trend = TrendForecast(
                    trend_name=trend_data['trend_name'],
                    trend_category=trend_data['trend_category'],
                    confidence_score=trend_data['confidence_score'],
                    trend_strength=trend_data['trend_strength'],
                    adoption_speed=trend_data['adoption_speed'],
                    description=trend_data['description'],
                    styling_tips=json.dumps(trend_data['styling_tips']),
                    color_palette=json.dumps(trend_data['color_palette']),
                    target_demographics=json.dumps(trend_data['target_demographics']),
                    style_compatibility=json.dumps(trend_data['style_compatibility']),
                    seasonal_relevance=json.dumps(trend_data['seasonal_relevance']),
                    status=trend_data['status']
                )
                db.session.add(new_trend)
                forecasts.append(new_trend)
        
        db.session.commit()
        return [trend.to_dict() for trend in forecasts]
    
    @staticmethod
    def analyze_wardrobe_optimization(user_id, wardrobe_items):
        """
        Perform comprehensive wardrobe optimization analysis
        "We girls have no time" - Optimize your wardrobe intelligently!
        """
        if not wardrobe_items:
            return {
                'status': 'no_wardrobe',
                'message': 'No wardrobe items to analyze',
                'recommendation': 'Start building your wardrobe with essential pieces'
            }
        
        # Analyze wardrobe composition
        total_items = len(wardrobe_items)
        category_counts = Counter(item.get('category', 'unknown') for item in wardrobe_items)
        color_counts = Counter(item.get('primary_color', 'unknown') for item in wardrobe_items)
        
        # Calculate optimization scores
        versatility_score = AdvancedAIEngine._calculate_versatility_score(wardrobe_items)
        completeness_score = AdvancedAIEngine._calculate_completeness_score(category_counts)
        efficiency_score = AdvancedAIEngine._calculate_efficiency_score(wardrobe_items)
        style_coherence_score = AdvancedAIEngine._calculate_style_coherence_score(wardrobe_items)
        
        # Identify gaps and opportunities
        missing_essentials = AdvancedAIEngine._identify_missing_essentials(category_counts)
        color_gaps = AdvancedAIEngine._identify_color_gaps(color_counts)
        styling_opportunities = AdvancedAIEngine._identify_styling_opportunities(wardrobe_items)
        
        # Generate recommendations
        priority_purchases = AdvancedAIEngine._generate_priority_purchases(missing_essentials, color_gaps)
        
        # Create or update optimization record
        existing_optimization = WardrobeOptimization.query.filter_by(user_id=user_id).first()
        
        if existing_optimization:
            # Update existing record
            optimization = existing_optimization
            optimization.analysis_date = datetime.utcnow()
        else:
            # Create new record
            optimization = WardrobeOptimization(user_id=user_id)
            db.session.add(optimization)
        
        # Update optimization data
        optimization.total_items = total_items
        optimization.category_distribution = json.dumps(dict(category_counts))
        optimization.color_distribution = json.dumps(dict(color_counts))
        optimization.versatility_score = versatility_score
        optimization.completeness_score = completeness_score
        optimization.efficiency_score = efficiency_score
        optimization.style_coherence_score = style_coherence_score
        optimization.missing_essentials = json.dumps(missing_essentials)
        optimization.color_gaps = json.dumps(color_gaps)
        optimization.styling_opportunities = json.dumps(styling_opportunities)
        optimization.priority_purchases = json.dumps(priority_purchases)
        
        db.session.commit()
        
        return optimization.to_dict()
    
    @staticmethod
    def _calculate_versatility_score(wardrobe_items):
        """Calculate how versatile the wardrobe is"""
        if not wardrobe_items:
            return 0.0
        
        # Count items that can work for multiple occasions
        versatile_items = 0
        for item in wardrobe_items:
            category = item.get('category', '').lower()
            color = item.get('primary_color', '').lower()
            
            # Basic versatility rules
            if category in ['blazer', 'jeans', 'white shirt', 'black dress', 'cardigan']:
                versatile_items += 1
            elif color in ['black', 'white', 'navy', 'gray', 'beige']:
                versatile_items += 0.5
        
        return min(versatile_items / len(wardrobe_items), 1.0)
    
    @staticmethod
    def _calculate_completeness_score(category_counts):
        """Calculate how complete the wardrobe is"""
        essential_categories = ['tops', 'bottoms', 'dresses', 'outerwear', 'shoes']
        present_essentials = sum(1 for cat in essential_categories if cat in category_counts)
        return present_essentials / len(essential_categories)
    
    @staticmethod
    def _calculate_efficiency_score(wardrobe_items):
        """Calculate how efficiently items are used"""
        # In a real implementation, this would use actual wear data
        # For now, we'll estimate based on item types
        efficient_items = 0
        for item in wardrobe_items:
            # Items that are typically worn frequently
            category = item.get('category', '').lower()
            if category in ['jeans', 'basic tops', 'sneakers', 'cardigan']:
                efficient_items += 1
            else:
                efficient_items += 0.7  # Assume moderate efficiency
        
        return min(efficient_items / len(wardrobe_items), 1.0) if wardrobe_items else 0.0
    
    @staticmethod
    def _calculate_style_coherence_score(wardrobe_items):
        """Calculate how coherent the style is"""
        if not wardrobe_items:
            return 0.0
        
        # Count items that fit common style themes
        style_themes = defaultdict(int)
        for item in wardrobe_items:
            category = item.get('category', '').lower()
            color = item.get('primary_color', '').lower()
            
            # Assign style points
            if color in ['black', 'white', 'gray']:
                style_themes['minimalist'] += 1
            if category in ['blazer', 'dress pants', 'button-down']:
                style_themes['classic'] += 1
            if color in ['earth tones', 'brown', 'green']:
                style_themes['bohemian'] += 1
        
        # Calculate coherence based on dominant style
        if style_themes:
            max_style_count = max(style_themes.values())
            return min(max_style_count / len(wardrobe_items), 1.0)
        
        return 0.5  # Neutral score if no clear style
    
    @staticmethod
    def _identify_missing_essentials(category_counts):
        """Identify essential items missing from wardrobe"""
        essential_items = {
            'basic white shirt': 'tops' not in category_counts or category_counts['tops'] < 3,
            'well-fitted jeans': 'bottoms' not in category_counts or category_counts['bottoms'] < 2,
            'little black dress': 'dresses' not in category_counts,
            'versatile blazer': 'outerwear' not in category_counts,
            'comfortable flats': 'shoes' not in category_counts or category_counts['shoes'] < 2,
            'quality handbag': 'accessories' not in category_counts
        }
        
        return [item for item, missing in essential_items.items() if missing]
    
    @staticmethod
    def _identify_color_gaps(color_counts):
        """Identify color gaps in wardrobe"""
        essential_colors = ['black', 'white', 'navy']
        missing_colors = [color for color in essential_colors if color not in color_counts]
        
        # Suggest complementary colors based on existing palette
        if 'brown' in color_counts and 'cream' not in color_counts:
            missing_colors.append('cream')
        if 'navy' in color_counts and 'white' not in color_counts:
            missing_colors.append('white')
        
        return missing_colors
    
    @staticmethod
    def _identify_styling_opportunities(wardrobe_items):
        """Identify new styling opportunities"""
        opportunities = []
        
        # Look for items that could be styled differently
        categories = [item.get('category', '') for item in wardrobe_items]
        
        if 'blazer' in categories and 'jeans' in categories:
            opportunities.append('Try blazer with jeans for smart-casual look')
        
        if 'dress' in categories and 'cardigan' in categories:
            opportunities.append('Layer cardigan over dress for versatile styling')
        
        if len(set(item.get('primary_color', '') for item in wardrobe_items)) > 3:
            opportunities.append('Experiment with color blocking combinations')
        
        return opportunities
    
    @staticmethod
    def _generate_priority_purchases(missing_essentials, color_gaps):
        """Generate prioritized shopping recommendations"""
        priorities = []
        
        # High priority essentials
        high_priority_essentials = ['basic white shirt', 'well-fitted jeans', 'versatile blazer']
        for essential in missing_essentials:
            if essential in high_priority_essentials:
                priorities.append({
                    'item': essential,
                    'priority': 'high',
                    'reason': 'Essential wardrobe staple',
                    'estimated_cost': '$50-150'
                })
        
        # Medium priority items
        medium_priority_essentials = ['little black dress', 'comfortable flats']
        for essential in missing_essentials:
            if essential in medium_priority_essentials:
                priorities.append({
                    'item': essential,
                    'priority': 'medium',
                    'reason': 'Versatile addition',
                    'estimated_cost': '$75-200'
                })
        
        # Color gap items
        for color in color_gaps[:2]:  # Top 2 color gaps
            priorities.append({
                'item': f'{color} basic top',
                'priority': 'medium',
                'reason': f'Fill {color} color gap',
                'estimated_cost': '$30-80'
            })
        
        return priorities
    
    @staticmethod
    def analyze_style_compatibility(item1_data, item2_data):
        """
        Analyze compatibility between two style items
        "We girls have no time" - Perfect style matching every time!
        """
        # Extract item characteristics
        item1_color = item1_data.get('primary_color', '').lower()
        item2_color = item2_data.get('primary_color', '').lower()
        item1_category = item1_data.get('category', '').lower()
        item2_category = item2_data.get('category', '').lower()
        
        # Calculate compatibility scores
        color_compatibility = AdvancedAIEngine._calculate_color_compatibility(item1_color, item2_color)
        style_compatibility = AdvancedAIEngine._calculate_style_compatibility(item1_category, item2_category)
        formality_compatibility = AdvancedAIEngine._calculate_formality_compatibility(item1_data, item2_data)
        
        # Overall compatibility
        overall_compatibility = (color_compatibility + style_compatibility + formality_compatibility) / 3
        
        # Generate compatibility reasons
        compatibility_reasons = []
        incompatibility_reasons = []
        styling_suggestions = []
        
        if color_compatibility > 0.7:
            compatibility_reasons.append('Colors work harmoniously together')
        elif color_compatibility < 0.4:
            incompatibility_reasons.append('Color combination may clash')
            styling_suggestions.append('Consider adding a neutral piece to bridge colors')
        
        if style_compatibility > 0.7:
            compatibility_reasons.append('Styles complement each other well')
        elif style_compatibility < 0.4:
            incompatibility_reasons.append('Style mismatch - different aesthetic directions')
        
        # Determine suitable occasions
        suitable_occasions = []
        if overall_compatibility > 0.7:
            if formality_compatibility > 0.7:
                suitable_occasions.extend(['work', 'formal events'])
            else:
                suitable_occasions.extend(['casual', 'weekend'])
        
        # Create compatibility record
        item1_id = item1_data.get('id', 'item1')
        item2_id = item2_data.get('id', 'item2')
        
        compatibility = StyleCompatibility(
            item1_id=str(item1_id),
            item2_id=str(item2_id),
            overall_compatibility=overall_compatibility,
            color_compatibility=color_compatibility,
            style_compatibility=style_compatibility,
            formality_compatibility=formality_compatibility,
            compatibility_reasons=json.dumps(compatibility_reasons),
            incompatibility_reasons=json.dumps(incompatibility_reasons),
            styling_suggestions=json.dumps(styling_suggestions),
            suitable_occasions=json.dumps(suitable_occasions),
            styling_difficulty='easy' if overall_compatibility > 0.7 else 'medium' if overall_compatibility > 0.4 else 'advanced'
        )
        
        db.session.add(compatibility)
        db.session.commit()
        
        return compatibility.to_dict()
    
    @staticmethod
    def _calculate_color_compatibility(color1, color2):
        """Calculate color compatibility score"""
        # Color harmony rules
        harmonious_pairs = {
            ('black', 'white'): 1.0,
            ('navy', 'white'): 0.9,
            ('gray', 'white'): 0.9,
            ('black', 'gray'): 0.8,
            ('navy', 'cream'): 0.8,
            ('brown', 'cream'): 0.8,
            ('blue', 'white'): 0.9,
            ('red', 'black'): 0.7,
            ('green', 'brown'): 0.7
        }
        
        # Check direct pairs
        pair = tuple(sorted([color1, color2]))
        if pair in harmonious_pairs:
            return harmonious_pairs[pair]
        
        # Check reverse pairs
        reverse_pair = (color2, color1)
        if reverse_pair in harmonious_pairs:
            return harmonious_pairs[reverse_pair]
        
        # Neutral colors work with most things
        neutrals = ['black', 'white', 'gray', 'beige', 'cream', 'navy']
        if color1 in neutrals or color2 in neutrals:
            return 0.7
        
        # Same color family
        if color1 == color2:
            return 0.6  # Monochromatic can work but may lack interest
        
        # Default compatibility
        return 0.5
    
    @staticmethod
    def _calculate_style_compatibility(category1, category2):
        """Calculate style compatibility score"""
        # Style compatibility rules
        compatible_combinations = {
            ('blazer', 'jeans'): 0.9,
            ('blazer', 'dress pants'): 1.0,
            ('cardigan', 'dress'): 0.8,
            ('t-shirt', 'jeans'): 0.9,
            ('blouse', 'skirt'): 0.9,
            ('sweater', 'jeans'): 0.8,
            ('dress', 'jacket'): 0.8
        }
        
        pair = tuple(sorted([category1, category2]))
        if pair in compatible_combinations:
            return compatible_combinations[pair]
        
        # Default compatibility based on formality levels
        formal_items = ['blazer', 'dress pants', 'blouse', 'dress shirt']
        casual_items = ['jeans', 't-shirt', 'sneakers', 'hoodie']
        
        if (category1 in formal_items and category2 in formal_items) or \
           (category1 in casual_items and category2 in casual_items):
            return 0.7
        
        return 0.5
    
    @staticmethod
    def _calculate_formality_compatibility(item1_data, item2_data):
        """Calculate formality level compatibility"""
        # Assign formality scores
        formality_scores = {
            'suit': 1.0, 'blazer': 0.8, 'dress pants': 0.8, 'blouse': 0.7,
            'dress': 0.6, 'cardigan': 0.5, 'jeans': 0.3, 't-shirt': 0.2,
            'sneakers': 0.2, 'hoodie': 0.1
        }
        
        item1_formality = formality_scores.get(item1_data.get('category', '').lower(), 0.5)
        item2_formality = formality_scores.get(item2_data.get('category', '').lower(), 0.5)
        
        # Calculate compatibility based on formality difference
        formality_diff = abs(item1_formality - item2_formality)
        return max(0.0, 1.0 - formality_diff)
    
    @staticmethod
    def generate_predictive_recommendations(user_id, context=None):
        """
        Generate predictive recommendations based on trends, behavior, and context
        "We girls have no time" - AI that predicts what you'll love!
        """
        # Get user's style profile for personalization
        style_profile = UserStyleProfile.query.filter_by(user_id=user_id).first()
        
        # Get current trends
        current_trends = TrendForecast.get_current_trends(5)
        emerging_trends = TrendForecast.get_emerging_trends(3)
        
        # Generate predictions
        predictions = []
        
        # Trend-based predictions
        for trend in current_trends[:2]:
            if style_profile:
                # Check if trend matches user's style
                trend_data = trend.to_dict()
                style_compatibility = trend_data.get('style_compatibility', {})
                user_primary_style = style_profile.primary_style
                
                if user_primary_style and user_primary_style in style_compatibility:
                    compatibility_score = style_compatibility[user_primary_style]
                    if compatibility_score > 0.6:
                        prediction = PredictiveRecommendation(
                            user_id=user_id,
                            recommendation_type='trend',
                            prediction_confidence=compatibility_score * trend.confidence_score,
                            prediction_reasoning=json.dumps([
                                f"Trending {trend.trend_name} matches your {user_primary_style} style",
                                f"High compatibility score: {compatibility_score:.1f}",
                                f"Trend confidence: {trend.confidence_score:.1f}"
                            ]),
                            trend_influence=0.8,
                            personal_style_influence=0.6,
                            status='active',
                            expires_date=datetime.utcnow() + timedelta(days=30)
                        )
                        db.session.add(prediction)
                        predictions.append(prediction)
        
        # Seasonal predictions
        current_season = AdvancedAIEngine._get_current_season()
        seasonal_prediction = PredictiveRecommendation(
            user_id=user_id,
            recommendation_type='seasonal',
            prediction_confidence=0.75,
            prediction_reasoning=json.dumps([
                f"Seasonal transition to {current_season}",
                "Update wardrobe for weather changes",
                "Add seasonal colors and textures"
            ]),
            seasonal_influence=0.9,
            personal_style_influence=0.4,
            predicted_context=json.dumps({'season': current_season}),
            status='active',
            expires_date=datetime.utcnow() + timedelta(days=60)
        )
        db.session.add(seasonal_prediction)
        predictions.append(seasonal_prediction)
        
        db.session.commit()
        
        return [pred.to_dict() for pred in predictions]
    
    @staticmethod
    def _get_current_season():
        """Determine current season"""
        month = datetime.now().month
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'fall'

