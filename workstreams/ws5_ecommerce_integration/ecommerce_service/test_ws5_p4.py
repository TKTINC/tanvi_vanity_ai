#!/usr/bin/env python3
"""
Test script for WS5-P4: Shopping Cart & Checkout Experience
Tests shopping cart, checkout flow, shipping, coupons, and order management
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.ecommerce_models import db, Market, Merchant, Product, ShoppingCart, CartItem, Order, OrderItem
from src.models.shopping_checkout import (
    ShippingAddress, ShippingMethod, Coupon, CouponUsage, 
    CheckoutSession, OrderNotification
)
from src.models.payment_processing import PaymentMethod
from flask import Flask
import json
from datetime import datetime, timedelta
import uuid

def create_test_app():
    """Create test Flask app and test WS5-P4 shopping cart and checkout features"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_ws5_p4.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        print("🚀 Testing WS5-P4: Shopping Cart & Checkout Experience")
        print("🎯 Tagline: 'We girls have no time' - Lightning-fast checkout!")
        
        # Setup test data
        setup_test_data()
        
        # Test shopping cart
        test_shopping_cart()
        
        # Test shipping addresses
        test_shipping_addresses()
        
        # Test shipping methods
        test_shipping_methods()
        
        # Test coupons
        test_coupon_system()
        
        # Test checkout flow
        test_checkout_flow()
        
        # Test order management
        test_order_management()
        
        print("\n🎉 All WS5-P4 shopping cart and checkout tests passed!")
        print("🛒 Express checkout experience ready!")

def setup_test_data():
    """Setup test markets, merchants, and products"""
    print("\n📋 Setting up test data...")
    
    # Create markets if they don't exist
    us_market = Market.query.filter_by(code='US').first()
    if not us_market:
        us_market = Market(
            code='US', name='United States', currency='USD', currency_symbol='$',
            tax_rate=0.08, shipping_base_cost=5.99, free_shipping_threshold=50.0
        )
        db.session.add(us_market)
    
    india_market = Market.query.filter_by(code='IN').first()
    if not india_market:
        india_market = Market(
            code='IN', name='India', currency='INR', currency_symbol='₹',
            tax_rate=0.18, shipping_base_cost=50.0, free_shipping_threshold=999.0
        )
        db.session.add(india_market)
    
    db.session.commit()
    
    # Create test merchant and products
    test_merchant = Merchant.query.filter_by(code='fashion_store').first()
    if not test_merchant:
        test_merchant = Merchant(
            name='Fashion Store',
            code='fashion_store',
            market_id=us_market.id,
            integration_type='api',
            commission_rate=0.05
        )
        db.session.add(test_merchant)
        db.session.flush()
        
        # Create test products
        products = [
            {
                'sku': 'DRESS-001',
                'name': 'Summer Floral Dress',
                'description': 'Beautiful floral dress perfect for summer',
                'brand': 'StyleCo',
                'category': 'dresses',
                'original_price': 89.99,
                'sale_price': 69.99,
                'colors': ['blue', 'pink', 'white'],
                'sizes': ['XS', 'S', 'M', 'L', 'XL']
            },
            {
                'sku': 'TOP-001',
                'name': 'Casual Cotton Top',
                'description': 'Comfortable cotton top for everyday wear',
                'brand': 'ComfortWear',
                'category': 'tops',
                'original_price': 39.99,
                'sale_price': 29.99,
                'colors': ['black', 'white', 'navy'],
                'sizes': ['XS', 'S', 'M', 'L', 'XL']
            },
            {
                'sku': 'JEANS-001',
                'name': 'High-Waist Skinny Jeans',
                'description': 'Trendy high-waist skinny jeans',
                'brand': 'DenimCo',
                'category': 'bottoms',
                'original_price': 79.99,
                'sale_price': None,
                'colors': ['dark_blue', 'light_blue', 'black'],
                'sizes': ['24', '26', '28', '30', '32']
            }
        ]
        
        for product_data in products:
            product = Product(
                merchant_id=test_merchant.id,
                sku=product_data['sku'],
                name=product_data['name'],
                description=product_data['description'],
                brand=product_data['brand'],
                category=product_data['category'],
                original_price=product_data['original_price'],
                sale_price=product_data['sale_price'],
                currency='USD',
                colors=json.dumps(product_data['colors']),
                sizes=json.dumps(product_data['sizes']),
                stock_quantity=50,
                is_in_stock=True
            )
            db.session.add(product)
        
        db.session.commit()
    
    print("✅ Test data setup complete")

