from datetime import datetime, date, timedelta
import json
import math
from collections import defaultdict, Counter
from src.models.user import db
from src.models.ai_models import StyleAnalysis, OutfitRecommendation
from src.models.enhanced_recommendations import OutfitFeedback

class UserStyleProfile(db.Model):
    """
    Advanced user style profile with learning and evolution
    "We girls have no time" - Personalized style that evolves with you!
    """
    __tablename__ = 'user_style_profile'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)
    
    # Core style personality (evolved from feedback)
    primary_style = db.Column(db.String(30), nullable=True)  # Main style personality
    secondary_style = db.Column(db.String(30), nullable=True)  # Secondary style influence
    style_confidence = db.Column(db.Float, default=0.5)  # How confident we are in style detection
    
    # Style evolution tracking
    style_evolution = db.Column(db.Text, nullable=True)  # JSON: historical style changes
    style_flexibility = db.Column(db.Float, default=0.5)  # How much user varies style (0-1)
    
    # Personalized preferences (learned from feedback)
    preferred_colors = db.Column(db.Text, nullable=True)  # JSON: color preferences with weights
    avoided_colors = db.Column(db.Text, nullable=True)  # JSON: colors user dislikes
    preferred_categories = db.Column(db.Text, nullable=True)  # JSON: clothing categories with weights
    avoided_categories = db.Column(db.Text, nullable=True)  # JSON: categories user avoids
    
    # Fit and comfort preferences
    fit_preferences = db.Column(db.Text, nullable=True)  # JSON: loose, fitted, etc.
    comfort_priorities = db.Column(db.Text, nullable=True)  # JSON: comfort factors
    fabric_preferences = db.Column(db.Text, nullable=True)  # JSON: fabric likes/dislikes
    
    # Occasion-specific preferences
    work_style_preferences = db.Column(db.Text, nullable=True)  # JSON: work outfit preferences
    casual_style_preferences = db.Column(db.Text, nullable=True)  # JSON: casual preferences
    formal_style_preferences = db.Column(db.Text, nullable=True)  # JSON: formal preferences
    
    # Lifestyle and context
    lifestyle_factors = db.Column(db.Text, nullable=True)  # JSON: active, professional, etc.
    climate_preferences = db.Column(db.Text, nullable=True)  # JSON: weather/season preferences
    budget_consciousness = db.Column(db.Float, default=0.5)  # How budget-conscious (0-1)
    
    # Learning metadata
    learning_data_points = db.Column(db.Integer, default=0)  # Number of feedback points used
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    confidence_score = db.Column(db.Float, default=0.1)  # Overall confidence in profile
    
    # Personalization flags
    auto_learn_enabled = db.Column(db.Boolean, default=True)
    style_exploration_mode = db.Column(db.Boolean, default=False)  # User wants to try new styles
    
    def __repr__(self):
        return f'<UserStyleProfile {self.user_id}:{self.primary_style}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'primary_style': self.primary_style,
            'secondary_style': self.secondary_style,
            'style_confidence': self.style_confidence,
            'style_evolution': json.loads(self.style_evolution) if self.style_evolution else [],
            'style_flexibility': self.style_flexibility,
            'preferred_colors': json.loads(self.preferred_colors) if self.preferred_colors else {},
            'avoided_colors': json.loads(self.avoided_colors) if self.avoided_colors else {},
            'preferred_categories': json.loads(self.preferred_categories) if self.preferred_categories else {},
            'avoided_categories': json.loads(self.avoided_categories) if self.avoided_categories else {},
            'fit_preferences': json.loads(self.fit_preferences) if self.fit_preferences else {},
            'comfort_priorities': json.loads(self.comfort_priorities) if self.comfort_priorities else {},
            'fabric_preferences': json.loads(self.fabric_preferences) if self.fabric_preferences else {},
            'work_style_preferences': json.loads(self.work_style_preferences) if self.work_style_preferences else {},
            'casual_style_preferences': json.loads(self.casual_style_preferences) if self.casual_style_preferences else {},
            'formal_style_preferences': json.loads(self.formal_style_preferences) if self.formal_style_preferences else {},
            'lifestyle_factors': json.loads(self.lifestyle_factors) if self.lifestyle_factors else {},
            'climate_preferences': json.loads(self.climate_preferences) if self.climate_preferences else {},
            'budget_consciousness': self.budget_consciousness,
            'learning_data_points': self.learning_data_points,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'confidence_score': self.confidence_score,
            'auto_learn_enabled': self.auto_learn_enabled,
            'style_exploration_mode': self.style_exploration_mode
        }
    
    @staticmethod
    def get_or_create_profile(user_id):
        """Get existing profile or create new one"""
        profile = UserStyleProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            profile = UserStyleProfile(user_id=user_id)
            db.session.add(profile)
            db.session.commit()
        return profile
    
    def update_from_feedback(self, feedback_data):
        """Update profile based on user feedback"""
        if not self.auto_learn_enabled:
            return
        
        # Update learning metadata
        self.learning_data_points += 1
        self.last_updated = datetime.utcnow()
        
        # Update confidence based on feedback consistency
        if feedback_data.get('rating', 0) >= 4:
            self.confidence_score = min(self.confidence_score + 0.02, 1.0)
        elif feedback_data.get('rating', 0) <= 2:
            self.confidence_score = max(self.confidence_score - 0.01, 0.0)
        
        # Update color preferences
        self._update_color_preferences(feedback_data)
        
        # Update category preferences
        self._update_category_preferences(feedback_data)
        
        # Update fit and comfort preferences
        self._update_comfort_preferences(feedback_data)
        
        # Update occasion-specific preferences
        self._update_occasion_preferences(feedback_data)
        
        db.session.commit()
    
    def _update_color_preferences(self, feedback_data):
        """Update color preferences based on feedback"""
        preferred_colors = json.loads(self.preferred_colors) if self.preferred_colors else {}
        avoided_colors = json.loads(self.avoided_colors) if self.avoided_colors else {}
        
        rating = feedback_data.get('rating', 3)
        liked_aspects = feedback_data.get('liked_aspects', [])
        disliked_aspects = feedback_data.get('disliked_aspects', [])
        
        # If user liked colors
        if 'colors' in liked_aspects and rating >= 4:
            # This would need actual color data from the outfit
            # For now, we'll use a placeholder approach
            outfit_colors = feedback_data.get('outfit_colors', [])
            for color in outfit_colors:
                preferred_colors[color] = preferred_colors.get(color, 0) + 0.1
        
        # If user disliked colors
        if 'colors' in disliked_aspects or rating <= 2:
            outfit_colors = feedback_data.get('outfit_colors', [])
            for color in outfit_colors:
                avoided_colors[color] = avoided_colors.get(color, 0) + 0.1
        
        self.preferred_colors = json.dumps(preferred_colors)
        self.avoided_colors = json.dumps(avoided_colors)
    
    def _update_category_preferences(self, feedback_data):
        """Update category preferences based on feedback"""
        preferred_categories = json.loads(self.preferred_categories) if self.preferred_categories else {}
        avoided_categories = json.loads(self.avoided_categories) if self.avoided_categories else {}
        
        rating = feedback_data.get('rating', 3)
        outfit_categories = feedback_data.get('outfit_categories', [])
        
        for category in outfit_categories:
            if rating >= 4:
                preferred_categories[category] = preferred_categories.get(category, 0) + 0.1
            elif rating <= 2:
                avoided_categories[category] = avoided_categories.get(category, 0) + 0.1
        
        self.preferred_categories = json.dumps(preferred_categories)
        self.avoided_categories = json.dumps(avoided_categories)
    
    def _update_comfort_preferences(self, feedback_data):
        """Update comfort preferences based on feedback"""
        comfort_priorities = json.loads(self.comfort_priorities) if self.comfort_priorities else {}
        
        comfort_rating = feedback_data.get('comfort_rating')
        if comfort_rating:
            if comfort_rating >= 4:
                comfort_priorities['high_comfort_preference'] = comfort_priorities.get('high_comfort_preference', 0) + 0.1
            elif comfort_rating <= 2:
                comfort_priorities['comfort_issues'] = comfort_priorities.get('comfort_issues', 0) + 0.1
        
        self.comfort_priorities = json.dumps(comfort_priorities)
    
    def _update_occasion_preferences(self, feedback_data):
        """Update occasion-specific preferences"""
        occasion = feedback_data.get('occasion_actual') or feedback_data.get('occasion')
        rating = feedback_data.get('rating', 3)
        
        if not occasion:
            return
        
        occasion_field = f"{occasion}_style_preferences"
        if hasattr(self, occasion_field):
            current_prefs = getattr(self, occasion_field)
            prefs_dict = json.loads(current_prefs) if current_prefs else {}
            
            if rating >= 4:
                prefs_dict['successful_combinations'] = prefs_dict.get('successful_combinations', 0) + 1
            elif rating <= 2:
                prefs_dict['unsuccessful_combinations'] = prefs_dict.get('unsuccessful_combinations', 0) + 1
            
            setattr(self, occasion_field, json.dumps(prefs_dict))


