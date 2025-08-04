from datetime import datetime, date
import json
from src.models.user import db

class StyleAnalysis(db.Model):
    """
    AI-powered style analysis results
    "We girls have no time" - Instant AI style analysis for busy lifestyles!
    """
    __tablename__ = 'style_analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Reference to WS1 user
    
    # Style personality analysis
    style_personality = db.Column(db.String(50), nullable=False)  # e.g., 'edgy', 'classic', 'bohemian'
    confidence_score = db.Column(db.Float, default=0.0)  # 0.0 to 1.0
    
    # Body type analysis
    body_type = db.Column(db.String(30), nullable=True)  # e.g., 'pear', 'apple', 'hourglass'
    body_confidence = db.Column(db.Float, default=0.0)
    
    # Color analysis
    color_season = db.Column(db.String(20), nullable=True)  # e.g., 'spring', 'summer', 'autumn', 'winter'
    primary_colors = db.Column(db.Text, nullable=True)  # JSON array of recommended colors
    avoid_colors = db.Column(db.Text, nullable=True)  # JSON array of colors to avoid
    
    # Style preferences analysis
    preferred_styles = db.Column(db.Text, nullable=True)  # JSON array of style categories
    lifestyle_match = db.Column(db.String(50), nullable=True)  # e.g., 'professional', 'casual', 'social'
    
    # AI analysis metadata
    analysis_version = db.Column(db.String(20), default='1.0')
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Analysis sources
    data_sources = db.Column(db.Text, nullable=True)  # JSON array of data sources used
    
    def __repr__(self):
        return f'<StyleAnalysis {self.user_id}:{self.style_personality}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'style_personality': self.style_personality,
            'confidence_score': round(self.confidence_score, 2),
            'body_type': self.body_type,
            'body_confidence': round(self.body_confidence, 2) if self.body_confidence else None,
            'color_season': self.color_season,
            'primary_colors': json.loads(self.primary_colors) if self.primary_colors else [],
            'avoid_colors': json.loads(self.avoid_colors) if self.avoid_colors else [],
            'preferred_styles': json.loads(self.preferred_styles) if self.preferred_styles else [],
            'lifestyle_match': self.lifestyle_match,
            'analysis_version': self.analysis_version,
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'data_sources': json.loads(self.data_sources) if self.data_sources else []
        }
    
    @staticmethod
    def analyze_style_personality(user_data, wardrobe_data, preferences):
        """
        AI-powered style personality analysis
        "We girls have no time" - Instant style personality detection!
        """
        # Style personality scoring algorithm
        style_scores = {
            'classic': 0.0,
            'edgy': 0.0,
            'bohemian': 0.0,
            'minimalist': 0.0,
            'romantic': 0.0,
            'trendy': 0.0
        }
        
        # Analyze wardrobe items
        if wardrobe_data:
            for item in wardrobe_data:
                category = item.get('category', '').lower()
                colors = [item.get('primary_color', '').lower()]
                brand = item.get('brand', '').lower()
                
                # Classic style indicators
                if category in ['blazers', 'trousers', 'button_downs'] or 'black' in colors or 'navy' in colors:
                    style_scores['classic'] += 0.2
                
                # Edgy style indicators
                if category in ['leather_jackets', 'boots', 'ripped_jeans'] or 'black' in colors:
                    style_scores['edgy'] += 0.3
                
                # Bohemian style indicators
                if category in ['maxi_dresses', 'kimonos', 'sandals'] or 'earth' in str(colors):
                    style_scores['bohemian'] += 0.25
                
                # Minimalist style indicators
                if colors and colors[0] in ['white', 'black', 'grey', 'beige']:
                    style_scores['minimalist'] += 0.2
                
                # Romantic style indicators
                if category in ['dresses', 'skirts', 'blouses'] or 'pink' in colors or 'floral' in str(item):
                    style_scores['romantic'] += 0.2
                
                # Trendy style indicators
                if brand in ['zara', 'h&m', 'forever21'] or category in ['crop_tops', 'high_waisted']:
                    style_scores['trendy'] += 0.25
        
        # Analyze user preferences
        if preferences:
            style_pref = preferences.get('style_preference', '').lower()
            if style_pref in style_scores:
                style_scores[style_pref] += 0.4
            
            lifestyle = preferences.get('lifestyle', '').lower()
            if lifestyle == 'professional':
                style_scores['classic'] += 0.3
                style_scores['minimalist'] += 0.2
            elif lifestyle == 'creative':
                style_scores['edgy'] += 0.3
                style_scores['bohemian'] += 0.2
            elif lifestyle == 'social':
                style_scores['trendy'] += 0.3
                style_scores['romantic'] += 0.2
        
        # Determine dominant style
        dominant_style = max(style_scores, key=style_scores.get)
        confidence = min(style_scores[dominant_style], 1.0)
        
        return dominant_style, confidence, style_scores
    
    @staticmethod
    def analyze_color_palette(user_data, style_personality):
        """
        AI-powered color palette analysis
        "We girls have no time" - Instant color recommendations!
        """
        # Color season mapping based on style personality
        color_seasons = {
            'classic': 'winter',
            'edgy': 'winter',
            'minimalist': 'winter',
            'bohemian': 'autumn',
            'romantic': 'spring',
            'trendy': 'summer'
        }
        
        season = color_seasons.get(style_personality, 'winter')
        
        # Color palettes by season
        color_palettes = {
            'spring': {
                'primary': ['coral', 'peach', 'light_blue', 'mint_green', 'lavender', 'warm_yellow'],
                'avoid': ['black', 'dark_brown', 'burgundy', 'navy']
            },
            'summer': {
                'primary': ['soft_blue', 'rose_pink', 'lavender', 'mint', 'soft_yellow', 'light_grey'],
                'avoid': ['orange', 'bright_yellow', 'warm_brown', 'gold']
            },
            'autumn': {
                'primary': ['rust', 'olive_green', 'burnt_orange', 'deep_brown', 'gold', 'burgundy'],
                'avoid': ['bright_pink', 'electric_blue', 'pure_white', 'silver']
            },
            'winter': {
                'primary': ['black', 'white', 'navy', 'burgundy', 'emerald', 'royal_blue'],
                'avoid': ['orange', 'yellow', 'brown', 'beige']
            }
        }
        
        palette = color_palettes.get(season, color_palettes['winter'])
        return season, palette['primary'], palette['avoid']


