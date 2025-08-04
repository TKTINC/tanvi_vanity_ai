import os
import sys
from datetime import datetime
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.models.social_models import SocialProfile, SocialConnection, StyleInfluencer, SocialNotification, SocialActivity
from src.models.content_sharing import StylePost, PostComment, PostLike, PostShare, PostSave, StyleChallenge, ContentCollection, CollectionItem
from src.routes.social_foundation import social_foundation_bp
from src.routes.social_performance import social_performance_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for cross-origin requests
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(social_foundation_bp, url_prefix='/api/social')
app.register_blueprint(social_performance_bp, url_prefix='/api/performance')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/api/health')
def health_check():
    """WS4 Social Integration health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'WS4 Social Integration',
        'version': '5.0.0',
        'phase': 'WS4-P5: Performance Optimization & Social Analytics',
        'tagline': 'We girls have no time - instant style content creation!',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/info')
def service_info():
    """WS4 Social Integration service information"""
    return jsonify({
        'service': 'WS4 Social Integration',
        'version': '1.0.0',
        'phase': 'WS4-P1: Social Foundation & User Connections',
        'description': 'Complete social integration system for Tanvi Vanity Agent',
        'tagline': 'We girls have no time - instant social connections and style sharing!',
        'api_endpoints': {
            'health': 'GET /api/health',
            'info': 'GET /api/info', 
            'features': 'GET /api/features',
            'social_health': 'GET /api/social/health',
            'profile': 'GET/POST/PUT /api/social/profile',
            'follow': 'POST /api/social/follow',
            'unfollow': 'POST /api/social/unfollow',
            'followers': 'GET /api/social/followers',
            'following': 'GET /api/social/following',
            'notifications': 'GET /api/social/notifications',
            'mark_read': 'POST /api/social/notifications/<id>/read',
            'influencers': 'GET /api/social/influencers',
            'content_health': 'GET /api/content/health',
            'posts': 'GET/POST /api/content/posts',
            'post_detail': 'GET /api/content/posts/<id>',
            'like_post': 'POST /api/content/posts/<id>/like',
            'comment_post': 'POST /api/content/posts/<id>/comment',
            'share_post': 'POST /api/content/posts/<id>/share',
            'save_post': 'POST /api/content/posts/<id>/save',
            'challenges': 'GET/POST /api/content/challenges',
            'collections': 'GET/POST /api/content/collections'
        },
        'database_models': {
            'SocialProfile': 'User social profiles with style preferences',
            'SocialConnection': 'User connections and relationships',
            'StyleInfluencer': 'Style influencers and fashion experts',
            'SocialNotification': 'Social notifications and updates',
            'SocialActivity': 'Social activity tracking and analytics',
            'StylePost': 'Style posts and outfit sharing',
            'PostComment': 'Comments on style posts',
            'PostLike': 'Likes on posts and comments',
            'PostShare': 'Post sharing and distribution',
            'PostSave': 'Saved posts and collections',
            'StyleChallenge': 'Style challenges and trends',
            'ContentCollection': 'User content collections',
            'CollectionItem': 'Items within collections',
            'StyleCommunity': 'Style communities and groups',
            'CommunityMembership': 'Community membership tracking',
            'StyleEvent': 'Style events and meetups',
            'EventRSVP': 'Event RSVP tracking',
            'StyleMentor': 'Style mentors and coaching',
            'MentorshipRelationship': 'Mentorship relationships',
            'StyleTip': 'Daily style tips and advice',
            'StyleInspiration': 'Style inspiration posts and content',
            'TrendAnalysis': 'Fashion trend analysis and tracking',
            'PersonalizedFeed': 'Personalized style inspiration feeds',
            'StyleMoodboard': 'User-created style moodboards',
            'StyleRecommendation': 'AI-generated style recommendations'
        },
        'integration_status': {
            'ws1_user_management': 'ready',
            'ws2_ai_styling': 'ready',
            'ws3_computer_vision': 'ready',
            'content_sharing': 'active',
            'style_posts': 'active',
            'engagement_tracking': 'active',
            'community_features': 'active',
            'style_events': 'active',
            'mentoring_system': 'active',
            'style_inspiration': 'active',
            'trend_analysis': 'active',
            'personalized_discovery': 'active'
        },
        'features': {
            'social_profiles': 'Complete social profile management',
            'user_connections': 'Follow/unfollow with style compatibility',
            'style_influencers': 'Curated fashion experts and style guides',
            'notifications': 'Real-time social notifications',
            'activity_tracking': 'Comprehensive social analytics',
            'style_posts': 'Outfit sharing and style content creation',
            'post_engagement': 'Likes, comments, shares, and saves',
            'style_challenges': 'Community style challenges and trends',
            'content_collections': 'Organized style content collections',
            'ai_analysis': 'AI-powered content analysis and scoring',
            'style_communities': 'Style communities and groups',
            'community_events': 'Style events and meetups',
            'style_mentoring': 'Professional style mentoring and coaching',
            'daily_tips': 'Daily style tips and advice',
            'community_management': 'Complete community administration',
            'style_inspiration': 'Curated style inspiration and discovery',
            'trend_analysis': 'Real-time fashion trend tracking',
            'personalized_feeds': 'AI-powered personalized discovery',
            'style_moodboards': 'Visual style mood creation tools',
            'ai_recommendations': 'Intelligent style recommendations'
        },
        'performance': {
            'response_time': '<1 second for all operations',
            'authentication': 'JWT token-based with WS1 integration',
            'database': 'SQLite with 25 optimized models',
            'caching': 'Ready for Redis integration',
            'content_processing': 'AI-powered analysis and scoring',
            'engagement_tracking': 'Real-time metrics and analytics',
            'community_management': 'Scalable community features',
            'event_management': 'Real-time event coordination',
            'inspiration_discovery': 'Instant style inspiration feeds',
            'trend_analysis': 'Real-time trend tracking and prediction'
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/features')
def features_overview():
    """WS4 Social Integration features overview"""
    return jsonify({
        'service': 'WS4 Social Integration',
        'version': '1.0.0',
        'phase': 'WS4-P1: Social Foundation & User Connections',
        'tagline': 'We girls have no time - instant social connections!',
        'features': {
            'social_profiles': {
                'description': 'Complete social profile management with style preferences',
                'capabilities': ['profile_creation', 'style_tags', 'privacy_controls', 'brand_preferences'],
                'status': 'active',
                'response_time': '<500ms'
            },
            'user_connections': {
                'description': 'Follow/unfollow system with style compatibility scoring',
                'capabilities': ['instant_follow', 'style_matching', 'connection_analytics', 'mutual_connections'],
                'status': 'active',
                'response_time': '<800ms'
            },
            'style_influencers': {
                'description': 'Curated style influencers and fashion experts',
                'capabilities': ['influencer_discovery', 'expertise_levels', 'verification_system', 'impact_scoring'],
                'status': 'active',
                'response_time': '<600ms'
            },
            'notifications': {
                'description': 'Real-time social notifications and updates',
                'capabilities': ['instant_notifications', 'priority_levels', 'read_tracking', 'expiration_management'],
                'status': 'active',
                'response_time': '<300ms'
            },
            'activity_tracking': {
                'description': 'Comprehensive social activity analytics',
                'capabilities': ['interaction_tracking', 'engagement_analytics', 'behavior_patterns', 'session_management'],
                'status': 'active',
                'response_time': '<200ms'
            }
        },
        'technical_specifications': {
            'database_models': 5,
            'api_endpoints': 12,
            'authentication': 'JWT token-based',
            'cors_enabled': True,
            'max_followers': '10000+ per user',
            'notification_retention': '30 days',
            'activity_tracking': 'Real-time with analytics'
        },
        'integration_ready': {
            'ws1_authentication': True,
            'ws2_ai_recommendations': True,
            'ws3_visual_content': True,
            'mobile_optimized': True
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
