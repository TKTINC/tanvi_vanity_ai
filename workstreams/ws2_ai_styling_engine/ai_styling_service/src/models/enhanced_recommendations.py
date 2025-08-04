from datetime import datetime, date, timedelta
import json
import random
from src.models.user import db
from src.models.ai_models import StyleAnalysis, OutfitRecommendation

class WeatherOutfitRule(db.Model):
    """
    Weather-based outfit recommendation rules
    "We girls have no time" - Smart weather-appropriate styling!
    """
    __tablename__ = 'weather_outfit_rule'
    
    id = db.Column(db.Integer, primary_key=True)
    weather_condition = db.Column(db.String(30), nullable=False)  # e.g., 'sunny', 'rainy', 'cold', 'hot'
    temperature_range = db.Column(db.String(20), nullable=True)  # e.g., '60-75F', 'below_50F'
    
    # Recommended categories
    required_categories = db.Column(db.Text, nullable=True)  # JSON array
    optional_categories = db.Column(db.Text, nullable=True)  # JSON array
    avoid_categories = db.Column(db.Text, nullable=True)  # JSON array
    
    # Fabric and material preferences
    preferred_fabrics = db.Column(db.Text, nullable=True)  # JSON array
    avoid_fabrics = db.Column(db.Text, nullable=True)  # JSON array
    
    # Color preferences for weather
    preferred_colors = db.Column(db.Text, nullable=True)  # JSON array
    avoid_colors = db.Column(db.Text, nullable=True)  # JSON array
    
    # Style adjustments
    layering_required = db.Column(db.Boolean, default=False)
    coverage_level = db.Column(db.String(20), nullable=True)  # 'minimal', 'moderate', 'full'
    
    # Rule metadata
    priority = db.Column(db.Integer, default=1)  # Higher number = higher priority
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<WeatherOutfitRule {self.weather_condition}:{self.temperature_range}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'weather_condition': self.weather_condition,
            'temperature_range': self.temperature_range,
            'required_categories': json.loads(self.required_categories) if self.required_categories else [],
            'optional_categories': json.loads(self.optional_categories) if self.optional_categories else [],
            'avoid_categories': json.loads(self.avoid_categories) if self.avoid_categories else [],
            'preferred_fabrics': json.loads(self.preferred_fabrics) if self.preferred_fabrics else [],
            'avoid_fabrics': json.loads(self.avoid_fabrics) if self.avoid_fabrics else [],
            'preferred_colors': json.loads(self.preferred_colors) if self.preferred_colors else [],
            'avoid_colors': json.loads(self.avoid_colors) if self.avoid_colors else [],
            'layering_required': self.layering_required,
            'coverage_level': self.coverage_level,
            'priority': self.priority,
            'active': self.active
        }
    
    @staticmethod
    def get_weather_rules(weather_condition, temperature=None):
        """Get applicable weather rules for given conditions"""
        rules = WeatherOutfitRule.query.filter_by(
            weather_condition=weather_condition,
            active=True
        ).order_by(WeatherOutfitRule.priority.desc()).all()
        
        # Filter by temperature if provided
        if temperature and rules:
            temp_filtered = []
            for rule in rules:
                if rule.temperature_range:
                    if WeatherOutfitRule.temperature_matches(temperature, rule.temperature_range):
                        temp_filtered.append(rule)
                else:
                    temp_filtered.append(rule)
            return temp_filtered
        
        return rules
    
    @staticmethod
    def temperature_matches(temp, temp_range):
        """Check if temperature matches the range"""
        try:
            if 'below_' in temp_range:
                threshold = int(temp_range.replace('below_', '').replace('F', ''))
                return temp < threshold
            elif 'above_' in temp_range:
                threshold = int(temp_range.replace('above_', '').replace('F', ''))
                return temp > threshold
            elif '-' in temp_range:
                min_temp, max_temp = temp_range.replace('F', '').split('-')
                return int(min_temp) <= temp <= int(max_temp)
        except:
            pass
        return True