class OutfitRecommendation(db.Model):
    """
    AI-generated outfit recommendations
    "We girls have no time" - Instant outfit suggestions for any occasion!
    """
    __tablename__ = 'outfit_recommendation'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    
    # Recommendation metadata
    occasion = db.Column(db.String(50), nullable=False)  # e.g., 'work', 'date', 'casual'
    weather = db.Column(db.String(30), nullable=True)  # e.g., 'sunny', 'rainy', 'cold'
    season = db.Column(db.String(20), nullable=True)  # e.g., 'spring', 'summer'
    
    # Outfit composition
    outfit_items = db.Column(db.Text, nullable=False)  # JSON array of wardrobe item IDs
    outfit_description = db.Column(db.Text, nullable=True)  # Human-readable description
    
    # AI scoring
    style_match_score = db.Column(db.Float, default=0.0)  # How well it matches user's style
    occasion_match_score = db.Column(db.Float, default=0.0)  # How appropriate for occasion
    color_harmony_score = db.Column(db.Float, default=0.0)  # Color coordination score
    overall_score = db.Column(db.Float, default=0.0)  # Combined score
    
    # User interaction
    user_rating = db.Column(db.Integer, nullable=True)  # 1-5 stars
    worn_date = db.Column(db.Date, nullable=True)  # When user wore this outfit
    user_feedback = db.Column(db.Text, nullable=True)  # User comments
    
    # Recommendation metadata
    algorithm_version = db.Column(db.String(20), default='1.0')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<OutfitRecommendation {self.user_id}:{self.occasion}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'occasion': self.occasion,
            'weather': self.weather,
            'season': self.season,
            'outfit_items': json.loads(self.outfit_items) if self.outfit_items else [],
            'outfit_description': self.outfit_description,
            'style_match_score': round(self.style_match_score, 2),
            'occasion_match_score': round(self.occasion_match_score, 2),
            'color_harmony_score': round(self.color_harmony_score, 2),
            'overall_score': round(self.overall_score, 2),
            'user_rating': self.user_rating,
            'worn_date': self.worn_date.isoformat() if self.worn_date else None,
            'user_feedback': self.user_feedback,
            'algorithm_version': self.algorithm_version,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def generate_outfit_recommendation(user_id, wardrobe_items, style_analysis, occasion, weather=None, season=None):
        """
        AI-powered outfit generation
        "We girls have no time" - Smart outfit creation in seconds!
        """
        if not wardrobe_items:
            return None
        
        # Occasion-based item requirements
        occasion_requirements = {
            'work': {
                'required_categories': ['tops', 'bottoms'],
                'optional_categories': ['blazers', 'shoes', 'accessories'],
                'avoid_categories': ['crop_tops', 'mini_skirts', 'flip_flops'],
                'formality_level': 'formal'
            },
            'casual': {
                'required_categories': ['tops', 'bottoms'],
                'optional_categories': ['outerwear', 'shoes', 'accessories'],
                'avoid_categories': ['formal_wear', 'evening_wear'],
                'formality_level': 'casual'
            },
            'date': {
                'required_categories': ['tops', 'bottoms'],
                'optional_categories': ['dresses', 'shoes', 'accessories', 'outerwear'],
                'avoid_categories': ['gym_wear', 'pajamas'],
                'formality_level': 'semi_formal'
            },
            'party': {
                'required_categories': ['tops', 'bottoms'],
                'optional_categories': ['dresses', 'shoes', 'accessories', 'jewelry'],
                'avoid_categories': ['work_wear', 'gym_wear'],
                'formality_level': 'dressy'
            }
        }
        
        requirements = occasion_requirements.get(occasion, occasion_requirements['casual'])
        
        # Filter items by occasion appropriateness
        suitable_items = []
        for item in wardrobe_items:
            category = item.get('category', '').lower()
            if category not in requirements.get('avoid_categories', []):
                suitable_items.append(item)
        
        if len(suitable_items) < 2:
            return None
        
        # Select items for outfit
        outfit_items = []
        used_categories = set()
        
        # Prioritize required categories
        for req_category in requirements['required_categories']:
            category_items = [item for item in suitable_items 
                            if item.get('category', '').lower() == req_category]
            if category_items:
                # Select best item from category (prefer favorites)
                best_item = max(category_items, 
                              key=lambda x: (x.get('favorite', False), x.get('wear_count', 0)))
                outfit_items.append(best_item)
                used_categories.add(req_category)
        
        # Add optional items if space allows
        for opt_category in requirements['optional_categories']:
            if len(outfit_items) >= 5:  # Limit outfit size
                break
            if opt_category not in used_categories:
                category_items = [item for item in suitable_items 
                                if item.get('category', '').lower() == opt_category]
                if category_items:
                    best_item = max(category_items, 
                                  key=lambda x: (x.get('favorite', False), x.get('wear_count', 0)))
                    outfit_items.append(best_item)
                    used_categories.add(opt_category)
        
        if len(outfit_items) < 2:
            return None
        
        # Calculate scores
        style_score = OutfitRecommendation.calculate_style_match_score(outfit_items, style_analysis)
        occasion_score = OutfitRecommendation.calculate_occasion_score(outfit_items, requirements)
        color_score = OutfitRecommendation.calculate_color_harmony_score(outfit_items, style_analysis)
        overall_score = (style_score + occasion_score + color_score) / 3
        
        # Generate description
        description = OutfitRecommendation.generate_outfit_description(outfit_items, occasion)
        
        return {
            'outfit_items': [item.get('id') for item in outfit_items],
            'outfit_description': description,
            'style_match_score': style_score,
            'occasion_match_score': occasion_score,
            'color_harmony_score': color_score,
            'overall_score': overall_score
        }
    
    @staticmethod
    def calculate_style_match_score(outfit_items, style_analysis):
        """Calculate how well outfit matches user's style"""
        if not style_analysis:
            return 0.5
        
        style_personality = style_analysis.get('style_personality', '').lower()
        
        # Style-specific scoring
        style_bonuses = {
            'classic': ['blazers', 'trousers', 'button_downs', 'pumps'],
            'edgy': ['leather_jackets', 'boots', 'black_items', 'ripped_jeans'],
            'minimalist': ['simple_cuts', 'neutral_colors', 'clean_lines'],
            'bohemian': ['maxi_dresses', 'flowing_fabrics', 'earth_tones'],
            'romantic': ['dresses', 'soft_fabrics', 'pastels', 'florals'],
            'trendy': ['current_styles', 'bold_colors', 'statement_pieces']
        }
        
        score = 0.5  # Base score
        bonus_items = style_bonuses.get(style_personality, [])
        
        for item in outfit_items:
            category = item.get('category', '').lower()
            color = item.get('primary_color', '').lower()
            
            if category in bonus_items or color in bonus_items:
                score += 0.1
        
        return min(score, 1.0)
    
    @staticmethod
    def calculate_occasion_score(outfit_items, requirements):
        """Calculate appropriateness for occasion"""
        score = 0.5
        
        # Check required categories are present
        present_categories = [item.get('category', '').lower() for item in outfit_items]
        required_present = sum(1 for cat in requirements['required_categories'] 
                             if cat in present_categories)
        
        if required_present == len(requirements['required_categories']):
            score += 0.3
        
        # Check no avoided categories
        avoided_present = sum(1 for cat in requirements.get('avoid_categories', []) 
                            if cat in present_categories)
        if avoided_present == 0:
            score += 0.2
        
        return min(score, 1.0)
    
    @staticmethod
    def calculate_color_harmony_score(outfit_items, style_analysis):
        """Calculate color coordination score"""
        if len(outfit_items) < 2:
            return 1.0
        
        colors = [item.get('primary_color', '').lower() for item in outfit_items if item.get('primary_color')]
        
        if not colors:
            return 0.5
        
        # Color harmony rules
        neutral_colors = ['black', 'white', 'grey', 'beige', 'navy', 'brown']
        
        # All neutrals = high harmony
        if all(color in neutral_colors for color in colors):
            return 0.9
        
        # Mix of neutrals and one accent = good harmony
        non_neutrals = [color for color in colors if color not in neutral_colors]
        if len(non_neutrals) <= 1:
            return 0.8
        
        # Multiple non-neutrals = lower harmony (unless they're complementary)
        return 0.6
    
    @staticmethod
    def generate_outfit_description(outfit_items, occasion):
        """Generate human-readable outfit description"""
        if not outfit_items:
            return "Empty outfit"
        
        categories = [item.get('category', 'item').replace('_', ' ') for item in outfit_items]
        colors = [item.get('primary_color', '') for item in outfit_items if item.get('primary_color')]
        
        # Build description
        description_parts = []
        
        if colors:
            main_colors = list(set(colors))[:2]  # Top 2 colors
            color_desc = ' and '.join(main_colors)
            description_parts.append(f"A {color_desc} ensemble")
        
        if categories:
            category_desc = ', '.join(categories[:3])  # Top 3 categories
            description_parts.append(f"featuring {category_desc}")
        
        description_parts.append(f"perfect for {occasion}")
        
        return ' '.join(description_parts) + "."


