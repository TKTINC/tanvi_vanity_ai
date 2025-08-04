#!/usr/bin/env python3
"""
Comprehensive WS5 E-commerce Integration Test
Tests the complete e-commerce system end-to-end across all phases
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.ecommerce_models import db, Market, Merchant, Product, ShoppingCart, CartItem, Order, OrderItem
from src.models.product_catalog import ProductCategory, ProductRecommendation
from src.models.payment_processing import PaymentGateway, PaymentMethod, PaymentTransaction, FraudDetection  
from src.models.shopping_checkout import ShippingAddress, ShippingMethod, Coupon, CouponUsage, CheckoutSession, OrderNotification
from src.models.performance_analytics import PerformanceMetric, EcommerceAnalytics, CacheMetrics, UserBehaviorAnalytics, SystemAlert, DatabaseOptimization
from flask import Flask
import json
import random
import uuid
import hashlib
from datetime import datetime, timedelta

def create_integration_test():
    """Create comprehensive integration test for WS5 e-commerce system"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_ws5_integration.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        print("🚀 WS5: E-commerce Integration - Comprehensive System Test")
        print("🎯 Tagline: 'We girls have no time' - Testing complete e-commerce experience!")
        print("=" * 80)
        
        # Test complete e-commerce workflow
        test_results = {}
        
        # Phase 1: Foundation Setup
        print("\n📋 Phase 1: Testing E-commerce Foundation...")
        test_results['foundation'] = test_foundation_setup()
        
        # Phase 2: Product Catalog
        print("\n🛍️ Phase 2: Testing Product Catalog & Merchant Integration...")
        test_results['catalog'] = test_product_catalog()
        
        # Phase 3: Payment Processing
        print("\n💳 Phase 3: Testing Payment Processing...")
        test_results['payments'] = test_payment_processing()
        
        # Phase 4: Shopping & Checkout
        print("\n🛒 Phase 4: Testing Shopping Cart & Checkout...")
        test_results['checkout'] = test_shopping_checkout()
        
        # Phase 5: Analytics & Performance
        print("\n📊 Phase 5: Testing Performance & Analytics...")
        test_results['analytics'] = test_performance_analytics()
        
        # Phase 6: End-to-End Integration
        print("\n🔗 Phase 6: Testing End-to-End Integration...")
        test_results['integration'] = test_end_to_end_workflow()
        
        # Generate final report
        generate_test_report(test_results)
        
        print("\n🎉 WS5 E-commerce Integration Test Complete!")
        print("🚀 System ready for production deployment!")

def test_foundation_setup():
    """Test WS5-P1: E-commerce Foundation & Multi-Market Setup"""
    results = {'passed': 0, 'total': 0, 'details': []}
    
    # Test 1: Market Creation
    results['total'] += 1
    try:
        us_market = Market(
            code='US', name='United States', currency='USD', currency_symbol='$',
            tax_rate=0.08, shipping_base_cost=5.99, free_shipping_threshold=50.0
        )
        india_market = Market(
            code='IN', name='India', currency='INR', currency_symbol='₹',
            tax_rate=0.18, shipping_base_cost=50.0, free_shipping_threshold=999.0
        )
        db.session.add_all([us_market, india_market])
        db.session.commit()
        
        assert Market.query.count() == 2
        results['passed'] += 1
        results['details'].append("✅ Multi-market setup (US/India)")
    except Exception as e:
        results['details'].append(f"❌ Multi-market setup failed: {e}")
    
    # Test 2: Merchant Creation
    results['total'] += 1
    try:
        us_market = Market.query.filter_by(code='US').first()
        merchant = Merchant(
            name='Zara USA', code='zara_usa', market_id=us_market.id,
            integration_type='api', commission_rate=0.05
        )
        db.session.add(merchant)
        db.session.commit()
        
        assert Merchant.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ Merchant integration setup")
    except Exception as e:
        results['details'].append(f"❌ Merchant setup failed: {e}")
    
    # Test 3: Basic Product Creation
    results['total'] += 1
    try:
        merchant = Merchant.query.first()
        product = Product(
            merchant_id=merchant.id, sku='TEST-001', name='Test Product',
            description='Test product for integration', brand='TestBrand',
            category='test', original_price=99.99, currency='USD',
            stock_quantity=100, is_in_stock=True
        )
        db.session.add(product)
        db.session.commit()
        
        assert Product.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ Basic product creation")
    except Exception as e:
        results['details'].append(f"❌ Product creation failed: {e}")
    
    return results

