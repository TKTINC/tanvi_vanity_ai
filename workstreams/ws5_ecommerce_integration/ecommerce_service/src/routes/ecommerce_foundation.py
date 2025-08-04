from flask import Blueprint, request, jsonify
from src.models.ecommerce_models import db, Market, Merchant, Product, ShoppingCart, CartItem, Order, OrderItem
import json
import requests
from datetime import datetime
import uuid

ecommerce_bp = Blueprint('ecommerce', __name__)

# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

@ecommerce_bp.route('/ecommerce/health', methods=['GET'])
def health_check():
    """Health check for WS5 E-commerce service"""
    return jsonify({
        "status": "healthy",
        "service": "WS5: E-commerce Integration", 
        "version": "1.0.0",
        "tagline": "We girls have no time",
        "philosophy": "Lightning-fast shopping for busy women",
        "markets_supported": ["US", "India"],
        "database_status": "connected",
        "features": [
            "Multi-market e-commerce platform",
            "Product catalog management",
            "Shopping cart & checkout",
            "Order management system",
            "Merchant integrations",
            "Payment processing ready"
        ],
        "message": "Ready to revolutionize fashion shopping globally!"
    })

@ecommerce_bp.route('/ecommerce/info', methods=['GET'])
def service_info():
    """Detailed service information"""
    return jsonify({
        "service_name": "Tanvi Vanity E-commerce Integration",
        "version": "1.0.0",
        "tagline": "We girls have no time",
        "description": "Complete e-commerce solution for instant fashion shopping",
        "markets": {
            "US": {
                "currency": "USD",
                "symbol": "$",
                "payment_methods": ["Credit Card", "PayPal", "Apple Pay", "Google Pay", "BNPL"],
                "shipping": ["Same-day", "Next-day", "Standard"],
                "merchants": ["Zara", "H&M", "Target", "Amazon Fashion", "Nordstrom"]
            },
            "India": {
                "currency": "INR", 
                "symbol": "₹",
                "payment_methods": ["UPI", "Paytm", "Credit Card", "Net Banking", "COD", "EMI"],
                "shipping": ["Same-day (Metro)", "Express", "Standard", "COD"],
                "merchants": ["Myntra", "Ajio", "Amazon India", "Flipkart Fashion", "Nykaa Fashion"]
            }
        },
        "capabilities": [
            "Real-time product catalog",
            "Multi-merchant shopping cart",
            "Intelligent product recommendations", 
            "Market-specific payment processing",
            "Order tracking & management",
            "Inventory synchronization",
            "Price comparison across merchants",
            "AI-powered shopping assistance"
        ],
        "integration_ready": {
            "WS1": "User management & authentication",
            "WS2": "AI styling recommendations", 
            "WS3": "Computer vision product matching",
            "WS4": "Social commerce features"
        }
    })

# ============================================================================
# MARKET MANAGEMENT ENDPOINTS
# ============================================================================

@ecommerce_bp.route('/ecommerce/markets', methods=['GET'])
def get_markets():
    """Get all available markets"""
    markets = Market.query.all()
    return jsonify({
        "markets": [market.to_dict() for market in markets],
        "count": len(markets),
        "message": "Available markets for Tanvi Vanity shopping"
    })

@ecommerce_bp.route('/ecommerce/markets', methods=['POST'])
def create_market():
    """Create a new market configuration"""
    data = request.get_json()
    
    try:
        market = Market(
            code=data['code'],
            name=data['name'],
            currency=data['currency'],
            currency_symbol=data['currency_symbol'],
            tax_rate=data.get('tax_rate', 0.0),
            shipping_base_cost=data.get('shipping_base_cost', 0.0),
            free_shipping_threshold=data.get('free_shipping_threshold', 0.0),
            payment_methods=json.dumps(data.get('payment_methods', [])),
            shipping_options=json.dumps(data.get('shipping_options', [])),
            preferences=json.dumps(data.get('preferences', {}))
        )
        
        db.session.add(market)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "market": market.to_dict(),
            "message": f"Market {market.name} created successfully!"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to create market"
        }), 400

