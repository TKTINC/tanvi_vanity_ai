from datetime import datetime, timedelta, date
import json
from collections import defaultdict

# Import db from user module to avoid circular imports
from src.models.user import db

class UserAnalytics(db.Model):
    """
    User behavior analytics for personalized insights
    "We girls have no time" - Smart analytics with instant insights
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Daily activity metrics
    date = db.Column(db.Date, default=date.today, nullable=False)
    login_count = db.Column(db.Integer, default=0)
    session_duration = db.Column(db.Integer, default=0)  # Total seconds
    api_calls = db.Column(db.Integer, default=0)
    
    # Style engagement metrics
    style_quiz_taken = db.Column(db.Boolean, default=False)
    wardrobe_items_added = db.Column(db.Integer, default=0)
    outfits_logged = db.Column(db.Integer, default=0)
    outfits_rated = db.Column(db.Integer, default=0)
    profile_updates = db.Column(db.Integer, default=0)
    
    # Feature usage tracking
    features_used = db.Column(db.Text, nullable=True)  # JSON array of feature names
    most_used_category = db.Column(db.String(50), nullable=True)  # wardrobe category
    
    # Time-based patterns
    peak_usage_hour = db.Column(db.Integer, nullable=True)  # 0-23
    weekend_usage = db.Column(db.Boolean, default=False)
    
    # Engagement quality
    completion_rate = db.Column(db.Float, default=0.0)  # Percentage of completed actions
    satisfaction_score = db.Column(db.Float, nullable=True)  # Average rating given
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<UserAnalytics {self.user_id}:{self.date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat(),
            'login_count': self.login_count,
            'session_duration': self.session_duration,
            'api_calls': self.api_calls,
            'style_quiz_taken': self.style_quiz_taken,
            'wardrobe_items_added': self.wardrobe_items_added,
            'outfits_logged': self.outfits_logged,
            'outfits_rated': self.outfits_rated,
            'profile_updates': self.profile_updates,
            'features_used': json.loads(self.features_used) if self.features_used else [],
            'most_used_category': self.most_used_category,
            'peak_usage_hour': self.peak_usage_hour,
            'weekend_usage': self.weekend_usage,
            'completion_rate': self.completion_rate,
            'satisfaction_score': self.satisfaction_score,
            'updated_at': self.updated_at.isoformat()
        }


class StyleInsights(db.Model):
    """
    AI-generated style insights and recommendations
    "We girls have no time" - Instant style intelligence
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Insight metadata
    insight_type = db.Column(db.String(50), nullable=False)  # wardrobe_gap, color_analysis, style_evolution, etc.
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    confidence_score = db.Column(db.Float, nullable=False)  # AI confidence 0-1
    
    # Insight content
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    actionable_tips = db.Column(db.Text, nullable=True)  # JSON array of tips
    
    # Data supporting the insight
    supporting_data = db.Column(db.Text, nullable=True)  # JSON with metrics/evidence
    
    # User interaction
    viewed = db.Column(db.Boolean, default=False)
    dismissed = db.Column(db.Boolean, default=False)
    acted_upon = db.Column(db.Boolean, default=False)
    user_feedback = db.Column(db.Integer, nullable=True)  # 1-5 rating
    
    # Timing and relevance
    expires_at = db.Column(db.DateTime, nullable=True)  # When insight becomes irrelevant
    seasonal_relevance = db.Column(db.String(20), nullable=True)  # spring, summer, fall, winter
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<StyleInsights {self.user_id}:{self.insight_type}>'

    def is_expired(self):
        """Check if insight is still relevant"""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'insight_type': self.insight_type,
            'priority': self.priority,
            'confidence_score': self.confidence_score,
            'title': self.title,
            'description': self.description,
            'actionable_tips': json.loads(self.actionable_tips) if self.actionable_tips else [],
            'supporting_data': json.loads(self.supporting_data) if self.supporting_data else {},
            'viewed': self.viewed,
            'dismissed': self.dismissed,
            'acted_upon': self.acted_upon,
            'user_feedback': self.user_feedback,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'seasonal_relevance': self.seasonal_relevance,
            'is_expired': self.is_expired(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class UsagePattern(db.Model):
    """
    Long-term usage patterns and trends
    "We girls have no time" - Pattern recognition for better UX
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Pattern identification
    pattern_type = db.Column(db.String(50), nullable=False)  # daily, weekly, seasonal, event_based
    pattern_name = db.Column(db.String(100), nullable=False)  # "Morning Stylist", "Weekend Warrior", etc.
    
    # Pattern details
    description = db.Column(db.Text, nullable=False)
    frequency = db.Column(db.String(30), nullable=False)  # daily, weekly, monthly, seasonal
    strength = db.Column(db.Float, nullable=False)  # 0-1, how consistent the pattern is
    
    # Timing information
    typical_times = db.Column(db.Text, nullable=True)  # JSON array of hours/days
    duration_minutes = db.Column(db.Integer, nullable=True)  # Typical session length
    
    # Associated behaviors
    common_actions = db.Column(db.Text, nullable=True)  # JSON array of actions
    preferred_features = db.Column(db.Text, nullable=True)  # JSON array of features
    
    # Pattern evolution
    first_detected = db.Column(db.DateTime, default=datetime.utcnow)
    last_observed = db.Column(db.DateTime, default=datetime.utcnow)
    trend_direction = db.Column(db.String(20), nullable=True)  # increasing, decreasing, stable
    
    # Personalization opportunities
    optimization_suggestions = db.Column(db.Text, nullable=True)  # JSON array
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<UsagePattern {self.user_id}:{self.pattern_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pattern_type': self.pattern_type,
            'pattern_name': self.pattern_name,
            'description': self.description,
            'frequency': self.frequency,
            'strength': self.strength,
            'typical_times': json.loads(self.typical_times) if self.typical_times else [],
            'duration_minutes': self.duration_minutes,
            'common_actions': json.loads(self.common_actions) if self.common_actions else [],
            'preferred_features': json.loads(self.preferred_features) if self.preferred_features else [],
            'first_detected': self.first_detected.isoformat(),
            'last_observed': self.last_observed.isoformat(),
            'trend_direction': self.trend_direction,
            'optimization_suggestions': json.loads(self.optimization_suggestions) if self.optimization_suggestions else [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class PersonalizationScore(db.Model):
    """
    Dynamic personalization scoring for adaptive UX
    "We girls have no time" - Smart adaptation to user preferences
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Overall personalization metrics
    overall_score = db.Column(db.Float, default=0.0)  # 0-100 overall personalization
    profile_completeness = db.Column(db.Float, default=0.0)  # 0-100
    engagement_level = db.Column(db.Float, default=0.0)  # 0-100
    satisfaction_level = db.Column(db.Float, default=0.0)  # 0-100
    
    # Feature-specific scores
    style_confidence = db.Column(db.Float, default=0.0)  # How well we know their style
    wardrobe_knowledge = db.Column(db.Float, default=0.0)  # How complete wardrobe data is
    preference_accuracy = db.Column(db.Float, default=0.0)  # How accurate our recommendations are
    
    # Behavioral indicators
    quick_decisions = db.Column(db.Boolean, default=True)  # Prefers fast interactions
    detail_oriented = db.Column(db.Boolean, default=False)  # Likes detailed information
    trend_follower = db.Column(db.Boolean, default=False)  # Follows fashion trends
    budget_conscious = db.Column(db.Boolean, default=True)  # Price-sensitive
    
    # Adaptation parameters
    ui_complexity_preference = db.Column(db.String(20), default='simple')  # simple, moderate, advanced
    notification_tolerance = db.Column(db.String(20), default='low')  # low, medium, high
    recommendation_frequency = db.Column(db.String(20), default='daily')  # daily, weekly, on_demand
    
    # Learning indicators
    learning_rate = db.Column(db.Float, default=1.0)  # How quickly they adapt to suggestions
    feedback_frequency = db.Column(db.Float, default=0.0)  # How often they provide feedback
    
    # Temporal factors
    time_of_day_preference = db.Column(db.Text, nullable=True)  # JSON array of preferred hours
    seasonal_activity = db.Column(db.Text, nullable=True)  # JSON with seasonal patterns
    
    last_calculated = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<PersonalizationScore {self.user_id}:{self.overall_score}>'

    def calculate_overall_score(self):
        """Calculate overall personalization score from components"""
        components = [
            self.profile_completeness * 0.3,
            self.engagement_level * 0.25,
            self.satisfaction_level * 0.25,
            self.preference_accuracy * 0.2
        ]
        self.overall_score = sum(components)
        return self.overall_score

    def get_personalization_level(self):
        """Get personalization level category"""
        if self.overall_score >= 80:
            return 'highly_personalized'
        elif self.overall_score >= 60:
            return 'well_personalized'
        elif self.overall_score >= 40:
            return 'moderately_personalized'
        elif self.overall_score >= 20:
            return 'basic_personalization'
        else:
            return 'minimal_personalization'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'overall_score': self.overall_score,
            'personalization_level': self.get_personalization_level(),
            'profile_completeness': self.profile_completeness,
            'engagement_level': self.engagement_level,
            'satisfaction_level': self.satisfaction_level,
            'style_confidence': self.style_confidence,
            'wardrobe_knowledge': self.wardrobe_knowledge,
            'preference_accuracy': self.preference_accuracy,
            'quick_decisions': self.quick_decisions,
            'detail_oriented': self.detail_oriented,
            'trend_follower': self.trend_follower,
            'budget_conscious': self.budget_conscious,
            'ui_complexity_preference': self.ui_complexity_preference,
            'notification_tolerance': self.notification_tolerance,
            'recommendation_frequency': self.recommendation_frequency,
            'learning_rate': self.learning_rate,
            'feedback_frequency': self.feedback_frequency,
            'time_of_day_preference': json.loads(self.time_of_day_preference) if self.time_of_day_preference else [],
            'seasonal_activity': json.loads(self.seasonal_activity) if self.seasonal_activity else {},
            'last_calculated': self.last_calculated.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class AnalyticsHelper:
    """
    Helper class for analytics calculations and insights generation
    "We girls have no time" - Instant analytics processing
    """
    
    @staticmethod
    def get_or_create_daily_analytics(user_id, target_date=None):
        """Get or create daily analytics record"""
        if target_date is None:
            target_date = date.today()
        
        analytics = UserAnalytics.query.filter_by(
            user_id=user_id,
            date=target_date
        ).first()
        
        if not analytics:
            analytics = UserAnalytics(user_id=user_id, date=target_date)
            db.session.add(analytics)
            db.session.commit()
        
        return analytics
    
    @staticmethod
    def track_feature_usage(user_id, feature_name):
        """Track usage of a specific feature"""
        analytics = AnalyticsHelper.get_or_create_daily_analytics(user_id)
        
        # Update features used
        features = json.loads(analytics.features_used) if analytics.features_used else []
        if feature_name not in features:
            features.append(feature_name)
            analytics.features_used = json.dumps(features)
        
        analytics.api_calls += 1
        analytics.updated_at = datetime.utcnow()
        db.session.commit()
    
    @staticmethod
    def calculate_user_insights(user_id):
        """Generate personalized insights for user"""
        from src.models.user import User
        from src.models.profile import StyleProfile, WardrobeItem, OutfitHistory
        
        user = User.query.get(user_id)
        if not user:
            return []
        
        insights = []
        
        # Wardrobe gap analysis
        wardrobe_items = WardrobeItem.query.filter_by(user_id=user_id).all()
        if wardrobe_items:
            categories = defaultdict(int)
            for item in wardrobe_items:
                categories[item.category] += 1
            
            # Check for missing basic categories
            basic_categories = ['top', 'bottom', 'shoes', 'outerwear']
            missing_categories = [cat for cat in basic_categories if categories[cat] == 0]
            
            if missing_categories:
                insight = StyleInsights(
                    user_id=user_id,
                    insight_type='wardrobe_gap',
                    priority='medium',
                    confidence_score=0.8,
                    title=f"Missing {len(missing_categories)} wardrobe essentials",
                    description=f"Your wardrobe could benefit from adding {', '.join(missing_categories)}. These are versatile pieces that work with many outfits.",
                    actionable_tips=json.dumps([
                        f"Consider adding a basic {cat}" for cat in missing_categories[:2]
                    ]),
                    supporting_data=json.dumps({
                        'missing_categories': missing_categories,
                        'current_categories': dict(categories)
                    }),
                    expires_at=datetime.utcnow() + timedelta(days=30)
                )
                insights.append(insight)
        
        # Style evolution insight
        style_profile = StyleProfile.query.filter_by(user_id=user_id).first()
        if style_profile and style_profile.last_style_quiz:
            days_since_quiz = (datetime.utcnow() - style_profile.last_style_quiz).days
            if days_since_quiz > 90:  # 3 months
                insight = StyleInsights(
                    user_id=user_id,
                    insight_type='style_evolution',
                    priority='low',
                    confidence_score=0.6,
                    title="Time for a style refresh?",
                    description="It's been a while since your last style quiz. Your preferences might have evolved!",
                    actionable_tips=json.dumps([
                        "Take a quick 2-minute style quiz to update your profile",
                        "Review your recent outfit ratings for pattern changes"
                    ]),
                    supporting_data=json.dumps({
                        'days_since_quiz': days_since_quiz,
                        'last_quiz_date': style_profile.last_style_quiz.isoformat()
                    }),
                    expires_at=datetime.utcnow() + timedelta(days=7)
                )
                insights.append(insight)
        
        # Save insights to database
        for insight in insights:
            db.session.add(insight)
        
        db.session.commit()
        return insights
    
    @staticmethod
    def update_personalization_score(user_id):
        """Update personalization score based on current data"""
        from src.models.user import User
        from src.models.profile import StyleProfile, WardrobeItem, OutfitHistory
        
        user = User.query.get(user_id)
        if not user:
            return None
        
        # Get or create personalization score
        score = PersonalizationScore.query.filter_by(user_id=user_id).first()
        if not score:
            score = PersonalizationScore(user_id=user_id)
            db.session.add(score)
        
        # Calculate profile completeness
        profile_fields = 0
        completed_fields = 0
        
        # Basic profile
        basic_fields = [user.first_name, user.age_range, user.style_preference]
        profile_fields += len(basic_fields)
        completed_fields += sum(1 for field in basic_fields if field)
        
        # Style profile
        style_profile = user.style_profile
        if style_profile:
            style_fields = [
                style_profile.body_type, style_profile.style_personality,
                style_profile.skin_tone, style_profile.favorite_colors
            ]
            profile_fields += len(style_fields)
            completed_fields += sum(1 for field in style_fields if field)
        
        score.profile_completeness = (completed_fields / profile_fields * 100) if profile_fields > 0 else 0
        
        # Calculate wardrobe knowledge
        wardrobe_items = WardrobeItem.query.filter_by(user_id=user_id).count()
        score.wardrobe_knowledge = min(wardrobe_items * 10, 100)  # 10 points per item, max 100
        
        # Calculate engagement level
        recent_analytics = UserAnalytics.query.filter_by(user_id=user_id)\
            .filter(UserAnalytics.date >= date.today() - timedelta(days=7))\
            .all()
        
        if recent_analytics:
            total_sessions = sum(a.login_count for a in recent_analytics)
            total_actions = sum(a.wardrobe_items_added + a.outfits_logged + a.outfits_rated for a in recent_analytics)
            score.engagement_level = min(total_sessions * 5 + total_actions * 3, 100)
        
        # Calculate satisfaction level from outfit ratings
        recent_outfits = OutfitHistory.query.filter_by(user_id=user_id)\
            .filter(OutfitHistory.user_rating.isnot(None))\
            .limit(10).all()
        
        if recent_outfits:
            avg_rating = sum(o.user_rating for o in recent_outfits) / len(recent_outfits)
            score.satisfaction_level = avg_rating * 20  # Convert 1-5 scale to 0-100
        
        # Update overall score
        score.calculate_overall_score()
        score.last_calculated = datetime.utcnow()
        score.updated_at = datetime.utcnow()
        
        db.session.commit()
        return score

