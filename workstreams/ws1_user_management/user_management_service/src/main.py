import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.models.profile import StyleProfile, WardrobeItem, OutfitHistory, QuickStyleQuiz
from src.models.analytics import UserAnalytics, StyleInsights, UsagePattern, PersonalizationScore
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.profile import profile_bp
from src.routes.analytics import analytics_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tanvi-vanity-dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for all routes - essential for frontend-backend communication
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(profile_bp, url_prefix='/api/profile')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring
    "We girls have no time" - quick system status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Tanvi Vanity Agent - User Management',
        'tagline': 'We girls have no time - system is running fast!',
        'version': '1.0.0',
        'phase': 'WS1-P3: Advanced User Analytics',
        'endpoints': {
            'auth': '/api/auth/*',
            'users': '/api/*',
            'profiles': '/api/profile/*',
            'analytics': '/api/analytics/*',
            'health': '/api/health'
        }
    }), 200

@app.route('/api/info', methods=['GET'])
def service_info():
    """
    Service information endpoint
    """
    return jsonify({
        'service_name': 'User Management Service',
        'tagline': 'We girls have no time - quick user management for busy lifestyles!',
        'description': 'Authentication, profile management, and advanced analytics for Tanvi Vanity Agent',
        'workstream': 'WS1: User Management & Authentication',
        'phase': 'P3: Advanced User Analytics',
        'new_features': [
            'Real-time user behavior analytics',
            'AI-generated style insights and recommendations',
            'Usage pattern recognition and optimization',
            'Dynamic personalization scoring',
            'Quick activity summaries and dashboards',
            'Intelligent user action tracking'
        ],
        'api_endpoints': {
            # Authentication endpoints (from P1)
            'POST /api/auth/register': 'Quick user registration',
            'POST /api/auth/login': 'Fast user login',
            'POST /api/auth/logout': 'Secure logout',
            'POST /api/auth/verify-token': 'Token verification',
            'POST /api/auth/refresh-token': 'Token refresh',
            'POST /api/auth/quick-setup': 'Streamlined profile setup',
            
            # User management endpoints (from P1)
            'GET /api/profile': 'Get user profile',
            'PUT /api/profile': 'Update user profile',
            'GET /api/preferences': 'Get styling preferences',
            'PUT /api/preferences': 'Update styling preferences',
            'GET /api/sessions': 'Get active sessions',
            'DELETE /api/sessions/<id>': 'Terminate session',
            'GET /api/quick-stats': 'Get account statistics',
            'POST /api/deactivate': 'Deactivate account',
            
            # Enhanced profile endpoints (from P2)
            'GET /api/profile/style-profile': 'Get comprehensive style profile',
            'PUT /api/profile/style-profile': 'Update style profile',
            'POST /api/profile/quick-style-quiz': 'Take 2-minute style quiz',
            'GET /api/profile/wardrobe': 'Get wardrobe items',
            'POST /api/profile/wardrobe': 'Add wardrobe item',
            'PUT /api/profile/wardrobe/<id>': 'Update wardrobe item',
            'POST /api/profile/wardrobe/<id>/worn': 'Mark item as worn',
            'GET /api/profile/outfit-history': 'Get outfit history',
            'POST /api/profile/outfit-history': 'Log new outfit',
            'POST /api/profile/outfit-history/<id>/rate': 'Rate outfit for AI learning',
            
            # Advanced analytics endpoints (NEW in P3)
            'GET /api/analytics/dashboard': 'Get analytics dashboard overview',
            'GET /api/analytics/insights': 'Get AI-generated style insights',
            'POST /api/analytics/insights/<id>/action': 'Interact with style insight',
            'GET /api/analytics/patterns': 'Get usage patterns and behaviors',
            'GET /api/analytics/personalization': 'Get personalization score and recommendations',
            'GET /api/analytics/activity-summary': 'Get activity summary for date range',
            'POST /api/analytics/track-action': 'Track user action for analytics'
        }
    }), 200