@ecommerce_bp.route('/ecommerce/markets/<market_code>', methods=['GET'])
def get_market(market_code):
    """Get specific market details"""
    market = Market.query.filter_by(code=market_code.upper()).first()
    if not market:
        return jsonify({
            "success": False,
            "error": "Market not found",
            "message": f"Market {market_code} does not exist"
        }), 404
    
    return jsonify({
        "success": True,
        "market": market.to_dict(),
        "merchants_count": len(market.merchants),
        "message": f"Market details for {market.name}"
    })

# ============================================================================
# MERCHANT MANAGEMENT ENDPOINTS  
# ============================================================================

@ecommerce_bp.route('/ecommerce/merchants', methods=['GET'])
def get_merchants():
    """Get all merchants with optional market filtering"""
    market_code = request.args.get('market')
    
    query = Merchant.query
    if market_code:
        market = Market.query.filter_by(code=market_code.upper()).first()
        if market:
            query = query.filter_by(market_id=market.id)
    
    merchants = query.filter_by(is_active=True).all()
    
    return jsonify({
        "merchants": [merchant.to_dict() for merchant in merchants],
        "count": len(merchants),
        "market_filter": market_code,
        "message": f"Active merchants{' for ' + market_code if market_code else ''}"
    })

@ecommerce_bp.route('/ecommerce/merchants', methods=['POST'])
def create_merchant():
    """Create a new merchant"""
    data = request.get_json()
    
    try:
        # Find market
        market = Market.query.filter_by(code=data['market_code'].upper()).first()
        if not market:
            return jsonify({
                "success": False,
                "error": "Market not found",
                "message": f"Market {data['market_code']} does not exist"
            }), 400
        
        merchant = Merchant(
            name=data['name'],
            code=data['code'],
            market_id=market.id,
            website_url=data.get('website_url'),
            logo_url=data.get('logo_url'),
            description=data.get('description'),
            api_endpoint=data.get('api_endpoint'),
            integration_type=data.get('integration_type', 'affiliate'),
            supports_real_time_inventory=data.get('supports_real_time_inventory', False),
            supports_price_updates=data.get('supports_price_updates', False),
            supports_order_tracking=data.get('supports_order_tracking', False),
            commission_rate=data.get('commission_rate', 0.0)
        )
        
        db.session.add(merchant)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "merchant": merchant.to_dict(),
            "message": f"Merchant {merchant.name} created successfully!"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to create merchant"
        }), 400

# ============================================================================
# PRODUCT CATALOG ENDPOINTS
# ============================================================================

@ecommerce_bp.route('/ecommerce/products', methods=['GET'])
def get_products():
    """Get products with filtering and search"""
    # Query parameters
    market_code = request.args.get('market')
    merchant_code = request.args.get('merchant')
    category = request.args.get('category')
    search = request.args.get('search')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    
    # Build query
    query = Product.query.filter_by(is_active=True, is_in_stock=True)
    
    # Market filter
    if market_code:
        market = Market.query.filter_by(code=market_code.upper()).first()
        if market:
            merchant_ids = [m.id for m in market.merchants]
            query = query.filter(Product.merchant_id.in_(merchant_ids))
    
    # Merchant filter
    if merchant_code:
        merchant = Merchant.query.filter_by(code=merchant_code).first()
        if merchant:
            query = query.filter_by(merchant_id=merchant.id)
    
    # Category filter
    if category:
        query = query.filter_by(category=category)
    
    # Price range filter
    if min_price is not None:
        query = query.filter(
            db.or_(
                db.and_(Product.sale_price.isnot(None), Product.sale_price >= min_price),
                db.and_(Product.sale_price.is_(None), Product.original_price >= min_price)
            )
        )
    
    if max_price is not None:
        query = query.filter(
            db.or_(
                db.and_(Product.sale_price.isnot(None), Product.sale_price <= max_price),
                db.and_(Product.sale_price.is_(None), Product.original_price <= max_price)
            )
        )
    
    # Search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
                Product.brand.ilike(search_term),
                Product.tags.ilike(search_term)
            )
        )
    
    # Pagination
    products = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        "products": [product.to_dict() for product in products.items],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": products.total,
            "pages": products.pages,
            "has_next": products.has_next,
            "has_prev": products.has_prev
        },
        "filters": {
            "market": market_code,
            "merchant": merchant_code,
            "category": category,
            "search": search,
            "min_price": min_price,
            "max_price": max_price
        },
        "message": f"Found {products.total} products matching your criteria"
    })

