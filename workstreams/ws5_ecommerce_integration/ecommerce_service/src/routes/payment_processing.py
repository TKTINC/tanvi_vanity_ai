from flask import Blueprint, request, jsonify
from src.models.ecommerce_models import db, Market, Order
from src.models.payment_processing import (
    PaymentGateway, PaymentMethod, PaymentTransaction, CurrencyExchange,
    PaymentSubscription, FraudDetection
)
import json
import uuid
from datetime import datetime, timedelta
import hashlib
import hmac

payment_processing_bp = Blueprint('payment_processing', __name__)

# ============================================================================
# PAYMENT PROCESSING HEALTH & STATUS
# ============================================================================

@payment_processing_bp.route('/payments/health', methods=['GET'])
def payment_health_check():
    """Health check for payment processing service"""
    # Get payment statistics
    total_gateways = PaymentGateway.query.filter_by(is_active=True).count()
    total_transactions_today = PaymentTransaction.query.filter(
        PaymentTransaction.created_at >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    ).count()
    successful_transactions_today = PaymentTransaction.query.filter(
        PaymentTransaction.created_at >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0),
        PaymentTransaction.status == 'completed'
    ).count()
    
    success_rate = (successful_transactions_today / max(total_transactions_today, 1)) * 100
    
    return jsonify({
        "status": "healthy",
        "service": "WS5: Payment Processing & Multi-Market Payments",
        "version": "3.0.0",
        "tagline": "We girls have no time",
        "philosophy": "Lightning-fast, secure payments across all markets",
        "payment_stats": {
            "active_gateways": total_gateways,
            "transactions_today": total_transactions_today,
            "success_rate_today": f"{success_rate:.1f}%",
            "supported_currencies": ["USD", "INR"],
            "supported_methods": ["Cards", "UPI", "Wallets", "COD", "BNPL"]
        },
        "features": [
            "Multi-market payment processing",
            "Real-time fraud detection",
            "Currency conversion",
            "Subscription management",
            "PCI DSS compliant tokenization",
            "Advanced risk scoring",
            "Webhook integration"
        ],
        "markets": {
            "US": ["Stripe", "PayPal", "Apple Pay", "Google Pay"],
            "India": ["Razorpay", "Paytm", "UPI", "COD", "Net Banking"]
        },
        "message": "Multi-market payment processing ready for instant transactions!"
    })

# ============================================================================
# PAYMENT GATEWAY MANAGEMENT
# ============================================================================

@payment_processing_bp.route('/payments/gateways', methods=['GET'])
def get_payment_gateways():
    """Get available payment gateways by market"""
    market_code = request.args.get('market', 'US')
    method_type = request.args.get('method_type')  # cards, wallets, upi, cod
    
    # Get market
    market = Market.query.filter_by(code=market_code.upper()).first()
    if not market:
        return jsonify({
            "success": False,
            "error": "Market not found",
            "message": f"Market {market_code} does not exist"
        }), 404
    
    # Build query
    query = PaymentGateway.query.filter_by(market_id=market.id, is_active=True)
    
    # Filter by method type
    if method_type == 'cards':
        query = query.filter_by(supports_cards=True)
    elif method_type == 'wallets':
        query = query.filter_by(supports_wallets=True)
    elif method_type == 'upi':
        query = query.filter_by(supports_upi=True)
    elif method_type == 'cod':
        query = query.filter_by(supports_cod=True)
    elif method_type == 'bnpl':
        query = query.filter_by(supports_bnpl=True)
    
    gateways = query.order_by(PaymentGateway.success_rate.desc()).all()
    
    return jsonify({
        "gateways": [gateway.to_dict() for gateway in gateways],
        "market": market.to_dict(),
        "total_gateways": len(gateways),
        "filters": {
            "market": market_code,
            "method_type": method_type
        },
        "message": f"Available payment gateways for {market.name}"
    })

