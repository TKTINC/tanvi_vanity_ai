#!/usr/bin/env python3
"""
Test script for WS5-P2: Product Catalog & Merchant Integration
Tests advanced product catalog and merchant integration features
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.ecommerce_models import db, Market, Merchant, Product
from src.models.product_catalog import (
    ProductCategory, ProductBrand, ProductReview, ProductInventory,
    ProductRecommendation, ProductCollection, CollectionProduct
)
from src.models.merchant_integration import MerchantAPI, ProductSync, MerchantWebhook
from flask import Flask
import json
from datetime import datetime, timedelta

def create_test_app():
    """Create test Flask app and test WS5-P2 features"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_ws5_p2.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        print("🚀 Testing WS5-P2: Product Catalog & Merchant Integration")
        print("🎯 Tagline: 'We girls have no time' - Advanced catalog features!")
        
        # Test product categories
        test_product_categories()
        
        # Test product brands
        test_product_brands()
        
        # Test product collections
        test_product_collections()
        
        # Test merchant API configuration
        test_merchant_api_config()
        
        # Test product recommendations
        test_product_recommendations()
        
        # Test inventory management
        test_inventory_management()
        
        print("\n🎉 All WS5-P2 tests passed!")
        print("🛍️ Advanced product catalog and merchant integration ready!")

def test_product_categories():
    """Test product category hierarchy"""
    print("\n📂 Testing Product Categories...")
    
    # Create main categories
    clothing = ProductCategory(
        name='Clothing',
        code='clothing',
        description='All clothing items',
        sort_order=1,
        attributes=json.dumps({
            'size_types': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
            'color_families': ['neutral', 'bright', 'pastel', 'dark']
        })
    )
    
    accessories = ProductCategory(
        name='Accessories',
        code='accessories',
        description='Fashion accessories',
        sort_order=2
    )
    
    db.session.add(clothing)
    db.session.add(accessories)
    db.session.flush()  # Get IDs
    
    # Create subcategories
    dresses = ProductCategory(
        name='Dresses',
        code='dresses',
        parent_id=clothing.id,
        description='All types of dresses',
        sort_order=1
    )
    
    tops = ProductCategory(
        name='Tops',
        code='tops',
        parent_id=clothing.id,
        description='Shirts, blouses, and tops',
        sort_order=2
    )
    
    db.session.add(dresses)
    db.session.add(tops)
    db.session.commit()
    
    print(f"✅ Created category hierarchy: {clothing.name} with {len(clothing.children)} subcategories")
    print(f"   - {dresses.name} (parent: {dresses.parent.name})")
    print(f"   - {tops.name} (parent: {tops.parent.name})")

def test_product_brands():
    """Test product brand management"""
    print("\n🏷️ Testing Product Brands...")
    
    # Create brands for different markets
    zara = ProductBrand(
        name='Zara',
        code='zara',
        description='Spanish fast fashion retailer',
        price_range='mid-range',
        target_demographic='young-adults',
        style_category='fast-fashion',
        popularity_score=8.5,
        quality_rating=7.8
    )
    
    libas = ProductBrand(
        name='Libas',
        code='libas',
        description='Indian ethnic wear brand',
        price_range='budget',
        target_demographic='women',
        style_category='ethnic',
        popularity_score=7.2,
        quality_rating=8.0
    )
    
    db.session.add(zara)
    db.session.add(libas)
    db.session.commit()
    
    print(f"✅ Created brands:")
    print(f"   - {zara.name}: {zara.price_range}, {zara.style_category} (Rating: {zara.quality_rating})")
    print(f"   - {libas.name}: {libas.price_range}, {libas.style_category} (Rating: {libas.quality_rating})")

def test_product_collections():
    """Test curated product collections"""
    print("\n📦 Testing Product Collections...")
    
    # Create seasonal collection
    summer_collection = ProductCollection(
        name='Summer Essentials 2024',
        code='summer_2024',
        description='Must-have pieces for summer',
        collection_type='seasonal',
        target_market='ALL',
        tags=json.dumps(['summer', 'essentials', 'trending']),
        style_attributes=json.dumps({
            'target_age': '18-35',
            'style_type': 'casual-chic',
            'season': 'summer'
        }),
        is_featured=True,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=90)
    )
    
    # Create work wardrobe collection
    work_collection = ProductCollection(
        name='Professional Wardrobe',
        code='work_wardrobe',
        description='Essential pieces for the modern working woman',
        collection_type='occasion',
        target_market='US',
        tags=json.dumps(['work', 'professional', 'office']),
        style_attributes=json.dumps({
            'target_age': '25-45',
            'style_type': 'professional',
            'occasion': 'work'
        }),
        is_featured=True
    )
    
    db.session.add(summer_collection)
    db.session.add(work_collection)
    db.session.commit()
    
    print(f"✅ Created collections:")
    print(f"   - {summer_collection.name}: {summer_collection.collection_type} ({summer_collection.target_market})")
    print(f"   - {work_collection.name}: {work_collection.collection_type} ({work_collection.target_market})")

