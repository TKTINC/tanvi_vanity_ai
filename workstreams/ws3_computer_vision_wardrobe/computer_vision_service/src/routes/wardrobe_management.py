"""
WS3-P2: Wardrobe Management & Visual Cataloging
Enhanced Wardrobe Management API Routes for Tanvi Vanity Agent
"We girls have no time" - Smart wardrobe organization in seconds!
"""

from flask import Blueprint, request, jsonify
from src.models.cv_models import db, WardrobeItem
from src.models.wardrobe_management import (
    WardrobeCollection, WardrobeItemCollection, WardrobeAnalytics, 
    BatchProcessingJob, WardrobeTag, WardrobeItemTag, WardrobeMaintenanceLog
)
import json
import time
from datetime import datetime, timedelta
from collections import Counter

wardrobe_management_bp = Blueprint('wardrobe_management', __name__)

def get_user_from_token(request):
    """Extract user ID from JWT token (integration with WS1)"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    return 1  # Mock user ID

def calculate_wardrobe_analytics(user_id):
    """
    Calculate comprehensive wardrobe analytics
    "We girls have no time" - Instant wardrobe intelligence!
    """
    items = WardrobeItem.query.filter_by(user_id=user_id).all()
    
    if not items:
        return None
    
    # Basic composition
    total_items = len(items)
    categories = Counter([item.category for item in items])
    colors = Counter([item.color_primary for item in items])
    brands = Counter([item.brand for item in items if item.brand])
    
    # Usage analytics
    worn_items = [item for item in items if item.wear_count > 0]
    unworn_items = [item for item in items if item.wear_count == 0]
    
    most_worn = sorted(worn_items, key=lambda x: x.wear_count, reverse=True)[:5]
    least_worn = sorted(worn_items, key=lambda x: x.wear_count)[:5]
    
    avg_wear_frequency = sum([item.wear_count for item in items]) / total_items if total_items > 0 else 0
    
    # Style analytics
    styles = []
    for item in items:
        if item.cv_style_tags:
            styles.extend(json.loads(item.cv_style_tags))
    style_distribution = Counter(styles)
    
    # Health metrics (simplified calculations)
    versatility_score = min(100, (len(categories) / max(1, total_items)) * 100)
    completeness_score = min(100, len(categories) * 10)  # Basic categories coverage
    efficiency_score = (len(worn_items) / max(1, total_items)) * 100
    style_coherence_score = max(style_distribution.values()) / max(1, len(styles)) * 100 if styles else 0
    
    # Recommendations
    essential_categories = ['tops', 'bottoms', 'dresses', 'outerwear', 'shoes']
    wardrobe_gaps = [cat for cat in essential_categories if cat not in categories]
    
    # Find potential duplicates (same category and color)
    duplicates = []
    for i, item1 in enumerate(items):
        for item2 in items[i+1:]:
            if (item1.category == item2.category and 
                item1.color_primary == item2.color_primary and
                item1.id != item2.id):
                duplicates.append([item1.id, item2.id])
    
    underutilized = [item.id for item in items if item.wear_count < avg_wear_frequency * 0.5]
    
    return {
        'total_items': total_items,
        'category_breakdown': dict(categories),
        'color_breakdown': dict(colors),
        'brand_breakdown': dict(brands),
        'most_worn_items': [item.id for item in most_worn],
        'least_worn_items': [item.id for item in least_worn],
        'unworn_items': [item.id for item in unworn_items],
        'average_wear_frequency': avg_wear_frequency,
        'style_distribution': dict(style_distribution),
        'formality_distribution': {},  # Placeholder
        'seasonal_distribution': {},  # Placeholder
        'versatility_score': versatility_score,
        'completeness_score': completeness_score,
        'efficiency_score': efficiency_score,
        'style_coherence_score': style_coherence_score,
        'wardrobe_gaps': wardrobe_gaps,
        'duplicate_items': duplicates,
        'underutilized_items': underutilized
    }

@wardrobe_management_bp.route('/collections', methods=['GET'])
def get_collections():
    """
    Get user's wardrobe collections
    "We girls have no time" - Quick collection overview!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        collections = WardrobeCollection.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'collections': [collection.to_dict() for collection in collections],
            'total_collections': len(collections),
            'tagline': 'We girls have no time - Collections loaded instantly!'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get collections: {str(e)}'}), 500

