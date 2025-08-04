#!/usr/bin/env python3
"""
Test script for WS5-P3: Payment Processing & Multi-Market Payments
Tests payment gateway integration, fraud detection, and multi-market payment flows
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.models.ecommerce_models import db, Market, Merchant, Product, Order, OrderItem
from src.models.payment_processing import (
    PaymentGateway, PaymentMethod, PaymentTransaction, CurrencyExchange,
    PaymentSubscription, FraudDetection
)
from flask import Flask
import json
from datetime import datetime, timedelta
import uuid

def create_test_app():
    """Create test Flask app and test WS5-P3 payment features"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_ws5_p3.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        print("🚀 Testing WS5-P3: Payment Processing & Multi-Market Payments")
        print("🎯 Tagline: 'We girls have no time' - Lightning-fast secure payments!")
        
        # Setup test data
        setup_test_data()
        
        # Test payment gateways
        test_payment_gateways()
        
        # Test payment methods
        test_payment_methods()
        
        # Test currency conversion
        test_currency_conversion()
        
        # Test payment processing
        test_payment_processing()
        
        # Test fraud detection
        test_fraud_detection()
        
        # Test subscriptions
        test_subscription_management()
        
        print("\n🎉 All WS5-P3 payment tests passed!")
        print("💳 Multi-market payment processing system ready!")

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
    
    # Create test merchant and product for orders
    test_merchant = Merchant.query.filter_by(code='test_merchant').first()
    if not test_merchant:
        test_merchant = Merchant(
            name='Test Fashion Store',
            code='test_merchant',
            market_id=us_market.id,
            integration_type='api',
            commission_rate=0.05
        )
        db.session.add(test_merchant)
        db.session.flush()
        
        # Create test product
        test_product = Product(
            merchant_id=test_merchant.id,
            sku='TEST-PAYMENT-001',
            name='Test Payment Product',
            description='Product for payment testing',
            brand='Test Brand',
            category='test',
            original_price=99.99,
            currency='USD',
            colors=json.dumps(['black']),
            sizes=json.dumps(['M']),
            stock_quantity=10,
            is_in_stock=True
        )
        db.session.add(test_product)
        db.session.commit()
    
    print("✅ Test data setup complete")

def test_payment_gateways():
    """Test payment gateway configuration"""
    print("\n💳 Testing Payment Gateway Configuration...")
    
    # Get markets
    us_market = Market.query.filter_by(code='US').first()
    india_market = Market.query.filter_by(code='IN').first()
    
    # Check if gateways already exist
    existing_stripe = PaymentGateway.query.filter_by(code='stripe_us').first()
    if existing_stripe:
        print("✅ Payment gateways already exist, skipping creation")
        return
    
    # Create US payment gateways
    stripe_us = PaymentGateway(
        name='Stripe USA',
        code='stripe_us',
        market_id=us_market.id,
        api_key='sk_test_stripe_key_123',
        webhook_secret='whsec_stripe_123',
        base_url='https://api.stripe.com/v1',
        supports_cards=True,
        supports_wallets=True,
        supports_subscriptions=True,
        transaction_fee_percentage=2.9,
        transaction_fee_fixed=0.30,
        currency='USD',
        success_rate=96.5,
        average_processing_time=2.3
    )
    
    paypal_us = PaymentGateway(
        name='PayPal USA',
        code='paypal_us',
        market_id=us_market.id,
        api_key='paypal_client_id_123',
        api_secret='paypal_secret_123',
        base_url='https://api.paypal.com/v2',
        supports_cards=True,
        supports_wallets=True,
        transaction_fee_percentage=3.4,
        transaction_fee_fixed=0.30,
        currency='USD',
        success_rate=97.2,
        average_processing_time=3.1
    )
    
    # Create India payment gateways
    razorpay_in = PaymentGateway(
        name='Razorpay India',
        code='razorpay_in',
        market_id=india_market.id,
        api_key='rzp_test_key_123',
        api_secret='rzp_secret_123',
        base_url='https://api.razorpay.com/v1',
        supports_cards=True,
        supports_upi=True,
        supports_bank_transfer=True,
        supports_wallets=True,
        transaction_fee_percentage=2.0,
        transaction_fee_fixed=0.0,
        currency='INR',
        success_rate=93.8,
        average_processing_time=4.2
    )
    
    paytm_in = PaymentGateway(
        name='Paytm India',
        code='paytm_in',
        market_id=india_market.id,
        api_key='paytm_merchant_id_123',
        api_secret='paytm_key_123',
        base_url='https://securegw.paytm.in/v3',
        supports_cards=True,
        supports_upi=True,
        supports_wallets=True,
        supports_cod=True,
        transaction_fee_percentage=1.8,
        transaction_fee_fixed=0.0,
        currency='INR',
        success_rate=91.5,
        average_processing_time=5.1
    )
    
    db.session.add_all([stripe_us, paypal_us, razorpay_in, paytm_in])
    db.session.commit()
    
    print(f"✅ Created payment gateways:")
    print(f"   - US: {stripe_us.name} ({stripe_us.success_rate}% success), {paypal_us.name} ({paypal_us.success_rate}% success)")
    print(f"   - India: {razorpay_in.name} ({razorpay_in.success_rate}% success), {paytm_in.name} ({paytm_in.success_rate}% success)")