def test_merchant_api_config():
    """Test merchant API configuration"""
    print("\n🔌 Testing Merchant API Configuration...")
    
    # Get existing merchants from WS5-P1
    zara_us = Merchant.query.filter_by(code='zara_us').first()
    myntra = Merchant.query.filter_by(code='myntra').first()
    
    if not zara_us or not myntra:
        print("⚠️ Creating test merchants...")
        # Create markets first
        us_market = Market(
            code='US', name='United States', currency='USD', currency_symbol='$'
        )
        india_market = Market(
            code='IN', name='India', currency='INR', currency_symbol='₹'
        )
        db.session.add(us_market)
        db.session.add(india_market)
        db.session.flush()
        
        # Create merchants
        zara_us = Merchant(
            name='Zara USA', code='zara_us', market_id=us_market.id,
            integration_type='api', commission_rate=0.05
        )
        myntra = Merchant(
            name='Myntra', code='myntra', market_id=india_market.id,
            integration_type='api', commission_rate=0.08
        )
        db.session.add(zara_us)
        db.session.add(myntra)
        db.session.flush()
    
    # Create API configurations
    zara_api = MerchantAPI(
        merchant_id=zara_us.id,
        api_name='Zara REST API',
        base_url='https://api.zara.com/v1',
        auth_type='api_key',
        api_key='zara_test_key_123',
        supports_product_sync=True,
        supports_inventory_sync=True,
        supports_price_sync=True,
        rate_limit_per_minute=100,
        rate_limit_per_hour=5000
    )
    
    myntra_api = MerchantAPI(
        merchant_id=myntra.id,
        api_name='Myntra Partner API',
        base_url='https://api.myntra.com/partner/v2',
        auth_type='bearer',
        access_token='myntra_bearer_token_456',
        supports_product_sync=True,
        supports_inventory_sync=True,
        supports_order_creation=True,
        supports_webhooks=True,
        rate_limit_per_minute=200,
        rate_limit_per_hour=10000
    )
    
    db.session.add(zara_api)
    db.session.add(myntra_api)
    db.session.commit()
    
    print(f"✅ Created API configurations:")
    print(f"   - {zara_api.api_name}: {zara_api.auth_type}, {zara_api.rate_limit_per_minute}/min")
    print(f"   - {myntra_api.api_name}: {myntra_api.auth_type}, {myntra_api.rate_limit_per_minute}/min")

def test_product_recommendations():
    """Test AI-powered product recommendations"""
    print("\n🤖 Testing Product Recommendations...")
    
    # Create test product first
    zara_us = Merchant.query.filter_by(code='zara_us').first()
    if zara_us:
        test_product = Product(
            merchant_id=zara_us.id,
            sku='TEST-DRESS-001',
            name='Black Work Dress',
            description='Professional black dress for office wear',
            brand='Zara',
            category='dresses',
            original_price=89.90,
            currency='USD',
            colors=json.dumps(['black', 'navy']),
            sizes=json.dumps(['S', 'M', 'L']),
            style_tags=json.dumps(['professional', 'elegant']),
            occasion_tags=json.dumps(['work', 'meeting']),
            stock_quantity=15,
            is_in_stock=True
        )
        db.session.add(test_product)
        db.session.flush()
        
        # Create recommendations for test user
        ai_recommendation = ProductRecommendation(
            user_id=1,
            product_id=test_product.id,
            recommendation_type='ai_styling',
            confidence_score=0.92,
            context=json.dumps({
                'occasion': 'work',
                'style_preference': 'professional',
                'budget_range': '50-100'
            }),
            reasoning='Perfect for professional settings based on your style profile',
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        
        trending_recommendation = ProductRecommendation(
            user_id=1,
            product_id=test_product.id,
            recommendation_type='trending',
            confidence_score=0.78,
            context=json.dumps({
                'trend_factor': 'high',
                'market': 'US'
            }),
            reasoning='Trending among professional women in your area',
            expires_at=datetime.utcnow() + timedelta(days=3)
        )
        
        db.session.add(ai_recommendation)
        db.session.add(trending_recommendation)
        db.session.commit()
        
        print(f"✅ Created recommendations for user 1:")
        print(f"   - AI Styling: {ai_recommendation.confidence_score:.1%} confidence")
        print(f"   - Trending: {trending_recommendation.confidence_score:.1%} confidence")

def test_inventory_management():
    """Test detailed inventory tracking"""
    print("\n📦 Testing Inventory Management...")
    
    # Get test product
    test_product = Product.query.filter_by(sku='TEST-DRESS-001').first()
    if test_product:
        # Create inventory variants
        black_s = ProductInventory(
            product_id=test_product.id,
            color='black',
            size='S',
            sku_variant='TEST-DRESS-001-BLACK-S',
            quantity_available=5,
            quantity_reserved=2,
            low_stock_threshold=3,
            reorder_point=5
        )
        
        black_m = ProductInventory(
            product_id=test_product.id,
            color='black',
            size='M',
            sku_variant='TEST-DRESS-001-BLACK-M',
            quantity_available=8,
            quantity_reserved=1,
            low_stock_threshold=3,
            reorder_point=5
        )
        
        navy_l = ProductInventory(
            product_id=test_product.id,
            color='navy',
            size='L',
            sku_variant='TEST-DRESS-001-NAVY-L',
            quantity_available=2,  # Low stock
            quantity_reserved=0,
            low_stock_threshold=3,
            reorder_point=5
        )
        
        db.session.add(black_s)
        db.session.add(black_m)
        db.session.add(navy_l)
        db.session.commit()
        
        # Calculate inventory summary
        total_available = black_s.quantity_available + black_m.quantity_available + navy_l.quantity_available
        low_stock_variants = [inv for inv in [black_s, black_m, navy_l] if inv.quantity_available <= inv.low_stock_threshold]
        
        print(f"✅ Created inventory variants:")
        print(f"   - Total available: {total_available} units across 3 variants")
        print(f"   - Low stock alerts: {len(low_stock_variants)} variants")
        print(f"   - Black S: {black_s.quantity_available} available, {black_s.quantity_reserved} reserved")
        print(f"   - Navy L: {navy_l.quantity_available} available (⚠️ Low stock)")

if __name__ == '__main__':
    create_test_app()