def test_shopping_cart():
    """Test shopping cart functionality"""
    print("\n🛒 Testing Shopping Cart Functionality...")
    
    # Get test products
    dress = Product.query.filter_by(sku='DRESS-001').first()
    top = Product.query.filter_by(sku='TOP-001').first()
    jeans = Product.query.filter_by(sku='JEANS-001').first()
    
    us_market = Market.query.filter_by(code='US').first()
    
    # Create shopping cart
    cart = ShoppingCart(
        user_id=1,
        market_id=us_market.id,
        status='active'
    )
    db.session.add(cart)
    db.session.flush()
    
    # Add items to cart
    cart_items = [
        CartItem(
            cart_id=cart.id,
            product_id=dress.id,
            quantity=1,
            selected_color='blue',
            selected_size='M',
            unit_price=dress.sale_price or dress.original_price,
            total_price=dress.sale_price or dress.original_price
        ),
        CartItem(
            cart_id=cart.id,
            product_id=top.id,
            quantity=2,
            selected_color='black',
            selected_size='S',
            unit_price=top.sale_price or top.original_price,
            total_price=(top.sale_price or top.original_price) * 2
        ),
        CartItem(
            cart_id=cart.id,
            product_id=jeans.id,
            quantity=1,
            selected_color='dark_blue',
            selected_size='28',
            unit_price=jeans.original_price,
            total_price=jeans.original_price
        )
    ]
    
    db.session.add_all(cart_items)
    
    # Calculate cart totals
    subtotal = sum(item.total_price for item in cart_items)
    tax_amount = subtotal * us_market.tax_rate
    shipping_cost = us_market.shipping_base_cost if subtotal < us_market.free_shipping_threshold else 0.0
    total_amount = subtotal + tax_amount + shipping_cost
    
    cart.subtotal = subtotal
    cart.tax_amount = tax_amount
    cart.shipping_cost = shipping_cost
    cart.total_amount = total_amount
    
    db.session.commit()
    
    print(f"✅ Shopping cart created:")
    print(f"   - Items: {len(cart_items)} products, {sum(item.quantity for item in cart_items)} total quantity")
    print(f"   - Subtotal: ${cart.subtotal:.2f}")
    print(f"   - Tax: ${cart.tax_amount:.2f} ({us_market.tax_rate*100}%)")
    print(f"   - Shipping: ${cart.shipping_cost:.2f}")
    print(f"   - Total: ${cart.total_amount:.2f}")
    print(f"   - Free shipping: {'Yes' if cart.shipping_cost == 0 else f'No (need ${us_market.free_shipping_threshold - subtotal:.2f} more)'}")

def test_shipping_addresses():
    """Test shipping address management"""
    print("\n📍 Testing Shipping Address Management...")
    
    # Create shipping addresses
    addresses = [
        ShippingAddress(
            user_id=1,
            label='Home',
            first_name='Jane',
            last_name='Doe',
            address_line_1='123 Main Street',
            address_line_2='Apt 4B',
            city='New York',
            state='NY',
            postal_code='10001',
            country='US',
            phone='+1-555-0123',
            email='jane.doe@example.com',
            delivery_instructions='Leave at front door',
            is_default=True,
            is_verified=True
        ),
        ShippingAddress(
            user_id=1,
            label='Work',
            first_name='Jane',
            last_name='Doe',
            company='Tech Corp',
            address_line_1='456 Business Ave',
            city='New York',
            state='NY',
            postal_code='10002',
            country='US',
            phone='+1-555-0124',
            email='jane.doe@example.com',
            delivery_instructions='Reception desk',
            is_verified=True
        )
    ]
    
    db.session.add_all(addresses)
    db.session.commit()
    
    print(f"✅ Shipping addresses created:")
    for addr in addresses:
        full_address = f"{addr.address_line_1}, {addr.city}, {addr.state} {addr.postal_code}, {addr.country}"
        print(f"   - {addr.label}: {full_address} (Default: {addr.is_default})")