@wardrobe_management_bp.route('/collections', methods=['POST'])
def create_collection():
    """
    Create new wardrobe collection
    "We girls have no time" - Quick collection creation!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Collection name required'}), 400
    
    try:
        collection = WardrobeCollection(
            user_id=user_id,
            name=data['name'],
            description=data.get('description'),
            collection_type=data.get('collection_type', 'custom'),
            auto_rules=json.dumps(data.get('auto_rules')) if data.get('auto_rules') else None,
            color_theme=data.get('color_theme'),
            style_theme=data.get('style_theme')
        )
        
        db.session.add(collection)
        db.session.commit()
        
        return jsonify({
            'message': 'Collection created successfully',
            'collection': collection.to_dict(),
            'tagline': 'We girls have no time - Collection created instantly!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create collection: {str(e)}'}), 500

@wardrobe_management_bp.route('/collections/<int:collection_id>/items', methods=['POST'])
def add_item_to_collection():
    """
    Add item to collection
    "We girls have no time" - Quick item organization!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    if not data or 'item_id' not in data:
        return jsonify({'error': 'Item ID required'}), 400
    
    try:
        # Verify collection belongs to user
        collection = WardrobeCollection.query.filter_by(id=collection_id, user_id=user_id).first()
        if not collection:
            return jsonify({'error': 'Collection not found'}), 404
        
        # Verify item belongs to user
        item = WardrobeItem.query.filter_by(id=data['item_id'], user_id=user_id).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        # Check if already in collection
        existing = WardrobeItemCollection.query.filter_by(
            wardrobe_item_id=data['item_id'],
            collection_id=collection_id
        ).first()
        
        if existing:
            return jsonify({'error': 'Item already in collection'}), 400
        
        # Add to collection
        item_collection = WardrobeItemCollection(
            wardrobe_item_id=data['item_id'],
            collection_id=collection_id,
            added_by=data.get('added_by', 'user')
        )
        
        db.session.add(item_collection)
        
        # Update collection item count
        collection.item_count += 1
        collection.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Item added to collection successfully',
            'collection': collection.to_dict(),
            'tagline': 'We girls have no time - Item organized instantly!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to add item to collection: {str(e)}'}), 500

@wardrobe_management_bp.route('/analytics', methods=['GET'])
def get_wardrobe_analytics():
    """
    Get comprehensive wardrobe analytics
    "We girls have no time" - Instant wardrobe insights!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        # Check for existing analytics
        today = datetime.utcnow().date()
        existing_analytics = WardrobeAnalytics.query.filter_by(
            user_id=user_id,
            analysis_date=today,
            period_type='daily'
        ).first()
        
        if existing_analytics:
            return jsonify({
                'analytics': existing_analytics.to_dict(),
                'cached': True,
                'tagline': 'We girls have no time - Analytics loaded from cache!'
            })
        
        # Calculate new analytics
        analytics_data = calculate_wardrobe_analytics(user_id)
        
        if not analytics_data:
            return jsonify({
                'message': 'No wardrobe items found',
                'analytics': None,
                'tagline': 'We girls have no time - Add items to see analytics!'
            })
        
        # Create analytics record
        analytics = WardrobeAnalytics(
            user_id=user_id,
            analysis_date=today,
            period_type='daily',
            total_items=analytics_data['total_items'],
            category_breakdown=json.dumps(analytics_data['category_breakdown']),
            color_breakdown=json.dumps(analytics_data['color_breakdown']),
            brand_breakdown=json.dumps(analytics_data['brand_breakdown']),
            most_worn_items=json.dumps(analytics_data['most_worn_items']),
            least_worn_items=json.dumps(analytics_data['least_worn_items']),
            unworn_items=json.dumps(analytics_data['unworn_items']),
            average_wear_frequency=analytics_data['average_wear_frequency'],
            style_distribution=json.dumps(analytics_data['style_distribution']),
            formality_distribution=json.dumps(analytics_data['formality_distribution']),
            seasonal_distribution=json.dumps(analytics_data['seasonal_distribution']),
            versatility_score=analytics_data['versatility_score'],
            completeness_score=analytics_data['completeness_score'],
            efficiency_score=analytics_data['efficiency_score'],
            style_coherence_score=analytics_data['style_coherence_score'],
            wardrobe_gaps=json.dumps(analytics_data['wardrobe_gaps']),
            duplicate_items=json.dumps(analytics_data['duplicate_items']),
            underutilized_items=json.dumps(analytics_data['underutilized_items'])
        )
        
        db.session.add(analytics)
        db.session.commit()
        
        return jsonify({
            'analytics': analytics.to_dict(),
            'cached': False,
            'tagline': 'We girls have no time - Fresh analytics generated!'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get analytics: {str(e)}'}), 500

@wardrobe_management_bp.route('/batch-jobs', methods=['POST'])
def create_batch_job():
    """
    Create batch processing job
    "We girls have no time" - Bulk operations in the background!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    if not data or 'job_type' not in data:
        return jsonify({'error': 'Job type required'}), 400
    
    try:
        job = BatchProcessingJob(
            user_id=user_id,
            job_type=data['job_type'],
            job_name=data.get('job_name', f"{data['job_type']} job"),
            job_description=data.get('job_description'),
            job_parameters=json.dumps(data.get('job_parameters', {}))
        )
        
        # Estimate job size based on type
        if data['job_type'] == 'analyze_all_images':
            total_items = WardrobeItem.query.filter_by(user_id=user_id).count()
            job.total_items = total_items
            job.estimated_completion = datetime.utcnow() + timedelta(minutes=total_items * 2)
        elif data['job_type'] == 'organize_wardrobe':
            total_items = WardrobeItem.query.filter_by(user_id=user_id).count()
            job.total_items = total_items
            job.estimated_completion = datetime.utcnow() + timedelta(minutes=5)
        
        db.session.add(job)
        db.session.commit()
        
        return jsonify({
            'message': 'Batch job created successfully',
            'job': job.to_dict(),
            'tagline': 'We girls have no time - Batch job queued for processing!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create batch job: {str(e)}'}), 500

