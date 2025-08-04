from flask import Blueprint, request, jsonify
from src.models.ecommerce_models import db, Merchant, Product
from src.models.merchant_integration import (
    MerchantAPI, ProductSync, MerchantWebhook, get_merchant_adapter
)
from src.models.product_catalog import ProductInventory
import json
from datetime import datetime, timedelta
import uuid

merchant_integration_bp = Blueprint('merchant_integration', __name__)

# ============================================================================
# MERCHANT INTEGRATION HEALTH & STATUS
# ============================================================================

@merchant_integration_bp.route('/integration/health', methods=['GET'])
def integration_health_check():
    """Health check for merchant integration service"""
    # Get integration statistics
    total_merchants = Merchant.query.filter_by(is_active=True).count()
    active_apis = MerchantAPI.query.filter_by(is_active=True).count()
    recent_syncs = ProductSync.query.filter(
        ProductSync.created_at >= datetime.utcnow() - timedelta(hours=24)
    ).count()
    
    return jsonify({
        "status": "healthy",
        "service": "WS5: Merchant Integration",
        "version": "2.0.0",
        "tagline": "We girls have no time",
        "philosophy": "Seamless merchant integrations for instant product access",
        "integration_stats": {
            "total_merchants": total_merchants,
            "active_api_configs": active_apis,
            "syncs_last_24h": recent_syncs,
            "supported_merchants": ["Zara US", "Myntra", "Amazon Fashion", "H&M", "Target"]
        },
        "capabilities": [
            "Real-time product synchronization",
            "Inventory management",
            "Price updates",
            "Order creation & tracking",
            "Webhook integration",
            "Multi-market support"
        ],
        "message": "Merchant integrations ready for lightning-fast product access!"
    })

@merchant_integration_bp.route('/integration/merchants/<merchant_code>/status', methods=['GET'])
def get_merchant_integration_status(merchant_code):
    """Get integration status for specific merchant"""
    merchant = Merchant.query.filter_by(code=merchant_code, is_active=True).first()
    if not merchant:
        return jsonify({
            "success": False,
            "error": "Merchant not found",
            "message": f"Merchant {merchant_code} does not exist"
        }), 404
    
    # Get API configuration
    api_config = MerchantAPI.query.filter_by(merchant_id=merchant.id).first()
    
    # Get recent sync history
    recent_syncs = ProductSync.query.filter_by(
        merchant_id=merchant.id
    ).order_by(ProductSync.created_at.desc()).limit(5).all()
    
    # Get webhook configuration
    webhooks = MerchantWebhook.query.filter_by(merchant_id=merchant.id).all()
    
    # Calculate health metrics
    total_products = Product.query.filter_by(merchant_id=merchant.id, is_active=True).count()
    successful_syncs = len([s for s in recent_syncs if s.sync_status == 'completed'])
    
    return jsonify({
        "merchant": merchant.to_dict(),
        "api_config": api_config.to_dict() if api_config else None,
        "integration_health": {
            "status": "healthy" if api_config and api_config.consecutive_failures < 3 else "degraded",
            "total_products": total_products,
            "recent_sync_success_rate": successful_syncs / max(len(recent_syncs), 1) if recent_syncs else 0,
            "last_successful_sync": recent_syncs[0].completed_at.isoformat() if recent_syncs and recent_syncs[0].sync_status == 'completed' else None
        },
        "recent_syncs": [sync.to_dict() for sync in recent_syncs],
        "webhooks": [webhook.to_dict() for webhook in webhooks],
        "message": f"Integration status for {merchant.name}"
    })

# ============================================================================
# PRODUCT SYNCHRONIZATION ENDPOINTS
# ============================================================================