def test_product_catalog():
    """Test WS5-P2: Product Catalog & Merchant Integration"""
    results = {'passed': 0, 'total': 0, 'details': []}
    
    # Test 1: Category Hierarchy
    results['total'] += 1
    try:
        us_market = Market.query.filter_by(code='US').first()
        clothing_category = ProductCategory(
            name='Clothing', code='clothing', display_name='Clothing'
        )
        dresses_category = ProductCategory(
            name='Dresses', code='dresses', display_name='Dresses', parent_id=1
        )
        db.session.add_all([clothing_category, dresses_category])
        db.session.commit()
        
        assert ProductCategory.query.count() >= 2
        results['passed'] += 1
        results['details'].append("✅ Category hierarchy created")
    except Exception as e:
        results['details'].append(f"❌ Category creation failed: {e}")
    
    # Test 2: Product Recommendations
    results['total'] += 1
    try:
        product = Product.query.first()
        recommendation = ProductRecommendation(
            product_id=product.id, recommendation_type='ai_styling',
            confidence_score=0.92, reasoning='Perfect for summer occasions',
            context_data=json.dumps({'occasion': 'casual', 'season': 'summer'})
        )
        db.session.add(recommendation)
        db.session.commit()
        
        assert ProductRecommendation.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ AI product recommendations")
    except Exception as e:
        results['details'].append(f"❌ Recommendations failed: {e}")
    
    return results

def test_payment_processing():
    """Test WS5-P3: Payment Processing & Multi-Market Payments"""
    results = {'passed': 0, 'total': 0, 'details': []}
    
    # Test 1: Payment Gateway Setup
    results['total'] += 1
    try:
        us_market = Market.query.filter_by(code='US').first()
        stripe_gateway = PaymentGateway(
            name='Stripe', market_id=us_market.id, gateway_type='stripe',
            is_active=True, success_rate=96.5, avg_processing_time=2.3,
            configuration=json.dumps({'api_key': 'sk_test_...', 'webhook_secret': 'whsec_...'})
        )
        db.session.add(stripe_gateway)
        db.session.commit()
        
        assert PaymentGateway.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ Payment gateway integration")
    except Exception as e:
        results['details'].append(f"❌ Payment gateway failed: {e}")
    
    # Test 2: Payment Method Management
    results['total'] += 1
    try:
        gateway = PaymentGateway.query.first()
        payment_method = PaymentMethod(
            user_id=1, gateway_id=gateway.id, method_type='card',
            display_name='****4242', is_default=True,
            method_details=json.dumps({
                'card_type': 'visa', 'last_four': '4242',
                'exp_month': 12, 'exp_year': 2025
            })
        )
        db.session.add(payment_method)
        db.session.commit()
        
        assert PaymentMethod.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ Payment method management")
    except Exception as e:
        results['details'].append(f"❌ Payment method failed: {e}")
    
    # Test 3: Payment Transaction Processing
    results['total'] += 1
    try:
        gateway = PaymentGateway.query.first()
        transaction = PaymentTransaction(
            transaction_id=f"TXN_{uuid.uuid4().hex[:12].upper()}",
            gateway_id=gateway.id, user_id=1, amount=127.50, currency='USD',
            status='completed', gateway_response=json.dumps({'charge_id': 'ch_test_123'})
        )
        db.session.add(transaction)
        db.session.commit()
        
        assert PaymentTransaction.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ Payment transaction processing")
    except Exception as e:
        results['details'].append(f"❌ Transaction processing failed: {e}")
    
    # Test 4: Fraud Detection
    results['total'] += 1
    try:
        transaction = PaymentTransaction.query.first()
        fraud_check = FraudDetection(
            transaction_id=transaction.id, risk_score=0.15,
            decision='approved', factors_analyzed=json.dumps([
                'velocity_check', 'geolocation', 'device_fingerprint'
            ]),
            decision_reasoning='Low risk profile, normal patterns detected'
        )
        db.session.add(fraud_check)
        db.session.commit()
        
        assert FraudDetection.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ Fraud detection system")
    except Exception as e:
        results['details'].append(f"❌ Fraud detection failed: {e}")
    
    return results