@payment_processing_bp.route('/payments/gateways/<gateway_code>/status', methods=['GET'])
def get_gateway_status(gateway_code):
    """Get payment gateway status and health"""
    gateway = PaymentGateway.query.filter_by(code=gateway_code, is_active=True).first()
    if not gateway:
        return jsonify({
            "success": False,
            "error": "Gateway not found"
        }), 404
    
    # Get recent transaction statistics
    recent_transactions = PaymentTransaction.query.filter(
        PaymentTransaction.gateway_id == gateway.id,
        PaymentTransaction.created_at >= datetime.utcnow() - timedelta(hours=24)
    ).all()
    
    successful_transactions = [t for t in recent_transactions if t.status == 'completed']
    failed_transactions = [t for t in recent_transactions if t.status == 'failed']
    
    # Calculate metrics
    success_rate = len(successful_transactions) / max(len(recent_transactions), 1) * 100
    avg_processing_time = sum(t.processing_time_seconds for t in successful_transactions if t.processing_time_seconds) / max(len(successful_transactions), 1)
    
    return jsonify({
        "gateway": gateway.to_dict(),
        "health_metrics": {
            "transactions_24h": len(recent_transactions),
            "success_rate_24h": f"{success_rate:.1f}%",
            "failed_transactions_24h": len(failed_transactions),
            "average_processing_time": f"{avg_processing_time:.2f}s",
            "status": "healthy" if success_rate > 95 else "degraded" if success_rate > 85 else "unhealthy"
        },
        "message": f"Gateway status for {gateway.name}"
    })

# ============================================================================
# PAYMENT METHOD MANAGEMENT
# ============================================================================

@payment_processing_bp.route('/payments/methods/<int:user_id>', methods=['GET'])
def get_user_payment_methods(user_id):
    """Get user's saved payment methods"""
    payment_methods = PaymentMethod.query.filter_by(
        user_id=user_id,
        is_active=True
    ).order_by(PaymentMethod.is_default.desc(), PaymentMethod.last_used_at.desc()).all()
    
    return jsonify({
        "payment_methods": [method.to_dict() for method in payment_methods],
        "user_id": user_id,
        "total_methods": len(payment_methods),
        "default_method": next((method.to_dict() for method in payment_methods if method.is_default), None),
        "message": f"Payment methods for user {user_id}"
    })

@payment_processing_bp.route('/payments/methods', methods=['POST'])
def add_payment_method():
    """Add new payment method for user"""
    data = request.get_json()
    
    try:
        # Create payment method (tokenized data only)
        payment_method = PaymentMethod(
            user_id=data['user_id'],
            method_type=data['method_type'],
            provider=data.get('provider'),
            gateway_token=data.get('gateway_token'),  # From payment gateway tokenization
            last_four_digits=data.get('last_four_digits'),
            card_brand=data.get('card_brand'),
            expiry_month=data.get('expiry_month'),
            expiry_year=data.get('expiry_year'),
            cardholder_name=data.get('cardholder_name'),
            upi_id=data.get('upi_id'),
            bank_name=data.get('bank_name'),
            account_type=data.get('account_type'),
            billing_address=json.dumps(data.get('billing_address', {})),
            is_default=data.get('is_default', False)
        )
        
        # If this is set as default, unset other defaults
        if payment_method.is_default:
            PaymentMethod.query.filter_by(
                user_id=payment_method.user_id,
                is_default=True
            ).update({'is_default': False})
        
        db.session.add(payment_method)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "payment_method": payment_method.to_dict(),
            "message": "Payment method added successfully"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# ============================================================================
# PAYMENT PROCESSING ENDPOINTS
# ============================================================================

