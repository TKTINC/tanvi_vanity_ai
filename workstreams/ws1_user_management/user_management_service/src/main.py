import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.models.profile import StyleProfile, WardrobeItem, OutfitHistory, QuickStyleQuiz
from src.models.analytics import UserAnalytics, StyleInsights, UsagePattern, PersonalizationScore
from src.models.security import SecurityAuditLog, UserPrivacySettings, DataAccessLog, UserSecuritySettings, DataExportRequest
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.profile import profile_bp
from src.routes.analytics import analytics_bp
from src.routes.security import security_bp

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
app.register_blueprint(security_bp, url_prefix='/api/security')

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
        'tagline': 'We girls have no time - system is running fast and secure!',
        'version': '1.0.0',
        'phase': 'WS1-P4: Security & Privacy Controls',
        'endpoints': {
            'auth': '/api/auth/*',
            'users': '/api/*',
            'profiles': '/api/profile/*',
            'analytics': '/api/analytics/*',
            'security': '/api/security/*',
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
        'description': 'Authentication, profile management, advanced analytics, and security controls for Tanvi Vanity Agent',
        'workstream': 'WS1: User Management & Authentication',
        'phase': 'P4: Security & Privacy Controls',
        'new_features': [
            'Comprehensive privacy settings with simple controls',
            'Advanced security settings and monitoring',
            'Complete security audit logging',
            'Data access transparency logs',
            'GDPR-compliant data export system',
            'Account deletion with grace period',
            'Automated suspicious activity detection',
            'Device fingerprinting and tracking'
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
            
            # Advanced analytics endpoints (from P3)
            'GET /api/analytics/dashboard': 'Get analytics dashboard overview',
            'GET /api/analytics/insights': 'Get AI-generated style insights',
            'POST /api/analytics/insights/<id>/action': 'Interact with style insight',
            'GET /api/analytics/patterns': 'Get usage patterns and behaviors',
            'GET /api/analytics/personalization': 'Get personalization score and recommendations',
            'GET /api/analytics/activity-summary': 'Get activity summary for date range',
            'POST /api/analytics/track-action': 'Track user action for analytics',
            
            # Security & Privacy endpoints (NEW in P4)
            'GET /api/security/privacy-settings': 'Get privacy settings and controls',
            'PUT /api/security/privacy-settings': 'Update privacy settings',
            'GET /api/security/security-settings': 'Get security settings and controls',
            'PUT /api/security/security-settings': 'Update security settings',
            'GET /api/security/audit-log': 'Get security audit log for transparency',
            'GET /api/security/data-access-log': 'Get data access log for transparency',
            'POST /api/security/export-data': 'Request GDPR data export',
            'GET /api/security/export-data/<id>': 'Get data export status',
            'GET /api/security/download-data/<token>': 'Download exported data',
            'POST /api/security/delete-account': 'Request account deletion'
        }
    }), 200

@app.route('/api/features', methods=['GET'])
def feature_overview():
    """
    Overview of WS1-P4 security and privacy features
    """
    return jsonify({
        'phase': 'WS1-P4: Security & Privacy Controls',
        'tagline': 'We girls have no time - security and privacy made simple!',
        'key_features': {
            'privacy_controls': {
                'description': 'Simple privacy settings with clear explanations',
                'benefits': [
                    'Granular visibility controls for all data types',
                    'Smart defaults that protect privacy',
                    'One-click privacy level changes',
                    'Clear explanations of what each setting does'
                ],
                'setup_time': '2 minutes for full privacy review'
            },
            'security_monitoring': {
                'description': 'Advanced security with automated monitoring',
                'benefits': [
                    'Real-time suspicious activity detection',
                    'Automatic account locking after failed attempts',
                    'Device fingerprinting and tracking',
                    'Comprehensive security event logging'
                ],
                'response_time': 'Instant threat detection'
            },
            'data_transparency': {
                'description': 'Complete transparency into data access and usage',
                'benefits': [
                    'Real-time data access logging',
                    'Clear audit trail of all security events',
                    'Easy-to-understand access summaries',
                    'Automated compliance tracking'
                ],
                'visibility': 'Every data access logged and visible'
            },
            'gdpr_compliance': {
                'description': 'Full GDPR compliance with user-friendly tools',
                'benefits': [
                    'One-click data export in multiple formats',
                    'Right to be forgotten with grace period',
                    'Consent management with version tracking',
                    'Automated data retention policies'
                ],
                'export_time': '5-10 minutes for complete data export'
            },
            'user_control': {
                'description': 'Complete user control over data and security',
                'benefits': [
                    'Flexible session management',
                    'Customizable security notifications',
                    'Data retention preferences',
                    'Third-party integration controls'
                ],
                'customization': 'Every security aspect is user-configurable'
            }
        },
        'security_features': {
            'audit_logging': 'Every security event is logged with full context',
            'data_access_tracking': 'Complete transparency into who accessed what data when',
            'privacy_by_design': 'Privacy-first approach with secure defaults',
            'compliance_ready': 'GDPR, CCPA, and other privacy regulation compliance',
            'user_empowerment': 'Users have complete control over their data and privacy'
        },
        'privacy_levels': {
            'private': 'Data visible only to the user (default)',
            'friends': 'Data visible to approved connections',
            'public': 'Data visible to all users',
            'anonymous': 'Data used anonymously for improvements'
        },
        'integration_ready': [
            'WS2: AI-Powered Styling Engine (privacy-compliant AI training)',
            'WS3: Computer Vision & Wardrobe (secure image processing)',
            'WS4: Social Integration (privacy-controlled social features)',
            'WS5: E-commerce Integration (secure payment and data handling)',
            'WS6: Mobile Application & UX (privacy-first mobile experience)'
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
            'tagline': 'We girls have no time - this is the secure and intelligent API service!',
            'message': 'This is a backend API service. Use /api/info for endpoint information.',
            'phase': 'WS1-P4: Security & Privacy Controls',
            'new_capabilities': [
                'Comprehensive privacy controls',
                'Advanced security monitoring',
                'Data access transparency',
                'GDPR-compliant data export',
                'User-controlled account deletion'
            ],
            'security_note': 'All data is protected with enterprise-grade security and privacy controls',
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
                'tagline': 'We girls have no time - this is the secure and intelligent API service!',
                'message': 'This is a backend API service. Use /api/info for endpoint information.',
                'phase': 'WS1-P4: Security & Privacy Controls'
            }), 200


if __name__ == '__main__':
    print("🌟 Starting Tanvi Vanity Agent - User Management Service")
    print("💫 Tagline: 'We girls have no time' - Quick user management for busy lifestyles!")
    print("🚀 Phase: WS1-P4 Security & Privacy Controls")
    print("🔒 New Features: Privacy controls, security monitoring, data transparency, GDPR compliance")
    print("🛡️ Security: Advanced threat detection, audit logging, user empowerment")
    print("🚀 Service running on http://0.0.0.0:5001")
    print("📚 API documentation: http://0.0.0.0:5001/api/info")
    print("🎯 Feature overview: http://0.0.0.0:5001/api/features")
    print("📊 Analytics dashboard: http://0.0.0.0:5001/api/analytics/dashboard")
    print("🔒 Privacy settings: http://0.0.0.0:5001/api/security/privacy-settings")
    
    app.run(host='0.0.0.0', port=5001, debug=True)

