from flask import Blueprint, jsonify, request
from src.models.user import User, UserPreference, UserSession, db
from datetime import datetime
import json

user_bp = Blueprint('user', __name__)

def get_current_user():
    """Helper function to get current authenticated user"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    return User.verify_auth_token(token)

@user_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    Get current user profile - "We girls have no time" for complex profile views
    Quick access to essential profile information
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    profile_data = user.to_dict(include_sensitive=True)
    
    # Include preferences if they exist
    if user.preferences:
        profile_data['preferences'] = user.preferences.to_dict()
    
    return jsonify({
        'message': 'Profile retrieved successfully',
        'tagline': 'We girls have no time - here\'s your quick profile!',
        'profile': profile_data
    }), 200


@user_bp.route('/profile', methods=['PUT'])
def update_profile():
    """
    Update user profile - quick and efficient updates
    "We girls have no time" for lengthy profile editing
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        data = request.json
        
        # Update basic profile information
        if data.get('first_name'):
            user.first_name = data['first_name']
        
        if data.get('last_name'):
            user.last_name = data['last_name']
        
        if data.get('age_range'):
            user.age_range = data['age_range']
        
        if data.get('style_preference'):
            user.style_preference = data['style_preference']
        
        if data.get('color_preferences'):
            user.color_preferences = json.dumps(data['color_preferences'])
        
        if data.get('size_info'):
            user.size_info = json.dumps(data['size_info'])
        
        # Update privacy settings
        if data.get('privacy_level'):
            user.privacy_level = data['privacy_level']
        
        if 'allow_social_sharing' in data:
            user.allow_social_sharing = data['allow_social_sharing']
        
        if 'marketing_consent' in data:
            user.marketing_consent = data['marketing_consent']
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'tagline': 'We girls have no time - profile updated in seconds!',
            'profile': user.to_dict(include_sensitive=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Profile update failed',
            'message': str(e)
        }), 500


@user_bp.route('/preferences', methods=['GET'])
def get_preferences():
    """
    Get user styling preferences - quick access for AI recommendations
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    preferences = user.preferences
    if not preferences:
        # Create default preferences if none exist
        preferences = UserPreference(
            user_id=user.id,
            occasion_preferences=json.dumps(['casual', 'work']),
            weather_sensitivity='medium',
            comfort_priority=7,
            trend_following=5,
            budget_range='medium',
            conversation_style='friendly',
            notification_frequency='daily'
        )
        db.session.add(preferences)
        db.session.commit()
    
    return jsonify({
        'message': 'Preferences retrieved successfully',
        'tagline': 'We girls have no time - here are your quick styling preferences!',
        'preferences': preferences.to_dict()
    }), 200


@user_bp.route('/preferences', methods=['PUT'])
def update_preferences():
    """
    Update styling preferences - quick customization for better AI recommendations
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        data = request.json
        
        preferences = user.preferences
        if not preferences:
            preferences = UserPreference(user_id=user.id)
            db.session.add(preferences)
        
        # Update preferences with provided data
        if data.get('occasion_preferences'):
            preferences.occasion_preferences = json.dumps(data['occasion_preferences'])
        
        if data.get('weather_sensitivity'):
            preferences.weather_sensitivity = data['weather_sensitivity']
        
        if data.get('comfort_priority'):
            preferences.comfort_priority = data['comfort_priority']
        
        if data.get('trend_following'):
            preferences.trend_following = data['trend_following']
        
        if data.get('budget_range'):
            preferences.budget_range = data['budget_range']
        
        if data.get('preferred_brands'):
            preferences.preferred_brands = json.dumps(data['preferred_brands'])
        
        if data.get('shopping_frequency'):
            preferences.shopping_frequency = data['shopping_frequency']
        
        if data.get('conversation_style'):
            preferences.conversation_style = data['conversation_style']
        
        if data.get('notification_frequency'):
            preferences.notification_frequency = data['notification_frequency']
        
        preferences.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Preferences updated successfully',
            'tagline': 'We girls have no time - preferences updated for better styling!',
            'preferences': preferences.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Preferences update failed',
            'message': str(e)
        }), 500