@payment_processing_bp.route('/payments/process', methods=['POST'])
def process_payment():
    """Process payment for an order"""
    data = request.get_json()
    
    try:
        # Get order
        order = Order.query.get(data['order_id'])
        if not order:
            return jsonify({
                "success": False,
                "error": "Order not found"
            }), 404
        
        # Get payment gateway
        gateway = PaymentGateway.query.get(data['gateway_id'])
        if not gateway or not gateway.is_active:
            return jsonify({
                "success": False,
                "error": "Payment gateway not available"
            }), 400
        
        # Create transaction record
        transaction = PaymentTransaction(
            transaction_id=f"TXN_{uuid.uuid4().hex[:12].upper()}",
            order_id=order.id,
            user_id=data['user_id'],
            gateway_id=gateway.id,
            payment_method_id=data.get('payment_method_id'),
            amount=data['amount'],
            currency=data['currency'],
            payment_method_type=data.get('payment_method_type', 'card'),
            status='pending'
        )
        
        db.session.add(transaction)
        db.session.flush()  # Get transaction ID
        
        # Perform fraud detection
        fraud_result = _perform_fraud_detection(transaction, data)
        
        if fraud_result['decision'] == 'decline':
            transaction.status = 'failed'
            transaction.error_message = 'Transaction declined due to fraud risk'
            db.session.commit()
            
            return jsonify({
                "success": False,
                "transaction": transaction.to_dict(),
                "fraud_result": fraud_result,
                "message": "Transaction declined due to security concerns"
            }), 400
        
        # Process payment with gateway
        payment_result = _process_with_gateway(gateway, transaction, data)
        
        # Update transaction with result
        transaction.status = payment_result['status']
        transaction.gateway_transaction_id = payment_result.get('gateway_transaction_id')
        transaction.gateway_payment_intent_id = payment_result.get('payment_intent_id')
        transaction.gateway_fee = payment_result.get('gateway_fee', 0.0)
        transaction.processing_fee = payment_result.get('processing_fee', 0.0)
        transaction.net_amount = transaction.amount - transaction.gateway_fee - transaction.processing_fee
        transaction.gateway_response = json.dumps(payment_result.get('gateway_response', {}))
        
        if payment_result['status'] == 'completed':
            transaction.completed_at = datetime.utcnow()
            transaction.processing_time_seconds = (datetime.utcnow() - transaction.initiated_at).total_seconds()
            
            # Update order status
            order.payment_status = 'paid'
            order.status = 'confirmed'
        
        db.session.commit()
        
        return jsonify({
            "success": payment_result['status'] == 'completed',
            "transaction": transaction.to_dict(),
            "payment_result": payment_result,
            "message": f"Payment {payment_result['status']}"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@payment_processing_bp.route('/payments/transactions/<transaction_id>/status', methods=['GET'])
def get_transaction_status(transaction_id):
    """Get payment transaction status"""
    transaction = PaymentTransaction.query.filter_by(transaction_id=transaction_id).first()
    if not transaction:
        return jsonify({
            "success": False,
            "error": "Transaction not found"
        }), 404
    
    return jsonify({
        "transaction": transaction.to_dict(),
        "order": transaction.order.to_dict() if transaction.order else None,
        "gateway": transaction.gateway.to_dict() if transaction.gateway else None,
        "message": f"Transaction status: {transaction.status}"
    })

# ============================================================================
# CURRENCY CONVERSION ENDPOINTS
# ============================================================================

@payment_processing_bp.route('/payments/currency/convert', methods=['POST'])
def convert_currency():
    """Convert amount between currencies"""
    data = request.get_json()
    
    from_currency = data['from_currency'].upper()
    to_currency = data['to_currency'].upper()
    amount = float(data['amount'])
    
    # Get exchange rate
    exchange_rate = CurrencyExchange.query.filter_by(
        from_currency=from_currency,
        to_currency=to_currency,
        is_active=True
    ).order_by(CurrencyExchange.created_at.desc()).first()
    
    if not exchange_rate:
        # Try reverse rate
        reverse_rate = CurrencyExchange.query.filter_by(
            from_currency=to_currency,
            to_currency=from_currency,
            is_active=True
        ).order_by(CurrencyExchange.created_at.desc()).first()
        
        if reverse_rate:
            converted_amount = amount / reverse_rate.exchange_rate
            rate_used = 1 / reverse_rate.exchange_rate
        else:
            return jsonify({
                "success": False,
                "error": "Exchange rate not available",
                "message": f"No exchange rate found for {from_currency} to {to_currency}"
            }), 404
    else:
        converted_amount = amount * exchange_rate.exchange_rate
        rate_used = exchange_rate.exchange_rate
        
        # Update usage tracking
        exchange_rate.last_used_at = datetime.utcnow()
        exchange_rate.usage_count += 1
        db.session.commit()
    
    return jsonify({
        "success": True,
        "conversion": {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "original_amount": amount,
            "converted_amount": round(converted_amount, 2),
            "exchange_rate": rate_used,
            "rate_timestamp": exchange_rate.created_at.isoformat() if 'exchange_rate' in locals() else reverse_rate.created_at.isoformat()
        },
        "message": f"Converted {amount} {from_currency} to {converted_amount:.2f} {to_currency}"
    })

@payment_processing_bp.route('/payments/currency/rates', methods=['GET'])
def get_exchange_rates():
    """Get current exchange rates"""
    base_currency = request.args.get('base', 'USD')
    
    rates = CurrencyExchange.query.filter_by(
        from_currency=base_currency.upper(),
        is_active=True
    ).order_by(CurrencyExchange.created_at.desc()).all()
    
    # Group by to_currency to get latest rates
    latest_rates = {}
    for rate in rates:
        if rate.to_currency not in latest_rates:
            latest_rates[rate.to_currency] = rate
    
    return jsonify({
        "base_currency": base_currency.upper(),
        "rates": {currency: rate.to_dict() for currency, rate in latest_rates.items()},
        "total_currencies": len(latest_rates),
        "last_updated": max(rate.created_at for rate in latest_rates.values()).isoformat() if latest_rates else None,
        "message": f"Exchange rates with base currency {base_currency.upper()}"
    })

# ============================================================================
# SUBSCRIPTION MANAGEMENT ENDPOINTS
# ============================================================================

@payment_processing_bp.route('/payments/subscriptions/<int:user_id>', methods=['GET'])
def get_user_subscriptions(user_id):
    """Get user's active subscriptions"""
    subscriptions = PaymentSubscription.query.filter_by(
        user_id=user_id
    ).order_by(PaymentSubscription.created_at.desc()).all()
    
    active_subscriptions = [sub for sub in subscriptions if sub.status == 'active']
    
    return jsonify({
        "subscriptions": [sub.to_dict() for sub in subscriptions],
        "active_subscriptions": [sub.to_dict() for sub in active_subscriptions],
        "user_id": user_id,
        "total_subscriptions": len(subscriptions),
        "active_count": len(active_subscriptions),
        "message": f"Subscriptions for user {user_id}"
    })

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _perform_fraud_detection(transaction, payment_data):
    """Perform fraud detection on transaction"""
    risk_score = 0.0
    risk_factors = []
    
    # Velocity check - multiple transactions in short time
    recent_transactions = PaymentTransaction.query.filter(
        PaymentTransaction.user_id == transaction.user_id,
        PaymentTransaction.created_at >= datetime.utcnow() - timedelta(minutes=10)
    ).count()
    
    if recent_transactions > 3:
        risk_score += 0.3
        risk_factors.append('high_velocity')
    
    # Amount check - unusually high amount
    if transaction.amount > 1000:  # $1000 or equivalent
        risk_score += 0.2
        risk_factors.append('high_amount')
    
    # IP geolocation check (simulated)
    ip_address = payment_data.get('ip_address', '127.0.0.1')
    if ip_address.startswith('192.168') or ip_address == '127.0.0.1':
        # Local/test IP
        risk_score += 0.1
        risk_factors.append('local_ip')
    
    # Determine risk level and decision
    if risk_score < 0.3:
        risk_level = 'low'
        decision = 'approve'
    elif risk_score < 0.6:
        risk_level = 'medium'
        decision = 'review'
    else:
        risk_level = 'high'
        decision = 'decline'
    
    # Create fraud detection record
    fraud_detection = FraudDetection(
        transaction_id=transaction.id,
        risk_score=risk_score,
        risk_level=risk_level,
        risk_factors=json.dumps(risk_factors),
        ip_address=ip_address,
        decision=decision,
        decision_reason=f"Risk score: {risk_score:.2f}, Factors: {', '.join(risk_factors)}"
    )
    
    db.session.add(fraud_detection)
    
    return {
        'decision': decision,
        'risk_score': risk_score,
        'risk_level': risk_level,
        'risk_factors': risk_factors
    }

def _process_with_gateway(gateway, transaction, payment_data):
    """Process payment with specific gateway (simulated)"""
    # This would integrate with actual payment gateways
    # For now, return simulated responses
    
    if gateway.code == 'stripe_us':
        return _process_stripe_payment(gateway, transaction, payment_data)
    elif gateway.code == 'razorpay_in':
        return _process_razorpay_payment(gateway, transaction, payment_data)
    elif gateway.code == 'paypal_us':
        return _process_paypal_payment(gateway, transaction, payment_data)
    else:
        return {
            'status': 'failed',
            'error': 'Gateway not implemented',
            'gateway_response': {'error': 'Gateway integration not available'}
        }

def _process_stripe_payment(gateway, transaction, payment_data):
    """Process payment with Stripe (simulated)"""
    # Simulate Stripe payment processing
    import random
    
    # 95% success rate simulation
    if random.random() < 0.95:
        return {
            'status': 'completed',
            'gateway_transaction_id': f'pi_{uuid.uuid4().hex[:24]}',
            'payment_intent_id': f'pi_{uuid.uuid4().hex[:24]}',
            'gateway_fee': transaction.amount * 0.029 + 0.30,  # Stripe fees
            'processing_fee': 0.0,
            'gateway_response': {
                'id': f'pi_{uuid.uuid4().hex[:24]}',
                'status': 'succeeded',
                'amount': int(transaction.amount * 100),  # Cents
                'currency': transaction.currency.lower()
            }
        }
    else:
        return {
            'status': 'failed',
            'error': 'card_declined',
            'gateway_response': {
                'error': {
                    'code': 'card_declined',
                    'message': 'Your card was declined.'
                }
            }
        }

def _process_razorpay_payment(gateway, transaction, payment_data):
    """Process payment with Razorpay (simulated)"""
    import random
    
    # 93% success rate simulation for India
    if random.random() < 0.93:
        return {
            'status': 'completed',
            'gateway_transaction_id': f'pay_{uuid.uuid4().hex[:14]}',
            'payment_intent_id': f'order_{uuid.uuid4().hex[:14]}',
            'gateway_fee': transaction.amount * 0.02,  # Razorpay fees (2%)
            'processing_fee': 0.0,
            'gateway_response': {
                'id': f'pay_{uuid.uuid4().hex[:14]}',
                'status': 'captured',
                'amount': int(transaction.amount * 100),  # Paise
                'currency': transaction.currency.upper()
            }
        }
    else:
        return {
            'status': 'failed',
            'error': 'payment_failed',
            'gateway_response': {
                'error': {
                    'code': 'PAYMENT_FAILED',
                    'description': 'Payment processing failed'
                }
            }
        }

def _process_paypal_payment(gateway, transaction, payment_data):
    """Process payment with PayPal (simulated)"""
    import random
    
    # 97% success rate simulation
    if random.random() < 0.97:
        return {
            'status': 'completed',
            'gateway_transaction_id': f'{uuid.uuid4().hex[:17].upper()}',
            'payment_intent_id': f'PAYID-{uuid.uuid4().hex[:20].upper()}',
            'gateway_fee': transaction.amount * 0.034 + 0.30,  # PayPal fees
            'processing_fee': 0.0,
            'gateway_response': {
                'id': f'{uuid.uuid4().hex[:17].upper()}',
                'status': 'COMPLETED',
                'amount': {
                    'value': str(transaction.amount),
                    'currency_code': transaction.currency.upper()
                }
            }
        }
    else:
        return {
            'status': 'failed',
            'error': 'INSTRUMENT_DECLINED',
            'gateway_response': {
                'error': {
                    'name': 'INSTRUMENT_DECLINED',
                    'message': 'The instrument presented was either declined by the processor or bank, or it can\'t be used for this payment.'
                }
            }
        }