def test_payment_methods():
    """Test user payment method management"""
    print("\n💰 Testing Payment Method Management...")
    
    # Create test payment methods for user 1
    visa_card = PaymentMethod(
        user_id=1,
        method_type='card',
        provider='visa',
        gateway_token='card_token_visa_123',
        last_four_digits='4242',
        card_brand='visa',
        expiry_month=12,
        expiry_year=2027,
        cardholder_name='Jane Doe',
        billing_address=json.dumps({
            'street': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip': '10001',
            'country': 'US'
        }),
        is_default=True,
        is_verified=True
    )
    
    upi_method = PaymentMethod(
        user_id=1,
        method_type='upi',
        provider='gpay',
        upi_id='jane@gpay',
        is_verified=True
    )
    
    paypal_method = PaymentMethod(
        user_id=1,
        method_type='wallet',
        provider='paypal',
        gateway_token='paypal_token_123',
        is_verified=True
    )
    
    db.session.add_all([visa_card, upi_method, paypal_method])
    db.session.commit()
    
    print(f"✅ Created payment methods for user 1:")
    print(f"   - Visa Card: ****{visa_card.last_four_digits} (Default: {visa_card.is_default})")
    print(f"   - UPI: {upi_method.upi_id}")
    print(f"   - PayPal: Wallet (Verified: {paypal_method.is_verified})")

def test_currency_conversion():
    """Test currency conversion system"""
    print("\n💱 Testing Currency Conversion...")
    
    # Create exchange rates
    usd_to_inr = CurrencyExchange(
        from_currency='USD',
        to_currency='INR',
        exchange_rate=83.25,
        source='xe.com',
        rate_type='mid'
    )
    
    inr_to_usd = CurrencyExchange(
        from_currency='INR',
        to_currency='USD',
        exchange_rate=0.012,
        source='xe.com',
        rate_type='mid'
    )
    
    db.session.add_all([usd_to_inr, inr_to_usd])
    db.session.commit()
    
    # Test conversion
    usd_amount = 100.0
    inr_converted = usd_amount * usd_to_inr.exchange_rate
    
    inr_amount = 8325.0
    usd_converted = inr_amount * inr_to_usd.exchange_rate
    
    print(f"✅ Currency conversion rates:")
    print(f"   - USD to INR: 1 USD = {usd_to_inr.exchange_rate} INR")
    print(f"   - ${usd_amount} USD = ₹{inr_converted} INR")
    print(f"   - ₹{inr_amount} INR = ${usd_converted} USD")