@app.route('/api/features', methods=['GET'])
def feature_overview():
    """
    Overview of WS1-P3 advanced analytics features
    """
    return jsonify({
        'phase': 'WS1-P3: Advanced User Analytics',
        'tagline': 'We girls have no time - intelligent insights made instant!',
        'key_features': {
            'real_time_analytics': {
                'description': 'Live tracking of user behavior and engagement',
                'benefits': [
                    'Daily activity monitoring',
                    'Session duration tracking',
                    'Feature usage analytics',
                    'Peak usage time identification'
                ],
                'response_time': 'Real-time updates'
            },
            'ai_style_insights': {
                'description': 'AI-generated personalized style recommendations',
                'benefits': [
                    'Wardrobe gap analysis',
                    'Style evolution tracking',
                    'Seasonal recommendations',
                    'Actionable styling tips'
                ],
                'response_time': 'Generated in seconds'
            },
            'usage_patterns': {
                'description': 'Intelligent pattern recognition for UX optimization',
                'benefits': [
                    'Morning vs evening usage patterns',
                    'Weekend planning behaviors',
                    'Feature preference identification',
                    'Optimization suggestions'
                ],
                'response_time': 'Instant pattern analysis'
            },
            'personalization_scoring': {
                'description': 'Dynamic scoring for adaptive user experience',
                'benefits': [
                    'Profile completeness tracking',
                    'Engagement level monitoring',
                    'Satisfaction measurement',
                    'UX adaptation recommendations'
                ],
                'response_time': 'Live score updates'
            },
            'quick_dashboards': {
                'description': 'Instant overview of user activity and insights',
                'benefits': [
                    '7-day activity summaries',
                    'Key metrics at a glance',
                    'Priority insights display',
                    'Personalization recommendations'
                ],
                'response_time': 'Sub-second loading'
            }
        },
        'intelligence_features': {
            'predictive_insights': 'AI predicts wardrobe needs and style evolution',
            'behavioral_adaptation': 'System adapts to user preferences automatically',
            'smart_recommendations': 'Context-aware suggestions based on usage patterns',
            'efficiency_optimization': 'Identifies ways to save user time'
        },
        'integration_ready': [
            'WS2: AI-Powered Styling Engine (analytics data ready)',
            'WS3: Computer Vision & Wardrobe (usage patterns ready)',
            'WS4: Social Integration (engagement metrics ready)',
            'WS6: Mobile Application & UX (personalization scores ready)'
        ]
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Custom 404 handler with Tanvi branding"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist',
        'tagline': 'We girls have no time - but this endpoint doesn\'t exist!',
        'available_endpoints': '/api/info'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 handler with Tanvi branding"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end',
        'tagline': 'We girls have no time - and neither do our servers! Please try again.'
    }), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serve static files and handle SPA routing"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return jsonify({
            'service': 'Tanvi Vanity Agent - User Management API',
            'tagline': 'We girls have no time - this is the intelligent API service!',
            'message': 'This is a backend API service. Use /api/info for endpoint information.',
            'phase': 'WS1-P3: Advanced User Analytics',
            'new_capabilities': [
                'Real-time behavior analytics',
                'AI-generated style insights',
                'Usage pattern recognition',
                'Dynamic personalization scoring'
            ],
            'frontend_note': 'Frontend will be served from the mobile app workstream'
        }), 200

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return jsonify({
                'service': 'Tanvi Vanity Agent - User Management API',
                'tagline': 'We girls have no time - this is the intelligent API service!',
                'message': 'This is a backend API service. Use /api/info for endpoint information.',
                'phase': 'WS1-P3: Advanced User Analytics'
            }), 200


if __name__ == '__main__':
    print("🌟 Starting Tanvi Vanity Agent - User Management Service")
    print("💫 Tagline: 'We girls have no time' - Quick user management for busy lifestyles!")
    print("🚀 Phase: WS1-P3 Advanced User Analytics")
    print("🧠 New Features: Real-time analytics, AI insights, usage patterns, personalization scoring")
    print("📊 Intelligence: Predictive insights, behavioral adaptation, smart recommendations")
    print("🚀 Service running on http://0.0.0.0:5001")
    print("📚 API documentation: http://0.0.0.0:5001/api/info")
    print("🎯 Feature overview: http://0.0.0.0:5001/api/features")
    print("📊 Analytics dashboard: http://0.0.0.0:5001/api/analytics/dashboard")
    
    app.run(host='0.0.0.0', port=5001, debug=True)