class SeasonalRecommendation(db.Model):
    """
    Seasonal outfit recommendations and trends
    "We girls have no time" - Season-perfect styling instantly!
    """
    __tablename__ = 'seasonal_recommendation'
    
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.String(20), nullable=False)  # 'spring', 'summer', 'autumn', 'winter'
    month = db.Column(db.Integer, nullable=True)  # 1-12 for specific month recommendations
    
    # Seasonal style trends
    trending_styles = db.Column(db.Text, nullable=True)  # JSON array
    trending_colors = db.Column(db.Text, nullable=True)  # JSON array
    trending_patterns = db.Column(db.Text, nullable=True)  # JSON array
    
    # Seasonal wardrobe essentials
    essential_items = db.Column(db.Text, nullable=True)  # JSON array
    transition_items = db.Column(db.Text, nullable=True)  # JSON array for season transitions
    
    # Styling tips
    styling_tips = db.Column(db.Text, nullable=True)  # JSON array
    layering_advice = db.Column(db.Text, nullable=True)
    
    # Seasonal adjustments
    color_intensity = db.Column(db.String(20), nullable=True)  # 'bright', 'muted', 'neutral'
    fabric_weight = db.Column(db.String(20), nullable=True)  # 'light', 'medium', 'heavy'
    
    # Recommendation metadata
    year = db.Column(db.Integer, default=datetime.utcnow().year)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SeasonalRecommendation {self.season}:{self.year}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'season': self.season,
            'month': self.month,
            'trending_styles': json.loads(self.trending_styles) if self.trending_styles else [],
            'trending_colors': json.loads(self.trending_colors) if self.trending_colors else [],
            'trending_patterns': json.loads(self.trending_patterns) if self.trending_patterns else [],
            'essential_items': json.loads(self.essential_items) if self.essential_items else [],
            'transition_items': json.loads(self.transition_items) if self.transition_items else [],
            'styling_tips': json.loads(self.styling_tips) if self.styling_tips else [],
            'layering_advice': self.layering_advice,
            'color_intensity': self.color_intensity,
            'fabric_weight': self.fabric_weight,
            'year': self.year,
            'active': self.active
        }
    
    @staticmethod
    def get_current_season_recommendations():
        """Get recommendations for current season"""
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Determine season
        if current_month in [12, 1, 2]:
            season = 'winter'
        elif current_month in [3, 4, 5]:
            season = 'spring'
        elif current_month in [6, 7, 8]:
            season = 'summer'
        else:
            season = 'autumn'
        
        # Get seasonal recommendations
        recommendations = SeasonalRecommendation.query.filter_by(
            season=season,
            year=current_year,
            active=True
        ).first()
        
        if not recommendations:
            # Fallback to previous year or create default
            recommendations = SeasonalRecommendation.query.filter_by(
                season=season,
                active=True
            ).order_by(SeasonalRecommendation.year.desc()).first()
        
        return recommendations