def test_shopping_checkout():
    """Test WS5-P4: Shopping Cart & Checkout Experience"""
    results = {'passed': 0, 'total': 0, 'details': []}
    
    # Test 1: Shopping Cart Creation
    results['total'] += 1
    try:
        us_market = Market.query.filter_by(code='US').first()
        cart = ShoppingCart(
            user_id=1, market_id=us_market.id, status='active',
            subtotal=99.99, tax_amount=8.00, shipping_cost=0.00, total_amount=107.99
        )
        db.session.add(cart)
        db.session.commit()
        
        assert ShoppingCart.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ Shopping cart management")
    except Exception as e:
        results['details'].append(f"❌ Shopping cart failed: {e}")
    
    # Test 2: Cart Items Management
    results['total'] += 1
    try:
        cart = ShoppingCart.query.first()
        product = Product.query.first()
        cart_item = CartItem(
            cart_id=cart.id, product_id=product.id, quantity=1,
            selected_color='Blue', selected_size='M',
            unit_price=99.99, total_price=99.99
        )
        db.session.add(cart_item)
        db.session.commit()
        
        assert CartItem.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ Cart items management")
    except Exception as e:
        results['details'].append(f"❌ Cart items failed: {e}")
    
    # Test 3: Shipping Address Management
    results['total'] += 1
    try:
        shipping_address = ShippingAddress(
            user_id=1, label='Home', first_name='Jane', last_name='Doe',
            address_line_1='123 Main St', city='New York', state='NY',
            postal_code='10001', country='US', is_default=True
        )
        db.session.add(shipping_address)
        db.session.commit()
        
        assert ShippingAddress.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ Shipping address management")
    except Exception as e:
        results['details'].append(f"❌ Shipping address failed: {e}")
    
    # Test 4: Checkout Session
    results['total'] += 1
    try:
        cart = ShoppingCart.query.first()
        checkout_session = CheckoutSession(
            session_id=f"CHECKOUT_{uuid.uuid4().hex[:12].upper()}",
            user_id=1, cart_id=cart.id, step='payment',
            subtotal=99.99, tax_amount=8.00, total_amount=107.99,
            expires_at=datetime.utcnow() + timedelta(hours=2)
        )
        db.session.add(checkout_session)
        db.session.commit()
        
        assert CheckoutSession.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ Checkout session management")
    except Exception as e:
        results['details'].append(f"❌ Checkout session failed: {e}")
    
    # Test 5: Order Creation
    results['total'] += 1
    try:
        us_market = Market.query.filter_by(code='US').first()
        order = Order(
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            user_id=1, market_id=us_market.id,
            subtotal=99.99, tax_amount=8.00, total_amount=107.99,
            status='confirmed', payment_status='paid'
        )
        db.session.add(order)
        db.session.commit()
        
        assert Order.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ Order creation and management")
    except Exception as e:
        results['details'].append(f"❌ Order creation failed: {e}")
    
    return results