def test_shipping_methods():
    """Test shipping methods"""
    print("\n🚚 Testing Shipping Methods...")
    
    us_market = Market.query.filter_by(code='US').first()
    india_market = Market.query.filter_by(code='IN').first()
    
    # Create US shipping methods
    us_shipping_methods = [
        ShippingMethod(
            market_id=us_market.id,
            name='Standard Shipping',
            code='standard',
            description='5-7 business days delivery',
            base_cost=5.99,
            free_shipping_threshold=50.0,
            min_delivery_days=5,
            max_delivery_days=7,
            supports_tracking=True,
            carrier='USPS'
        ),
        ShippingMethod(
            market_id=us_market.id,
            name='Express Shipping',
            code='express',
            description='2-3 business days delivery',
            base_cost=12.99,
            min_delivery_days=2,
            max_delivery_days=3,
            supports_tracking=True,
            is_express=True,
            carrier='FedEx'
        ),
        ShippingMethod(
            market_id=us_market.id,
            name='Same-Day Delivery',
            code='same_day',
            description='Same day delivery in select cities',
            base_cost=19.99,
            min_delivery_days=0,
            max_delivery_days=0,
            supports_tracking=True,
            is_express=True,
            carrier='UberRush'
        )
    ]
    
    # Create India shipping methods
    india_shipping_methods = [
        ShippingMethod(
            market_id=india_market.id,
            name='Standard Delivery',
            code='standard_in',
            description='3-5 business days delivery',
            base_cost=50.0,
            free_shipping_threshold=999.0,
            min_delivery_days=3,
            max_delivery_days=5,
            supports_cod=True,
            supports_tracking=True,
            carrier='BlueDart'
        ),
        ShippingMethod(
            market_id=india_market.id,
            name='Express Delivery',
            code='express_in',
            description='1-2 business days delivery',
            base_cost=150.0,
            min_delivery_days=1,
            max_delivery_days=2,
            supports_cod=True,
            supports_tracking=True,
            is_express=True,
            carrier='Delhivery'
        )
    ]
    
    db.session.add_all(us_shipping_methods + india_shipping_methods)
    db.session.commit()
    
    print(f"✅ Shipping methods created:")
    print(f"   - US: {len(us_shipping_methods)} methods (Standard: $5.99, Express: $12.99, Same-day: $19.99)")
    print(f"   - India: {len(india_shipping_methods)} methods (Standard: ₹50, Express: ₹150)")