class StyleLearningEngine:
    """
    Advanced style learning engine with personalization
    "We girls have no time" - AI that learns your style perfectly!
    """
    
    @staticmethod
    def analyze_user_style_evolution(user_id, days_back=90):
        """
        Analyze how user's style has evolved over time
        "We girls have no time" - Track your style journey!
        """
        # Get feedback data from the specified period
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        feedback_records = OutfitFeedback.query.filter(
            OutfitFeedback.user_id == user_id,
            OutfitFeedback.feedback_date >= cutoff_date
        ).order_by(OutfitFeedback.feedback_date.asc()).all()
        
        if len(feedback_records) < 5:
            return {
                'status': 'insufficient_data',
                'message': 'Need more feedback data to analyze style evolution',
                'data_points': len(feedback_records),
                'minimum_required': 5
            }
        
        # Analyze evolution patterns
        evolution_data = {
            'timeline': [],
            'style_consistency': 0.0,
            'preference_stability': 0.0,
            'exploration_tendency': 0.0,
            'improvement_trend': 0.0,
            'key_insights': []
        }
        
        # Group feedback by time periods (weekly)
        weekly_data = defaultdict(list)
        for feedback in feedback_records:
            week_key = feedback.feedback_date.strftime('%Y-W%U')
            weekly_data[week_key].append(feedback)
        
        # Analyze each week
        weekly_ratings = []
        weekly_consistency = []
        
        for week, week_feedback in weekly_data.items():
            avg_rating = sum(f.rating for f in week_feedback) / len(week_feedback)
            weekly_ratings.append(avg_rating)
            
            # Calculate consistency (how similar the ratings are)
            rating_variance = sum((f.rating - avg_rating) ** 2 for f in week_feedback) / len(week_feedback)
            consistency = 1.0 - min(rating_variance / 4.0, 1.0)  # Normalize to 0-1
            weekly_consistency.append(consistency)
            
            evolution_data['timeline'].append({
                'week': week,
                'average_rating': round(avg_rating, 2),
                'consistency': round(consistency, 2),
                'feedback_count': len(week_feedback)
            })
        
        # Calculate overall metrics
        if len(weekly_ratings) > 1:
            # Style consistency (how consistent ratings are over time)
            evolution_data['style_consistency'] = sum(weekly_consistency) / len(weekly_consistency)
            
            # Improvement trend (are ratings getting better?)
            if len(weekly_ratings) >= 3:
                recent_avg = sum(weekly_ratings[-3:]) / 3
                early_avg = sum(weekly_ratings[:3]) / 3
                evolution_data['improvement_trend'] = (recent_avg - early_avg) / 5.0  # Normalize
            
            # Exploration tendency (how much variety in feedback types)
            feedback_types = [f.feedback_type for f in feedback_records]
            type_variety = len(set(feedback_types)) / len(feedback_types) if feedback_types else 0
            evolution_data['exploration_tendency'] = type_variety
        
        # Generate insights
        insights = []
        if evolution_data['improvement_trend'] > 0.1:
            insights.append("Your style satisfaction is improving over time!")
        elif evolution_data['improvement_trend'] < -0.1:
            insights.append("Consider exploring new style directions.")
        
        if evolution_data['style_consistency'] > 0.7:
            insights.append("You have a consistent style preference.")
        elif evolution_data['style_consistency'] < 0.4:
            insights.append("You enjoy experimenting with different styles.")
        
        if evolution_data['exploration_tendency'] > 0.6:
            insights.append("You're adventurous with trying new outfit combinations.")
        
        evolution_data['key_insights'] = insights
        
        return evolution_data
    
    @staticmethod
    def generate_personalized_recommendations(user_id, wardrobe_items, occasion, context=None):
        """
        Generate highly personalized recommendations based on learning
        "We girls have no time" - Perfectly personalized outfits!
        """
        # Get user's style profile
        profile = UserStyleProfile.get_or_create_profile(user_id)
        profile_data = profile.to_dict()
        
        if profile_data['confidence_score'] < 0.2:
            return {
                'status': 'learning_mode',
                'message': 'Still learning your style preferences',
                'recommendation': 'Basic recommendation with learning focus',
                'learning_priority': True
            }
        
        # Get user's feedback patterns
        feedback_patterns = OutfitFeedback.get_user_feedback_patterns(user_id)
        
        # Filter wardrobe based on learned preferences
        filtered_items = StyleLearningEngine._filter_items_by_preferences(
            wardrobe_items, profile_data, occasion
        )
        
        if not filtered_items:
            filtered_items = wardrobe_items  # Fallback to all items
        
        # Generate base recommendation
        from src.models.enhanced_recommendations import SmartRecommendationEngine
        base_recommendation = SmartRecommendationEngine.generate_enhanced_outfit(
            user_id, filtered_items, {}, occasion, 
            context.get('weather') if context else None,
            context.get('temperature') if context else None,
            context.get('season') if context else None,
            feedback_patterns
        )
        
        if not base_recommendation:
            return None
        
        # Apply personalization enhancements
        personalized_rec = StyleLearningEngine._apply_personalization(
            base_recommendation, profile_data, filtered_items, occasion
        )
        
        # Add personalization metadata
        personalized_rec['personalization'] = {
            'confidence_score': profile_data['confidence_score'],
            'learning_data_points': profile_data['learning_data_points'],
            'style_match_confidence': min(profile_data['style_confidence'] + 0.2, 1.0),
            'personalization_applied': True,
            'filtered_items_count': len(filtered_items),
            'total_items_count': len(wardrobe_items)
        }
        
        return personalized_rec
    
    @staticmethod
    def _filter_items_by_preferences(wardrobe_items, profile_data, occasion):
        """Filter wardrobe items based on learned preferences"""
        filtered_items = []
        
        preferred_colors = profile_data.get('preferred_colors', {})
        avoided_colors = profile_data.get('avoided_colors', {})
        preferred_categories = profile_data.get('preferred_categories', {})
        avoided_categories = profile_data.get('avoided_categories', {})
        
        for item in wardrobe_items:
            item_score = 1.0
            
            # Color preferences
            item_color = item.get('primary_color', '').lower()
            if item_color in preferred_colors:
                item_score += preferred_colors[item_color]
            if item_color in avoided_colors:
                item_score -= avoided_colors[item_color]
            
            # Category preferences
            item_category = item.get('category', '').lower()
            if item_category in preferred_categories:
                item_score += preferred_categories[item_category]
            if item_category in avoided_categories:
                item_score -= avoided_categories[item_category]
            
            # Only include items with positive score
            if item_score > 0.5:
                filtered_items.append(item)
        
        return filtered_items
    
    @staticmethod
    def _apply_personalization(recommendation, profile_data, wardrobe_items, occasion):
        """Apply personalization enhancements to recommendation"""
        # Boost score based on style confidence
        style_confidence = profile_data.get('style_confidence', 0.5)
        confidence_boost = style_confidence * 0.1
        recommendation['overall_score'] = min(recommendation['overall_score'] + confidence_boost, 1.0)
        
        # Add personalized styling tips
        styling_tips = []
        
        if profile_data.get('style_exploration_mode'):
            styling_tips.append("Try something new today - you're in exploration mode!")
        
        primary_style = profile_data.get('primary_style')
        if primary_style:
            styling_tips.append(f"This outfit matches your {primary_style} style perfectly.")
        
        if profile_data.get('comfort_priorities', {}).get('high_comfort_preference', 0) > 0.3:
            styling_tips.append("Comfort-focused styling based on your preferences.")
        
        recommendation['personalized_tips'] = styling_tips
        
        # Add confidence indicators
        recommendation['confidence_indicators'] = {
            'style_match': 'high' if style_confidence > 0.7 else 'medium' if style_confidence > 0.4 else 'learning',
            'color_harmony': 'personalized' if profile_data.get('preferred_colors') else 'general',
            'fit_preference': 'customized' if profile_data.get('fit_preferences') else 'standard'
        }
        
        return recommendation
    
    @staticmethod
    def update_style_profile_from_feedback(user_id, feedback_data):
        """Update user's style profile based on new feedback"""
        profile = UserStyleProfile.get_or_create_profile(user_id)
        profile.update_from_feedback(feedback_data)
        
        # Analyze if style evolution is happening
        evolution_data = StyleLearningEngine.analyze_user_style_evolution(user_id, days_back=30)
        
        if evolution_data.get('status') != 'insufficient_data':
            # Update style evolution tracking
            current_evolution = json.loads(profile.style_evolution) if profile.style_evolution else []
            
            new_evolution_point = {
                'date': datetime.utcnow().isoformat(),
                'confidence_score': profile.confidence_score,
                'improvement_trend': evolution_data.get('improvement_trend', 0),
                'style_consistency': evolution_data.get('style_consistency', 0)
            }
            
            current_evolution.append(new_evolution_point)
            
            # Keep only last 10 evolution points
            if len(current_evolution) > 10:
                current_evolution = current_evolution[-10:]
            
            profile.style_evolution = json.dumps(current_evolution)
            
            # Update style flexibility based on consistency
            consistency = evolution_data.get('style_consistency', 0.5)
            profile.style_flexibility = 1.0 - consistency  # More consistent = less flexible
            
            db.session.commit()
        
        return profile.to_dict()