class OutfitFeedback(db.Model):
    """
    User feedback on outfit recommendations for learning
    "We girls have no time" - Learn from every outfit choice!
    """
    __tablename__ = 'outfit_feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    recommendation_id = db.Column(db.Integer, db.ForeignKey('outfit_recommendation.id'), nullable=False)
    
    # User feedback
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    feedback_type = db.Column(db.String(30), nullable=False)  # 'worn', 'saved', 'dismissed', 'modified'
    
    # Specific feedback
    liked_aspects = db.Column(db.Text, nullable=True)  # JSON array: ['colors', 'style', 'comfort']
    disliked_aspects = db.Column(db.Text, nullable=True)  # JSON array
    suggested_changes = db.Column(db.Text, nullable=True)  # JSON array
    
    # Context when feedback was given
    occasion_actual = db.Column(db.String(50), nullable=True)  # What occasion it was actually worn for
    weather_actual = db.Column(db.String(30), nullable=True)  # Actual weather conditions
    comfort_rating = db.Column(db.Integer, nullable=True)  # 1-5 comfort rating
    
    # Feedback metadata
    feedback_date = db.Column(db.DateTime, default=datetime.utcnow)
    worn_date = db.Column(db.Date, nullable=True)  # When outfit was actually worn
    
    # Learning data
    style_match_feedback = db.Column(db.Float, nullable=True)  # User's perception of style match
    occasion_match_feedback = db.Column(db.Float, nullable=True)  # User's perception of occasion appropriateness
    
    def __repr__(self):
        return f'<OutfitFeedback {self.user_id}:{self.recommendation_id}:{self.rating}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recommendation_id': self.recommendation_id,
            'rating': self.rating,
            'feedback_type': self.feedback_type,
            'liked_aspects': json.loads(self.liked_aspects) if self.liked_aspects else [],
            'disliked_aspects': json.loads(self.disliked_aspects) if self.disliked_aspects else [],
            'suggested_changes': json.loads(self.suggested_changes) if self.suggested_changes else [],
            'occasion_actual': self.occasion_actual,
            'weather_actual': self.weather_actual,
            'comfort_rating': self.comfort_rating,
            'feedback_date': self.feedback_date.isoformat() if self.feedback_date else None,
            'worn_date': self.worn_date.isoformat() if self.worn_date else None,
            'style_match_feedback': self.style_match_feedback,
            'occasion_match_feedback': self.occasion_match_feedback
        }
    
    @staticmethod
    def get_user_feedback_patterns(user_id, limit=50):
        """Get user's feedback patterns for learning"""
        feedback_records = OutfitFeedback.query.filter_by(user_id=user_id)\
            .order_by(OutfitFeedback.feedback_date.desc())\
            .limit(limit).all()
        
        if not feedback_records:
            return {}
        
        # Analyze patterns
        patterns = {
            'average_rating': sum(f.rating for f in feedback_records) / len(feedback_records),
            'preferred_feedback_types': {},
            'liked_aspects_frequency': {},
            'disliked_aspects_frequency': {},
            'comfort_patterns': {},
            'occasion_preferences': {}
        }
        
        for feedback in feedback_records:
            # Feedback type patterns
            feedback_type = feedback.feedback_type
            patterns['preferred_feedback_types'][feedback_type] = \
                patterns['preferred_feedback_types'].get(feedback_type, 0) + 1
            
            # Liked aspects
            if feedback.liked_aspects:
                for aspect in json.loads(feedback.liked_aspects):
                    patterns['liked_aspects_frequency'][aspect] = \
                        patterns['liked_aspects_frequency'].get(aspect, 0) + 1
            
            # Disliked aspects
            if feedback.disliked_aspects:
                for aspect in json.loads(feedback.disliked_aspects):
                    patterns['disliked_aspects_frequency'][aspect] = \
                        patterns['disliked_aspects_frequency'].get(aspect, 0) + 1
            
            # Comfort patterns
            if feedback.comfort_rating:
                comfort_key = f"comfort_{feedback.comfort_rating}"
                patterns['comfort_patterns'][comfort_key] = \
                    patterns['comfort_patterns'].get(comfort_key, 0) + 1
            
            # Occasion preferences
            if feedback.occasion_actual:
                patterns['occasion_preferences'][feedback.occasion_actual] = \
                    patterns['occasion_preferences'].get(feedback.occasion_actual, 0) + 1
        
        return patterns


