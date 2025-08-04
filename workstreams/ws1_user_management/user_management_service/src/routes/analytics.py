from flask import Blueprint, jsonify, request
from src.models.user import User, db
from src.models.analytics import UserAnalytics, StyleInsights, UsagePattern, PersonalizationScore, AnalyticsHelper
from datetime import datetime, date, timedelta
import json

analytics_bp = Blueprint('analytics', __name__)

def get_current_user():
    """Helper function to get current authenticated user"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    return User.verify_auth_token(token)

@analytics_bp.route('/dashboard', methods=['GET'])
def get_analytics_dashboard():
    """
    Get user analytics dashboard - "We girls have no time" for complex analytics
    Quick overview of user behavior and insights
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        # Get recent analytics (last 7 days)
        end_date = date.today()
        start_date = end_date - timedelta(days=6)
        
        recent_analytics = UserAnalytics.query.filter_by(user_id=user.id)\
            .filter(UserAnalytics.date >= start_date)\
            .filter(UserAnalytics.date <= end_date)\
            .order_by(UserAnalytics.date.desc()).all()
        
        # Calculate quick stats
        total_sessions = sum(a.login_count for a in recent_analytics)
        total_time = sum(a.session_duration for a in recent_analytics)
        total_actions = sum(a.wardrobe_items_added + a.outfits_logged + a.outfits_rated for a in recent_analytics)
        
        # Get personalization score
        personalization = PersonalizationScore.query.filter_by(user_id=user.id).first()
        if not personalization:
            personalization = AnalyticsHelper.update_personalization_score(user.id)
        
        # Get active insights
        active_insights = StyleInsights.query.filter_by(user_id=user.id, dismissed=False)\
            .filter(StyleInsights.expires_at > datetime.utcnow())\
            .order_by(StyleInsights.priority.desc(), StyleInsights.created_at.desc())\
            .limit(5).all()
        
        # Get usage patterns
        patterns = UsagePattern.query.filter_by(user_id=user.id)\
            .order_by(UsagePattern.strength.desc())\
            .limit(3).all()
        
        dashboard_data = {
            'summary': {
                'total_sessions_week': total_sessions,
                'total_time_minutes': total_time // 60,
                'total_actions_week': total_actions,
                'personalization_score': personalization.overall_score if personalization else 0,
                'personalization_level': personalization.get_personalization_level() if personalization else 'minimal_personalization'
            },
            'recent_activity': [a.to_dict() for a in recent_analytics],
            'insights': [i.to_dict() for i in active_insights],
            'usage_patterns': [p.to_dict() for p in patterns],
            'personalization': personalization.to_dict() if personalization else None
        }
        
        return jsonify({
            'message': 'Analytics dashboard retrieved successfully',
            'tagline': 'We girls have no time - here\'s your quick insights overview!',
            'dashboard': dashboard_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve analytics dashboard',
            'message': str(e)
        }), 500


@analytics_bp.route('/insights', methods=['GET'])
def get_style_insights():
    """
    Get personalized style insights - "We girls have no time" for manual analysis
    AI-generated insights for quick style improvements
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        # Get query parameters
        include_dismissed = request.args.get('include_dismissed', 'false').lower() == 'true'
        priority_filter = request.args.get('priority')  # high, medium, low
        
        # Build query
        query = StyleInsights.query.filter_by(user_id=user.id)
        
        if not include_dismissed:
            query = query.filter_by(dismissed=False)
        
        if priority_filter:
            query = query.filter_by(priority=priority_filter)
        
        # Only show non-expired insights
        query = query.filter(StyleInsights.expires_at > datetime.utcnow())
        
        insights = query.order_by(
            StyleInsights.priority.desc(),
            StyleInsights.created_at.desc()
        ).all()
        
        # Generate new insights if we have less than 3
        if len(insights) < 3:
            new_insights = AnalyticsHelper.calculate_user_insights(user.id)
            insights.extend(new_insights)
        
        # Track feature usage
        AnalyticsHelper.track_feature_usage(user.id, 'style_insights')
        
        return jsonify({
            'message': 'Style insights retrieved successfully',
            'tagline': 'We girls have no time - here are your instant style insights!',
            'insights': [insight.to_dict() for insight in insights],
            'total_count': len(insights)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve style insights',
            'message': str(e)
        }), 500


@analytics_bp.route('/insights/<int:insight_id>/action', methods=['POST'])
def interact_with_insight(insight_id):
    """
    Interact with a style insight - quick feedback for AI learning
    "We girls have no time" for complex feedback forms
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        insight = StyleInsights.query.filter_by(id=insight_id, user_id=user.id).first()
        if not insight:
            return jsonify({'error': 'Insight not found'}), 404
        
        data = request.json
        action = data.get('action')  # view, dismiss, act_upon, rate
        
        if action == 'view':
            insight.viewed = True
        elif action == 'dismiss':
            insight.dismissed = True
        elif action == 'act_upon':
            insight.acted_upon = True
        elif action == 'rate':
            rating = data.get('rating')
            if rating and 1 <= rating <= 5:
                insight.user_feedback = rating
        
        insight.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Track feature usage
        AnalyticsHelper.track_feature_usage(user.id, f'insight_{action}')
        
        return jsonify({
            'message': f'Insight {action} recorded successfully',
            'tagline': 'We girls have no time - feedback recorded instantly!',
            'insight': insight.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to interact with insight',
            'message': str(e)
        }), 500


