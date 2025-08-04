"""
WS4-P3: Community Features & Engagement Routes
Tanvi Vanity Agent - Social Integration API
"We girls have no time" - Instant community engagement and style discovery!
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json
import requests
from src.models.community_features import (
    db, StyleCommunity, CommunityMembership, StyleEvent, EventRSVP,
    StyleMentor, MentorshipRelationship, StyleTip
)
from src.models.social_models import SocialActivity, SocialNotification

community_features_bp = Blueprint('community_features', __name__)

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

@community_features_bp.route('/health', methods=['GET'])
def community_features_health():
    """
    Community features health check
    "We girls have no time" - instant community system status!
    """
    return jsonify({
        'status': 'healthy',
        'service': 'WS4 Social Integration - Community Features',
        'version': '3.0.0',
        'phase': 'WS4-P3: Community Features & Engagement',
        'tagline': 'We girls have no time - instant community engagement!',
        'features': {
            'style_communities': 'active',
            'community_events': 'active',
            'style_mentoring': 'active',
            'style_tips': 'active',
            'community_management': 'active'
        },
        'integration_status': {
            'ws1_user_management': 'ready',
            'ws2_ai_styling': 'ready',
            'ws3_computer_vision': 'ready',
            'content_sharing': 'ready'
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@community_features_bp.route('/communities', methods=['GET'])
def get_communities():
    """
    Get style communities
    "We girls have no time" - instant community discovery!
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    community_type = request.args.get('type')
    search = request.args.get('search')
    
    # Build query
    query = StyleCommunity.query.filter_by(is_public=True)
    
    if community_type:
        query = query.filter_by(community_type=community_type)
    
    if search:
        query = query.filter(
            StyleCommunity.name.contains(search) |
            StyleCommunity.description.contains(search)
        )
    
    # Order by engagement and member count
    communities = query.order_by(
        StyleCommunity.engagement_score.desc(),
        StyleCommunity.members_count.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    communities_data = [community.to_dict() for community in communities.items]
    
    # Log activity if user is authenticated
    user_id = get_user_from_token()
    if user_id:
        SocialActivity.log_activity(
            user_id=user_id,
            activity_type='view',
            target_type='communities',
            target_id='list',
            activity_data={'communities_viewed': len(communities_data)},
            source_location='communities_page'
        )
    
    return jsonify({
        'success': True,
        'communities': communities_data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': communities.total,
            'pages': communities.pages,
            'has_next': communities.has_next,
            'has_prev': communities.has_prev
        },
        'message': 'We girls have no time - communities discovered instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@community_features_bp.route('/communities', methods=['POST'])
def create_community():
    """
    Create a new style community
    "We girls have no time" - instant community creation!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    
    # Create style community
    community = StyleCommunity(
        creator_id=user_id,
        name=data.get('name', ''),
        description=data.get('description', ''),
        community_type=data.get('community_type', 'style'),
        cover_image_url=data.get('cover_image_url'),
        banner_image_url=data.get('banner_image_url'),
        tags=json.dumps(data.get('tags', [])),
        style_focus=json.dumps(data.get('style_focus', [])),
        is_public=data.get('is_public', True),
        requires_approval=data.get('requires_approval', False),
        allow_posts=data.get('allow_posts', True),
        allow_challenges=data.get('allow_challenges', True),
        rules=json.dumps(data.get('rules', [])),
        guidelines=data.get('guidelines', '')
    )
    
    db.session.add(community)
    db.session.commit()
    
    # Auto-join creator as admin
    membership = CommunityMembership(
        community_id=community.id,
        user_id=user_id,
        role='creator',
        status='active',
        join_reason='Community creator'
    )
    
    db.session.add(membership)
    community.add_member()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='create',
        target_type='community',
        target_id=str(community.id),
        activity_data={
            'community_type': community.community_type,
            'is_public': community.is_public
        },
        source_location='community_creation'
    )
    
    return jsonify({
        'success': True,
        'community': community.to_dict(),
        'message': 'We girls have no time - community created instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@community_features_bp.route('/communities/<int:community_id>/join', methods=['POST'])
def join_community(community_id):
    """
    Join a style community
    "We girls have no time" - instant community joining!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    community = StyleCommunity.query.get_or_404(community_id)
    
    # Check if already a member
    existing_membership = CommunityMembership.query.filter_by(
        community_id=community_id,
        user_id=user_id
    ).first()
    
    if existing_membership:
        return jsonify({'error': 'Already a member of this community'}), 400
    
    data = request.get_json() or {}
    
    # Create membership
    membership = CommunityMembership(
        community_id=community_id,
        user_id=user_id,
        role='member',
        status='pending' if community.requires_approval else 'active',
        join_reason=data.get('join_reason'),
        introduction=data.get('introduction')
    )
    
    db.session.add(membership)
    
    if not community.requires_approval:
        community.add_member()
    
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='join',
        target_type='community',
        target_id=str(community_id),
        activity_data={
            'requires_approval': community.requires_approval,
            'status': membership.status
        },
        source_location='community_detail'
    )
    
    # Create notification for community creator
    SocialNotification.create_notification(
        user_id=community.creator_id,
        sender_id=user_id,
        notification_type='community_join',
        title='New member joined your community!',
        message=f'Someone joined "{community.name}"!',
        action_url=f'/communities/{community_id}',
        related_content_id=str(community_id),
        related_content_type='community'
    )
    
    return jsonify({
        'success': True,
        'membership': membership.to_dict(),
        'message': 'We girls have no time - joined community instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@community_features_bp.route('/events', methods=['GET'])
def get_events():
    """
    Get style events
    "We girls have no time" - instant event discovery!
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    event_type = request.args.get('type')
    community_id = request.args.get('community_id', type=int)
    upcoming_only = request.args.get('upcoming_only', 'true').lower() == 'true'
    
    # Build query
    query = StyleEvent.query.filter_by(is_public=True)
    
    if event_type:
        query = query.filter_by(event_type=event_type)
    
    if community_id:
        query = query.filter_by(community_id=community_id)
    
    if upcoming_only:
        query = query.filter(StyleEvent.start_time > datetime.utcnow())
    
    # Order by start time
    events = query.order_by(StyleEvent.start_time.asc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    events_data = [event.to_dict() for event in events.items]
    
    # Log activity if user is authenticated
    user_id = get_user_from_token()
    if user_id:
        SocialActivity.log_activity(
            user_id=user_id,
            activity_type='view',
            target_type='events',
            target_id='list',
            activity_data={'events_viewed': len(events_data)},
            source_location='events_page'
        )
    
    return jsonify({
        'success': True,
        'events': events_data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': events.total,
            'pages': events.pages,
            'has_next': events.has_next,
            'has_prev': events.has_prev
        },
        'message': 'We girls have no time - events discovered instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@community_features_bp.route('/events', methods=['POST'])
def create_event():
    """
    Create a new style event
    "We girls have no time" - instant event creation!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    
    # Parse start time
    start_time = datetime.fromisoformat(data['start_time'])
    end_time = datetime.fromisoformat(data['end_time']) if data.get('end_time') else None
    
    # Create style event
    event = StyleEvent(
        creator_id=user_id,
        community_id=data.get('community_id'),
        title=data.get('title', ''),
        description=data.get('description', ''),
        event_type=data.get('event_type', 'virtual'),
        cover_image_url=data.get('cover_image_url'),
        tags=json.dumps(data.get('tags', [])),
        dress_code=data.get('dress_code'),
        style_theme=data.get('style_theme'),
        start_time=start_time,
        end_time=end_time,
        timezone=data.get('timezone', 'UTC'),
        duration_minutes=data.get('duration_minutes'),
        location_name=data.get('location_name'),
        location_address=data.get('location_address'),
        location_coordinates=data.get('location_coordinates'),
        meeting_url=data.get('meeting_url'),
        meeting_platform=data.get('meeting_platform'),
        meeting_id=data.get('meeting_id'),
        meeting_password=data.get('meeting_password'),
        is_public=data.get('is_public', True),
        requires_rsvp=data.get('requires_rsvp', True),
        max_attendees=data.get('max_attendees'),
        allow_guests=data.get('allow_guests', False)
    )
    
    db.session.add(event)
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='create',
        target_type='event',
        target_id=str(event.id),
        activity_data={
            'event_type': event.event_type,
            'start_time': event.start_time.isoformat()
        },
        source_location='event_creation'
    )
    
    return jsonify({
        'success': True,
        'event': event.to_dict(),
        'message': 'We girls have no time - event created instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@community_features_bp.route('/events/<int:event_id>/rsvp', methods=['POST'])
def rsvp_event(event_id):
    """
    RSVP to a style event
    "We girls have no time" - instant event responses!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    event = StyleEvent.query.get_or_404(event_id)
    
    # Check if already RSVP'd
    existing_rsvp = EventRSVP.query.filter_by(
        event_id=event_id,
        user_id=user_id
    ).first()
    
    data = request.get_json()
    response = data.get('response', 'yes')
    
    if existing_rsvp:
        # Update existing RSVP
        existing_rsvp.response = response
        existing_rsvp.guest_count = data.get('guest_count', 0)
        existing_rsvp.notes = data.get('notes')
        existing_rsvp.planned_outfit_id = data.get('planned_outfit_id')
        existing_rsvp.outfit_notes = data.get('outfit_notes')
        existing_rsvp.updated_at = datetime.utcnow()
        
        rsvp = existing_rsvp
    else:
        # Create new RSVP
        rsvp = EventRSVP(
            event_id=event_id,
            user_id=user_id,
            response=response,
            guest_count=data.get('guest_count', 0),
            notes=data.get('notes'),
            planned_outfit_id=data.get('planned_outfit_id'),
            outfit_notes=data.get('outfit_notes')
        )
        
        db.session.add(rsvp)
        
        # Update event stats
        if response == 'yes':
            event.rsvp_yes_count += 1
            event.attendees_count += 1 + rsvp.guest_count
        elif response == 'maybe':
            event.rsvp_maybe_count += 1
        elif response == 'interested':
            event.interested_count += 1
    
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='rsvp',
        target_type='event',
        target_id=str(event_id),
        activity_data={
            'response': response,
            'guest_count': rsvp.guest_count
        },
        source_location='event_detail'
    )
    
    return jsonify({
        'success': True,
        'rsvp': rsvp.to_dict(),
        'message': 'We girls have no time - RSVP sent instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@community_features_bp.route('/mentors', methods=['GET'])
def get_mentors():
    """
    Get style mentors
    "We girls have no time" - instant mentor discovery!
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    specialty = request.args.get('specialty')
    accepting_only = request.args.get('accepting_only', 'true').lower() == 'true'
    
    # Build query
    query = StyleMentor.query.filter_by(status='active')
    
    if accepting_only:
        query = query.filter_by(is_accepting_mentees=True)
    
    if specialty:
        query = query.filter(StyleMentor.specialties.contains(specialty))
    
    # Order by rating and verification
    mentors = query.order_by(
        StyleMentor.is_verified.desc(),
        StyleMentor.average_rating.desc(),
        StyleMentor.reviews_count.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    mentors_data = [mentor.to_dict() for mentor in mentors.items]
    
    # Log activity if user is authenticated
    user_id = get_user_from_token()
    if user_id:
        SocialActivity.log_activity(
            user_id=user_id,
            activity_type='view',
            target_type='mentors',
            target_id='list',
            activity_data={'mentors_viewed': len(mentors_data)},
            source_location='mentors_page'
        )
    
    return jsonify({
        'success': True,
        'mentors': mentors_data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': mentors.total,
            'pages': mentors.pages,
            'has_next': mentors.has_next,
            'has_prev': mentors.has_prev
        },
        'message': 'We girls have no time - mentors discovered instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@community_features_bp.route('/mentors/<int:mentor_id>/request', methods=['POST'])
def request_mentorship(mentor_id):
    """
    Request mentorship from a style mentor
    "We girls have no time" - instant mentoring connections!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    mentor = StyleMentor.query.get_or_404(mentor_id)
    
    if not mentor.is_accepting_mentees:
        return jsonify({'error': 'Mentor not accepting new mentees'}), 400
    
    if mentor.current_mentees_count >= mentor.max_mentees:
        return jsonify({'error': 'Mentor has reached maximum mentees'}), 400
    
    # Check if already has active mentorship
    existing_relationship = MentorshipRelationship.query.filter_by(
        mentor_id=mentor_id,
        mentee_user_id=user_id,
        status='active'
    ).first()
    
    if existing_relationship:
        return jsonify({'error': 'Already have active mentorship with this mentor'}), 400
    
    data = request.get_json()
    
    # Create mentorship relationship
    relationship = MentorshipRelationship(
        mentor_id=mentor_id,
        mentee_user_id=user_id,
        status='pending',
        mentorship_type=data.get('mentorship_type', 'general'),
        goals=json.dumps(data.get('goals', [])),
        focus_areas=json.dumps(data.get('focus_areas', [])),
        timeline_weeks=data.get('timeline_weeks', 4),
        sessions_planned=data.get('sessions_planned', 4)
    )
    
    db.session.add(relationship)
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='request',
        target_type='mentorship',
        target_id=str(relationship.id),
        activity_data={
            'mentor_id': mentor_id,
            'mentorship_type': relationship.mentorship_type
        },
        source_location='mentor_profile'
    )
    
    # Create notification for mentor
    SocialNotification.create_notification(
        user_id=mentor.mentor_user_id,
        sender_id=user_id,
        notification_type='mentorship_request',
        title='New mentorship request!',
        message=f'Someone requested mentorship from you!',
        action_url=f'/mentorships/{relationship.id}',
        related_content_id=str(relationship.id),
        related_content_type='mentorship'
    )
    
    return jsonify({
        'success': True,
        'relationship': relationship.to_dict(),
        'message': 'We girls have no time - mentorship requested instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@community_features_bp.route('/tips', methods=['GET'])
def get_style_tips():
    """
    Get daily style tips
    "We girls have no time" - instant style wisdom!
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    tip_type = request.args.get('type')
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    
    # Build query
    query = StyleTip.query.filter_by(status='published')
    
    if tip_type:
        query = query.filter_by(tip_type=tip_type)
    
    if category:
        query = query.filter_by(category=category)
    
    if difficulty:
        query = query.filter_by(difficulty_level=difficulty)
    
    # Order by featured, likes, and recency
    tips = query.order_by(
        StyleTip.is_featured.desc(),
        StyleTip.likes_count.desc(),
        StyleTip.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    tips_data = [tip.to_dict() for tip in tips.items]
    
    # Log activity if user is authenticated
    user_id = get_user_from_token()
    if user_id:
        SocialActivity.log_activity(
            user_id=user_id,
            activity_type='view',
            target_type='tips',
            target_id='list',
            activity_data={'tips_viewed': len(tips_data)},
            source_location='tips_page'
        )
    
    return jsonify({
        'success': True,
        'tips': tips_data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': tips.total,
            'pages': tips.pages,
            'has_next': tips.has_next,
            'has_prev': tips.has_prev
        },
        'message': 'We girls have no time - style wisdom delivered instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@community_features_bp.route('/tips', methods=['POST'])
def create_style_tip():
    """
    Create a new style tip
    "We girls have no time" - instant wisdom sharing!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    
    # Create style tip
    tip = StyleTip(
        creator_id=user_id,
        title=data.get('title', ''),
        content=data.get('content', ''),
        tip_type=data.get('tip_type', 'general'),
        difficulty_level=data.get('difficulty_level', 'easy'),
        time_to_implement=data.get('time_to_implement'),
        category=data.get('category'),
        image_url=data.get('image_url'),
        video_url=data.get('video_url'),
        target_audience=json.dumps(data.get('target_audience', [])),
        style_types=json.dumps(data.get('style_types', [])),
        occasions=json.dumps(data.get('occasions', []))
    )
    
    db.session.add(tip)
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='create',
        target_type='tip',
        target_id=str(tip.id),
        activity_data={
            'tip_type': tip.tip_type,
            'category': tip.category
        },
        source_location='tip_creation'
    )
    
    return jsonify({
        'success': True,
        'tip': tip.to_dict(),
        'message': 'We girls have no time - style wisdom shared instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

