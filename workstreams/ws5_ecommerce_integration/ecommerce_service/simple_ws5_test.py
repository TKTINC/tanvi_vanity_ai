#!/usr/bin/env python3
"""
Simple test script for WS5 E-commerce Integration
Tests core functionality without running the full Flask server
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.ecommerce_models import db, Market, Merchant, Product, ShoppingCart, CartItem
from flask import Flask
import json

def create_test_app():
    """Create a test Flask app with database"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_ecommerce.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        print("✅ Database tables created successfully!")
        
        # Test market creation
        test_market_creation()
        
        # Test merchant creation
        test_merchant_creation()
        
        # Test product creation
        test_product_creation()
        
        # Test shopping cart
        test_shopping_cart()
        
        print("\n🎉 All WS5 E-commerce tests passed!")
        print("🛍️ 'We girls have no time' - E-commerce foundation is ready!")

def test_market_creation():
    """Test market creation for US and India"""
    print("\n📍 Testing Market Creation...")
    
    # Create US market
    us_market = Market(
        code='US',
        name='United States',
        currency='USD',
        currency_symbol='$',
        tax_rate=0.08,
        shipping_base_cost=5.99,
        free_shipping_threshold=50.0,
        payment_methods=json.dumps(['Credit Card', 'PayPal', 'Apple Pay', 'Google Pay']),
        shipping_options=json.dumps(['Same-day', 'Next-day', 'Standard']),
        preferences=json.dumps({'default_language': 'en', 'measurement_unit': 'imperial'})
    )
    
    # Create India market
    india_market = Market(
        code='IN',
        name='India',
        currency='INR',
        currency_symbol='₹',
        tax_rate=0.18,
        shipping_base_cost=50.0,
        free_shipping_threshold=999.0,
        payment_methods=json.dumps(['UPI', 'Paytm', 'Credit Card', 'Net Banking', 'COD']),
        shipping_options=json.dumps(['Same-day (Metro)', 'Express', 'Standard', 'COD']),
        preferences=json.dumps({'default_language': 'en', 'measurement_unit': 'metric'})
    )
    
    db.session.add(us_market)
    db.session.add(india_market)
    db.session.commit()
    
    print(f"✅ Created US market: {us_market.name} ({us_market.currency})")
    print(f"✅ Created India market: {india_market.name} ({india_market.currency})")

def test_merchant_creation():
    """Test merchant creation for both markets"""
    print("\n🏪 Testing Merchant Creation...")
    
    us_market = Market.query.filter_by(code='US').first()
    india_market = Market.query.filter_by(code='IN').first()
    
    # US merchants
    zara_us = Merchant(
        name='Zara USA',
        code='zara_us',
        market_id=us_market.id,
        website_url='https://www.zara.com/us',
        description='Fast fashion retailer',
        integration_type='affiliate',
        commission_rate=0.05
    )
    
    # India merchants
    myntra = Merchant(
        name='Myntra',
        code='myntra',
        market_id=india_market.id,
        website_url='https://www.myntra.com',
        description='Leading fashion e-commerce platform in India',
        integration_type='api',
        commission_rate=0.08
    )
    
    db.session.add(zara_us)
    db.session.add(myntra)
    db.session.commit()
    
    print(f"✅ Created US merchant: {zara_us.name}")
    print(f"✅ Created India merchant: {myntra.name}")

def test_product_creation():
    """Test product creation"""
    print("\n👗 Testing Product Creation...")
    
    zara_us = Merchant.query.filter_by(code='zara_us').first()
    myntra = Merchant.query.filter_by(code='myntra').first()
    
    # US product
    us_dress = Product(
        merchant_id=zara_us.id,
        sku='ZARA-US-001',
        name='Black Midi Dress',
        description='Elegant black midi dress perfect for work or evening',
        brand='Zara',
        category='dresses',
        subcategory='midi-dresses',
        original_price=79.90,
        currency='USD',
        colors=json.dumps(['black', 'navy']),
        sizes=json.dumps(['XS', 'S', 'M', 'L', 'XL']),
        style_tags=json.dumps(['elegant', 'professional', 'versatile']),
        occasion_tags=json.dumps(['work', 'date-night', 'dinner']),
        stock_quantity=25,
        is_in_stock=True
    )
    
    # India product
    india_kurta = Product(
        merchant_id=myntra.id,
        sku='MYNTRA-001',
        name='Cotton Anarkali Kurta',
        description='Beautiful cotton anarkali kurta with embroidered details',
        brand='Libas',
        category='ethnic-wear',
        subcategory='kurtas',
        original_price=1299.0,
        sale_price=999.0,
        currency='INR',
        colors=json.dumps(['pink', 'blue', 'white']),
        sizes=json.dumps(['S', 'M', 'L', 'XL', 'XXL']),
        style_tags=json.dumps(['ethnic', 'traditional', 'festive']),
        occasion_tags=json.dumps(['festival', 'wedding', 'casual']),
        stock_quantity=50,
        is_in_stock=True
    )
    
    db.session.add(us_dress)
    db.session.add(india_kurta)
    db.session.commit()
    
    print(f"✅ Created US product: {us_dress.name} - ${us_dress.original_price}")
    print(f"✅ Created India product: {india_kurta.name} - ₹{india_kurta.sale_price}")

def test_shopping_cart():
    """Test shopping cart functionality"""
    print("\n🛒 Testing Shopping Cart...")
    
    us_market = Market.query.filter_by(code='US').first()
    us_dress = Product.query.filter_by(sku='ZARA-US-001').first()
    
    # Create shopping cart
    cart = ShoppingCart(
        user_id=1,
        market_id=us_market.id,
        status='active'
    )
    db.session.add(cart)
    db.session.flush()  # Get cart ID
    
    # Add item to cart
    cart_item = CartItem(
        cart_id=cart.id,
        product_id=us_dress.id,
        quantity=1,
        selected_color='black',
        selected_size='M',
        unit_price=us_dress.original_price,
        total_price=us_dress.original_price
    )
    db.session.add(cart_item)
    db.session.commit()
    
    # Calculate cart totals
    subtotal = cart_item.total_price
    tax_amount = subtotal * us_market.tax_rate
    shipping_cost = 0.0 if subtotal >= us_market.free_shipping_threshold else us_market.shipping_base_cost
    total_amount = subtotal + tax_amount + shipping_cost
    
    cart.subtotal = subtotal
    cart.tax_amount = tax_amount
    cart.shipping_cost = shipping_cost
    cart.total_amount = total_amount
    db.session.commit()
    
    print(f"✅ Created shopping cart for user 1")
    print(f"   📦 Item: {us_dress.name} (Size: M, Color: black)")
    print(f"   💰 Subtotal: ${subtotal:.2f}")
    print(f"   🏛️ Tax: ${tax_amount:.2f}")
    print(f"   🚚 Shipping: ${shipping_cost:.2f}")
    print(f"   💳 Total: ${total_amount:.2f}")

if __name__ == '__main__':
    print("🚀 Starting WS5 E-commerce Integration Tests...")
    print("🎯 Tagline: 'We girls have no time' - Testing lightning-fast e-commerce!")
    
    create_test_app()