@analytics_bp.route('/patterns', methods=['GET'])
def get_usage_patterns():
    """
    Get user usage patterns - "We girls have no time" for complex behavior analysis
    Quick insights into user behavior patterns
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        patterns = UsagePattern.query.filter_by(user_id=user.id)\
            .order_by(UsagePattern.strength.desc())\
            .all()
        
        # If no patterns exist, generate some basic ones
        if not patterns:
            patterns = generate_basic_patterns(user.id)
        
        # Track feature usage
        AnalyticsHelper.track_feature_usage(user.id, 'usage_patterns')
        
        return jsonify({
            'message': 'Usage patterns retrieved successfully',
            'tagline': 'We girls have no time - here are your quick behavior insights!',
            'patterns': [pattern.to_dict() for pattern in patterns]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve usage patterns',
            'message': str(e)
        }), 500


def generate_basic_patterns(user_id):
    """Generate basic usage patterns for new users"""
    patterns = []
    
    # Analyze recent activity
    recent_analytics = UserAnalytics.query.filter_by(user_id=user_id)\
        .filter(UserAnalytics.date >= date.today() - timedelta(days=30))\
        .all()
    
    if recent_analytics:
        # Morning vs Evening usage
        morning_sessions = sum(1 for a in recent_analytics if a.peak_usage_hour and 6 <= a.peak_usage_hour <= 12)
        evening_sessions = sum(1 for a in recent_analytics if a.peak_usage_hour and 18 <= a.peak_usage_hour <= 23)
        
        if morning_sessions > evening_sessions:
            pattern = UsagePattern(
                user_id=user_id,
                pattern_type='daily',
                pattern_name='Morning Stylist',
                description='You tend to plan your outfits in the morning, getting ready for the day ahead.',
                frequency='daily',
                strength=0.7,
                typical_times=json.dumps([7, 8, 9, 10]),
                common_actions=json.dumps(['wardrobe_check', 'outfit_planning']),
                optimization_suggestions=json.dumps([
                    'Set up quick morning outfit suggestions',
                    'Enable weather-based recommendations for morning planning'
                ])
            )
            patterns.append(pattern)
        
        # Weekend usage
        weekend_sessions = sum(1 for a in recent_analytics if a.weekend_usage)
        if weekend_sessions > 0:
            pattern = UsagePattern(
                user_id=user_id,
                pattern_type='weekly',
                pattern_name='Weekend Planner',
                description='You like to organize and plan your wardrobe during weekends.',
                frequency='weekly',
                strength=0.6,
                typical_times=json.dumps([10, 11, 14, 15]),
                common_actions=json.dumps(['wardrobe_organization', 'outfit_logging']),
                optimization_suggestions=json.dumps([
                    'Weekend wardrobe review reminders',
                    'Batch outfit planning for the week ahead'
                ])
            )
            patterns.append(pattern)
    
    # Save patterns
    for pattern in patterns:
        db.session.add(pattern)
    db.session.commit()
    
    return patterns


@analytics_bp.route('/personalization', methods=['GET'])
def get_personalization_score():
    """
    Get personalization score and recommendations - quick UX adaptation insights
    "We girls have no time" for complex personalization analysis
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        # Get or update personalization score
        score = AnalyticsHelper.update_personalization_score(user.id)
        
        # Generate personalization recommendations
        recommendations = []
        
        if score.profile_completeness < 70:
            recommendations.append({
                'type': 'profile_completion',
                'priority': 'high',
                'title': 'Complete your style profile',
                'description': 'Add more details to get better recommendations',
                'action': 'Complete missing profile fields',
                'estimated_time': '2 minutes'
            })
        
        if score.wardrobe_knowledge < 50:
            recommendations.append({
                'type': 'wardrobe_building',
                'priority': 'medium',
                'title': 'Build your digital wardrobe',
                'description': 'Add more items for better outfit suggestions',
                'action': 'Photograph and catalog 5 favorite items',
                'estimated_time': '5 minutes'
            })
        
        if score.engagement_level < 40:
            recommendations.append({
                'type': 'engagement_boost',
                'priority': 'low',
                'title': 'Try new features',
                'description': 'Explore more features to improve your experience',
                'action': 'Rate recent outfits or take style quiz',
                'estimated_time': '3 minutes'
            })
        
        # Track feature usage
        AnalyticsHelper.track_feature_usage(user.id, 'personalization_score')
        
        return jsonify({
            'message': 'Personalization score retrieved successfully',
            'tagline': 'We girls have no time - here\'s your quick personalization overview!',
            'personalization': score.to_dict(),
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve personalization score',
            'message': str(e)
        }), 500


