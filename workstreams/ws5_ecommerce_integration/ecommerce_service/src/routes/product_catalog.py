from flask import Blueprint, request, jsonify
from src.models.ecommerce_models import db, Product, Merchant, Market
from src.models.product_catalog import (
    ProductCategory, ProductBrand, ProductReview, ProductInventory, 
    ProductRecommendation, ProductCollection, CollectionProduct
)
import json
import requests
from datetime import datetime, timedelta
from sqlalchemy import func, desc, asc, or_, and_

product_catalog_bp = Blueprint('product_catalog', __name__)

# ============================================================================
# PRODUCT CATALOG MANAGEMENT ENDPOINTS
# ============================================================================

@product_catalog_bp.route('/catalog/health', methods=['GET'])
def catalog_health_check():
    """Health check for product catalog service"""
    return jsonify({
        "status": "healthy",
        "service": "WS5: Product Catalog & Merchant Integration",
        "version": "2.0.0",
        "tagline": "We girls have no time",
        "philosophy": "Instant product discovery for busy women",
        "features": [
            "Advanced product search & filtering",
            "Intelligent product recommendations",
            "Multi-market inventory management",
            "Curated product collections",
            "Brand and category management",
            "Product reviews and ratings",
            "Real-time inventory tracking"
        ],
        "catalog_stats": {
            "total_products": Product.query.filter_by(is_active=True).count(),
            "total_brands": ProductBrand.query.filter_by(is_active=True).count(),
            "total_categories": ProductCategory.query.filter_by(is_active=True).count(),
            "total_collections": ProductCollection.query.filter_by(is_active=True).count(),
            "in_stock_products": Product.query.filter_by(is_active=True, is_in_stock=True).count()
        },
        "message": "Advanced product catalog ready for lightning-fast shopping!"
    })