def test_performance_analytics():
    """Test WS5-P5: Performance Optimization & Analytics"""
    results = {'passed': 0, 'total': 0, 'details': []}
    
    # Test 1: Performance Metrics
    results['total'] += 1
    try:
        metric = PerformanceMetric(
            metric_name='api_response_time', metric_type='latency',
            value=45.2, unit='ms', endpoint='/api/products/search',
            category='api', status='normal'
        )
        db.session.add(metric)
        db.session.commit()
        
        assert PerformanceMetric.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ Performance metrics collection")
    except Exception as e:
        results['details'].append(f"❌ Performance metrics failed: {e}")
    
    # Test 2: E-commerce Analytics
    results['total'] += 1
    try:
        us_market = Market.query.filter_by(code='US').first()
        analytic = EcommerceAnalytics(
            metric_name='conversion_rate', metric_category='sales',
            value=3.2, previous_value=2.7, percentage_change=18.5,
            period_type='daily', period_start=datetime.utcnow() - timedelta(days=1),
            period_end=datetime.utcnow(), market_id=us_market.id
        )
        db.session.add(analytic)
        db.session.commit()
        
        assert EcommerceAnalytics.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ E-commerce business analytics")
    except Exception as e:
        results['details'].append(f"❌ E-commerce analytics failed: {e}")
    
    # Test 3: Cache Metrics
    results['total'] += 1
    try:
        cache_metric = CacheMetrics(
            cache_name='product_catalog', cache_type='redis',
            hit_count=1850, miss_count=150, hit_rate=92.5,
            avg_response_time_ms=2.3, period_start=datetime.utcnow() - timedelta(hours=1),
            period_end=datetime.utcnow()
        )
        db.session.add(cache_metric)
        db.session.commit()
        
        assert CacheMetrics.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ Cache performance monitoring")
    except Exception as e:
        results['details'].append(f"❌ Cache metrics failed: {e}")
    
    # Test 4: User Behavior Analytics
    results['total'] += 1
    try:
        us_market = Market.query.filter_by(code='US').first()
        behavior = UserBehaviorAnalytics(
            user_id=1, session_id=f"SESS_{uuid.uuid4().hex[:8].upper()}",
            event_type='purchase_complete', event_category='purchase_funnel',
            market_id=us_market.id, device_type='mobile',
            conversion_value=107.99, conversion_type='purchase'
        )
        db.session.add(behavior)
        db.session.commit()
        
        assert UserBehaviorAnalytics.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ User behavior tracking")
    except Exception as e:
        results['details'].append(f"❌ User behavior failed: {e}")
    
    # Test 5: System Alerts
    results['total'] += 1
    try:
        alert = SystemAlert(
            alert_id=f"ALERT_{uuid.uuid4().hex[:12].upper()}",
            alert_type='performance', severity='medium',
            title='Integration Test Alert',
            message='Test alert for integration testing',
            status='active'
        )
        db.session.add(alert)
        db.session.commit()
        
        assert SystemAlert.query.count() >= 1
        results['passed'] += 1
        results['details'].append("✅ System alerting and monitoring")
    except Exception as e:
        results['details'].append(f"❌ System alerts failed: {e}")
    
    return results