@analytics_bp.route('/activity-summary', methods=['GET'])
def get_activity_summary():
    """
    Get activity summary for a date range - quick activity overview
    "We girls have no time" for detailed activity reports
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        # Get query parameters
        days = int(request.args.get('days', 7))  # Default to 7 days
        days = min(days, 90)  # Max 90 days
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days-1)
        
        analytics = UserAnalytics.query.filter_by(user_id=user.id)\
            .filter(UserAnalytics.date >= start_date)\
            .filter(UserAnalytics.date <= end_date)\
            .order_by(UserAnalytics.date.desc()).all()
        
        # Calculate summary statistics
        summary = {
            'date_range': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'days': days
            },
            'totals': {
                'sessions': sum(a.login_count for a in analytics),
                'time_minutes': sum(a.session_duration for a in analytics) // 60,
                'api_calls': sum(a.api_calls for a in analytics),
                'wardrobe_items_added': sum(a.wardrobe_items_added for a in analytics),
                'outfits_logged': sum(a.outfits_logged for a in analytics),
                'outfits_rated': sum(a.outfits_rated for a in analytics),
                'profile_updates': sum(a.profile_updates for a in analytics)
            },
            'averages': {
                'sessions_per_day': sum(a.login_count for a in analytics) / days,
                'time_per_day': sum(a.session_duration for a in analytics) / days / 60,
                'actions_per_session': sum(a.wardrobe_items_added + a.outfits_logged + a.outfits_rated for a in analytics) / max(sum(a.login_count for a in analytics), 1)
            },
            'activity_by_day': [a.to_dict() for a in analytics]
        }
        
        # Track feature usage
        AnalyticsHelper.track_feature_usage(user.id, 'activity_summary')
        
        return jsonify({
            'message': 'Activity summary retrieved successfully',
            'tagline': f'We girls have no time - here\'s your {days}-day activity overview!',
            'summary': summary
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve activity summary',
            'message': str(e)
        }), 500


@analytics_bp.route('/track-action', methods=['POST'])
def track_user_action():
    """
    Track a user action for analytics - quick action logging
    "We girls have no time" for complex tracking setup
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        data = request.json
        action_type = data.get('action_type')  # login, wardrobe_add, outfit_log, etc.
        
        if not action_type:
            return jsonify({'error': 'Action type is required'}), 400
        
        # Get today's analytics
        analytics = AnalyticsHelper.get_or_create_daily_analytics(user.id)
        
        # Update based on action type
        if action_type == 'login':
            analytics.login_count += 1
        elif action_type == 'wardrobe_add':
            analytics.wardrobe_items_added += 1
        elif action_type == 'outfit_log':
            analytics.outfits_logged += 1
        elif action_type == 'outfit_rate':
            analytics.outfits_rated += 1
        elif action_type == 'profile_update':
            analytics.profile_updates += 1
        elif action_type == 'style_quiz':
            analytics.style_quiz_taken = True
        
        # Update session duration if provided
        if data.get('session_duration'):
            analytics.session_duration += data['session_duration']
        
        # Update peak usage hour
        current_hour = datetime.now().hour
        analytics.peak_usage_hour = current_hour
        analytics.weekend_usage = datetime.now().weekday() >= 5
        
        # Track feature usage
        AnalyticsHelper.track_feature_usage(user.id, action_type)
        
        analytics.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Action tracked successfully',
            'tagline': 'We girls have no time - action logged instantly!',
            'analytics': analytics.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to track action',
            'message': str(e)
        }), 500

