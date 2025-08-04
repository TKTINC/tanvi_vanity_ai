from flask import Blueprint, request, jsonify
from src.models.ecommerce_models import db, Market, Product, ShoppingCart, CartItem, Order, OrderItem
from src.models.shopping_checkout import (
    ShippingAddress, ShippingMethod, Coupon, CouponUsage, 
    CheckoutSession, OrderNotification
)
from src.models.payment_processing import PaymentMethod, PaymentTransaction
import json
import uuid
from datetime import datetime, timedelta

shopping_checkout_bp = Blueprint('shopping_checkout', __name__)

# ============================================================================
# SHOPPING CART & CHECKOUT HEALTH
# ============================================================================

@shopping_checkout_bp.route('/checkout/health', methods=['GET'])
def checkout_health_check():
    """Health check for shopping cart and checkout service"""
    # Get checkout statistics
    active_carts = ShoppingCart.query.filter_by(status='active').count()
    active_checkouts = CheckoutSession.query.filter_by(status='active').count()
    completed_orders_today = Order.query.filter(
        Order.created_at >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0),
        Order.status.in_(['confirmed', 'processing', 'shipped', 'delivered'])
    ).count()
    
    return jsonify({
        "status": "healthy",
        "service": "WS5: Shopping Cart & Checkout Experience",
        "version": "4.0.0",
        "tagline": "We girls have no time",
        "philosophy": "Lightning-fast checkout, zero friction shopping",
        "checkout_stats": {
            "active_carts": active_carts,
            "active_checkouts": active_checkouts,
            "orders_today": completed_orders_today,
            "conversion_features": ["1-click checkout", "Guest checkout", "Auto-fill", "Smart recommendations"]
        },
        "features": [
            "Smart shopping cart with auto-save",
            "Express checkout flow (3 steps max)",
            "Multiple shipping addresses",
            "Real-time shipping calculations",
            "Coupon and discount management",
            "Abandoned cart recovery",
            "Order tracking and notifications",
            "Guest checkout support"
        ],
        "checkout_flow": [
            "Cart Review → Shipping → Payment → Confirmation",
            "Average completion time: <2 minutes",
            "Mobile-optimized experience",
            "Auto-save progress"
        ],
        "message": "Express checkout experience ready - because we girls have no time!"
    })

# ============================================================================
# SHOPPING CART MANAGEMENT
# ============================================================================

@shopping_checkout_bp.route('/cart/<int:user_id>', methods=['GET'])
def get_user_cart(user_id):
    """Get user's active shopping cart"""
    market_code = request.args.get('market', 'US')
    
    # Get market
    market = Market.query.filter_by(code=market_code.upper()).first()
    if not market:
        return jsonify({
            "success": False,
            "error": "Market not found"
        }), 404
    
    # Get or create cart
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
    
    # Get cart items with product details
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    
    # Calculate cart totals
    _calculate_cart_totals(cart)
    
    return jsonify({
        "cart": cart.to_dict(),
        "items": [item.to_dict() for item in cart_items],
        "item_count": len(cart_items),
        "total_quantity": sum(item.quantity for item in cart_items),
        "market": market.to_dict(),
        "message": f"Shopping cart for user {user_id}"
    })