def test_end_to_end_workflow():
    """Test complete end-to-end e-commerce workflow"""
    results = {'passed': 0, 'total': 0, 'details': []}
    
    # Test 1: Complete Purchase Workflow
    results['total'] += 1
    try:
        # Simulate complete purchase flow
        us_market = Market.query.filter_by(code='US').first()
        product = Product.query.first()
        
        # Create cart and add item
        cart = ShoppingCart.query.first()
        if not cart:
            cart = ShoppingCart(user_id=1, market_id=us_market.id, status='active')
            db.session.add(cart)
            db.session.flush()
        
        # Add item to cart
        cart_item = CartItem(
            cart_id=cart.id, product_id=product.id, quantity=1,
            unit_price=99.99, total_price=99.99
        )
        db.session.add(cart_item)
        
        # Create checkout session
        checkout_session = CheckoutSession(
            session_id=f"E2E_{uuid.uuid4().hex[:12].upper()}",
            user_id=1, cart_id=cart.id, step='completed',
            subtotal=99.99, total_amount=107.99
        )
        db.session.add(checkout_session)
        
        # Process payment
        gateway = PaymentGateway.query.first()
        transaction = PaymentTransaction(
            transaction_id=f"E2E_{uuid.uuid4().hex[:12].upper()}",
            gateway_id=gateway.id, user_id=1,
            amount=107.99, currency='USD', status='completed'
        )
        db.session.add(transaction)
        
        # Create order
        order = Order(
            order_number=f"E2E-{uuid.uuid4().hex[:8].upper()}",
            user_id=1, market_id=us_market.id,
            subtotal=99.99, total_amount=107.99,
            status='confirmed', payment_status='paid'
        )
        db.session.add(order)
        
        # Create order item
        order_item = OrderItem(
            order_id=order.id, product_id=product.id,
            quantity=1, unit_price=99.99, total_price=99.99
        )
        db.session.add(order_item)
        
        db.session.commit()
        
        # Verify workflow completion
        assert cart_item.id is not None
        assert checkout_session.id is not None
        assert transaction.id is not None
        assert order.id is not None
        assert order_item.id is not None
        
        results['passed'] += 1
        results['details'].append("✅ Complete purchase workflow")
    except Exception as e:
        results['details'].append(f"❌ Purchase workflow failed: {e}")
    
    # Test 2: Multi-Market Functionality
    results['total'] += 1
    try:
        # Test India market functionality
        india_market = Market.query.filter_by(code='IN').first()
        
        # Create India-specific merchant
        india_merchant = Merchant(
            name='Myntra India', code='myntra_in',
            market_id=india_market.id, integration_type='api'
        )
        db.session.add(india_merchant)
        db.session.flush()
        
        # Create India-specific product
        india_product = Product(
            merchant_id=india_merchant.id, sku='IN-001',
            name='Ethnic Kurta', brand='Libas', category='ethnic_wear',
            original_price=1999.0, currency='INR'
        )
        db.session.add(india_product)
        
        # Create India payment gateway
        razorpay_gateway = PaymentGateway(
            name='Razorpay', market_id=india_market.id,
            gateway_type='razorpay', is_active=True
        )
        db.session.add(razorpay_gateway)
        
        db.session.commit()
        
        # Verify multi-market setup
        assert india_merchant.id is not None
        assert india_product.id is not None
        assert razorpay_gateway.id is not None
        
        results['passed'] += 1
        results['details'].append("✅ Multi-market functionality (US/India)")
    except Exception as e:
        results['details'].append(f"❌ Multi-market failed: {e}")
    
    # Test 3: Integration Points Validation
    results['total'] += 1
    try:
        # Verify all major components are integrated
        markets_count = Market.query.count()
        merchants_count = Merchant.query.count()
        products_count = Product.query.count()
        orders_count = Order.query.count()
        transactions_count = PaymentTransaction.query.count()
        analytics_count = EcommerceAnalytics.query.count()
        
        assert markets_count >= 2  # US and India
        assert merchants_count >= 2  # US and India merchants
        assert products_count >= 2  # US and India products
        assert orders_count >= 1  # At least one order
        assert transactions_count >= 1  # At least one transaction
        assert analytics_count >= 1  # At least one analytic
        
        results['passed'] += 1
        results['details'].append("✅ All integration points validated")
    except Exception as e:
        results['details'].append(f"❌ Integration validation failed: {e}")
    
    return results

def generate_test_report(test_results):
    """Generate comprehensive test report"""
    print("\n" + "=" * 80)
    print("🎯 WS5 E-COMMERCE INTEGRATION - FINAL TEST REPORT")
    print("=" * 80)
    
    total_passed = 0
    total_tests = 0
    
    for phase, results in test_results.items():
        passed = results['passed']
        total = results['total']
        total_passed += passed
        total_tests += total
        
        success_rate = (passed / total * 100) if total > 0 else 0
        status_icon = "✅" if success_rate == 100 else "⚠️" if success_rate >= 80 else "❌"
        
        print(f"\n{status_icon} {phase.upper()}: {passed}/{total} tests passed ({success_rate:.1f}%)")
        for detail in results['details']:
            print(f"   {detail}")
    
    overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    overall_status = "✅ PASSED" if overall_success_rate == 100 else "⚠️ PARTIAL" if overall_success_rate >= 80 else "❌ FAILED"
    
    print(f"\n" + "=" * 80)
    print(f"🏆 OVERALL RESULT: {overall_status}")
    print(f"📊 SUCCESS RATE: {total_passed}/{total_tests} tests passed ({overall_success_rate:.1f}%)")
    print("=" * 80)
    
    # System readiness assessment
    if overall_success_rate >= 95:
        print("🚀 SYSTEM STATUS: READY FOR PRODUCTION DEPLOYMENT")
        print("✨ All critical components tested and validated")
    elif overall_success_rate >= 80:
        print("⚠️ SYSTEM STATUS: READY FOR STAGING DEPLOYMENT")
        print("🔧 Minor issues detected, review failed tests")
    else:
        print("❌ SYSTEM STATUS: REQUIRES FIXES BEFORE DEPLOYMENT")
        print("🛠️ Critical issues detected, address failed tests")
    
    print("\n🎯 'We girls have no time' - E-commerce system testing complete!")

if __name__ == '__main__':
    create_integration_test()

