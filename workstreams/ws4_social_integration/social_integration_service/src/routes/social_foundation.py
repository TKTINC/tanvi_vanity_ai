"""
WS4-P1: Social Foundation & User Connections Routes
Tanvi Vanity Agent - Social Integration API
"We girls have no time" - Instant social connections and style sharing!
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json
import requests
from src.models.social_models import (
    db, SocialProfile, SocialConnection, StyleInfluencer, 
    SocialNotification, SocialActivity
)

social_foundation_bp = Blueprint('social_foundation', __name__)

# WS1 User Management Service URL (for integration)
WS1_SERVICE_URL = "http://localhost:5001"

def verify_user_token(token):
    """Verify user token with WS1 User Management service"""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f"{WS1_SERVICE_URL}/api/auth/verify", headers=headers, timeout=3)
        if response.status_code == 200:
            return response.json().get('user_id')
    except:
        pass
    return None

def get_user_from_token():
    """Extract user ID from authorization header"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    return verify_user_token(token)

@social_foundation_bp.route('/health', methods=['GET'])
def social_health():
    """
    Social foundation health check
    "We girls have no time" - instant social system status!
    """
    return jsonify({
        'status': 'healthy',
        'service': 'WS4 Social Integration',
        'version': '1.0.0',
        'phase': 'WS4-P1: Social Foundation & User Connections',
        'tagline': 'We girls have no time - instant social connections!',
        'features': {
            'social_profiles': 'active',
            'user_connections': 'active', 
            'style_influencers': 'active',
            'notifications': 'active',
            'activity_tracking': 'active'
        },
        'integration_status': {
            'ws1_user_management': 'ready',
            'ws2_ai_styling': 'ready',
            'ws3_computer_vision': 'ready'
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@social_foundation_bp.route('/profile', methods=['GET'])
def get_social_profile():
    """
    Get user's social profile
    "We girls have no time" - instant profile access!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    profile = SocialProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({'error': 'Social profile not found'}), 404
    
    # Update last active
    profile.update_activity()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='view',
        target_type='profile',
        target_id=user_id,
        source_location='profile_page'
    )
    
    return jsonify({
        'success': True,
        'profile': profile.to_dict(),
        'message': 'We girls have no time - profile loaded instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@social_foundation_bp.route('/profile', methods=['POST'])
def create_social_profile():
    """
    Create social profile for user
    "We girls have no time" - instant profile setup!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    
    # Check if profile already exists
    existing_profile = SocialProfile.query.filter_by(user_id=user_id).first()
    if existing_profile:
        return jsonify({'error': 'Social profile already exists'}), 400
    
    # Create new social profile
    profile = SocialProfile(
        user_id=user_id,
        display_name=data.get('display_name', f'StyleUser{user_id[:8]}'),
        bio=data.get('bio', 'We girls have no time - but we always have style!'),
        profile_image_url=data.get('profile_image_url'),
        is_public=data.get('is_public', True),
        allow_followers=data.get('allow_followers', True),
        allow_style_sharing=data.get('allow_style_sharing', True),
        allow_outfit_copying=data.get('allow_outfit_copying', True),
        style_tags=json.dumps(data.get('style_tags', [])),
        favorite_brands=json.dumps(data.get('favorite_brands', [])),
        size_info=json.dumps(data.get('size_info', {}))
    )
    
    db.session.add(profile)
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='create',
        target_type='profile',
        target_id=user_id,
        activity_data={'setup_time': 'instant'},
        source_location='profile_setup'
    )
    
    # Create welcome notification
    SocialNotification.create_notification(
        user_id=user_id,
        notification_type='welcome',
        title='Welcome to Tanvi Style Community!',
        message='We girls have no time - but we always make time for style! Your profile is ready.',
        priority='high'
    )
    
    return jsonify({
        'success': True,
        'profile': profile.to_dict(),
        'message': 'We girls have no time - profile created instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@social_foundation_bp.route('/profile', methods=['PUT'])
def update_social_profile():
    """
    Update social profile
    "We girls have no time" - instant profile updates!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    profile = SocialProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({'error': 'Social profile not found'}), 404
    
    data = request.get_json()
    
    # Update profile fields
    if 'display_name' in data:
        profile.display_name = data['display_name']
    if 'bio' in data:
        profile.bio = data['bio']
    if 'profile_image_url' in data:
        profile.profile_image_url = data['profile_image_url']
    if 'is_public' in data:
        profile.is_public = data['is_public']
    if 'allow_followers' in data:
        profile.allow_followers = data['allow_followers']
    if 'allow_style_sharing' in data:
        profile.allow_style_sharing = data['allow_style_sharing']
    if 'allow_outfit_copying' in data:
        profile.allow_outfit_copying = data['allow_outfit_copying']
    if 'style_tags' in data:
        profile.style_tags = json.dumps(data['style_tags'])
    if 'favorite_brands' in data:
        profile.favorite_brands = json.dumps(data['favorite_brands'])
    if 'size_info' in data:
        profile.size_info = json.dumps(data['size_info'])
    
    profile.updated_at = datetime.utcnow()
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='update',
        target_type='profile',
        target_id=user_id,
        activity_data={'updated_fields': list(data.keys())},
        source_location='profile_settings'
    )
    
    return jsonify({
        'success': True,
        'profile': profile.to_dict(),
        'message': 'We girls have no time - profile updated instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@social_foundation_bp.route('/follow', methods=['POST'])
def follow_user():
    """
    Follow another user
    "We girls have no time" - instant style connections!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    following_id = data.get('user_id')
    
    if not following_id:
        return jsonify({'error': 'User ID required'}), 400
    
    if user_id == following_id:
        return jsonify({'error': 'Cannot follow yourself'}), 400
    
    # Check if already following
    existing_connection = SocialConnection.query.filter_by(
        follower_id=user_id, 
        following_id=following_id
    ).first()
    
    if existing_connection:
        return jsonify({'error': 'Already following this user'}), 400
    
    # Check if target user exists and allows followers
    target_profile = SocialProfile.query.filter_by(user_id=following_id).first()
    if not target_profile:
        return jsonify({'error': 'User not found'}), 404
    
    if not target_profile.allow_followers:
        return jsonify({'error': 'User does not allow followers'}), 403
    
    # Create connection
    connection = SocialConnection(
        follower_id=user_id,
        following_id=following_id,
        connection_type='follow',
        status='active'
    )
    
    # Calculate style compatibility (placeholder - would integrate with WS2)
    connection.style_compatibility_score = 0.75  # Mock score
    connection.shared_style_tags = json.dumps(['casual', 'trendy'])  # Mock shared tags
    
    db.session.add(connection)
    
    # Update follower counts
    follower_profile = SocialProfile.query.filter_by(user_id=user_id).first()
    if follower_profile:
        follower_profile.following_count += 1
    
    target_profile.followers_count += 1
    
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='follow',
        target_type='user',
        target_id=following_id,
        activity_data={'style_compatibility': connection.style_compatibility_score},
        source_location='user_profile'
    )
    
    # Create notification for followed user
    SocialNotification.create_notification(
        user_id=following_id,
        sender_id=user_id,
        notification_type='follow',
        title='New Follower!',
        message=f'{follower_profile.display_name if follower_profile else "Someone"} started following you!',
        action_url=f'/profile/{user_id}',
        related_content_id=user_id,
        related_content_type='user'
    )
    
    return jsonify({
        'success': True,
        'connection': connection.to_dict(),
        'message': 'We girls have no time - instant style connection made!',
        'timestamp': datetime.utcnow().isoformat()
    })

@social_foundation_bp.route('/unfollow', methods=['POST'])
def unfollow_user():
    """
    Unfollow a user
    "We girls have no time" - instant connection management!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    following_id = data.get('user_id')
    
    if not following_id:
        return jsonify({'error': 'User ID required'}), 400
    
    # Find existing connection
    connection = SocialConnection.query.filter_by(
        follower_id=user_id, 
        following_id=following_id
    ).first()
    
    if not connection:
        return jsonify({'error': 'Not following this user'}), 400
    
    # Remove connection
    db.session.delete(connection)
    
    # Update follower counts
    follower_profile = SocialProfile.query.filter_by(user_id=user_id).first()
    target_profile = SocialProfile.query.filter_by(user_id=following_id).first()
    
    if follower_profile:
        follower_profile.following_count = max(0, follower_profile.following_count - 1)
    
    if target_profile:
        target_profile.followers_count = max(0, target_profile.followers_count - 1)
    
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='unfollow',
        target_type='user',
        target_id=following_id,
        source_location='user_profile'
    )
    
    return jsonify({
        'success': True,
        'message': 'We girls have no time - connection removed instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@social_foundation_bp.route('/followers', methods=['GET'])
def get_followers():
    """
    Get user's followers
    "We girls have no time" - instant follower overview!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    
    # Get followers
    followers_query = db.session.query(SocialConnection, SocialProfile).join(
        SocialProfile, SocialConnection.follower_id == SocialProfile.user_id
    ).filter(SocialConnection.following_id == user_id)
    
    followers = followers_query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    followers_data = []
    for connection, profile in followers.items:
        follower_data = profile.to_dict()
        follower_data['connection_info'] = {
            'style_compatibility_score': connection.style_compatibility_score,
            'shared_style_tags': json.loads(connection.shared_style_tags) if connection.shared_style_tags else [],
            'connected_since': connection.created_at.isoformat(),
            'interaction_count': connection.interaction_count
        }
        followers_data.append(follower_data)
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='view',
        target_type='followers',
        target_id=user_id,
        source_location='followers_page'
    )
    
    return jsonify({
        'success': True,
        'followers': followers_data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': followers.total,
            'pages': followers.pages,
            'has_next': followers.has_next,
            'has_prev': followers.has_prev
        },
        'message': 'We girls have no time - followers loaded instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@social_foundation_bp.route('/following', methods=['GET'])
def get_following():
    """
    Get users that current user is following
    "We girls have no time" - instant following overview!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    
    # Get following
    following_query = db.session.query(SocialConnection, SocialProfile).join(
        SocialProfile, SocialConnection.following_id == SocialProfile.user_id
    ).filter(SocialConnection.follower_id == user_id)
    
    following = following_query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    following_data = []
    for connection, profile in following.items:
        following_user_data = profile.to_dict()
        following_user_data['connection_info'] = {
            'style_compatibility_score': connection.style_compatibility_score,
            'shared_style_tags': json.loads(connection.shared_style_tags) if connection.shared_style_tags else [],
            'connected_since': connection.created_at.isoformat(),
            'interaction_count': connection.interaction_count
        }
        following_data.append(following_user_data)
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='view',
        target_type='following',
        target_id=user_id,
        source_location='following_page'
    )
    
    return jsonify({
        'success': True,
        'following': following_data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': following.total,
            'pages': following.pages,
            'has_next': following.has_next,
            'has_prev': following.has_prev
        },
        'message': 'We girls have no time - following list loaded instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@social_foundation_bp.route('/notifications', methods=['GET'])
def get_notifications():
    """
    Get user's notifications
    "We girls have no time" - instant notification updates!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    
    # Build query
    query = SocialNotification.query.filter_by(user_id=user_id)
    
    if unread_only:
        query = query.filter_by(is_read=False)
    
    # Filter out expired notifications
    query = query.filter(
        db.or_(
            SocialNotification.expires_at.is_(None),
            SocialNotification.expires_at > datetime.utcnow()
        )
    )
    
    notifications = query.order_by(SocialNotification.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    notifications_data = [notification.to_dict() for notification in notifications.items]
    
    # Count unread notifications
    unread_count = SocialNotification.query.filter_by(
        user_id=user_id, 
        is_read=False
    ).filter(
        db.or_(
            SocialNotification.expires_at.is_(None),
            SocialNotification.expires_at > datetime.utcnow()
        )
    ).count()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='view',
        target_type='notifications',
        target_id=user_id,
        activity_data={'unread_count': unread_count},
        source_location='notifications_page'
    )
    
    return jsonify({
        'success': True,
        'notifications': notifications_data,
        'unread_count': unread_count,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': notifications.total,
            'pages': notifications.pages,
            'has_next': notifications.has_next,
            'has_prev': notifications.has_prev
        },
        'message': 'We girls have no time - notifications loaded instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@social_foundation_bp.route('/notifications/<int:notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    """
    Mark notification as read
    "We girls have no time" - instant notification management!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    notification = SocialNotification.query.filter_by(
        id=notification_id, 
        user_id=user_id
    ).first()
    
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    
    notification.mark_as_read()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='read',
        target_type='notification',
        target_id=str(notification_id),
        source_location='notifications_page'
    )
    
    return jsonify({
        'success': True,
        'notification': notification.to_dict(),
        'message': 'We girls have no time - notification marked as read!',
        'timestamp': datetime.utcnow().isoformat()
    })

@social_foundation_bp.route('/influencers', methods=['GET'])
def get_style_influencers():
    """
    Get style influencers
    "We girls have no time" - instant style inspiration!
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    influencer_type = request.args.get('type')
    expertise_level = request.args.get('expertise')
    
    # Build query
    query = StyleInfluencer.query.filter_by(verification_status='verified')
    
    if influencer_type:
        query = query.filter_by(influencer_type=influencer_type)
    
    if expertise_level:
        query = query.filter_by(expertise_level=expertise_level)
    
    # Order by influence score (calculated)
    influencers = query.order_by(StyleInfluencer.style_impact_score.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    influencers_data = []
    for influencer in influencers.items:
        influencer_data = influencer.to_dict()
        influencer_data['influence_score'] = influencer.calculate_influence_score()
        influencers_data.append(influencer_data)
    
    # Log activity if user is authenticated
    user_id = get_user_from_token()
    if user_id:
        SocialActivity.log_activity(
            user_id=user_id,
            activity_type='view',
            target_type='influencers',
            target_id='list',
            activity_data={'filters': {'type': influencer_type, 'expertise': expertise_level}},
            source_location='influencers_page'
        )
    
    return jsonify({
        'success': True,
        'influencers': influencers_data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': influencers.total,
            'pages': influencers.pages,
            'has_next': influencers.has_next,
            'has_prev': influencers.has_prev
        },
        'message': 'We girls have no time - style influencers loaded instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