@wardrobe_management_bp.route('/batch-jobs', methods=['GET'])
def get_batch_jobs():
    """
    Get user's batch processing jobs
    "We girls have no time" - Quick job status overview!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        status_filter = request.args.get('status')
        
        query = BatchProcessingJob.query.filter_by(user_id=user_id)
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        jobs = query.order_by(BatchProcessingJob.created_at.desc()).all()
        
        return jsonify({
            'jobs': [job.to_dict() for job in jobs],
            'total_jobs': len(jobs),
            'tagline': 'We girls have no time - Job status loaded instantly!'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get batch jobs: {str(e)}'}), 500

@wardrobe_management_bp.route('/tags', methods=['GET'])
def get_tags():
    """
    Get user's wardrobe tags
    "We girls have no time" - Quick tag overview!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        category_filter = request.args.get('category')
        
        query = WardrobeTag.query.filter_by(user_id=user_id)
        if category_filter:
            query = query.filter_by(category=category_filter)
        
        tags = query.order_by(WardrobeTag.usage_count.desc()).all()
        
        # Get tag categories
        categories = db.session.query(WardrobeTag.category).filter_by(user_id=user_id).distinct().all()
        categories = [cat[0] for cat in categories if cat[0]]
        
        return jsonify({
            'tags': [tag.to_dict() for tag in tags],
            'categories': categories,
            'total_tags': len(tags),
            'tagline': 'We girls have no time - Tags loaded instantly!'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get tags: {str(e)}'}), 500

@wardrobe_management_bp.route('/tags', methods=['POST'])
def create_tag():
    """
    Create new wardrobe tag
    "We girls have no time" - Quick tag creation!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Tag name required'}), 400
    
    try:
        # Check if tag already exists
        existing_tag = WardrobeTag.query.filter_by(
            user_id=user_id,
            name=data['name'].lower()
        ).first()
        
        if existing_tag:
            return jsonify({'error': 'Tag already exists'}), 400
        
        tag = WardrobeTag(
            user_id=user_id,
            name=data['name'].lower(),
            category=data.get('category'),
            description=data.get('description'),
            color=data.get('color'),
            icon=data.get('icon'),
            auto_generated=data.get('auto_generated', False)
        )
        
        db.session.add(tag)
        db.session.commit()
        
        return jsonify({
            'message': 'Tag created successfully',
            'tag': tag.to_dict(),
            'tagline': 'We girls have no time - Tag created instantly!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create tag: {str(e)}'}), 500

@wardrobe_management_bp.route('/items/<int:item_id>/tags', methods=['POST'])
def add_tag_to_item():
    """
    Add tag to wardrobe item
    "We girls have no time" - Quick item tagging!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    if not data or 'tag_id' not in data:
        return jsonify({'error': 'Tag ID required'}), 400
    
    try:
        # Verify item belongs to user
        item = WardrobeItem.query.filter_by(id=item_id, user_id=user_id).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        # Verify tag belongs to user
        tag = WardrobeTag.query.filter_by(id=data['tag_id'], user_id=user_id).first()
        if not tag:
            return jsonify({'error': 'Tag not found'}), 404
        
        # Check if already tagged
        existing = WardrobeItemTag.query.filter_by(
            wardrobe_item_id=item_id,
            tag_id=data['tag_id']
        ).first()
        
        if existing:
            return jsonify({'error': 'Item already has this tag'}), 400
        
        # Add tag to item
        item_tag = WardrobeItemTag(
            wardrobe_item_id=item_id,
            tag_id=data['tag_id'],
            added_by=data.get('added_by', 'user'),
            confidence=data.get('confidence', 1.0)
        )
        
        db.session.add(item_tag)
        
        # Update tag usage count
        tag.usage_count += 1
        tag.last_used = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Tag added to item successfully',
            'item_id': item_id,
            'tag': tag.to_dict(),
            'tagline': 'We girls have no time - Item tagged instantly!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to add tag to item: {str(e)}'}), 500