@shopping_checkout_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to shopping cart"""
    data = request.get_json()
    
    try:
        # Get product
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({
                "success": False,
                "error": "Product not found"
            }), 404
        
        # Get or create cart
        cart = ShoppingCart.query.filter_by(
            user_id=data['user_id'],
            market_id=data['market_id'],
            status='active'
        ).first()
        
        if not cart:
            cart = ShoppingCart(
                user_id=data['user_id'],
                market_id=data['market_id'],
                status='active'
            )
            db.session.add(cart)
            db.session.flush()
        
        # Check if item already exists in cart
        existing_item = CartItem.query.filter_by(
            cart_id=cart.id,
            product_id=product.id,
            selected_color=data.get('selected_color'),
            selected_size=data.get('selected_size')
        ).first()
        
        if existing_item:
            # Update quantity
            existing_item.quantity += data.get('quantity', 1)
            existing_item.total_price = existing_item.quantity * existing_item.unit_price
            cart_item = existing_item
        else:
            # Create new cart item
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product.id,
                quantity=data.get('quantity', 1),
                selected_color=data.get('selected_color'),
                selected_size=data.get('selected_size'),
                unit_price=product.sale_price or product.original_price,
                total_price=(product.sale_price or product.original_price) * data.get('quantity', 1)
            )
            db.session.add(cart_item)
        
        # Update cart totals
        _calculate_cart_totals(cart)
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "cart_item": cart_item.to_dict(),
            "cart": cart.to_dict(),
            "message": f"Added {product.name} to cart"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@shopping_checkout_bp.route('/cart/update/<int:cart_item_id>', methods=['PUT'])
def update_cart_item(cart_item_id):
    """Update cart item quantity or options"""
    data = request.get_json()
    
    cart_item = CartItem.query.get(cart_item_id)
    if not cart_item:
        return jsonify({
            "success": False,
            "error": "Cart item not found"
        }), 404
    
    try:
        # Update quantity
        if 'quantity' in data:
            if data['quantity'] <= 0:
                db.session.delete(cart_item)
                db.session.commit()
                return jsonify({
                    "success": True,
                    "message": "Item removed from cart"
                })
            else:
                cart_item.quantity = data['quantity']
                cart_item.total_price = cart_item.quantity * cart_item.unit_price
        
        # Update selections
        if 'selected_color' in data:
            cart_item.selected_color = data['selected_color']
        if 'selected_size' in data:
            cart_item.selected_size = data['selected_size']
        
        # Update cart totals
        _calculate_cart_totals(cart_item.cart)
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "cart_item": cart_item.to_dict(),
            "cart": cart_item.cart.to_dict(),
            "message": "Cart item updated"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@shopping_checkout_bp.route('/cart/remove/<int:cart_item_id>', methods=['DELETE'])
def remove_from_cart(cart_item_id):
    """Remove item from cart"""
    cart_item = CartItem.query.get(cart_item_id)
    if not cart_item:
        return jsonify({
            "success": False,
            "error": "Cart item not found"
        }), 404
    
    cart = cart_item.cart
    product_name = cart_item.product.name if cart_item.product else "Item"
    
    db.session.delete(cart_item)
    
    # Update cart totals
    _calculate_cart_totals(cart)
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "cart": cart.to_dict(),
        "message": f"Removed {product_name} from cart"
    })

# ============================================================================
# SHIPPING ADDRESS MANAGEMENT
# ============================================================================

@shopping_checkout_bp.route('/addresses/<int:user_id>', methods=['GET'])
def get_user_addresses(user_id):
    """Get user's shipping addresses"""
    addresses = ShippingAddress.query.filter_by(
        user_id=user_id
    ).order_by(ShippingAddress.is_default.desc(), ShippingAddress.last_used_at.desc()).all()
    
    return jsonify({
        "addresses": [addr.to_dict() for addr in addresses],
        "user_id": user_id,
        "total_addresses": len(addresses),
        "default_address": next((addr.to_dict() for addr in addresses if addr.is_default), None),
        "message": f"Shipping addresses for user {user_id}"
    })

@shopping_checkout_bp.route('/addresses', methods=['POST'])
def add_shipping_address():
    """Add new shipping address"""
    data = request.get_json()
    
    try:
        # Create shipping address
        address = ShippingAddress(
            user_id=data['user_id'],
            label=data.get('label'),
            first_name=data['first_name'],
            last_name=data['last_name'],
            company=data.get('company'),
            address_line_1=data['address_line_1'],
            address_line_2=data.get('address_line_2'),
            city=data['city'],
            state=data['state'],
            postal_code=data['postal_code'],
            country=data['country'],
            phone=data.get('phone'),
            email=data.get('email'),
            delivery_instructions=data.get('delivery_instructions'),
            is_default=data.get('is_default', False)
        )
        
        # If this is set as default, unset other defaults
        if address.is_default:
            ShippingAddress.query.filter_by(
                user_id=address.user_id,
                is_default=True
            ).update({'is_default': False})
        
        db.session.add(address)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "address": address.to_dict(),
            "message": "Shipping address added successfully"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# ============================================================================