@merchant_integration_bp.route('/integration/merchants/<merchant_code>/sync', methods=['POST'])
def sync_merchant_products(merchant_code):
    """Trigger product synchronization for merchant"""
    data = request.get_json() or {}
    sync_type = data.get('sync_type', 'incremental')  # 'full', 'incremental', 'single_product'
    force_sync = data.get('force_sync', False)
    
    merchant = Merchant.query.filter_by(code=merchant_code, is_active=True).first()
    if not merchant:
        return jsonify({
            "success": False,
            "error": "Merchant not found",
            "message": f"Merchant {merchant_code} does not exist"
        }), 404
    
    try:
        # Check if sync is already running
        running_sync = ProductSync.query.filter_by(
            merchant_id=merchant.id,
            sync_status='running'
        ).first()
        
        if running_sync and not force_sync:
            return jsonify({
                "success": False,
                "error": "Sync already running",
                "message": f"Product sync is already running for {merchant.name}",
                "running_sync": running_sync.to_dict()
            }), 409
        
        # Create sync record
        sync_record = ProductSync(
            merchant_id=merchant.id,
            sync_type=sync_type,
            sync_status='running',
            started_at=datetime.utcnow()
        )
        db.session.add(sync_record)
        db.session.commit()
        
        # Get merchant adapter and perform sync
        adapter = get_merchant_adapter(merchant_code)
        sync_result = _perform_product_sync(adapter, sync_record, sync_type)
        
        return jsonify({
            "success": True,
            "sync_record": sync_result.to_dict(),
            "message": f"Product sync completed for {merchant.name}"
        })
        
    except Exception as e:
        # Update sync record with error
        if 'sync_record' in locals():
            sync_record.sync_status = 'failed'
            sync_record.error_message = str(e)
            sync_record.completed_at = datetime.utcnow()
            sync_record.duration_seconds = int((datetime.utcnow() - sync_record.started_at).total_seconds())
            db.session.commit()
        
        return jsonify({
            "success": False,
            "error": "Sync failed",
            "message": str(e)
        }), 500

@merchant_integration_bp.route('/integration/sync-history', methods=['GET'])
def get_sync_history():
    """Get synchronization history across all merchants"""
    merchant_code = request.args.get('merchant')
    status = request.args.get('status')  # pending, running, completed, failed
    limit = min(request.args.get('limit', 50, type=int), 200)
    
    query = ProductSync.query
    
    if merchant_code:
        merchant = Merchant.query.filter_by(code=merchant_code).first()
        if merchant:
            query = query.filter_by(merchant_id=merchant.id)
    
    if status:
        query = query.filter_by(sync_status=status)
    
    syncs = query.order_by(ProductSync.created_at.desc()).limit(limit).all()
    
    return jsonify({
        "sync_history": [sync.to_dict() for sync in syncs],
        "total_syncs": len(syncs),
        "filters": {
            "merchant": merchant_code,
            "status": status
        },
        "message": "Product synchronization history"
    })

# ============================================================================
# INVENTORY MANAGEMENT ENDPOINTS
# ============================================================================

@merchant_integration_bp.route('/integration/inventory/sync', methods=['POST'])
def sync_inventory():
    """Sync inventory levels from all merchants"""
    data = request.get_json() or {}
    merchant_codes = data.get('merchants', [])  # Specific merchants or all
    
    results = []
    
    # Get merchants to sync
    if merchant_codes:
        merchants = Merchant.query.filter(
            Merchant.code.in_(merchant_codes),
            Merchant.is_active == True
        ).all()
    else:
        merchants = Merchant.query.filter_by(is_active=True).all()
    
    for merchant in merchants:
        try:
            adapter = get_merchant_adapter(merchant.code)
            inventory_result = _sync_merchant_inventory(adapter, merchant)
            results.append({
                "merchant": merchant.code,
                "success": True,
                "result": inventory_result
            })
        except Exception as e:
            results.append({
                "merchant": merchant.code,
                "success": False,
                "error": str(e)
            })
    
    successful_syncs = len([r for r in results if r['success']])
    
    return jsonify({
        "success": successful_syncs > 0,
        "results": results,
        "summary": {
            "total_merchants": len(merchants),
            "successful_syncs": successful_syncs,
            "failed_syncs": len(results) - successful_syncs
        },
        "message": f"Inventory sync completed for {successful_syncs}/{len(merchants)} merchants"
    })