@wardrobe_management_bp.route('/maintenance-log', methods=['POST'])
def add_maintenance_log():
    """
    Add maintenance log entry
    "We girls have no time" - Quick care tracking!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    if not data or 'item_id' not in data or 'maintenance_type' not in data:
        return jsonify({'error': 'Item ID and maintenance type required'}), 400
    
    try:
        # Verify item belongs to user
        item = WardrobeItem.query.filter_by(id=data['item_id'], user_id=user_id).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        log_entry = WardrobeMaintenanceLog(
            wardrobe_item_id=data['item_id'],
            maintenance_type=data['maintenance_type'],
            maintenance_date=datetime.fromisoformat(data['maintenance_date']) if data.get('maintenance_date') else datetime.utcnow(),
            notes=data.get('notes'),
            cost=data.get('cost'),
            location=data.get('location'),
            care_instructions=data.get('care_instructions'),
            next_maintenance_due=datetime.fromisoformat(data['next_maintenance_due']) if data.get('next_maintenance_due') else None,
            condition_before=data.get('condition_before'),
            condition_after=data.get('condition_after')
        )
        
        db.session.add(log_entry)
        db.session.commit()
        
        return jsonify({
            'message': 'Maintenance log added successfully',
            'log_entry': log_entry.to_dict(),
            'tagline': 'We girls have no time - Care tracked instantly!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to add maintenance log: {str(e)}'}), 500

@wardrobe_management_bp.route('/smart-organize', methods=['POST'])
def smart_organize_wardrobe():
    """
    Smart wardrobe organization using AI
    "We girls have no time" - AI-powered organization!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        # Get all user items
        items = WardrobeItem.query.filter_by(user_id=user_id).all()
        
        if not items:
            return jsonify({
                'message': 'No items to organize',
                'suggestions': [],
                'tagline': 'We girls have no time - Add items to get organization suggestions!'
            })
        
        # Smart organization suggestions
        suggestions = []
        
        # Suggest collections by color
        colors = {}
        for item in items:
            color = item.color_primary
            if color not in colors:
                colors[color] = []
            colors[color].append(item.id)
        
        for color, item_ids in colors.items():
            if len(item_ids) >= 3:
                suggestions.append({
                    'type': 'color_collection',
                    'name': f'{color.title()} Collection',
                    'description': f'Collection of {color} items',
                    'item_ids': item_ids,
                    'reason': f'You have {len(item_ids)} {color} items that work well together'
                })
        
        # Suggest collections by category
        categories = {}
        for item in items:
            category = item.category
            if category not in categories:
                categories[category] = []
            categories[category].append(item.id)
        
        for category, item_ids in categories.items():
            if len(item_ids) >= 5:
                suggestions.append({
                    'type': 'category_collection',
                    'name': f'{category.title()} Essentials',
                    'description': f'Your {category} collection',
                    'item_ids': item_ids,
                    'reason': f'Organize your {len(item_ids)} {category} items for easy access'
                })
        
        # Suggest tags for untagged items
        untagged_items = []
        for item in items:
            # Check if item has tags (simplified check)
            if not item.cv_style_tags or item.cv_style_tags == '[]':
                untagged_items.append(item.id)
        
        if untagged_items:
            suggestions.append({
                'type': 'tagging_suggestion',
                'name': 'Tag Untagged Items',
                'description': 'Add tags to improve organization',
                'item_ids': untagged_items[:10],  # Limit to 10 items
                'reason': f'{len(untagged_items)} items could benefit from tagging'
            })
        
        return jsonify({
            'suggestions': suggestions,
            'total_suggestions': len(suggestions),
            'organization_score': min(100, len(suggestions) * 20),
            'tagline': 'We girls have no time - Smart organization suggestions ready!'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to organize wardrobe: {str(e)}'}), 500