# SHIPPING METHODS
# ============================================================================

@shopping_checkout_bp.route('/shipping/methods', methods=['GET'])
def get_shipping_methods():
    """Get available shipping methods by market"""
    market_code = request.args.get('market', 'US')
    order_amount = float(request.args.get('order_amount', 0))
    
    # Get market
    market = Market.query.filter_by(code=market_code.upper()).first()
    if not market:
        return jsonify({
            "success": False,
            "error": "Market not found"
        }), 404
    
    # Get shipping methods
    shipping_methods = ShippingMethod.query.filter_by(
        market_id=market.id,
        is_active=True
    ).order_by(ShippingMethod.min_delivery_days.asc()).all()
    
    # Calculate shipping costs
    methods_with_costs = []
    for method in shipping_methods:
        cost = method.base_cost
        
        # Check for free shipping
        if method.free_shipping_threshold and order_amount >= method.free_shipping_threshold:
            cost = 0.0
        
        method_dict = method.to_dict()
        method_dict['calculated_cost'] = cost
        method_dict['is_free'] = cost == 0.0
        method_dict['free_shipping_remaining'] = max(0, (method.free_shipping_threshold or 0) - order_amount) if method.free_shipping_threshold else None
        
        methods_with_costs.append(method_dict)
    
    return jsonify({
        "shipping_methods": methods_with_costs,
        "market": market.to_dict(),
        "order_amount": order_amount,
        "total_methods": len(methods_with_costs),
        "message": f"Shipping methods for {market.name}"
    })

# ============================================================================
# COUPON MANAGEMENT
# ============================================================================

@shopping_checkout_bp.route('/coupons/validate', methods=['POST'])
def validate_coupon():
    """Validate and apply coupon code"""
    data = request.get_json()
    
    coupon_code = data['coupon_code'].upper()
    user_id = data['user_id']
    order_amount = float(data['order_amount'])
    market_code = data.get('market', 'US')
    
    # Find coupon
    coupon = Coupon.query.filter_by(code=coupon_code, is_active=True).first()
    if not coupon:
        return jsonify({
            "success": False,
            "error": "Invalid coupon code",
            "message": "Coupon code not found or expired"
        }), 404
    
    # Check validity period
    now = datetime.utcnow()
    if now < coupon.valid_from or now > coupon.valid_until:
        return jsonify({
            "success": False,
            "error": "Coupon expired",
            "message": f"Coupon is valid from {coupon.valid_from.strftime('%Y-%m-%d')} to {coupon.valid_until.strftime('%Y-%m-%d')}"
        }), 400
    
    # Check minimum order amount
    if order_amount < coupon.minimum_order_amount:
        return jsonify({
            "success": False,
            "error": "Minimum order amount not met",
            "message": f"Minimum order amount is ${coupon.minimum_order_amount:.2f}"
        }), 400
    
    # Check usage limits
    if coupon.usage_limit and coupon.current_usage_count >= coupon.usage_limit:
        return jsonify({
            "success": False,
            "error": "Coupon usage limit exceeded",
            "message": "This coupon has reached its usage limit"
        }), 400
    
    # Check per-user usage limit
    user_usage_count = CouponUsage.query.filter_by(
        coupon_id=coupon.id,
        user_id=user_id
    ).count()
    
    if user_usage_count >= coupon.usage_limit_per_user:
        return jsonify({
            "success": False,
            "error": "Personal usage limit exceeded",
            "message": f"You can only use this coupon {coupon.usage_limit_per_user} time(s)"
        }), 400
    
    # Check market applicability
    if coupon.applicable_markets:
        applicable_markets = json.loads(coupon.applicable_markets)
        if market_code.upper() not in applicable_markets:
            return jsonify({
                "success": False,
                "error": "Coupon not applicable in this market",
                "message": f"This coupon is only valid in: {', '.join(applicable_markets)}"
            }), 400
    
    # Calculate discount
    if coupon.discount_type == 'percentage':
        discount_amount = (order_amount * coupon.discount_value) / 100
        if coupon.maximum_discount_amount:
            discount_amount = min(discount_amount, coupon.maximum_discount_amount)
    else:  # fixed_amount
        discount_amount = min(coupon.discount_value, order_amount)
    
    return jsonify({
        "success": True,
        "coupon": coupon.to_dict(),
        "discount_amount": round(discount_amount, 2),
        "final_amount": round(order_amount - discount_amount, 2),
        "savings": round(discount_amount, 2),
        "message": f"Coupon applied! You saved ${discount_amount:.2f}"
    })