@product_catalog_bp.route('/catalog/search', methods=['GET'])
def advanced_product_search():
    """Advanced product search with multiple filters"""
    # Query parameters
    query = request.args.get('q', '').strip()
    market_code = request.args.get('market', 'US')
    category_code = request.args.get('category')
    brand_code = request.args.get('brand')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    colors = request.args.getlist('color')
    sizes = request.args.getlist('size')
    style_tags = request.args.getlist('style')
    occasion_tags = request.args.getlist('occasion')
    sort_by = request.args.get('sort', 'relevance')  # relevance, price_low, price_high, newest, rating
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 24, type=int), 100)
    
    # Build base query
    query_obj = Product.query.filter_by(is_active=True, is_in_stock=True)
    
    # Market filter
    if market_code:
        market = Market.query.filter_by(code=market_code.upper()).first()
        if market:
            merchant_ids = [m.id for m in market.merchants if m.is_active]
            query_obj = query_obj.filter(Product.merchant_id.in_(merchant_ids))
    
    # Text search
    if query:
        search_term = f"%{query}%"
        query_obj = query_obj.filter(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
                Product.brand.ilike(search_term),
                Product.tags.ilike(search_term),
                Product.search_keywords.ilike(search_term)
            )
        )
    
    # Category filter
    if category_code:
        category = ProductCategory.query.filter_by(code=category_code, is_active=True).first()
        if category:
            query_obj = query_obj.filter(Product.category == category.name)
    
    # Brand filter
    if brand_code:
        brand = ProductBrand.query.filter_by(code=brand_code, is_active=True).first()
        if brand:
            query_obj = query_obj.filter(Product.brand == brand.name)
    
    # Price range filter
    if min_price is not None:
        query_obj = query_obj.filter(
            or_(
                and_(Product.sale_price.isnot(None), Product.sale_price >= min_price),
                and_(Product.sale_price.is_(None), Product.original_price >= min_price)
            )
        )
    
    if max_price is not None:
        query_obj = query_obj.filter(
            or_(
                and_(Product.sale_price.isnot(None), Product.sale_price <= max_price),
                and_(Product.sale_price.is_(None), Product.original_price <= max_price)
            )
        )
    
    # Color filter
    if colors:
        color_filters = []
        for color in colors:
            color_filters.append(Product.colors.ilike(f'%"{color}"%'))
        query_obj = query_obj.filter(or_(*color_filters))
    
    # Size filter
    if sizes:
        size_filters = []
        for size in sizes:
            size_filters.append(Product.sizes.ilike(f'%"{size}"%'))
        query_obj = query_obj.filter(or_(*size_filters))
    
    # Style tags filter
    if style_tags:
        style_filters = []
        for style in style_tags:
            style_filters.append(Product.style_tags.ilike(f'%"{style}"%'))
        query_obj = query_obj.filter(or_(*style_filters))
    
    # Occasion tags filter
    if occasion_tags:
        occasion_filters = []
        for occasion in occasion_tags:
            occasion_filters.append(Product.occasion_tags.ilike(f'%"{occasion}"%'))
        query_obj = query_obj.filter(or_(*occasion_filters))
    
    # Sorting
    if sort_by == 'price_low':
        query_obj = query_obj.order_by(
            func.coalesce(Product.sale_price, Product.original_price).asc()
        )
    elif sort_by == 'price_high':
        query_obj = query_obj.order_by(
            func.coalesce(Product.sale_price, Product.original_price).desc()
        )
    elif sort_by == 'newest':
        query_obj = query_obj.order_by(Product.created_at.desc())
    elif sort_by == 'rating':
        # Join with reviews to sort by average rating
        query_obj = query_obj.outerjoin(ProductReview).group_by(Product.id).order_by(
            func.coalesce(func.avg(ProductReview.rating), 0).desc()
        )
    else:  # relevance (default)
        query_obj = query_obj.order_by(Product.created_at.desc())
    
    # Pagination
    products = query_obj.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Get filter options for the current search
    filter_options = _get_filter_options(market_code, query)
    
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
        "filters_applied": {
            "query": query,
            "market": market_code,
            "category": category_code,
            "brand": brand_code,
            "min_price": min_price,
            "max_price": max_price,
            "colors": colors,
            "sizes": sizes,
            "style_tags": style_tags,
            "occasion_tags": occasion_tags,
            "sort_by": sort_by
        },
        "filter_options": filter_options,
        "search_time": "< 100ms",
        "message": f"Found {products.total} products matching your search - 'We girls have no time' so here are instant results!"
    })

@product_catalog_bp.route('/catalog/categories', methods=['GET'])
def get_product_categories():
    """Get product category hierarchy"""
    include_products_count = request.args.get('include_count', 'false').lower() == 'true'
    market_code = request.args.get('market')
    
    # Get root categories (no parent)
    root_categories = ProductCategory.query.filter_by(parent_id=None, is_active=True).order_by(ProductCategory.sort_order).all()
    
    def build_category_tree(categories):
        result = []
        for category in categories:
            category_dict = category.to_dict()
            
            # Add product count if requested
            if include_products_count:
                product_count = Product.query.filter_by(category=category.name, is_active=True).count()
                category_dict['product_count'] = product_count
            
            # Add children recursively
            if category.children:
                category_dict['children'] = build_category_tree(
                    sorted(category.children, key=lambda x: x.sort_order)
                )
            
            result.append(category_dict)
        
        return result
    
    category_tree = build_category_tree(root_categories)
    
    return jsonify({
        "categories": category_tree,
        "total_categories": ProductCategory.query.filter_by(is_active=True).count(),
        "market_filter": market_code,
        "message": "Product category hierarchy for easy navigation"
    })

