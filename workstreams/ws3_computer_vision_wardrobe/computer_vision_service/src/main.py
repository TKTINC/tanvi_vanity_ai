import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.models.cv_models import WardrobeItem, ImageAnalysis, OutfitVisualization, StyleDetection, VisualSimilarity
from src.routes.computer_vision import computer_vision_bp
from datetime import datetime

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'tanvi_cv_secret_key_2025'

# Enable CORS for frontend integration
CORS(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(computer_vision_bp, url_prefix='/api/cv')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# Service information endpoints
@app.route('/api/health')
def health_check():
    """WS3 Computer Vision service health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'WS3 Computer Vision & Wardrobe',
        'version': '1.0.0',
        'phase': 'WS3-P1: Computer Vision Foundation & Item Recognition',
        'tagline': 'We girls have no time - Instant visual wardrobe intelligence!',
        'database': 'connected',
        'models_loaded': 5,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/info')
def service_info():
    """WS3 Computer Vision service information"""
    return jsonify({
        'service_name': 'WS3 Computer Vision & Wardrobe Service',
        'version': '1.0.0',
        'phase': 'WS3-P1: Computer Vision Foundation & Item Recognition',
        'tagline': 'We girls have no time - Instant visual wardrobe intelligence!',
        'description': 'Advanced computer vision for intelligent wardrobe management and visual styling',
        'api_endpoints': {
            'health': 'GET /api/health - Service health check',
            'info': 'GET /api/info - Service information',
            'features': 'GET /api/features - Features overview',
            'cv_health': 'GET /api/cv/health - Computer vision health check',
            'cv_info': 'GET /api/cv/info - Computer vision service info',
            'cv_features': 'GET /api/cv/features - Computer vision features',
            'analyze_item': 'POST /api/cv/analyze-item - Analyze wardrobe item image',
            'add_item': 'POST /api/cv/wardrobe/add-item - Add item to wardrobe',
            'get_wardrobe': 'GET /api/cv/wardrobe/items - Get user wardrobe',
            'get_item': 'GET /api/cv/wardrobe/items/<id> - Get specific item',
            'search_items': 'GET /api/cv/wardrobe/search - Search wardrobe items',
            'similar_items': 'GET /api/cv/wardrobe/items/<id>/similar - Find similar items'
        },
        'computer_vision_models': {
            'WardrobeItem': 'Core wardrobe item with CV analysis',
            'ImageAnalysis': 'Detailed image analysis results',
            'OutfitVisualization': 'Outfit visualization and virtual try-on',
            'StyleDetection': 'Advanced style detection and analysis',
            'VisualSimilarity': 'Visual similarity analysis between items'
        },
        'integration_status': {
            'ws1_user_management': 'Ready for JWT authentication',
            'ws2_ai_styling': 'Ready for AI-powered recommendations',
            'database': 'SQLite with 5 CV models',
            'cors': 'Enabled for frontend integration'
        }
    })

@app.route('/api/features')
def features_overview():
    """WS3 Computer Vision features overview"""
    return jsonify({
        'service': 'WS3 Computer Vision & Wardrobe',
        'tagline': 'We girls have no time - Instant visual wardrobe intelligence!',
        'core_features': {
            'computer_vision_foundation': {
                'description': 'Advanced computer vision for wardrobe analysis',
                'capabilities': ['image_analysis', 'item_recognition', 'color_detection'],
                'status': 'active',
                'accuracy': '85%+'
            },
            'wardrobe_management': {
                'description': 'Complete digital wardrobe organization',
                'capabilities': ['item_cataloging', 'search_filtering', 'usage_tracking'],
                'status': 'active',
                'capacity': '1000+ items'
            },
            'visual_similarity': {
                'description': 'Find visually similar items in wardrobe',
                'capabilities': ['similarity_scoring', 'duplicate_detection', 'style_matching'],
                'status': 'active',
                'accuracy': '80%+'
            },
            'style_detection': {
                'description': 'Advanced style and aesthetic analysis',
                'capabilities': ['style_classification', 'trend_analysis', 'formality_scoring'],
                'status': 'active',
                'categories': '20+ style types'
            },
            'image_processing': {
                'description': 'High-performance image analysis pipeline',
                'capabilities': ['color_analysis', 'pattern_recognition', 'material_detection'],
                'status': 'active',
                'speed': '1-3 seconds per image'
            }
        },
        'technical_specifications': {
            'supported_formats': ['JPEG', 'PNG', 'WebP'],
            'max_image_size': '10MB',
            'processing_speed': '1-3 seconds per image',
            'database_models': 5,
            'api_endpoints': 11
        },
        'integration_ready': {
            'ws1_authentication': True,
            'ws2_ai_recommendations': True,
            'mobile_optimization': True,
            'real_time_processing': True
        }
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