# ============================================================================
# CHECKOUT FLOW
# ============================================================================

@shopping_checkout_bp.route('/checkout/start', methods=['POST'])
def start_checkout():
    """Start checkout process"""
    data = request.get_json()
    
    try:
        # Get cart
        cart = ShoppingCart.query.get(data['cart_id'])
        if not cart or cart.status != 'active':
            return jsonify({
                "success": False,
                "error": "Cart not found or inactive"
            }), 404
        
        # Create checkout session
        checkout_session = CheckoutSession(
            session_id=f"CHECKOUT_{uuid.uuid4().hex[:12].upper()}",
            user_id=data['user_id'],
            cart_id=cart.id,
            step='cart_review',
            browser_info=json.dumps(data.get('browser_info', {})),
            device_info=json.dumps(data.get('device_info', {})),
            expires_at=datetime.utcnow() + timedelta(hours=2)  # 2-hour session
        )
        
        db.session.add(checkout_session)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "checkout_session": checkout_session.to_dict(),
            "cart": cart.to_dict(),
            "message": "Checkout session started"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@shopping_checkout_bp.route('/checkout/<session_id>/update', methods=['PUT'])
def update_checkout_session(session_id):
    """Update checkout session with selected options"""
    data = request.get_json()
    
    checkout_session = CheckoutSession.query.filter_by(session_id=session_id).first()
    if not checkout_session:
        return jsonify({
            "success": False,
            "error": "Checkout session not found"
        }), 404
    
    try:
        # Update step
        if 'step' in data:
            checkout_session.step = data['step']
        
        # Update selected options
        if 'shipping_address_id' in data:
            checkout_session.shipping_address_id = data['shipping_address_id']
        
        if 'shipping_method_id' in data:
            checkout_session.shipping_method_id = data['shipping_method_id']
        
        if 'payment_method_id' in data:
            checkout_session.payment_method_id = data['payment_method_id']
        
        if 'coupon_id' in data:
            checkout_session.coupon_id = data['coupon_id']
        
        # Recalculate totals
        _calculate_checkout_totals(checkout_session)
        
        # Update activity timestamp
        checkout_session.last_activity_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "checkout_session": checkout_session.to_dict(),
            "message": "Checkout session updated"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@shopping_checkout_bp.route('/checkout/<session_id>/complete', methods=['POST'])