def test_coupon_system():
    """Test coupon and discount system"""
    print("\n🎫 Testing Coupon System...")
    
    # Check if coupons already exist
    existing_coupon = Coupon.query.filter_by(code='WELCOME10').first()
    if existing_coupon:
        print("✅ Coupons already exist, using existing ones")
        coupons = Coupon.query.all()
    else:
        # Create coupons
        coupons = [
        Coupon(
            code='WELCOME10',
            name='Welcome Discount',
            description='10% off your first order',
            discount_type='percentage',
            discount_value=10.0,
            minimum_order_amount=25.0,
            maximum_discount_amount=20.0,
            valid_from=datetime.utcnow() - timedelta(days=1),
            valid_until=datetime.utcnow() + timedelta(days=30),
            usage_limit=1000,
            usage_limit_per_user=1,
            applicable_markets=json.dumps(['US', 'IN']),
            is_active=True,
            is_public=True
        ),
        Coupon(
            code='SUMMER25',
            name='Summer Sale',
            description='$25 off orders over $100',
            discount_type='fixed_amount',
            discount_value=25.0,
            minimum_order_amount=100.0,
            valid_from=datetime.utcnow() - timedelta(days=7),
            valid_until=datetime.utcnow() + timedelta(days=60),
            usage_limit=500,
            usage_limit_per_user=2,
            applicable_markets=json.dumps(['US']),
            applicable_categories=json.dumps(['dresses', 'tops']),
            is_active=True,
            is_public=True
        ),
        Coupon(
            code='FREESHIP',
            name='Free Shipping',
            description='Free shipping on any order',
            discount_type='fixed_amount',
            discount_value=5.99,  # Standard shipping cost
            minimum_order_amount=0.0,
            valid_from=datetime.utcnow() - timedelta(days=3),
            valid_until=datetime.utcnow() + timedelta(days=14),
            usage_limit=100,
            usage_limit_per_user=1,
            applicable_markets=json.dumps(['US']),
            is_active=True,
            is_public=True
        )
        ]
        
        db.session.add_all(coupons)
        db.session.commit()
    
    # Test coupon validation
    cart = ShoppingCart.query.filter_by(user_id=1).first()
    order_amount = cart.subtotal
    
    for coupon in coupons:
        if coupon.discount_type == 'percentage':
            discount = min((order_amount * coupon.discount_value) / 100, coupon.maximum_discount_amount or float('inf'))
            display = f"{coupon.discount_value}%"
        else:
            discount = min(coupon.discount_value, order_amount)
            display = f"${coupon.discount_value}"
        
        print(f"   - {coupon.code}: {display} → ${discount:.2f} savings")
    
    print(f"✅ Coupon system ready:")
    print(f"   - {len(coupons)} active coupons")
    print(f"   - Order amount: ${order_amount:.2f}")

def test_checkout_flow():
    """Test checkout flow"""
    print("\n💳 Testing Checkout Flow...")
    
    # Get test data
    cart = ShoppingCart.query.filter_by(user_id=1).first()
    shipping_address = ShippingAddress.query.filter_by(user_id=1, is_default=True).first()
    shipping_method = ShippingMethod.query.filter_by(code='standard').first()
    coupon = Coupon.query.filter_by(code='WELCOME10').first()
    
    # Create checkout session
    checkout_session = CheckoutSession(
        session_id=f"CHECKOUT_{uuid.uuid4().hex[:12].upper()}",
        user_id=1,
        cart_id=cart.id,
        step='cart_review',
        shipping_address_id=shipping_address.id,
        shipping_method_id=shipping_method.id,
        coupon_id=coupon.id,
        browser_info=json.dumps({
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
            'screen_resolution': '375x812',
            'timezone': 'America/New_York'
        }),
        device_info=json.dumps({
            'device_type': 'mobile',
            'os': 'iOS',
            'browser': 'Safari'
        }),
        expires_at=datetime.utcnow() + timedelta(hours=2)
    )
    
    # Calculate checkout totals
    subtotal = cart.subtotal
    shipping_cost = shipping_method.base_cost
    if subtotal >= (shipping_method.free_shipping_threshold or float('inf')):
        shipping_cost = 0.0
    
    tax_amount = subtotal * cart.market.tax_rate
    
    # Apply coupon discount
    if coupon.discount_type == 'percentage':
        discount_amount = min((subtotal * coupon.discount_value) / 100, coupon.maximum_discount_amount or float('inf'))
    else:
        discount_amount = min(coupon.discount_value, subtotal)
    
    total_amount = subtotal + tax_amount + shipping_cost - discount_amount
    
    checkout_session.subtotal = subtotal
    checkout_session.tax_amount = tax_amount
    checkout_session.shipping_cost = shipping_cost
    checkout_session.discount_amount = discount_amount
    checkout_session.total_amount = total_amount
    
    db.session.add(checkout_session)
    db.session.commit()
    
    print(f"✅ Checkout session created:")
    print(f"   - Session ID: {checkout_session.session_id}")
    print(f"   - Step: {checkout_session.step}")
    print(f"   - Shipping: {shipping_method.name} (${shipping_cost:.2f})")
    print(f"   - Coupon: {coupon.code} (-${discount_amount:.2f})")
    print(f"   - Total: ${total_amount:.2f}")
    print(f"   - Expires: {checkout_session.expires_at.strftime('%Y-%m-%d %H:%M')}")

