import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.ecommerce_models import db
from src.routes.ecommerce_foundation import ecommerce_bp
from src.routes.product_catalog import product_catalog_bp
from src.routes.merchant_integration import merchant_integration_bp
from src.routes.payment_processing import payment_processing_bp
from src.routes.shopping_checkout import shopping_checkout_bp
from src.routes.performance_analytics import performance_analytics_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'tanvi_ecommerce_secret_key_2024'

# Enable CORS for all routes
CORS(app, origins="*")

# Register blueprints
app.register_blueprint(ecommerce_bp, url_prefix='/api')
app.register_blueprint(product_catalog_bp, url_prefix='/api')
app.register_blueprint(merchant_integration_bp, url_prefix='/api')
app.register_blueprint(payment_processing_bp, url_prefix='/api')
app.register_blueprint(shopping_checkout_bp, url_prefix='/api')
app.register_blueprint(performance_analytics_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize database
with app.app_context():
    db.create_all()

@app.route('/health')
def health_check():
    """Health check endpoint for WS5 E-commerce Service"""
    return jsonify({
        "status": "healthy",
        "service": "WS5: E-commerce Integration",
        "version": "1.0.0",
        "tagline": "We girls have no time",
        "markets": ["US", "India"],
        "features": [
            "Multi-market e-commerce",
            "Product catalog management", 
            "Payment processing",
            "Shopping cart & checkout",
            "Order management",
            "Merchant integrations"
        ],
        "message": "Lightning-fast shopping experience for busy women globally!"
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
    app.run(host='0.0.0.0', port=5006, debug=True)