def complete_checkout():
    """Complete checkout and create order"""
    data = request.get_json()
    
    checkout_session = CheckoutSession.query.filter_by(session_id=session_id).first()
    if not checkout_session:
        return jsonify({
            "success": False,
            "error": "Checkout session not found"
        }), 404
    
    try:
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
            status='pending',
            payment_status='pending'
        )
        
        # Add shipping and billing addresses
        if checkout_session.shipping_address:
            order.shipping_address = json.dumps(checkout_session.shipping_address.to_dict())
        
        # Add shipping method
        if checkout_session.shipping_method:
            order.shipping_method = checkout_session.shipping_method.name
        
        db.session.add(order)
        db.session.flush()
        
        # Create order items from cart items
        cart_items = CartItem.query.filter_by(cart_id=checkout_session.cart_id).all()
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                selected_color=cart_item.selected_color,
                selected_size=cart_item.selected_size,
                unit_price=cart_item.unit_price,
                total_price=cart_item.total_price
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
        
        # Update checkout session
        checkout_session.status = 'completed'
        checkout_session.completed_at = datetime.utcnow()
        
        # Update cart status
        checkout_session.cart.status = 'converted'
        
        db.session.commit()
        
        # Send order confirmation notification
        _send_order_notification(order, 'order_confirmed')
        
        return jsonify({
            "success": True,
            "order": order.to_dict(),
            "checkout_session": checkout_session.to_dict(),
            "message": f"Order {order.order_number} created successfully"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# ============================================================================
# ORDER TRACKING
# ============================================================================

@shopping_checkout_bp.route('/orders/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    """Get user's orders"""
    status_filter = request.args.get('status')
    limit = int(request.args.get('limit', 20))
    
    query = Order.query.filter_by(user_id=user_id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    orders = query.order_by(Order.created_at.desc()).limit(limit).all()
    
    return jsonify({
        "orders": [order.to_dict() for order in orders],
        "user_id": user_id,
        "total_orders": len(orders),
        "status_filter": status_filter,
        "message": f"Orders for user {user_id}"
    })

@shopping_checkout_bp.route('/orders/<order_number>/track', methods=['GET'])
def track_order(order_number):
    """Track order status"""
    order = Order.query.filter_by(order_number=order_number).first()
    if not order:
        return jsonify({
            "success": False,
            "error": "Order not found"
        }), 404
    
    # Get order notifications
    notifications = OrderNotification.query.filter_by(order_id=order.id).order_by(
        OrderNotification.created_at.desc()
    ).all()
    
    return jsonify({
        "order": order.to_dict(),
        "tracking": {
            "current_status": order.status,
            "payment_status": order.payment_status,
            "tracking_number": order.tracking_number,
            "estimated_delivery": None,  # Would integrate with shipping provider
            "order_timeline": [notif.to_dict() for notif in notifications]
        },
        "message": f"Order {order_number} tracking information"
    })

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _calculate_cart_totals(cart):
    """Calculate cart totals"""
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    
    subtotal = sum(item.total_price for item in cart_items)
    
    # Calculate tax (using market tax rate)
    tax_amount = subtotal * cart.market.tax_rate
    
    # Calculate shipping (basic logic)
    shipping_cost = cart.market.shipping_base_cost
    if subtotal >= cart.market.free_shipping_threshold:
        shipping_cost = 0.0
    
    total_amount = subtotal + tax_amount + shipping_cost
    
    # Update cart
    cart.subtotal = subtotal
    cart.tax_amount = tax_amount
    cart.shipping_cost = shipping_cost
    cart.total_amount = total_amount
    cart.updated_at = datetime.utcnow()

def _calculate_checkout_totals(checkout_session):
    """Calculate checkout session totals"""
    cart = checkout_session.cart
    
    # Start with cart totals
    subtotal = cart.subtotal
    tax_amount = cart.tax_amount
    shipping_cost = cart.shipping_cost
    discount_amount = 0.0
    
    # Apply shipping method cost if selected
    if checkout_session.shipping_method:
        shipping_cost = checkout_session.shipping_method.base_cost
        if checkout_session.shipping_method.free_shipping_threshold and subtotal >= checkout_session.shipping_method.free_shipping_threshold:
            shipping_cost = 0.0
    
    # Apply coupon discount if selected
    if checkout_session.coupon:
        coupon = checkout_session.coupon
        if coupon.discount_type == 'percentage':
            discount_amount = (subtotal * coupon.discount_value) / 100
            if coupon.maximum_discount_amount:
                discount_amount = min(discount_amount, coupon.maximum_discount_amount)
        else:  # fixed_amount
            discount_amount = min(coupon.discount_value, subtotal)
    
    total_amount = subtotal + tax_amount + shipping_cost - discount_amount
    
    # Update checkout session
    checkout_session.subtotal = subtotal
    checkout_session.tax_amount = tax_amount
    checkout_session.shipping_cost = shipping_cost
    checkout_session.discount_amount = discount_amount
    checkout_session.total_amount = total_amount

def _send_order_notification(order, notification_type):
    """Send order notification (simulated)"""
    # This would integrate with email/SMS services
    notification = OrderNotification(
        order_id=order.id,
        user_id=order.user_id,
        notification_type=notification_type,
        channel='email',
        subject=f"Order Confirmation - {order.order_number}",
        message=f"Thank you for your order! Your order {order.order_number} has been confirmed and is being processed.",
        status='sent',
        recipient='user@example.com',  # Would get from user profile
        sent_at=datetime.utcnow()
    )
    
    db.session.add(notification)
    return notification