@user_bp.route('/sessions', methods=['GET'])
def get_sessions():
    """
    Get active user sessions - quick security overview
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    active_sessions = UserSession.query.filter_by(
        user_id=user.id,
        is_active=True
    ).filter(
        UserSession.expires_at > datetime.utcnow()
    ).all()
    
    return jsonify({
        'message': 'Active sessions retrieved',
        'tagline': 'We girls have no time - quick security check!',
        'sessions': [session.to_dict() for session in active_sessions]
    }), 200


@user_bp.route('/sessions/<session_id>', methods=['DELETE'])
def terminate_session(session_id):
    """
    Terminate a specific session - quick security action
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        session = UserSession.query.filter_by(
            user_id=user.id,
            session_token=session_id,
            is_active=True
        ).first()
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        session.is_active = False
        db.session.commit()
        
        return jsonify({
            'message': 'Session terminated successfully',
            'tagline': 'We girls have no time - session ended quickly!'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Session termination failed',
            'message': str(e)
        }), 500


@user_bp.route('/quick-stats', methods=['GET'])
def get_quick_stats():
    """
    Get quick user statistics - "We girls have no time" for detailed analytics
    Essential stats at a glance
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Calculate quick stats
    days_since_signup = (datetime.utcnow() - user.created_at).days if user.created_at else 0
    active_sessions_count = UserSession.query.filter_by(
        user_id=user.id,
        is_active=True
    ).filter(
        UserSession.expires_at > datetime.utcnow()
    ).count()
    
    stats = {
        'days_since_signup': days_since_signup,
        'profile_completion': calculate_profile_completion(user),
        'active_sessions': active_sessions_count,
        'last_login': user.last_login.isoformat() if user.last_login else None,
        'account_status': 'active' if user.is_active else 'inactive',
        'verification_status': 'verified' if user.is_verified else 'pending'
    }
    
    return jsonify({
        'message': 'Quick stats retrieved',
        'tagline': 'We girls have no time - here\'s your account at a glance!',
        'stats': stats
    }), 200


def calculate_profile_completion(user):
    """Calculate profile completion percentage for quick overview"""
    total_fields = 10
    completed_fields = 0
    
    if user.first_name:
        completed_fields += 1
    if user.last_name:
        completed_fields += 1
    if user.age_range:
        completed_fields += 1
    if user.style_preference:
        completed_fields += 1
    if user.color_preferences:
        completed_fields += 1
    if user.size_info:
        completed_fields += 1
    if user.preferences:
        completed_fields += 4  # Preferences count as 4 fields
    
    return int((completed_fields / total_fields) * 100)


@user_bp.route('/deactivate', methods=['POST'])
def deactivate_account():
    """
    Deactivate user account - quick account management
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        data = request.json
        password = data.get('password')
        
        if not password or not user.check_password(password):
            return jsonify({
                'error': 'Password confirmation required',
                'message': 'Please confirm your password to deactivate'
            }), 400
        
        # Deactivate user account
        user.is_active = False
        user.updated_at = datetime.utcnow()
        
        # Deactivate all sessions
        UserSession.query.filter_by(user_id=user.id).update({'is_active': False})
        
        db.session.commit()
        
        return jsonify({
            'message': 'Account deactivated successfully',
            'tagline': 'We girls have no time - account deactivated quickly. We\'ll miss you!'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Account deactivation failed',
            'message': str(e)
        }), 500


# Legacy endpoints for backward compatibility
@user_bp.route('/users', methods=['GET'])
def get_users():
    """Legacy endpoint - returns public user profiles"""
    users = User.query.filter_by(is_active=True).all()
    return jsonify({
        'message': 'Public users retrieved',
        'users': [user.to_public_dict() for user in users]
    })


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Legacy endpoint - returns public user profile"""
    user = User.query.get_or_404(user_id)
    if not user.is_active:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'message': 'User profile retrieved',
        'user': user.to_public_dict()
    })

