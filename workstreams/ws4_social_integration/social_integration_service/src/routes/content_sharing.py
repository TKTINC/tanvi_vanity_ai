"""
WS4-P2: Content Sharing & Style Posts Routes
Tanvi Vanity Agent - Social Integration API
"We girls have no time" - Instant style content creation and sharing!
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json
import requests
from src.models.content_sharing import (
    db, StylePost, PostComment, PostLike, PostShare, PostSave, 
    StyleChallenge, ContentCollection, CollectionItem
)
from src.models.social_models import SocialActivity, SocialNotification

content_sharing_bp = Blueprint('content_sharing', __name__)

# WS1 User Management Service URL (for integration)
WS1_SERVICE_URL = "http://localhost:5001"
# WS2 AI Styling Service URL (for integration)
WS2_SERVICE_URL = "http://localhost:5000"
# WS3 Computer Vision Service URL (for integration)
WS3_SERVICE_URL = "http://localhost:5000"

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

def analyze_post_with_ai(post_data):
    """Analyze post content with WS2 AI service"""
    try:
        # Mock AI analysis - would integrate with WS2
        return {
            'style_score': 0.85,
            'trend_relevance': 0.78,
            'color_harmony': 0.92,
            'occasion_fit': 0.88
        }
    except:
        return {
            'style_score': 0.0,
            'trend_relevance': 0.0,
            'color_harmony': 0.0,
            'occasion_fit': 0.0
        }

@content_sharing_bp.route('/health', methods=['GET'])
def content_sharing_health():
    """
    Content sharing health check
    "We girls have no time" - instant content system status!
    """
    return jsonify({
        'status': 'healthy',
        'service': 'WS4 Social Integration - Content Sharing',
        'version': '2.0.0',
        'phase': 'WS4-P2: Content Sharing & Style Posts',
        'tagline': 'We girls have no time - instant style content creation!',
        'features': {
            'style_posts': 'active',
            'post_engagement': 'active',
            'style_challenges': 'active',
            'content_collections': 'active',
            'ai_analysis': 'active'
        },
        'integration_status': {
            'ws1_user_management': 'ready',
            'ws2_ai_styling': 'ready',
            'ws3_computer_vision': 'ready'
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@content_sharing_bp.route('/posts', methods=['POST'])
def create_style_post():
    """
    Create a new style post
    "We girls have no time" - instant style sharing!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    
    # Create style post
    post = StylePost(
        user_id=user_id,
        title=data.get('title', ''),
        caption=data.get('caption', ''),
        post_type=data.get('post_type', 'outfit'),
        image_urls=json.dumps(data.get('image_urls', [])),
        outfit_id=data.get('outfit_id'),
        wardrobe_items=json.dumps(data.get('wardrobe_items', [])),
        style_tags=json.dumps(data.get('style_tags', [])),
        occasion=data.get('occasion'),
        season=data.get('season'),
        weather=data.get('weather'),
        formality_level=data.get('formality_level'),
        brands_featured=json.dumps(data.get('brands_featured', [])),
        price_range=data.get('price_range'),
        shopping_links=json.dumps(data.get('shopping_links', [])),
        is_public=data.get('is_public', True),
        allow_comments=data.get('allow_comments', True),
        allow_sharing=data.get('allow_sharing', True),
        allow_outfit_copying=data.get('allow_outfit_copying', True),
        published_at=datetime.utcnow(),
        status='published'
    )
    
    # AI analysis of the post
    ai_analysis = analyze_post_with_ai(data)
    post.ai_style_score = ai_analysis['style_score']
    post.ai_trend_relevance = ai_analysis['trend_relevance']
    post.ai_color_harmony = ai_analysis['color_harmony']
    post.ai_occasion_fit = ai_analysis['occasion_fit']
    
    db.session.add(post)
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='create',
        target_type='post',
        target_id=str(post.id),
        activity_data={
            'post_type': post.post_type,
            'ai_style_score': post.ai_style_score,
            'creation_time': 'instant'
        },
        source_location='post_creation'
    )
    
    return jsonify({
        'success': True,
        'post': post.to_dict(),
        'message': 'We girls have no time - style post created instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@content_sharing_bp.route('/posts', methods=['GET'])
def get_style_posts():
    """
    Get style posts feed
    "We girls have no time" - instant style feed!
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    post_type = request.args.get('type')
    user_id_filter = request.args.get('user_id')
    
    # Build query
    query = StylePost.query.filter_by(status='published', is_public=True)
    
    if post_type:
        query = query.filter_by(post_type=post_type)
    
    if user_id_filter:
        query = query.filter_by(user_id=user_id_filter)
    
    # Order by engagement and recency
    posts = query.order_by(
        (StylePost.likes_count + StylePost.comments_count + StylePost.shares_count).desc(),
        StylePost.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    posts_data = [post.to_dict() for post in posts.items]
    
    # Log activity if user is authenticated
    user_id = get_user_from_token()
    if user_id:
        SocialActivity.log_activity(
            user_id=user_id,
            activity_type='view',
            target_type='feed',
            target_id='style_posts',
            activity_data={'posts_viewed': len(posts_data)},
            source_location='style_feed'
        )
    
    return jsonify({
        'success': True,
        'posts': posts_data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': posts.total,
            'pages': posts.pages,
            'has_next': posts.has_next,
            'has_prev': posts.has_prev
        },
        'message': 'We girls have no time - style feed loaded instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@content_sharing_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_style_post(post_id):
    """
    Get a specific style post
    "We girls have no time" - instant post access!
    """
    post = StylePost.query.get_or_404(post_id)
    
    # Check if post is accessible
    if not post.is_public:
        user_id = get_user_from_token()
        if not user_id or user_id != post.user_id:
            return jsonify({'error': 'Post not accessible'}), 403
    
    # Increment view count
    post.increment_engagement('view')
    
    # Log activity if user is authenticated
    user_id = get_user_from_token()
    if user_id:
        SocialActivity.log_activity(
            user_id=user_id,
            activity_type='view',
            target_type='post',
            target_id=str(post_id),
            source_location='post_detail'
        )
    
    return jsonify({
        'success': True,
        'post': post.to_dict(),
        'message': 'We girls have no time - post loaded instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@content_sharing_bp.route('/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    """
    Like a style post
    "We girls have no time" - instant style appreciation!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    post = StylePost.query.get_or_404(post_id)
    
    # Check if already liked
    existing_like = PostLike.query.filter_by(
        user_id=user_id, 
        post_id=post_id
    ).first()
    
    if existing_like:
        return jsonify({'error': 'Post already liked'}), 400
    
    data = request.get_json() or {}
    like_type = data.get('like_type', 'like')
    
    # Create like
    like = PostLike(
        user_id=user_id,
        post_id=post_id,
        like_type=like_type
    )
    
    db.session.add(like)
    
    # Update post engagement
    post.increment_engagement('like')
    
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='like',
        target_type='post',
        target_id=str(post_id),
        activity_data={'like_type': like_type},
        source_location='post_detail'
    )
    
    # Create notification for post owner
    if post.user_id != user_id:
        SocialNotification.create_notification(
            user_id=post.user_id,
            sender_id=user_id,
            notification_type='like',
            title='Your post got a like!',
            message=f'Someone loved your style post!',
            action_url=f'/posts/{post_id}',
            related_content_id=str(post_id),
            related_content_type='post'
        )
    
    return jsonify({
        'success': True,
        'like': like.to_dict(),
        'message': 'We girls have no time - style appreciation sent instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@content_sharing_bp.route('/posts/<int:post_id>/comment', methods=['POST'])
def comment_on_post(post_id):
    """
    Comment on a style post
    "We girls have no time" - instant style feedback!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    post = StylePost.query.get_or_404(post_id)
    
    if not post.allow_comments:
        return jsonify({'error': 'Comments not allowed on this post'}), 403
    
    data = request.get_json()
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({'error': 'Comment content required'}), 400
    
    # Create comment
    comment = PostComment(
        post_id=post_id,
        user_id=user_id,
        content=content,
        comment_type=data.get('comment_type', 'text'),
        parent_comment_id=data.get('parent_comment_id')
    )
    
    db.session.add(comment)
    
    # Update post engagement
    post.increment_engagement('comment')
    
    # Update parent comment replies count if this is a reply
    if comment.parent_comment_id:
        parent_comment = PostComment.query.get(comment.parent_comment_id)
        if parent_comment:
            parent_comment.replies_count += 1
    
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='comment',
        target_type='post',
        target_id=str(post_id),
        activity_data={
            'comment_type': comment.comment_type,
            'is_reply': comment.parent_comment_id is not None
        },
        source_location='post_detail'
    )
    
    # Create notification for post owner
    if post.user_id != user_id:
        SocialNotification.create_notification(
            user_id=post.user_id,
            sender_id=user_id,
            notification_type='comment',
            title='New comment on your post!',
            message=f'Someone commented on your style post: "{content[:50]}..."',
            action_url=f'/posts/{post_id}',
            related_content_id=str(post_id),
            related_content_type='post'
        )
    
    return jsonify({
        'success': True,
        'comment': comment.to_dict(),
        'message': 'We girls have no time - style feedback shared instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@content_sharing_bp.route('/posts/<int:post_id>/share', methods=['POST'])
def share_post(post_id):
    """
    Share a style post
    "We girls have no time" - instant style inspiration spreading!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    post = StylePost.query.get_or_404(post_id)
    
    if not post.allow_sharing:
        return jsonify({'error': 'Sharing not allowed on this post'}), 403
    
    data = request.get_json()
    
    # Create share
    share = PostShare(
        post_id=post_id,
        user_id=user_id,
        share_type=data.get('share_type', 'repost'),
        share_caption=data.get('share_caption'),
        share_platform=data.get('share_platform', 'internal'),
        recipient_user_id=data.get('recipient_user_id'),
        external_url=data.get('external_url')
    )
    
    db.session.add(share)
    
    # Update post engagement
    post.increment_engagement('share')
    
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='share',
        target_type='post',
        target_id=str(post_id),
        activity_data={
            'share_type': share.share_type,
            'share_platform': share.share_platform
        },
        source_location='post_detail'
    )
    
    # Create notification for post owner
    if post.user_id != user_id:
        SocialNotification.create_notification(
            user_id=post.user_id,
            sender_id=user_id,
            notification_type='share',
            title='Your post was shared!',
            message=f'Someone shared your style post!',
            action_url=f'/posts/{post_id}',
            related_content_id=str(post_id),
            related_content_type='post'
        )
    
    return jsonify({
        'success': True,
        'share': share.to_dict(),
        'message': 'We girls have no time - style inspiration spread instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@content_sharing_bp.route('/posts/<int:post_id>/save', methods=['POST'])
def save_post(post_id):
    """
    Save a style post
    "We girls have no time" - instant style bookmarking!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    post = StylePost.query.get_or_404(post_id)
    
    # Check if already saved
    existing_save = PostSave.query.filter_by(
        user_id=user_id, 
        post_id=post_id
    ).first()
    
    if existing_save:
        return jsonify({'error': 'Post already saved'}), 400
    
    data = request.get_json() or {}
    
    # Create save
    save = PostSave(
        post_id=post_id,
        user_id=user_id,
        collection_name=data.get('collection_name', 'Saved Posts'),
        save_reason=data.get('save_reason'),
        notes=data.get('notes'),
        is_private=data.get('is_private', True),
        reminder_date=datetime.fromisoformat(data['reminder_date']) if data.get('reminder_date') else None
    )
    
    db.session.add(save)
    
    # Update post engagement
    post.increment_engagement('save')
    
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='save',
        target_type='post',
        target_id=str(post_id),
        activity_data={
            'collection_name': save.collection_name,
            'save_reason': save.save_reason
        },
        source_location='post_detail'
    )
    
    return jsonify({
        'success': True,
        'save': save.to_dict(),
        'message': 'We girls have no time - style inspiration saved instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@content_sharing_bp.route('/challenges', methods=['GET'])
def get_style_challenges():
    """
    Get active style challenges
    "We girls have no time" - instant style challenges!
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    challenge_type = request.args.get('type')
    difficulty = request.args.get('difficulty')
    
    # Build query for active challenges
    query = StyleChallenge.query.filter_by(is_active=True)
    
    if challenge_type:
        query = query.filter_by(challenge_type=challenge_type)
    
    if difficulty:
        query = query.filter_by(difficulty_level=difficulty)
    
    # Order by participation and recency
    challenges = query.order_by(
        StyleChallenge.participants_count.desc(),
        StyleChallenge.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    challenges_data = [challenge.to_dict() for challenge in challenges.items]
    
    # Log activity if user is authenticated
    user_id = get_user_from_token()
    if user_id:
        SocialActivity.log_activity(
            user_id=user_id,
            activity_type='view',
            target_type='challenges',
            target_id='list',
            activity_data={'challenges_viewed': len(challenges_data)},
            source_location='challenges_page'
        )
    
    return jsonify({
        'success': True,
        'challenges': challenges_data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': challenges.total,
            'pages': challenges.pages,
            'has_next': challenges.has_next,
            'has_prev': challenges.has_prev
        },
        'message': 'We girls have no time - style challenges loaded instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@content_sharing_bp.route('/challenges', methods=['POST'])
def create_style_challenge():
    """
    Create a new style challenge
    "We girls have no time" - instant challenge creation!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    
    # Create style challenge
    challenge = StyleChallenge(
        creator_id=user_id,
        title=data.get('title', ''),
        description=data.get('description', ''),
        challenge_type=data.get('challenge_type', 'style'),
        rules=json.dumps(data.get('rules', {})),
        required_items=json.dumps(data.get('required_items', [])),
        style_constraints=json.dumps(data.get('style_constraints', {})),
        hashtag=data.get('hashtag'),
        difficulty_level=data.get('difficulty_level', 'medium'),
        estimated_time=data.get('estimated_time'),
        end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
        has_prizes=data.get('has_prizes', False),
        prize_description=data.get('prize_description')
    )
    
    db.session.add(challenge)
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='create',
        target_type='challenge',
        target_id=str(challenge.id),
        activity_data={
            'challenge_type': challenge.challenge_type,
            'difficulty_level': challenge.difficulty_level
        },
        source_location='challenge_creation'
    )
    
    return jsonify({
        'success': True,
        'challenge': challenge.to_dict(),
        'message': 'We girls have no time - style challenge created instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@content_sharing_bp.route('/collections', methods=['GET'])
def get_content_collections():
    """
    Get user's content collections
    "We girls have no time" - instant collection access!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    collection_type = request.args.get('type')
    
    # Build query
    query = ContentCollection.query.filter_by(user_id=user_id)
    
    if collection_type:
        query = query.filter_by(collection_type=collection_type)
    
    collections = query.order_by(ContentCollection.updated_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    collections_data = [collection.to_dict() for collection in collections.items]
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='view',
        target_type='collections',
        target_id=user_id,
        activity_data={'collections_viewed': len(collections_data)},
        source_location='collections_page'
    )
    
    return jsonify({
        'success': True,
        'collections': collections_data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': collections.total,
            'pages': collections.pages,
            'has_next': collections.has_next,
            'has_prev': collections.has_prev
        },
        'message': 'We girls have no time - collections loaded instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

@content_sharing_bp.route('/collections', methods=['POST'])
def create_content_collection():
    """
    Create a new content collection
    "We girls have no time" - instant collection creation!
    """
    user_id = get_user_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    
    # Create content collection
    collection = ContentCollection(
        user_id=user_id,
        name=data.get('name', ''),
        description=data.get('description', ''),
        collection_type=data.get('collection_type', 'custom'),
        cover_image_url=data.get('cover_image_url'),
        tags=json.dumps(data.get('tags', [])),
        color_theme=data.get('color_theme'),
        is_public=data.get('is_public', False),
        is_collaborative=data.get('is_collaborative', False),
        allow_contributions=data.get('allow_contributions', False)
    )
    
    db.session.add(collection)
    db.session.commit()
    
    # Log activity
    SocialActivity.log_activity(
        user_id=user_id,
        activity_type='create',
        target_type='collection',
        target_id=str(collection.id),
        activity_data={
            'collection_type': collection.collection_type,
            'is_public': collection.is_public
        },
        source_location='collection_creation'
    )
    
    return jsonify({
        'success': True,
        'collection': collection.to_dict(),
        'message': 'We girls have no time - collection created instantly!',
        'timestamp': datetime.utcnow().isoformat()
    })