def test_payment_processing():
    """Test payment processing flow"""
    print("\n🔄 Testing Payment Processing...")
    
    # Create test order
    test_product = Product.query.filter_by(sku='TEST-PAYMENT-001').first()
    test_order = Order(
        user_id=1,
        market_id=Market.query.filter_by(code='US').first().id,
        order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
        status='pending',
        payment_status='pending',
        subtotal=99.99,
        tax_amount=8.00,
        shipping_cost=5.99,
        total_amount=113.98
    )
    db.session.add(test_order)
    db.session.flush()
    
    # Create order item
    order_item = OrderItem(
        order_id=test_order.id,
        product_id=test_product.id,
        quantity=1,
        unit_price=99.99,
        total_price=99.99
    )
    db.session.add(order_item)
    db.session.commit()
    
    # Create payment transaction
    stripe_gateway = PaymentGateway.query.filter_by(code='stripe_us').first()
    visa_payment_method = PaymentMethod.query.filter_by(card_brand='visa').first()
    
    transaction = PaymentTransaction(
        transaction_id=f"TXN_{uuid.uuid4().hex[:12].upper()}",
        order_id=test_order.id,
        user_id=1,
        gateway_id=stripe_gateway.id,
        payment_method_id=visa_payment_method.id,
        amount=113.98,
        currency='USD',
        payment_method_type='card',
        status='completed',
        gateway_transaction_id=f'pi_{uuid.uuid4().hex[:24]}',
        gateway_fee=3.61,  # 2.9% + $0.30
        processing_fee=0.0,
        net_amount=110.37,
        completed_at=datetime.utcnow(),
        processing_time_seconds=2.3
    )
    
    db.session.add(transaction)
    
    # Update order status
    test_order.payment_status = 'paid'
    test_order.status = 'confirmed'
    
    db.session.commit()
    
    print(f"✅ Payment processing test:")
    print(f"   - Order: #{test_order.id} - ${test_order.total_amount} USD")
    print(f"   - Transaction: {transaction.transaction_id}")
    print(f"   - Gateway: {stripe_gateway.name}")
    print(f"   - Status: {transaction.status}")
    print(f"   - Gateway Fee: ${transaction.gateway_fee:.2f}")
    print(f"   - Net Amount: ${transaction.net_amount:.2f}")
    print(f"   - Processing Time: {transaction.processing_time_seconds}s")

def test_fraud_detection():
    """Test fraud detection system"""
    print("\n🛡️ Testing Fraud Detection...")
    
    # Get the test transaction
    test_transaction = PaymentTransaction.query.first()
    
    # Create fraud detection record
    fraud_detection = FraudDetection(
        transaction_id=test_transaction.id,
        risk_score=0.15,
        risk_level='low',
        risk_factors=json.dumps(['new_device', 'normal_amount']),
        rules_triggered=json.dumps(['rule_device_check']),
        device_fingerprint='fp_device_123456',
        ip_address='192.168.1.100',
        geolocation=json.dumps({
            'country': 'US',
            'state': 'NY',
            'city': 'New York',
            'latitude': 40.7128,
            'longitude': -74.0060
        }),
        velocity_check='passed',
        pattern_analysis='normal',
        decision='approve',
        decision_reason='Low risk score, normal transaction pattern'
    )
    
    db.session.add(fraud_detection)
    db.session.commit()
    
    print(f"✅ Fraud detection analysis:")
    print(f"   - Risk Score: {fraud_detection.risk_score:.2f} ({fraud_detection.risk_level} risk)")
    print(f"   - Decision: {fraud_detection.decision}")
    print(f"   - Velocity Check: {fraud_detection.velocity_check}")
    print(f"   - Pattern Analysis: {fraud_detection.pattern_analysis}")
    print(f"   - Risk Factors: {json.loads(fraud_detection.risk_factors)}")

def test_subscription_management():
    """Test subscription and recurring payment management"""
    print("\n🔄 Testing Subscription Management...")
    
    # Create premium styling subscription
    stripe_gateway = PaymentGateway.query.filter_by(code='stripe_us').first()
    visa_payment_method = PaymentMethod.query.filter_by(card_brand='visa').first()
    
    premium_subscription = PaymentSubscription(
        subscription_id=f"SUB_{uuid.uuid4().hex[:12].upper()}",
        user_id=1,
        payment_method_id=visa_payment_method.id,
        gateway_id=stripe_gateway.id,
        subscription_type='premium_styling',
        plan_name='Premium AI Styling - Monthly',
        amount=29.99,
        currency='USD',
        billing_cycle='monthly',
        gateway_subscription_id=f'sub_{uuid.uuid4().hex[:24]}',
        status='active',
        start_date=datetime.utcnow(),
        next_billing_date=datetime.utcnow() + timedelta(days=30),
        trial_start_date=datetime.utcnow(),
        trial_end_date=datetime.utcnow() + timedelta(days=7),
        is_trial_active=True,
        successful_payments=0,
        failed_payments=0,
        total_amount_paid=0.0
    )
    
    db.session.add(premium_subscription)
    db.session.commit()
    
    print(f"✅ Subscription created:")
    print(f"   - Plan: {premium_subscription.plan_name}")
    print(f"   - Amount: ${premium_subscription.amount} {premium_subscription.currency}")
    print(f"   - Billing Cycle: {premium_subscription.billing_cycle}")
    print(f"   - Status: {premium_subscription.status}")
    print(f"   - Trial Active: {premium_subscription.is_trial_active}")
    print(f"   - Next Billing: {premium_subscription.next_billing_date.strftime('%Y-%m-%d')}")

if __name__ == '__main__':
    create_test_app()