class SmartRecommendationEngine:
    """
    Enhanced recommendation engine with weather, season, and learning
    "We girls have no time" - Intelligent outfit suggestions that learn!
    """
    
    @staticmethod
    def generate_enhanced_outfit(user_id, wardrobe_items, style_analysis, occasion, 
                                weather=None, temperature=None, season=None, user_feedback_patterns=None):
        """
        Generate enhanced outfit recommendation with weather, season, and learning
        "We girls have no time" - Smart outfit creation with all factors considered!
        """
        if not wardrobe_items:
            return None
        
        # Get base recommendation
        base_outfit = OutfitRecommendation.generate_outfit_recommendation(
            user_id, wardrobe_items, style_analysis, occasion, weather, season
        )
        
        if not base_outfit:
            return None
        
        # Apply weather rules
        if weather:
            weather_rules = WeatherOutfitRule.get_weather_rules(weather, temperature)
            base_outfit = SmartRecommendationEngine.apply_weather_rules(
                base_outfit, wardrobe_items, weather_rules
            )
        
        # Apply seasonal recommendations
        if season or datetime.now():
            seasonal_rec = SeasonalRecommendation.get_current_season_recommendations()
            if seasonal_rec:
                base_outfit = SmartRecommendationEngine.apply_seasonal_trends(
                    base_outfit, wardrobe_items, seasonal_rec
                )
        
        # Apply user learning
        if user_feedback_patterns:
            base_outfit = SmartRecommendationEngine.apply_user_learning(
                base_outfit, wardrobe_items, user_feedback_patterns
            )
        
        # Enhance scoring with new factors
        base_outfit = SmartRecommendationEngine.enhance_scoring(
            base_outfit, weather, season, user_feedback_patterns
        )
        
        return base_outfit
    
    @staticmethod
    def apply_weather_rules(outfit_data, wardrobe_items, weather_rules):
        """Apply weather-specific rules to outfit"""
        if not weather_rules:
            return outfit_data
        
        # Get current outfit items
        current_item_ids = outfit_data['outfit_items']
        current_items = [item for item in wardrobe_items if item.get('id') in current_item_ids]
        
        # Apply rules from highest priority
        for rule in weather_rules:
            rule_data = rule.to_dict()
            
            # Check if layering is required
            if rule_data['layering_required']:
                # Add outerwear if not present
                has_outerwear = any(item.get('category', '').lower() in ['outerwear', 'jackets', 'coats'] 
                                  for item in current_items)
                if not has_outerwear:
                    outerwear_items = [item for item in wardrobe_items 
                                     if item.get('category', '').lower() in ['outerwear', 'jackets', 'coats']]
                    if outerwear_items:
                        best_outerwear = max(outerwear_items, 
                                           key=lambda x: x.get('favorite', False))
                        current_items.append(best_outerwear)
                        outfit_data['outfit_items'].append(best_outerwear.get('id'))
            
            # Avoid certain categories
            avoid_categories = rule_data.get('avoid_categories', [])
            if avoid_categories:
                filtered_items = []
                filtered_ids = []
                for item in current_items:
                    if item.get('category', '').lower() not in avoid_categories:
                        filtered_items.append(item)
                        filtered_ids.append(item.get('id'))
                current_items = filtered_items
                outfit_data['outfit_items'] = filtered_ids
            
            # Prefer certain colors
            preferred_colors = rule_data.get('preferred_colors', [])
            if preferred_colors:
                # Boost score for items with preferred colors
                for item in current_items:
                    if item.get('primary_color', '').lower() in preferred_colors:
                        outfit_data['color_harmony_score'] = min(outfit_data['color_harmony_score'] + 0.1, 1.0)
        
        return outfit_data
    
    @staticmethod
    def apply_seasonal_trends(outfit_data, wardrobe_items, seasonal_rec):
        """Apply seasonal trends to outfit"""
        if not seasonal_rec:
            return outfit_data
        
        seasonal_data = seasonal_rec.to_dict()
        
        # Boost score for trending colors
        trending_colors = seasonal_data.get('trending_colors', [])
        if trending_colors:
            current_item_ids = outfit_data['outfit_items']
            current_items = [item for item in wardrobe_items if item.get('id') in current_item_ids]
            
            for item in current_items:
                if item.get('primary_color', '').lower() in trending_colors:
                    outfit_data['style_match_score'] = min(outfit_data['style_match_score'] + 0.1, 1.0)
        
        # Add seasonal styling tip
        styling_tips = seasonal_data.get('styling_tips', [])
        if styling_tips:
            tip = random.choice(styling_tips)
            outfit_data['seasonal_tip'] = tip
        
        return outfit_data
    
    @staticmethod
    def apply_user_learning(outfit_data, wardrobe_items, feedback_patterns):
        """Apply user learning from feedback patterns"""
        if not feedback_patterns:
            return outfit_data
        
        # Boost score based on liked aspects
        liked_aspects = feedback_patterns.get('liked_aspects_frequency', {})
        current_item_ids = outfit_data['outfit_items']
        current_items = [item for item in wardrobe_items if item.get('id') in current_item_ids]
        
        # Check if outfit matches user's liked aspects
        if 'colors' in liked_aspects:
            # User likes color coordination
            outfit_data['color_harmony_score'] = min(outfit_data['color_harmony_score'] + 0.1, 1.0)
        
        if 'style' in liked_aspects:
            # User likes style matching
            outfit_data['style_match_score'] = min(outfit_data['style_match_score'] + 0.1, 1.0)
        
        if 'comfort' in liked_aspects:
            # Prefer comfortable items (favorites are usually comfortable)
            comfort_boost = sum(1 for item in current_items if item.get('favorite', False)) * 0.05
            outfit_data['overall_score'] = min(outfit_data['overall_score'] + comfort_boost, 1.0)
        
        # Avoid disliked aspects
        disliked_aspects = feedback_patterns.get('disliked_aspects_frequency', {})
        if 'tight_fit' in disliked_aspects:
            # Avoid items that might be tight (this would need item metadata)
            pass  # Would need more item details
        
        return outfit_data
    
    @staticmethod
    def enhance_scoring(outfit_data, weather, season, feedback_patterns):
        """Enhance overall scoring with new factors"""
        base_score = outfit_data['overall_score']
        
        # Weather appropriateness bonus
        weather_bonus = 0.0
        if weather:
            # Simple weather scoring (would be more sophisticated in production)
            weather_appropriate_items = {
                'sunny': ['light_colors', 'breathable_fabrics'],
                'rainy': ['waterproof', 'darker_colors'],
                'cold': ['warm_layers', 'outerwear'],
                'hot': ['light_fabrics', 'minimal_layers']
            }
            # This would need item metadata to properly implement
            weather_bonus = 0.05
        
        # Seasonal bonus
        seasonal_bonus = 0.0
        if season:
            seasonal_bonus = 0.05
        
        # User learning bonus
        learning_bonus = 0.0
        if feedback_patterns:
            avg_rating = feedback_patterns.get('average_rating', 3.0)
            if avg_rating > 3.5:
                learning_bonus = 0.1  # User generally likes recommendations
        
        # Calculate enhanced score
        enhanced_score = min(base_score + weather_bonus + seasonal_bonus + learning_bonus, 1.0)
        outfit_data['overall_score'] = enhanced_score
        
        # Add enhancement metadata
        outfit_data['enhancements'] = {
            'weather_considered': weather is not None,
            'seasonal_trends_applied': season is not None,
            'user_learning_applied': feedback_patterns is not None,
            'enhancement_score': weather_bonus + seasonal_bonus + learning_bonus
        }
        
        return outfit_data
    
    @staticmethod
    def get_alternative_recommendations(user_id, wardrobe_items, style_analysis, occasion, 
                                      primary_recommendation, count=3):
        """
        Generate alternative outfit recommendations
        "We girls have no time" - Multiple great options instantly!
        """
        alternatives = []
        
        # Generate variations by changing key pieces
        for i in range(count):
            # Create variation by shuffling items or changing key pieces
            variation = SmartRecommendationEngine.create_outfit_variation(
                wardrobe_items, style_analysis, occasion, primary_recommendation, i
            )
            
            if variation and variation['outfit_items'] != primary_recommendation['outfit_items']:
                alternatives.append(variation)
        
        # Sort by score
        alternatives.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return alternatives[:count]
    
    @staticmethod
    def create_outfit_variation(wardrobe_items, style_analysis, occasion, base_outfit, variation_index):
        """Create a variation of the base outfit"""
        # Simple variation strategy: replace one key item
        base_items = base_outfit['outfit_items']
        available_items = [item for item in wardrobe_items if item.get('id') not in base_items]
        
        if not available_items:
            return None
        
        # Replace a random item with an alternative
        if len(base_items) > 1:
            replace_index = variation_index % len(base_items)
            item_to_replace_id = base_items[replace_index]
            
            # Find the item to replace
            item_to_replace = next((item for item in wardrobe_items 
                                  if item.get('id') == item_to_replace_id), None)
            
            if item_to_replace:
                # Find alternative in same category
                same_category_items = [item for item in available_items 
                                     if item.get('category') == item_to_replace.get('category')]
                
                if same_category_items:
                    replacement = random.choice(same_category_items)
                    
                    # Create new outfit
                    new_items = base_items.copy()
                    new_items[replace_index] = replacement.get('id')
                    
                    # Calculate new scores (simplified)
                    variation = {
                        'outfit_items': new_items,
                        'outfit_description': f"Alternative {occasion} outfit with {replacement.get('name', 'item')}",
                        'style_match_score': max(base_outfit['style_match_score'] - 0.1, 0.5),
                        'occasion_match_score': base_outfit['occasion_match_score'],
                        'color_harmony_score': max(base_outfit['color_harmony_score'] - 0.05, 0.5),
                        'overall_score': max(base_outfit['overall_score'] - 0.08, 0.5)
                    }
                    
                    return variation
        
        return None