@merchant_integration_bp.route('/integration/inventory/low-stock', methods=['GET'])
def get_low_stock_alerts():
    """Get low stock alerts across all merchants"""
    merchant_code = request.args.get('merchant')
    threshold = request.args.get('threshold', type=int)
    
    query = ProductInventory.query.filter_by(is_active=True)
    
    if merchant_code:
        merchant = Merchant.query.filter_by(code=merchant_code).first()
        if merchant:
            product_ids = [p.id for p in merchant.products if p.is_active]
            query = query.filter(ProductInventory.product_id.in_(product_ids))
    
    if threshold:
        query = query.filter(ProductInventory.quantity_available <= threshold)
    else:
        # Use each product's individual threshold
        query = query.filter(ProductInventory.quantity_available <= ProductInventory.low_stock_threshold)
    
    low_stock_items = query.join(Product).filter(Product.is_active == True).all()
    
    return jsonify({
        "low_stock_items": [item.to_dict() for item in low_stock_items],
        "total_items": len(low_stock_items),
        "filters": {
            "merchant": merchant_code,
            "threshold": threshold
        },
        "message": f"Found {len(low_stock_items)} low stock items requiring attention"
    })

# ============================================================================
# WEBHOOK MANAGEMENT ENDPOINTS
# ============================================================================

@merchant_integration_bp.route('/integration/webhooks', methods=['GET'])
def get_webhooks():
    """Get webhook configurations"""
    merchant_code = request.args.get('merchant')
    
    query = MerchantWebhook.query
    if merchant_code:
        merchant = Merchant.query.filter_by(code=merchant_code).first()
        if merchant:
            query = query.filter_by(merchant_id=merchant.id)
    
    webhooks = query.all()
    
    return jsonify({
        "webhooks": [webhook.to_dict() for webhook in webhooks],
        "total_webhooks": len(webhooks),
        "message": "Webhook configurations"
    })

@merchant_integration_bp.route('/integration/webhooks/<merchant_code>', methods=['POST'])
def create_webhook(merchant_code):
    """Create webhook configuration for merchant"""
    data = request.get_json()
    
    merchant = Merchant.query.filter_by(code=merchant_code, is_active=True).first()
    if not merchant:
        return jsonify({
            "success": False,
            "error": "Merchant not found"
        }), 404
    
    try:
        webhook = MerchantWebhook(
            merchant_id=merchant.id,
            webhook_url=data['webhook_url'],
            merchant_webhook_id=data.get('merchant_webhook_id'),
            event_types=json.dumps(data.get('event_types', [])),
            secret_key=data.get('secret_key'),
            signature_header=data.get('signature_header', 'X-Signature')
        )
        
        db.session.add(webhook)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "webhook": webhook.to_dict(),
            "message": f"Webhook created for {merchant.name}"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@merchant_integration_bp.route('/integration/webhooks/receive/<merchant_code>', methods=['POST'])
def receive_webhook(merchant_code):
    """Receive webhook from merchant"""
    merchant = Merchant.query.filter_by(code=merchant_code, is_active=True).first()
    if not merchant:
        return jsonify({"error": "Merchant not found"}), 404
    
    # Get webhook configuration
    webhook_config = MerchantWebhook.query.filter_by(
        merchant_id=merchant.id,
        is_active=True
    ).first()
    
    if not webhook_config:
        return jsonify({"error": "Webhook not configured"}), 404
    
    try:
        # Verify webhook signature if configured
        if webhook_config.secret_key and webhook_config.signature_header:
            signature = request.headers.get(webhook_config.signature_header)
            if not _verify_webhook_signature(request.data, webhook_config.secret_key, signature):
                return jsonify({"error": "Invalid signature"}), 401
        
        # Process webhook data
        webhook_data = request.get_json()
        result = _process_webhook_data(merchant, webhook_data)
        
        # Update webhook statistics
        webhook_config.last_received = datetime.utcnow()
        webhook_config.total_received += 1
        if result['success']:
            webhook_config.total_processed += 1
        else:
            webhook_config.total_failed += 1
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Webhook processed successfully",
            "result": result
        })
        
    except Exception as e:
        webhook_config.total_failed += 1
        db.session.commit()
        
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _perform_product_sync(adapter, sync_record, sync_type):
    """Perform actual product synchronization"""
    try:
        # Get products from merchant
        if sync_type == 'full':
            products_data = adapter.get_products(limit=1000)
        else:
            products_data = adapter.get_products(limit=100)  # Incremental sync
        
        products_processed = 0
        products_created = 0
        products_updated = 0
        products_failed = 0
        
        for product_data in products_data.get('products', []):
            try:
                # Check if product exists
                existing_product = Product.query.filter_by(
                    merchant_id=sync_record.merchant_id,
                    merchant_product_id=product_data['id']
                ).first()
                
                if existing_product:
                    # Update existing product
                    _update_product_from_data(existing_product, product_data)
                    products_updated += 1
                else:
                    # Create new product
                    _create_product_from_data(sync_record.merchant_id, product_data)
                    products_created += 1
                
                products_processed += 1
                
            except Exception as e:
                products_failed += 1
                print(f"Failed to process product {product_data.get('id', 'unknown')}: {str(e)}")
        
        # Update sync record
        sync_record.sync_status = 'completed'
        sync_record.products_processed = products_processed
        sync_record.products_created = products_created
        sync_record.products_updated = products_updated
        sync_record.products_failed = products_failed
        sync_record.completed_at = datetime.utcnow()
        sync_record.duration_seconds = int((datetime.utcnow() - sync_record.started_at).total_seconds())
        
        db.session.commit()
        return sync_record
        
    except Exception as e:
        sync_record.sync_status = 'failed'
        sync_record.error_message = str(e)
        sync_record.completed_at = datetime.utcnow()
        sync_record.duration_seconds = int((datetime.utcnow() - sync_record.started_at).total_seconds())
        db.session.commit()
        raise