@product_catalog_bp.route('/catalog/brands', methods=['GET'])
def get_product_brands():
    """Get product brands with filtering options"""
    market_code = request.args.get('market')
    price_range = request.args.get('price_range')  # budget, mid-range, premium, luxury
    style_category = request.args.get('style_category')  # fast-fashion, sustainable, luxury
    include_products_count = request.args.get('include_count', 'false').lower() == 'true'
    sort_by = request.args.get('sort', 'popularity')  # popularity, name, rating
    
    # Build query
    query_obj = ProductBrand.query.filter_by(is_active=True)
    
    if price_range:
        query_obj = query_obj.filter_by(price_range=price_range)
    
    if style_category:
        query_obj = query_obj.filter_by(style_category=style_category)
    
    # Sorting
    if sort_by == 'name':
        query_obj = query_obj.order_by(ProductBrand.name.asc())
    elif sort_by == 'rating':
        query_obj = query_obj.order_by(ProductBrand.quality_rating.desc())
    else:  # popularity
        query_obj = query_obj.order_by(ProductBrand.popularity_score.desc())
    
    brands = query_obj.all()
    
    # Add product counts if requested
    brands_data = []
    for brand in brands:
        brand_dict = brand.to_dict()
        
        if include_products_count:
            product_count = Product.query.filter_by(brand=brand.name, is_active=True, is_in_stock=True).count()
            brand_dict['product_count'] = product_count
        
        brands_data.append(brand_dict)
    
    return jsonify({
        "brands": brands_data,
        "total_brands": len(brands),
        "filter_options": {
            "price_ranges": ['budget', 'mid-range', 'premium', 'luxury'],
            "style_categories": ['fast-fashion', 'sustainable', 'luxury', 'designer', 'indie']
        },
        "filters_applied": {
            "market": market_code,
            "price_range": price_range,
            "style_category": style_category,
            "sort_by": sort_by
        },
        "message": "Product brands for targeted shopping"
    })

# ============================================================================
# PRODUCT RECOMMENDATIONS ENDPOINTS
# ============================================================================

@product_catalog_bp.route('/catalog/recommendations/<int:user_id>', methods=['GET'])
def get_user_recommendations(user_id):
    """Get personalized product recommendations for user"""
    recommendation_type = request.args.get('type', 'personalized')  # ai_styling, similar_items, trending, personalized
    market_code = request.args.get('market', 'US')
    limit = min(request.args.get('limit', 20, type=int), 50)
    
    # Get active recommendations for user
    query_obj = ProductRecommendation.query.filter_by(
        user_id=user_id,
        is_active=True
    ).filter(
        or_(
            ProductRecommendation.expires_at.is_(None),
            ProductRecommendation.expires_at > datetime.utcnow()
        )
    )
    
    if recommendation_type != 'all':
        query_obj = query_obj.filter_by(recommendation_type=recommendation_type)
    
    # Join with products to ensure they're still available
    recommendations = query_obj.join(Product).filter(
        Product.is_active == True,
        Product.is_in_stock == True
    ).order_by(
        ProductRecommendation.confidence_score.desc(),
        ProductRecommendation.created_at.desc()
    ).limit(limit).all()
    
    # If no recommendations exist, generate some basic ones
    if not recommendations:
        recommendations = _generate_basic_recommendations(user_id, market_code, limit)
    
    # Track that recommendations were shown
    for rec in recommendations:
        rec.shown_count += 1
    db.session.commit()
    
    return jsonify({
        "recommendations": [rec.to_dict() for rec in recommendations],
        "user_id": user_id,
        "recommendation_type": recommendation_type,
        "market": market_code,
        "count": len(recommendations),
        "message": f"Personalized recommendations for user {user_id} - 'We girls have no time' so here's what you'll love!"
    })

@product_catalog_bp.route('/catalog/recommendations/<int:recommendation_id>/track', methods=['POST'])
def track_recommendation_interaction(recommendation_id):
    """Track user interaction with recommendation"""
    data = request.get_json()
    interaction_type = data.get('interaction_type')  # 'click', 'purchase', 'dismiss'
    
    recommendation = ProductRecommendation.query.get(recommendation_id)
    if not recommendation:
        return jsonify({
            "success": False,
            "error": "Recommendation not found"
        }), 404
    
    # Update interaction counts
    if interaction_type == 'click':
        recommendation.clicked_count += 1
    elif interaction_type == 'purchase':
        recommendation.purchased_count += 1
        recommendation.clicked_count += 1  # Assume they clicked before purchasing
    elif interaction_type == 'dismiss':
        recommendation.is_active = False
    
    recommendation.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        "success": True,
        "recommendation": recommendation.to_dict(),
        "message": f"Tracked {interaction_type} interaction successfully"
    })