class PersonalizationInsights:
    """
    Generate insights about user's style personalization
    "We girls have no time" - Understand your style instantly!
    """
    
    @staticmethod
    def generate_style_insights(user_id):
        """Generate comprehensive style insights for user"""
        profile = UserStyleProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            return {
                'status': 'no_profile',
                'message': 'No style profile found. Start rating outfits to build your profile!',
                'tagline': 'We girls have no time - But we need your feedback first!'
            }
        
        profile_data = profile.to_dict()
        
        # Get evolution data
        evolution_data = StyleLearningEngine.analyze_user_style_evolution(user_id)
        
        # Generate insights
        insights = {
            'style_personality': PersonalizationInsights._analyze_style_personality(profile_data),
            'color_preferences': PersonalizationInsights._analyze_color_preferences(profile_data),
            'wardrobe_patterns': PersonalizationInsights._analyze_wardrobe_patterns(profile_data),
            'style_evolution': evolution_data,
            'personalization_status': PersonalizationInsights._analyze_personalization_status(profile_data),
            'recommendations': PersonalizationInsights._generate_style_recommendations(profile_data)
        }
        
        return insights
    
    @staticmethod
    def _analyze_style_personality(profile_data):
        """Analyze user's style personality"""
        primary_style = profile_data.get('primary_style')
        secondary_style = profile_data.get('secondary_style')
        style_confidence = profile_data.get('style_confidence', 0)
        style_flexibility = profile_data.get('style_flexibility', 0.5)
        
        personality_analysis = {
            'primary_style': primary_style,
            'secondary_style': secondary_style,
            'confidence_level': 'high' if style_confidence > 0.7 else 'medium' if style_confidence > 0.4 else 'developing',
            'style_type': 'consistent' if style_flexibility < 0.3 else 'flexible' if style_flexibility < 0.7 else 'experimental'
        }
        
        # Generate description
        if primary_style:
            if style_flexibility < 0.3:
                personality_analysis['description'] = f"You have a strong, consistent {primary_style} style."
            elif style_flexibility < 0.7:
                personality_analysis['description'] = f"You primarily lean {primary_style} but enjoy some variety."
            else:
                personality_analysis['description'] = f"You love experimenting with {primary_style} and other styles."
        else:
            personality_analysis['description'] = "Your style personality is still developing."
        
        return personality_analysis
    
    @staticmethod
    def _analyze_color_preferences(profile_data):
        """Analyze user's color preferences"""
        preferred_colors = profile_data.get('preferred_colors', {})
        avoided_colors = profile_data.get('avoided_colors', {})
        
        color_analysis = {
            'top_preferred_colors': sorted(preferred_colors.items(), key=lambda x: x[1], reverse=True)[:5],
            'avoided_colors': list(avoided_colors.keys()),
            'color_adventurousness': 'high' if len(preferred_colors) > 8 else 'medium' if len(preferred_colors) > 4 else 'conservative',
            'color_confidence': 'established' if preferred_colors else 'developing'
        }
        
        return color_analysis
    
    @staticmethod
    def _analyze_wardrobe_patterns(profile_data):
        """Analyze wardrobe usage patterns"""
        preferred_categories = profile_data.get('preferred_categories', {})
        comfort_priorities = profile_data.get('comfort_priorities', {})
        
        patterns = {
            'favorite_categories': sorted(preferred_categories.items(), key=lambda x: x[1], reverse=True)[:3],
            'comfort_focus': comfort_priorities.get('high_comfort_preference', 0) > 0.3,
            'style_priorities': []
        }
        
        # Determine style priorities
        if comfort_priorities.get('high_comfort_preference', 0) > 0.3:
            patterns['style_priorities'].append('comfort')
        
        if len(preferred_categories) > 5:
            patterns['style_priorities'].append('variety')
        
        return patterns
    
    @staticmethod
    def _analyze_personalization_status(profile_data):
        """Analyze how well personalized the system is"""
        confidence_score = profile_data.get('confidence_score', 0)
        learning_data_points = profile_data.get('learning_data_points', 0)
        
        status = {
            'personalization_level': 'high' if confidence_score > 0.7 else 'medium' if confidence_score > 0.4 else 'developing',
            'data_richness': 'rich' if learning_data_points > 20 else 'moderate' if learning_data_points > 10 else 'building',
            'recommendation_accuracy': f"{min(confidence_score * 100, 95):.0f}%",
            'learning_progress': f"{min(learning_data_points / 30 * 100, 100):.0f}%"
        }
        
        return status
    
    @staticmethod
    def _generate_style_recommendations(profile_data):
        """Generate personalized style recommendations"""
        recommendations = []
        
        confidence_score = profile_data.get('confidence_score', 0)
        style_flexibility = profile_data.get('style_flexibility', 0.5)
        exploration_mode = profile_data.get('style_exploration_mode', False)
        
        if confidence_score < 0.3:
            recommendations.append("Keep rating outfits to help us learn your style better!")
        
        if style_flexibility > 0.7:
            recommendations.append("You love variety! Try our style exploration features.")
        elif style_flexibility < 0.3:
            recommendations.append("You have a signature style! We'll focus on perfecting it.")
        
        if exploration_mode:
            recommendations.append("Exploration mode is on - we'll suggest some adventurous options!")
        
        if not profile_data.get('preferred_colors'):
            recommendations.append("Try rating some colorful outfits to build your color profile.")
        
        return recommendations