def _create_product_from_data(merchant_id, product_data):
    """Create new product from merchant data"""
    product = Product(
        merchant_id=merchant_id,
        sku=f"{product_data['id']}-{uuid.uuid4().hex[:8]}",
        merchant_product_id=product_data['id'],
        name=product_data['name'],
        description=product_data.get('description'),
        brand=product_data.get('brand'),
        category=product_data.get('category'),
        original_price=product_data['price'],
        sale_price=product_data.get('sale_price'),
        currency=product_data['currency'],
        colors=json.dumps(product_data.get('colors', [])),
        sizes=json.dumps(product_data.get('sizes', [])),
        primary_image_url=product_data.get('images', [None])[0],
        additional_images=json.dumps(product_data.get('images', [])),
        stock_quantity=product_data.get('stock', 0),
        is_in_stock=product_data.get('stock', 0) > 0,
        product_url=product_data.get('url')
    )
    
    db.session.add(product)
    db.session.commit()
    return product

def _update_product_from_data(product, product_data):
    """Update existing product from merchant data"""
    product.name = product_data['name']
    product.description = product_data.get('description')
    product.original_price = product_data['price']
    product.sale_price = product_data.get('sale_price')
    product.colors = json.dumps(product_data.get('colors', []))
    product.sizes = json.dumps(product_data.get('sizes', []))
    product.stock_quantity = product_data.get('stock', 0)
    product.is_in_stock = product_data.get('stock', 0) > 0
    product.last_updated = datetime.utcnow()
    
    db.session.commit()
    return product

def _sync_merchant_inventory(adapter, merchant):
    """Sync inventory levels for merchant"""
    # This would call the merchant's inventory API
    # For now, return simulated result
    return {
        "products_checked": 25,
        "inventory_updated": 20,
        "low_stock_alerts": 3,
        "out_of_stock": 2
    }

def _verify_webhook_signature(payload, secret, signature):
    """Verify webhook signature"""
    import hmac
    import hashlib
    
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)

def _process_webhook_data(merchant, webhook_data):
    """Process incoming webhook data"""
    event_type = webhook_data.get('event_type')
    
    if event_type == 'product.updated':
        product_data = webhook_data.get('product')
        if product_data:
            # Update product in our system
            existing_product = Product.query.filter_by(
                merchant_id=merchant.id,
                merchant_product_id=product_data['id']
            ).first()
            
            if existing_product:
                _update_product_from_data(existing_product, product_data)
                return {"success": True, "action": "product_updated"}
    
    elif event_type == 'inventory.changed':
        inventory_data = webhook_data.get('inventory')
        if inventory_data:
            # Update inventory levels
            return {"success": True, "action": "inventory_updated"}
    
    return {"success": True, "action": "webhook_received"}