# ============================================================================
# PRODUCT COLLECTIONS ENDPOINTS
# ============================================================================

@product_catalog_bp.route('/catalog/collections', methods=['GET'])
def get_product_collections():
    """Get curated product collections"""
    market_code = request.args.get('market', 'US')
    collection_type = request.args.get('type')  # seasonal, occasion, style, trending
    featured_only = request.args.get('featured', 'false').lower() == 'true'
    include_products = request.args.get('include_products', 'false').lower() == 'true'
    
    # Build query
    query_obj = ProductCollection.query.filter_by(is_active=True)
    
    # Market filter
    if market_code:
        query_obj = query_obj.filter(
            or_(
                ProductCollection.target_market == market_code.upper(),
                ProductCollection.target_market == 'ALL'
            )
        )
    
    if collection_type:
        query_obj = query_obj.filter_by(collection_type=collection_type)
    
    if featured_only:
        query_obj = query_obj.filter_by(is_featured=True)
    
    # Filter by current date for time-based collections
    now = datetime.utcnow()
    query_obj = query_obj.filter(
        or_(
            ProductCollection.start_date.is_(None),
            ProductCollection.start_date <= now
        )
    ).filter(
        or_(
            ProductCollection.end_date.is_(None),
            ProductCollection.end_date >= now
        )
    )
    
    collections = query_obj.order_by(
        ProductCollection.sort_order.asc(),
        ProductCollection.created_at.desc()
    ).all()
    
    collections_data = []
    for collection in collections:
        collection_dict = collection.to_dict()
        
        if include_products:
            # Get products in this collection
            collection_products = CollectionProduct.query.filter_by(
                collection_id=collection.id
            ).join(Product).filter(
                Product.is_active == True,
                Product.is_in_stock == True
            ).order_by(CollectionProduct.sort_order.asc()).limit(12).all()
            
            collection_dict['products'] = [cp.product.to_dict() for cp in collection_products]
            collection_dict['product_count'] = len(collection_products)
        
        collections_data.append(collection_dict)
    
    return jsonify({
        "collections": collections_data,
        "total_collections": len(collections),
        "filters_applied": {
            "market": market_code,
            "type": collection_type,
            "featured_only": featured_only
        },
        "message": "Curated collections for instant style inspiration"
    })