@ecommerce_bp.route('/ecommerce/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get detailed product information"""
    product = Product.query.filter_by(id=product_id, is_active=True).first()
    if not product:
        return jsonify({
            "success": False,
            "error": "Product not found",
            "message": "Product does not exist or is not available"
        }), 404
    
    return jsonify({
        "success": True,
        "product": product.to_dict(),
        "merchant": product.merchant.to_dict(),
        "market": product.merchant.market.to_dict(),
        "message": f"Product details for {product.name}"
    })

# ============================================================================
# SHOPPING CART ENDPOINTS
# ============================================================================

@ecommerce_bp.route('/ecommerce/cart', methods=['GET'])
def get_cart():
    """Get user's shopping cart"""
    # In a real implementation, get user_id from JWT token
    user_id = request.args.get('user_id', type=int)
    market_code = request.args.get('market', 'US')
    
    if not user_id:
        return jsonify({
            "success": False,
            "error": "User ID required",
            "message": "Please provide user_id parameter"
        }), 400
    
    # Find market
    market = Market.query.filter_by(code=market_code.upper()).first()
    if not market:
        return jsonify({
            "success": False,
            "error": "Market not found",
            "message": f"Market {market_code} does not exist"
        }), 400
    
    # Find or create cart
    cart = ShoppingCart.query.filter_by(
        user_id=user_id, 
        market_id=market.id, 
        status='active'
    ).first()
    
    if not cart:
        cart = ShoppingCart(
            user_id=user_id,
            market_id=market.id,
            status='active'
        )
        db.session.add(cart)
        db.session.commit()
    
    # Calculate cart totals
    _calculate_cart_totals(cart)
    
    return jsonify({
        "success": True,
        "cart": cart.to_dict(),
        "items": [item.to_dict() for item in cart.items],
        "items_count": len(cart.items),
        "market": market.to_dict(),
        "message": f"Shopping cart for user {user_id} in {market.name}"
    })

@ecommerce_bp.route('/ecommerce/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to shopping cart"""
    data = request.get_json()
    
    try:
        user_id = data['user_id']
        product_id = data['product_id']
        quantity = data.get('quantity', 1)
        selected_color = data.get('selected_color')
        selected_size = data.get('selected_size')
        market_code = data.get('market', 'US')
        
        # Find market
        market = Market.query.filter_by(code=market_code.upper()).first()
        if not market:
            return jsonify({
                "success": False,
                "error": "Market not found",
                "message": f"Market {market_code} does not exist"
            }), 400
        
        # Find product
        product = Product.query.filter_by(id=product_id, is_active=True, is_in_stock=True).first()
        if not product:
            return jsonify({
                "success": False,
                "error": "Product not found or out of stock",
                "message": "Product is not available"
            }), 400
        
        # Find or create cart
        cart = ShoppingCart.query.filter_by(
            user_id=user_id,
            market_id=market.id,
            status='active'
        ).first()
        
        if not cart:
            cart = ShoppingCart(
                user_id=user_id,
                market_id=market.id,
                status='active'
            )
            db.session.add(cart)
            db.session.flush()  # Get cart ID
        
        # Check if item already exists in cart
        existing_item = CartItem.query.filter_by(
            cart_id=cart.id,
            product_id=product_id,
            selected_color=selected_color,
            selected_size=selected_size
        ).first()
        
        current_price = product.sale_price if product.sale_price else product.original_price
        
        if existing_item:
            # Update quantity
            existing_item.quantity += quantity
            existing_item.total_price = existing_item.quantity * current_price
            existing_item.updated_at = datetime.utcnow()
            cart_item = existing_item
        else:
            # Create new cart item
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
                selected_color=selected_color,
                selected_size=selected_size,
                unit_price=current_price,
                total_price=quantity * current_price
            )
            db.session.add(cart_item)
        
        db.session.commit()
        
        # Recalculate cart totals
        _calculate_cart_totals(cart)
        
        return jsonify({
            "success": True,
            "cart_item": cart_item.to_dict(),
            "cart": cart.to_dict(),
            "message": f"Added {product.name} to cart successfully!"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to add item to cart"
        }), 400

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _calculate_cart_totals(cart):
    """Calculate cart totals"""
    subtotal = sum(item.total_price for item in cart.items)
    tax_amount = subtotal * cart.market.tax_rate
    
    # Free shipping logic
    if subtotal >= cart.market.free_shipping_threshold:
        shipping_cost = 0.0
    else:
        shipping_cost = cart.market.shipping_base_cost
    
    total_amount = subtotal + tax_amount + shipping_cost - cart.discount_amount
    
    cart.subtotal = subtotal
    cart.tax_amount = tax_amount
    cart.shipping_cost = shipping_cost
    cart.total_amount = total_amount
    cart.updated_at = datetime.utcnow()
    
    db.session.commit()
    return cart

# ============================================================================
# INTEGRATION WITH OTHER WORKSTREAMS
# ============================================================================

@ecommerce_bp.route('/ecommerce/integration/ws1-user', methods=['POST'])
def verify_ws1_user():
    """Verify user with WS1 User Management service"""
    data = request.get_json()
    user_id = data.get('user_id')
    jwt_token = data.get('jwt_token')
    
    try:
        # Call WS1 service to verify user
        ws1_url = "http://localhost:5001/api/user/profile"  # WS1 service URL
        headers = {"Authorization": f"Bearer {jwt_token}"}
        
        response = requests.get(ws1_url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            user_data = response.json()
            return jsonify({
                "success": True,
                "user_verified": True,
                "user_data": user_data,
                "message": "User verified with WS1 successfully"
            })
        else:
            return jsonify({
                "success": False,
                "user_verified": False,
                "error": "User verification failed",
                "message": "Could not verify user with WS1"
            }), 401
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "user_verified": False,
            "error": "WS1 service unavailable",
            "message": "Could not connect to WS1 User Management service"
        }), 503

@ecommerce_bp.route('/ecommerce/integration/ws2-recommendations', methods=['POST'])
def get_ai_product_recommendations():
    """Get AI-powered product recommendations from WS2"""
    data = request.get_json()
    user_id = data.get('user_id')
    occasion = data.get('occasion', 'casual')
    budget_max = data.get('budget_max')
    
    try:
        # Call WS2 AI service for outfit recommendations
        ws2_url = "http://localhost:5002/api/personalized/personalized-outfit"
        payload = {
            "user_id": user_id,
            "occasion": occasion,
            "budget_max": budget_max
        }
        
        response = requests.post(ws2_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            ai_recommendations = response.json()
            
            # Convert AI recommendations to product suggestions
            # This would map AI outfit suggestions to actual products in our catalog
            suggested_products = []
            
            return jsonify({
                "success": True,
                "ai_recommendations": ai_recommendations,
                "suggested_products": suggested_products,
                "message": "AI-powered product recommendations ready!"
            })
        else:
            return jsonify({
                "success": False,
                "error": "AI recommendations unavailable",
                "message": "Could not get recommendations from WS2"
            }), 503
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": "WS2 service unavailable", 
            "message": "Could not connect to WS2 AI Styling service"
        }), 503

