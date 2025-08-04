import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.auth import auth_bp

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
        'endpoints': {
            'auth': '/api/auth/*',
            'users': '/api/*',
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
        'description': 'Authentication and user profile management for Tanvi Vanity Agent',
        'workstream': 'WS1: User Management & Authentication',
        'phase': 'P1: Foundation Sprint',
        'features': [
            'Quick user registration with smart defaults',
            'Fast authentication with JWT tokens',
            'Streamlined profile management',
            'Privacy-focused user preferences',
            'Session management and security',
            'Quick setup for AI styling'
        ],
        'api_endpoints': {
            'POST /api/auth/register': 'Quick user registration',
            'POST /api/auth/login': 'Fast user login',
            'POST /api/auth/logout': 'Secure logout',
            'POST /api/auth/verify-token': 'Token verification',
            'POST /api/auth/refresh-token': 'Token refresh',
            'POST /api/auth/quick-setup': 'Streamlined profile setup',
            'GET /api/profile': 'Get user profile',
            'PUT /api/profile': 'Update user profile',
            'GET /api/preferences': 'Get styling preferences',
            'PUT /api/preferences': 'Update styling preferences',
            'GET /api/sessions': 'Get active sessions',
            'DELETE /api/sessions/<id>': 'Terminate session',
            'GET /api/quick-stats': 'Get account statistics',
            'POST /api/deactivate': 'Deactivate account'
        }
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
            'tagline': 'We girls have no time - this is the API service!',
            'message': 'This is a backend API service. Use /api/info for endpoint information.',
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
                'tagline': 'We girls have no time - this is the API service!',
                'message': 'This is a backend API service. Use /api/info for endpoint information.'
            }), 200


if __name__ == '__main__':
    print("🌟 Starting Tanvi Vanity Agent - User Management Service")
    print("💫 Tagline: 'We girls have no time' - Quick user management for busy lifestyles!")
    print("🚀 Service running on http://0.0.0.0:5000")
    print("📚 API documentation: http://0.0.0.0:5000/api/info")
    
    app.run(host='0.0.0.0', port=5001, debug=True)