@product_catalog_bp.route('/catalog/collections/<collection_code>', methods=['GET'])
def get_collection_details(collection_code):
    """Get detailed collection information with products"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 24, type=int), 100)
    
    collection = ProductCollection.query.filter_by(code=collection_code, is_active=True).first()
    if not collection:
        return jsonify({
            "success": False,
            "error": "Collection not found",
            "message": f"Collection '{collection_code}' does not exist"
        }), 404
    
    # Get products in collection with pagination
    collection_products_query = CollectionProduct.query.filter_by(
        collection_id=collection.id
    ).join(Product).filter(
        Product.is_active == True,
        Product.is_in_stock == True
    ).order_by(CollectionProduct.sort_order.asc())
    
    collection_products = collection_products_query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        "collection": collection.to_dict(),
        "products": [cp.product.to_dict() for cp in collection_products.items],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": collection_products.total,
            "pages": collection_products.pages,
            "has_next": collection_products.has_next,
            "has_prev": collection_products.has_prev
        },
        "message": f"Collection '{collection.name}' with {collection_products.total} products"
    })

# ============================================================================
# INVENTORY MANAGEMENT ENDPOINTS
# ============================================================================

@product_catalog_bp.route('/catalog/inventory/<int:product_id>', methods=['GET'])
def get_product_inventory(product_id):
    """Get detailed inventory information for a product"""
    product = Product.query.filter_by(id=product_id, is_active=True).first()
    if not product:
        return jsonify({
            "success": False,
            "error": "Product not found"
        }), 404
    
    # Get all inventory variants for this product
    inventory_variants = ProductInventory.query.filter_by(
        product_id=product_id,
        is_active=True
    ).all()
    
    # Calculate total inventory
    total_available = sum(inv.quantity_available for inv in inventory_variants)
    total_reserved = sum(inv.quantity_reserved for inv in inventory_variants)
    low_stock_variants = [inv for inv in inventory_variants if inv.quantity_available <= inv.low_stock_threshold]
    
    return jsonify({
        "product": product.to_dict(),
        "inventory_summary": {
            "total_available": total_available,
            "total_reserved": total_reserved,
            "total_variants": len(inventory_variants),
            "low_stock_variants": len(low_stock_variants),
            "is_low_stock": len(low_stock_variants) > 0,
            "is_out_of_stock": total_available == 0
        },
        "inventory_variants": [inv.to_dict() for inv in inventory_variants],
        "low_stock_alerts": [inv.to_dict() for inv in low_stock_variants],
        "message": f"Inventory details for {product.name}"
    })

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _get_filter_options(market_code, search_query):
    """Get available filter options for current search context"""
    # This would typically be cached for performance
    base_query = Product.query.filter_by(is_active=True, is_in_stock=True)
    
    if market_code:
        market = Market.query.filter_by(code=market_code.upper()).first()
        if market:
            merchant_ids = [m.id for m in market.merchants if m.is_active]
            base_query = base_query.filter(Product.merchant_id.in_(merchant_ids))
    
    # Get available categories
    categories = db.session.query(Product.category).filter(
        Product.id.in_(base_query.with_entities(Product.id))
    ).distinct().all()
    
    # Get available brands
    brands = db.session.query(Product.brand).filter(
        Product.id.in_(base_query.with_entities(Product.id))
    ).distinct().all()
    
    # Get price range
    price_range = db.session.query(
        func.min(func.coalesce(Product.sale_price, Product.original_price)),
        func.max(func.coalesce(Product.sale_price, Product.original_price))
    ).filter(Product.id.in_(base_query.with_entities(Product.id))).first()
    
    return {
        "categories": [cat[0] for cat in categories if cat[0]],
        "brands": [brand[0] for brand in brands if brand[0]],
        "price_range": {
            "min": float(price_range[0]) if price_range[0] else 0,
            "max": float(price_range[1]) if price_range[1] else 1000
        },
        "colors": ["black", "white", "blue", "red", "pink", "green", "yellow", "purple", "brown", "gray"],
        "sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "style_tags": ["casual", "formal", "elegant", "trendy", "classic", "bohemian", "minimalist"],
        "occasion_tags": ["work", "party", "date-night", "casual", "formal", "weekend"]
    }

def _generate_basic_recommendations(user_id, market_code, limit):
    """Generate basic recommendations when none exist"""
    # Get trending products from the market
    market = Market.query.filter_by(code=market_code.upper()).first()
    if not market:
        return []
    
    merchant_ids = [m.id for m in market.merchants if m.is_active]
    
    # Get recent popular products
    trending_products = Product.query.filter(
        Product.merchant_id.in_(merchant_ids),
        Product.is_active == True,
        Product.is_in_stock == True
    ).order_by(Product.created_at.desc()).limit(limit).all()
    
    # Create basic recommendations
    recommendations = []
    for product in trending_products:
        rec = ProductRecommendation(
            user_id=user_id,
            product_id=product.id,
            recommendation_type='trending',
            confidence_score=0.7,
            context=json.dumps({"reason": "trending_product", "market": market_code}),
            reasoning=f"This {product.name} is trending in {market.name}",
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        db.session.add(rec)
        recommendations.append(rec)
    
    db.session.commit()
    return recommendations