class AIInsight(db.Model):
    """
    AI-generated fashion insights and recommendations
    "We girls have no time" - Smart fashion insights delivered instantly!
    """
    __tablename__ = 'ai_insight'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    
    # Insight metadata
    insight_type = db.Column(db.String(50), nullable=False)  # e.g., 'wardrobe_gap', 'style_tip', 'color_advice'
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # AI confidence and priority
    confidence_score = db.Column(db.Float, default=0.0)  # 0.0 to 1.0
    priority = db.Column(db.String(20), default='medium')  # 'low', 'medium', 'high'
    
    # Actionable recommendations
    recommendations = db.Column(db.Text, nullable=True)  # JSON array of specific actions
    shopping_suggestions = db.Column(db.Text, nullable=True)  # JSON array of items to buy
    
    # Insight lifecycle
    status = db.Column(db.String(20), default='active')  # 'active', 'dismissed', 'acted_upon'
    expires_at = db.Column(db.DateTime, nullable=True)
    user_action = db.Column(db.String(50), nullable=True)  # What user did with this insight
    
    # AI metadata
    algorithm_version = db.Column(db.String(20), default='1.0')
    data_sources = db.Column(db.Text, nullable=True)  # JSON array of data sources
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<AIInsight {self.user_id}:{self.insight_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'insight_type': self.insight_type,
            'title': self.title,
            'description': self.description,
            'confidence_score': round(self.confidence_score, 2),
            'priority': self.priority,
            'recommendations': json.loads(self.recommendations) if self.recommendations else [],
            'shopping_suggestions': json.loads(self.shopping_suggestions) if self.shopping_suggestions else [],
            'status': self.status,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'user_action': self.user_action,
            'algorithm_version': self.algorithm_version,
            'data_sources': json.loads(self.data_sources) if self.data_sources else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def generate_wardrobe_gap_insights(user_id, wardrobe_items, style_analysis):
        """
        Generate insights about missing wardrobe essentials
        "We girls have no time" - Identify wardrobe gaps instantly!
        """
        insights = []
        
        if not wardrobe_items:
            return [{
                'insight_type': 'wardrobe_gap',
                'title': 'Build Your Foundation Wardrobe',
                'description': 'Start building your wardrobe with essential pieces that work for any occasion.',
                'confidence_score': 1.0,
                'priority': 'high',
                'recommendations': ['Add basic tops', 'Get versatile bottoms', 'Invest in quality shoes'],
                'shopping_suggestions': ['White button-down shirt', 'Black trousers', 'Comfortable flats']
            }]
        
        # Analyze wardrobe categories
        categories = [item.get('category', '').lower() for item in wardrobe_items]
        category_counts = {}
        for cat in categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Essential categories by style
        style_personality = style_analysis.get('style_personality', 'classic') if style_analysis else 'classic'
        
        essential_categories = {
            'classic': ['tops', 'bottoms', 'blazers', 'shoes', 'outerwear'],
            'edgy': ['tops', 'bottoms', 'leather_jackets', 'boots', 'accessories'],
            'minimalist': ['tops', 'bottoms', 'shoes', 'outerwear'],
            'bohemian': ['dresses', 'tops', 'bottoms', 'sandals', 'accessories'],
            'romantic': ['dresses', 'tops', 'skirts', 'shoes', 'accessories'],
            'trendy': ['tops', 'bottoms', 'dresses', 'shoes', 'accessories']
        }
        
        essentials = essential_categories.get(style_personality, essential_categories['classic'])
        
        # Find missing categories
        missing_categories = [cat for cat in essentials if category_counts.get(cat, 0) == 0]
        
        for missing_cat in missing_categories[:3]:  # Top 3 missing categories
            insight = AIInsight.create_wardrobe_gap_insight(missing_cat, style_personality)
            if insight:
                insight['user_id'] = user_id
                insights.append(insight)
        
        # Check for insufficient quantities
        for cat in essentials:
            count = category_counts.get(cat, 0)
            if 0 < count < 2:  # Has some but not enough
                insight = AIInsight.create_quantity_insight(cat, count, style_personality)
                if insight:
                    insight['user_id'] = user_id
                    insights.append(insight)
        
        return insights[:5]  # Return top 5 insights
    
    @staticmethod
    def create_wardrobe_gap_insight(missing_category, style_personality):
        """Create insight for missing wardrobe category"""
        category_suggestions = {
            'tops': {
                'title': 'Essential Tops Missing',
                'description': 'Your wardrobe needs versatile tops that can be dressed up or down.',
                'recommendations': ['Add basic t-shirts', 'Get button-down shirts', 'Consider blouses'],
                'shopping': ['White t-shirt', 'Black t-shirt', 'Striped top']
            },
            'bottoms': {
                'title': 'Foundation Bottoms Needed',
                'description': 'Build your wardrobe foundation with versatile bottom pieces.',
                'recommendations': ['Add well-fitting jeans', 'Get dress pants', 'Consider skirts'],
                'shopping': ['Dark wash jeans', 'Black trousers', 'A-line skirt']
            },
            'blazers': {
                'title': 'Professional Blazer Missing',
                'description': 'A blazer instantly elevates any outfit and is essential for professional looks.',
                'recommendations': ['Invest in a quality blazer', 'Choose neutral colors', 'Ensure proper fit'],
                'shopping': ['Navy blazer', 'Black blazer', 'Grey blazer']
            },
            'shoes': {
                'title': 'Shoe Collection Needs Expansion',
                'description': 'Complete your outfits with appropriate footwear for different occasions.',
                'recommendations': ['Get comfortable flats', 'Add dress shoes', 'Consider casual sneakers'],
                'shopping': ['Black flats', 'Nude heels', 'White sneakers']
            },
            'dresses': {
                'title': 'Versatile Dresses Missing',
                'description': 'Dresses are perfect for busy lifestyles - one piece, complete outfit!',
                'recommendations': ['Add a little black dress', 'Get casual day dresses', 'Consider work dresses'],
                'shopping': ['Black midi dress', 'Wrap dress', 'Shirt dress']
            }
        }
        
        suggestion = category_suggestions.get(missing_category)
        if not suggestion:
            return None
        
        return {
            'insight_type': 'wardrobe_gap',
            'title': suggestion['title'],
            'description': suggestion['description'],
            'confidence_score': 0.8,
            'priority': 'medium',
            'recommendations': suggestion['recommendations'],
            'shopping_suggestions': suggestion['shopping']
        }
    
    @staticmethod
    def create_quantity_insight(category, current_count, style_personality):
        """Create insight for insufficient quantity in category"""
        return {
            'insight_type': 'wardrobe_expansion',
            'title': f'Expand Your {category.title()} Collection',
            'description': f'You have {current_count} {category} item(s). Adding more variety will give you more outfit options.',
            'confidence_score': 0.6,
            'priority': 'low',
            'recommendations': [f'Add 1-2 more {category} items', 'Choose different colors or styles', 'Consider seasonal variations'],
            'shopping_suggestions': [f'Additional {category} in different color', f'Alternative {category} style']
        }