def test_order_management():
    """Test order creation and management"""
    print("\n📦 Testing Order Management...")
    
    # Get checkout session
    checkout_session = CheckoutSession.query.first()
    
    # Create order
    order = Order(
        order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
        user_id=checkout_session.user_id,
        market_id=checkout_session.cart.market_id,
        subtotal=checkout_session.subtotal,
        tax_amount=checkout_session.tax_amount,
        shipping_cost=checkout_session.shipping_cost,
        discount_amount=checkout_session.discount_amount,
        total_amount=checkout_session.total_amount,
        status='confirmed',
        payment_status='paid',
        shipping_address=json.dumps(checkout_session.shipping_address.to_dict()),
        shipping_method=checkout_session.shipping_method.name,
        tracking_number=f"TRK{uuid.uuid4().hex[:10].upper()}"
    )
    
    db.session.add(order)
    db.session.flush()
    
    # Create order items from cart
    cart_items = CartItem.query.filter_by(cart_id=checkout_session.cart_id).all()
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            selected_color=cart_item.selected_color,
            selected_size=cart_item.selected_size,
            unit_price=cart_item.unit_price,
            total_price=cart_item.total_price,
            status='confirmed'
        )
        db.session.add(order_item)
    
    # Record coupon usage
    if checkout_session.coupon_id:
        coupon_usage = CouponUsage(
            coupon_id=checkout_session.coupon_id,
            user_id=checkout_session.user_id,
            order_id=order.id,
            discount_amount=checkout_session.discount_amount,
            order_amount=checkout_session.subtotal
        )
        db.session.add(coupon_usage)
        
        # Update coupon usage count
        coupon = Coupon.query.get(checkout_session.coupon_id)
        coupon.current_usage_count += 1
    
    # Create order notifications
    notifications = [
        OrderNotification(
            order_id=order.id,
            user_id=order.user_id,
            notification_type='order_confirmed',
            channel='email',
            subject=f'Order Confirmation - {order.order_number}',
            message=f'Thank you for your order! Your order {order.order_number} has been confirmed.',
            status='sent',
            recipient='jane.doe@example.com',
            sent_at=datetime.utcnow()
        ),
        OrderNotification(
            order_id=order.id,
            user_id=order.user_id,
            notification_type='payment_received',
            channel='sms',
            subject='Payment Confirmed',
            message=f'Payment of ${order.total_amount:.2f} received for order {order.order_number}',
            status='sent',
            recipient='+1-555-0123',
            sent_at=datetime.utcnow()
        )
    ]
    
    db.session.add_all(notifications)
    
    # Update checkout session and cart status
    checkout_session.status = 'completed'
    checkout_session.completed_at = datetime.utcnow()
    checkout_session.cart.status = 'converted'
    
    db.session.commit()
    
    print(f"✅ Order created successfully:")
    print(f"   - Order Number: {order.order_number}")
    print(f"   - Items: {len(cart_items)} products")
    print(f"   - Total: ${order.total_amount:.2f}")
    print(f"   - Status: {order.status}")
    print(f"   - Payment: {order.payment_status}")
    print(f"   - Tracking: {order.tracking_number}")
    print(f"   - Notifications: {len(notifications)} sent")
    print(f"   - Coupon Used: {coupon.code} (Usage count: {coupon.current_usage_count})")

if __name__ == '__main__':
    create_test_app()

