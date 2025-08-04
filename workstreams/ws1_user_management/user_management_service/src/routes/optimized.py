from flask import Blueprint, jsonify, request
from src.models.user import User, db
from src.models.profile import StyleProfile, WardrobeItem, OutfitHistory
from src.models.analytics import UserAnalytics, StyleInsights
from src.utils.performance import (
    PerformanceMonitor, ResponseOptimizer, CacheManager, 
    DatabaseOptimizer, APIOptimizer
)
from datetime import datetime, timedelta
import time

optimized_bp = Blueprint('optimized', __name__)

def get_current_user():
    """Helper function to get current authenticated user"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    return User.verify_auth_token(token)


@optimized_bp.route('/dashboard-fast', methods=['GET'])
@PerformanceMonitor.time_endpoint
def get_fast_dashboard():
    """
    Ultra-fast dashboard endpoint optimized for mobile
    "We girls have no time" - Dashboard loads in under 200ms
    """
    user = get_current_user()
    if not user:
        return jsonify(APIOptimizer.create_error_response('Authentication required')), 401
    
    try:
        # Check cache first
        cache_key = f"dashboard_{user.id}"
        cached_data = CacheManager.get(cache_key)
        
        if cached_data:
            cached_data['_meta']['cached'] = True
            return jsonify(cached_data), 200
        
        # Get optimized user profile
        user_profile = DatabaseOptimizer.get_optimized_user_profile(user.id)
        
        # Get optimized wardrobe summary
        wardrobe_summary = DatabaseOptimizer.get_optimized_wardrobe_summary(user.id)
        
        # Get recent activity count (simplified)
        recent_activity_count = UserAnalytics.query.filter(
            UserAnalytics.user_id == user.id,
            UserAnalytics.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        # Get active insights count
        active_insights_count = StyleInsights.query.filter(
            StyleInsights.user_id == user.id,
            StyleInsights.expires_at > datetime.utcnow()
        ).count()
        
        # Build optimized response
        dashboard_data = {
            'user': ResponseOptimizer.optimize_user_data(user_profile),
            'wardrobe': wardrobe_summary,
            'activity': {
                'recent_activity_count': recent_activity_count,
                'active_insights': active_insights_count
            },
            'quick_stats': {
                'profile_completion': user_profile.get('profile_completion', 0),
                'items_count': wardrobe_summary.get('total_items', 0),
                'favorites_count': wardrobe_summary.get('total_favorites', 0)
            }
        }
        
        response = APIOptimizer.create_fast_response(
            dashboard_data,
            'Fast dashboard loaded successfully',
            'We girls have no time - dashboard loaded in milliseconds!'
        )
        
        # Cache for 2 minutes
        CacheManager.set(cache_key, response, 2)
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify(APIOptimizer.create_error_response(
            'Failed to load dashboard',
            str(e)
        )), 500


@optimized_bp.route('/wardrobe-fast', methods=['GET'])
@PerformanceMonitor.time_endpoint
def get_fast_wardrobe():
    """
    Ultra-fast wardrobe endpoint with pagination and optimization
    "We girls have no time" - Wardrobe loads instantly with smart pagination
    """
    user = get_current_user()
    if not user:
        return jsonify(APIOptimizer.create_error_response('Authentication required')), 401
    
    try:
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        category = request.args.get('category')
        favorites_only = request.args.get('favorites') == 'true'
        
        # Build optimized query
        query = WardrobeItem.query.filter_by(user_id=user.id)
        
        if category:
            query = query.filter_by(category=category)
        
        if favorites_only:
            query = query.filter_by(favorite=True)
        
        # Order by most recently worn, then by favorites
        query = query.order_by(
            WardrobeItem.last_worn.desc().nullslast(),
            WardrobeItem.favorite.desc(),
            WardrobeItem.created_at.desc()
        )
        
        # Get paginated results
        paginated_data = ResponseOptimizer.paginate_results(query, page, per_page, 50)
        
        # Optimize wardrobe data for mobile
        paginated_data['items'] = ResponseOptimizer.optimize_wardrobe_data(
            [item.to_dict() for item in query.offset((page-1)*per_page).limit(per_page).all()]
        )
        
        response = APIOptimizer.create_paginated_response(
            paginated_data,
            'Fast wardrobe loaded successfully',
            'We girls have no time - wardrobe loaded instantly!'
        )
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify(APIOptimizer.create_error_response(
            'Failed to load wardrobe',
            str(e)
        )), 500


@optimized_bp.route('/insights-fast', methods=['GET'])
@PerformanceMonitor.time_endpoint
@PerformanceMonitor.cache_response(duration_minutes=3)
def get_fast_insights():
    """
    Ultra-fast insights endpoint with caching
    "We girls have no time" - AI insights load instantly
    """
    user = get_current_user()
    if not user:
        return jsonify(APIOptimizer.create_error_response('Authentication required')), 401
    
    try:
        # Get only active insights with optimized query
        insights = db.session.query(
            StyleInsights.id,
            StyleInsights.insight_type,
            StyleInsights.title,
            StyleInsights.description,
            StyleInsights.priority,
            StyleInsights.confidence_score,
            StyleInsights.created_at
        ).filter(
            StyleInsights.user_id == user.id,
            StyleInsights.expires_at > datetime.utcnow()
        ).order_by(
            StyleInsights.priority.desc(),
            StyleInsights.confidence_score.desc()
        ).limit(10).all()
        
        # Optimize insights data
        optimized_insights = []
        for insight in insights:
            optimized_insights.append({
                'id': insight.id,
                'type': insight.insight_type,
                'title': insight.title,
                'description': insight.description[:100] + '...' if len(insight.description) > 100 else insight.description,
                'priority': insight.priority,
                'confidence': round(insight.confidence_score, 1),
                'age_hours': int((datetime.utcnow() - insight.created_at).total_seconds() / 3600)
            })
        
        response = APIOptimizer.create_fast_response(
            optimized_insights,
            'Fast insights loaded successfully',
            'We girls have no time - AI insights ready instantly!',
            {'insights_count': len(optimized_insights)}
        )
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify(APIOptimizer.create_error_response(
            'Failed to load insights',
            str(e)
        )), 500


@optimized_bp.route('/profile-fast', methods=['GET'])
@PerformanceMonitor.time_endpoint
def get_fast_profile():
    """
    Ultra-fast profile endpoint with optimized data
    "We girls have no time" - Profile loads in a flash
    """
    user = get_current_user()
    if not user:
        return jsonify(APIOptimizer.create_error_response('Authentication required')), 401
    
    try:
        # Get optimized profile data
        profile_data = DatabaseOptimizer.get_optimized_user_profile(user.id)
        
        if not profile_data:
            return jsonify(APIOptimizer.create_error_response('Profile not found')), 404
        
        # Get style profile if exists
        style_profile = StyleProfile.query.filter_by(user_id=user.id).first()
        
        if style_profile:
            profile_data.update({
                'style_personality': style_profile.style_personality,
                'body_type': style_profile.body_type,
                'color_palette': style_profile.color_palette,
                'style_goals': style_profile.style_goals,
                'completion_percentage': style_profile.calculate_completion()
            })
        
        response = APIOptimizer.create_fast_response(
            profile_data,
            'Fast profile loaded successfully',
            'We girls have no time - profile loaded instantly!'
        )
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify(APIOptimizer.create_error_response(
            'Failed to load profile',
            str(e)
        )), 500


@optimized_bp.route('/quick-actions', methods=['POST'])
@PerformanceMonitor.time_endpoint
def quick_actions():
    """
    Ultra-fast actions endpoint for common operations
    "We girls have no time" - Execute actions instantly
    """
    user = get_current_user()
    if not user:
        return jsonify(APIOptimizer.create_error_response('Authentication required')), 401
    
    try:
        data = request.json
        action_type = data.get('action')
        
        if action_type == 'mark_favorite':
            # Quick favorite toggle
            item_id = data.get('item_id')
            item = WardrobeItem.query.filter_by(id=item_id, user_id=user.id).first()
            
            if item:
                item.favorite = not item.favorite
                db.session.commit()
                
                # Clear cache
                CacheManager.delete(f"wardrobe_summary_{user.id}")
                
                return jsonify(APIOptimizer.create_fast_response(
                    {'item_id': item_id, 'favorite': item.favorite},
                    'Favorite status updated',
                    'We girls have no time - favorite updated instantly!'
                )), 200
        
        elif action_type == 'mark_worn':
            # Quick wear tracking
            item_id = data.get('item_id')
            item = WardrobeItem.query.filter_by(id=item_id, user_id=user.id).first()
            
            if item:
                item.wear_count += 1
                item.last_worn = datetime.utcnow()
                db.session.commit()
                
                # Clear cache
                CacheManager.delete(f"wardrobe_summary_{user.id}")
                
                return jsonify(APIOptimizer.create_fast_response(
                    {'item_id': item_id, 'wear_count': item.wear_count},
                    'Wear count updated',
                    'We girls have no time - wear tracked instantly!'
                )), 200
        
        elif action_type == 'dismiss_insight':
            # Quick insight dismissal
            insight_id = data.get('insight_id')
            insight = StyleInsights.query.filter_by(id=insight_id, user_id=user.id).first()
            
            if insight:
                insight.expires_at = datetime.utcnow()  # Expire immediately
                db.session.commit()
                
                return jsonify(APIOptimizer.create_fast_response(
                    {'insight_id': insight_id, 'dismissed': True},
                    'Insight dismissed',
                    'We girls have no time - insight dismissed instantly!'
                )), 200
        
        return jsonify(APIOptimizer.create_error_response(
            'Unknown action type',
            f'Action "{action_type}" not supported'
        )), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify(APIOptimizer.create_error_response(
            'Failed to execute action',
            str(e)
        )), 500


@optimized_bp.route('/search-fast', methods=['GET'])
@PerformanceMonitor.time_endpoint
def fast_search():
    """
    Ultra-fast search across user data
    "We girls have no time" - Search results in milliseconds
    """
    user = get_current_user()
    if not user:
        return jsonify(APIOptimizer.create_error_response('Authentication required')), 401
    
    try:
        query = request.args.get('q', '').strip()
        search_type = request.args.get('type', 'all')  # all, wardrobe, insights
        limit = min(int(request.args.get('limit', 20)), 50)
        
        if not query:
            return jsonify(APIOptimizer.create_error_response('Search query required')), 400
        
        results = {'wardrobe': [], 'insights': []}
        
        if search_type in ['all', 'wardrobe']:
            # Search wardrobe items
            wardrobe_items = WardrobeItem.query.filter(
                WardrobeItem.user_id == user.id,
                db.or_(
                    WardrobeItem.name.ilike(f'%{query}%'),
                    WardrobeItem.category.ilike(f'%{query}%'),
                    WardrobeItem.primary_color.ilike(f'%{query}%'),
                    WardrobeItem.brand.ilike(f'%{query}%')
                )
            ).limit(limit).all()
            
            results['wardrobe'] = ResponseOptimizer.optimize_wardrobe_data(
                [item.to_dict() for item in wardrobe_items]
            )
        
        if search_type in ['all', 'insights']:
            # Search insights
            insights = StyleInsights.query.filter(
                StyleInsights.user_id == user.id,
                StyleInsights.expires_at > datetime.utcnow(),
                db.or_(
                    StyleInsights.title.ilike(f'%{query}%'),
                    StyleInsights.description.ilike(f'%{query}%'),
                    StyleInsights.insight_type.ilike(f'%{query}%')
                )
            ).limit(limit).all()
            
            results['insights'] = [
                {
                    'id': insight.id,
                    'title': insight.title,
                    'type': insight.insight_type,
                    'priority': insight.priority
                }
                for insight in insights
            ]
        
        total_results = len(results['wardrobe']) + len(results['insights'])
        
        response = APIOptimizer.create_fast_response(
            results,
            f'Search completed - {total_results} results found',
            'We girls have no time - search results ready instantly!',
            {
                'query': query,
                'total_results': total_results,
                'search_type': search_type
            }
        )
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify(APIOptimizer.create_error_response(
            'Search failed',
            str(e)
        )), 500


@optimized_bp.route('/bulk-operations', methods=['POST'])
@PerformanceMonitor.time_endpoint
def bulk_operations():
    """
    Bulk operations endpoint for batch processing
    "We girls have no time" - Process multiple operations at once
    """
    user = get_current_user()
    if not user:
        return jsonify(APIOptimizer.create_error_response('Authentication required')), 401
    
    try:
        data = request.json
        operations = data.get('operations', [])
        
        if not operations:
            return jsonify(APIOptimizer.create_error_response('No operations provided')), 400
        
        results = []
        
        # Process operations in batches
        for operation in operations[:50]:  # Limit to 50 operations
            op_type = operation.get('type')
            op_data = operation.get('data', {})
            
            if op_type == 'update_wardrobe_item':
                item_id = op_data.get('id')
                item = WardrobeItem.query.filter_by(id=item_id, user_id=user.id).first()
                
                if item:
                    for key, value in op_data.items():
                        if key != 'id' and hasattr(item, key):
                            setattr(item, key, value)
                    
                    results.append({'operation': op_type, 'item_id': item_id, 'success': True})
                else:
                    results.append({'operation': op_type, 'item_id': item_id, 'success': False, 'error': 'Item not found'})
        
        # Commit all changes at once
        db.session.commit()
        
        # Clear relevant caches
        CacheManager.delete(f"wardrobe_summary_{user.id}")
        CacheManager.delete(f"dashboard_{user.id}")
        
        response = APIOptimizer.create_fast_response(
            results,
            f'Bulk operations completed - {len(results)} operations processed',
            'We girls have no time - bulk operations completed instantly!'
        )
        
        return jsonify(response), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify(APIOptimizer.create_error_response(
            'Bulk operations failed',
            str(e)
        )), 500


@optimized_bp.route('/performance-stats', methods=['GET'])
def get_performance_stats():
    """
    Get performance statistics for monitoring
    "We girls have no time" - Monitor performance in real-time
    """
    try:
        stats = PerformanceMonitor.get_performance_metrics()
        cache_stats = {
            'cache_size': len(CacheManager._cache),
            'cached_keys': list(CacheManager._cache.keys())[:10]  # Show first 10 keys
        }
        
        db_stats = DatabaseOptimizer.optimize_user_queries()
        
        response = APIOptimizer.create_fast_response(
            {
                'performance': stats,
                'cache': cache_stats,
                'database': db_stats
            },
            'Performance statistics retrieved',
            'We girls have no time - here\'s how fast we are!'
        )
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify(APIOptimizer.create_error_response(
            'Failed to get performance stats',
            str(e)
        )), 500

