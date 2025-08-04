"""
WS3-P3: Outfit Visualization & Virtual Try-On
Outfit Visualization API Routes for Tanvi Vanity Agent
"We girls have no time" - Instant outfit visualization and virtual try-on!
"""

from flask import Blueprint, request, jsonify
from src.models.cv_models import db, WardrobeItem
from src.models.outfit_visualization import (
    OutfitComposition, VirtualTryOn, OutfitVisualizationTemplate, 
    OutfitStylingSession, OutfitVisualizationJob
)
import json
import time
from datetime import datetime, timedelta
import random

outfit_visualization_bp = Blueprint('outfit_visualization', __name__)

def get_user_from_token(request):
    """Extract user ID from JWT token (integration with WS1)"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    return 1  # Mock user ID

def generate_outfit_visualization(outfit_composition, template=None):
    """
    Generate outfit visualization (mock implementation)
    "We girls have no time" - Instant visualization generation!
    """
    # Mock visualization generation
    time.sleep(1)  # Simulate processing time
    
    # Generate mock URLs
    visualization_url = f"https://tanvi-visualizations.com/outfits/{outfit_composition.id}/main.jpg"
    thumbnail_url = f"https://tanvi-visualizations.com/outfits/{outfit_composition.id}/thumb.jpg"
    
    # Mock layout data
    layout_data = {
        "template_type": template.template_type if template else "flat_lay",
        "items": {
            "top": {"x": 150, "y": 100, "width": 200, "height": 250},
            "bottom": {"x": 150, "y": 350, "width": 200, "height": 300},
            "shoes": {"x": 50, "y": 650, "width": 150, "height": 100}
        },
        "background": "white",
        "style": "minimalist"
    }
    
    return visualization_url, thumbnail_url, layout_data

def calculate_ai_scores(outfit_composition):
    """
    Calculate AI scores for outfit composition
    "We girls have no time" - Instant AI analysis!
    """
    # Mock AI scoring
    ai_confidence = random.uniform(0.7, 0.95)
    style_score = random.uniform(0.6, 0.9)
    color_harmony = random.uniform(0.7, 0.95)
    occasion_fit = random.uniform(0.8, 0.95)
    
    return ai_confidence, style_score, color_harmony, occasion_fit

@outfit_visualization_bp.route('/outfits', methods=['POST'])
def create_outfit():
    """
    Create new outfit composition
    "We girls have no time" - Quick outfit creation!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Outfit name required'}), 400
    
    try:
        # Validate that items belong to user
        item_ids = [
            data.get('top_item_id'),
            data.get('bottom_item_id'),
            data.get('dress_item_id'),
            data.get('outerwear_item_id'),
            data.get('shoes_item_id')
        ]
        item_ids = [id for id in item_ids if id is not None]
        
        if data.get('accessories'):
            item_ids.extend(data['accessories'])
        
        # Verify all items belong to user
        for item_id in item_ids:
            item = WardrobeItem.query.filter_by(id=item_id, user_id=user_id).first()
            if not item:
                return jsonify({'error': f'Item {item_id} not found or not accessible'}), 404
        
        # Create outfit composition
        outfit = OutfitComposition(
            user_id=user_id,
            name=data['name'],
            description=data.get('description'),
            occasion=data.get('occasion'),
            season=data.get('season'),
            top_item_id=data.get('top_item_id'),
            bottom_item_id=data.get('bottom_item_id'),
            dress_item_id=data.get('dress_item_id'),
            outerwear_item_id=data.get('outerwear_item_id'),
            shoes_item_id=data.get('shoes_item_id'),
            accessories=json.dumps(data.get('accessories', [])),
            style_tags=json.dumps(data.get('style_tags', [])),
            color_palette=json.dumps(data.get('color_palette', [])),
            formality_level=data.get('formality_level', 5)
        )
        
        # Calculate AI scores
        ai_confidence, style_score, color_harmony, occasion_fit = calculate_ai_scores(outfit)
        outfit.ai_confidence = ai_confidence
        outfit.ai_style_score = style_score
        outfit.ai_color_harmony = color_harmony
        outfit.ai_occasion_fit = occasion_fit
        
        db.session.add(outfit)
        db.session.commit()
        
        # Generate visualization if requested
        if data.get('generate_visualization', True):
            template = None
            if data.get('template_id'):
                template = OutfitVisualizationTemplate.query.get(data['template_id'])
            
            visualization_url, thumbnail_url, layout_data = generate_outfit_visualization(outfit, template)
            
            outfit.visualization_url = visualization_url
            outfit.thumbnail_url = thumbnail_url
            outfit.layout_data = json.dumps(layout_data)
            
            db.session.commit()
        
        return jsonify({
            'message': 'Outfit created successfully',
            'outfit': outfit.to_dict(),
            'ai_analysis': {
                'confidence': ai_confidence,
                'style_score': style_score,
                'color_harmony': color_harmony,
                'occasion_fit': occasion_fit,
                'overall_rating': (ai_confidence + style_score + color_harmony + occasion_fit) / 4
            },
            'tagline': 'We girls have no time - Outfit created and visualized instantly!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create outfit: {str(e)}'}), 500

@outfit_visualization_bp.route('/outfits', methods=['GET'])
def get_outfits():
    """
    Get user's outfit compositions
    "We girls have no time" - Quick outfit overview!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        # Query parameters
        occasion = request.args.get('occasion')
        season = request.args.get('season')
        favorites_only = request.args.get('favorites') == 'true'
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Build query
        query = OutfitComposition.query.filter_by(user_id=user_id)
        
        if occasion:
            query = query.filter(OutfitComposition.occasion == occasion)
        if season:
            query = query.filter(OutfitComposition.season == season)
        if favorites_only:
            query = query.filter(OutfitComposition.favorite == True)
        
        # Order by most recent
        query = query.order_by(OutfitComposition.created_at.desc())
        
        # Paginate results
        outfits = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Get outfit statistics
        total_outfits = OutfitComposition.query.filter_by(user_id=user_id).count()
        favorites = OutfitComposition.query.filter_by(user_id=user_id, favorite=True).count()
        occasions = db.session.query(OutfitComposition.occasion, db.func.count(OutfitComposition.id)).filter_by(user_id=user_id).group_by(OutfitComposition.occasion).all()
        
        return jsonify({
            'outfits': [outfit.to_dict() for outfit in outfits.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': outfits.total,
                'pages': outfits.pages,
                'has_next': outfits.has_next,
                'has_prev': outfits.has_prev
            },
            'outfit_stats': {
                'total_outfits': total_outfits,
                'favorites': favorites,
                'occasions': [{'occasion': occ, 'count': count} for occ, count in occasions if occ]
            },
            'tagline': 'We girls have no time - Outfits loaded instantly!'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get outfits: {str(e)}'}), 500

@outfit_visualization_bp.route('/outfits/<int:outfit_id>/visualize', methods=['POST'])
def visualize_outfit():
    """
    Generate visualization for existing outfit
    "We girls have no time" - Instant outfit visualization!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        outfit = OutfitComposition.query.filter_by(id=outfit_id, user_id=user_id).first()
        if not outfit:
            return jsonify({'error': 'Outfit not found'}), 404
        
        data = request.get_json() or {}
        
        # Get template if specified
        template = None
        if data.get('template_id'):
            template = OutfitVisualizationTemplate.query.get(data['template_id'])
        
        # Generate visualization
        start_time = time.time()
        visualization_url, thumbnail_url, layout_data = generate_outfit_visualization(outfit, template)
        processing_time = time.time() - start_time
        
        # Update outfit with new visualization
        outfit.visualization_url = visualization_url
        outfit.thumbnail_url = thumbnail_url
        outfit.layout_data = json.dumps(layout_data)
        outfit.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Outfit visualization generated successfully',
            'visualization': {
                'url': visualization_url,
                'thumbnail': thumbnail_url,
                'layout': layout_data,
                'processing_time': processing_time
            },
            'outfit': outfit.to_dict(),
            'tagline': 'We girls have no time - Visualization ready in seconds!'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to visualize outfit: {str(e)}'}), 500

@outfit_visualization_bp.route('/virtual-try-on', methods=['POST'])
def create_virtual_try_on():
    """
    Create virtual try-on session
    "We girls have no time" - Instant virtual try-on!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Try-on data required'}), 400
    
    try:
        # Validate input
        if not data.get('user_photo_url') and not data.get('outfit_composition_id') and not data.get('primary_item_id'):
            return jsonify({'error': 'User photo and item/outfit required'}), 400
        
        # Create virtual try-on session
        try_on = VirtualTryOn(
            user_id=user_id,
            session_name=data.get('session_name', 'Virtual Try-On'),
            session_type=data.get('session_type', 'single_item'),
            primary_item_id=data.get('primary_item_id'),
            outfit_composition_id=data.get('outfit_composition_id'),
            comparison_items=json.dumps(data.get('comparison_items', [])),
            user_photo_url=data.get('user_photo_url'),
            body_measurements=json.dumps(data.get('body_measurements', {})),
            skin_tone=data.get('skin_tone'),
            hair_color=data.get('hair_color'),
            device_type=data.get('device_type', 'unknown')
        )
        
        db.session.add(try_on)
        db.session.flush()  # Get the ID
        
        # Mock virtual try-on processing
        start_time = time.time()
        time.sleep(2)  # Simulate processing
        processing_time = time.time() - start_time
        
        # Generate mock results
        result_image_url = f"https://tanvi-tryon.com/results/{try_on.id}/result.jpg"
        result_thumbnail_url = f"https://tanvi-tryon.com/results/{try_on.id}/thumb.jpg"
        
        # Mock AI analysis
        fit_analysis = {
            "overall_fit": "excellent",
            "fit_score": 0.92,
            "size_recommendation": "perfect",
            "fit_issues": []
        }
        
        color_analysis = {
            "skin_tone_compatibility": 0.88,
            "color_harmony": 0.91,
            "recommended_colors": ["navy", "burgundy", "forest green"],
            "avoid_colors": ["bright yellow", "neon pink"]
        }
        
        style_analysis = {
            "style_match": 0.85,
            "flattering_aspects": ["silhouette", "proportions"],
            "style_suggestions": ["add a belt", "try with heels"]
        }
        
        overall_score = (fit_analysis["fit_score"] + color_analysis["skin_tone_compatibility"] + style_analysis["style_match"]) / 3
        
        # Update try-on with results
        try_on.result_image_url = result_image_url
        try_on.result_thumbnail_url = result_thumbnail_url
        try_on.processing_time = processing_time
        try_on.fit_analysis = json.dumps(fit_analysis)
        try_on.color_analysis = json.dumps(color_analysis)
        try_on.style_analysis = json.dumps(style_analysis)
        try_on.overall_score = overall_score
        
        db.session.commit()
        
        return jsonify({
            'message': 'Virtual try-on completed successfully',
            'try_on': try_on.to_dict(),
            'recommendations': {
                'overall_score': overall_score,
                'fit_rating': 'excellent' if overall_score > 0.8 else 'good' if overall_score > 0.6 else 'fair',
                'key_insights': [
                    f"Fit score: {fit_analysis['fit_score']:.1%}",
                    f"Color compatibility: {color_analysis['skin_tone_compatibility']:.1%}",
                    f"Style match: {style_analysis['style_match']:.1%}"
                ]
            },
            'tagline': 'We girls have no time - Virtual try-on completed in seconds!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create virtual try-on: {str(e)}'}), 500

@outfit_visualization_bp.route('/templates', methods=['GET'])
def get_visualization_templates():
    """
    Get available visualization templates
    "We girls have no time" - Quick template selection!
    """
    try:
        category = request.args.get('category')
        template_type = request.args.get('type')
        
        query = OutfitVisualizationTemplate.query
        
        if category:
            query = query.filter(OutfitVisualizationTemplate.category == category)
        if template_type:
            query = query.filter(OutfitVisualizationTemplate.template_type == template_type)
        
        templates = query.order_by(OutfitVisualizationTemplate.usage_count.desc()).all()
        
        # Get template categories and types
        categories = db.session.query(OutfitVisualizationTemplate.category).distinct().all()
        types = db.session.query(OutfitVisualizationTemplate.template_type).distinct().all()
        
        return jsonify({
            'templates': [template.to_dict() for template in templates],
            'categories': [cat[0] for cat in categories if cat[0]],
            'types': [type[0] for type in types if type[0]],
            'total_templates': len(templates),
            'tagline': 'We girls have no time - Templates loaded instantly!'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get templates: {str(e)}'}), 500

@outfit_visualization_bp.route('/styling-session', methods=['POST'])
def start_styling_session():
    """
    Start interactive styling session
    "We girls have no time" - Guided styling assistance!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    if not data or 'session_goal' not in data:
        return jsonify({'error': 'Session goal required'}), 400
    
    try:
        session = OutfitStylingSession(
            user_id=user_id,
            session_name=data.get('session_name', f"Styling for {data['session_goal']}"),
            session_goal=data['session_goal'],
            target_occasion=data.get('target_occasion'),
            target_style=data.get('target_style'),
            budget_range=data.get('budget_range', 'medium'),
            time_constraint=data.get('time_constraint', 'quick'),
            style_preferences=json.dumps(data.get('style_preferences', {})),
            current_step='preferences',
            steps_completed=json.dumps([]),
            device_type=data.get('device_type', 'unknown')
        )
        
        db.session.add(session)
        db.session.commit()
        
        # Generate initial AI suggestions
        ai_suggestions = [
            {
                "type": "style_direction",
                "suggestion": f"For {data['session_goal']}, I recommend focusing on {data.get('target_style', 'versatile')} pieces",
                "confidence": 0.85
            },
            {
                "type": "color_palette",
                "suggestion": "Consider a neutral base with one accent color",
                "confidence": 0.78
            },
            {
                "type": "key_pieces",
                "suggestion": "Start with a statement piece and build around it",
                "confidence": 0.82
            }
        ]
        
        session.ai_suggestions = json.dumps(ai_suggestions)
        session.progress_percentage = 20.0  # Completed preferences step
        
        db.session.commit()
        
        return jsonify({
            'message': 'Styling session started successfully',
            'session': session.to_dict(),
            'next_steps': [
                'Review your wardrobe items',
                'Select base pieces',
                'Add complementary items',
                'Finalize and visualize outfit'
            ],
            'tagline': 'We girls have no time - Styling session ready to guide you!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to start styling session: {str(e)}'}), 500

@outfit_visualization_bp.route('/styling-session/<int:session_id>/step', methods=['POST'])
def update_styling_session():
    """
    Update styling session progress
    "We girls have no time" - Guided step-by-step styling!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    if not data or 'step' not in data:
        return jsonify({'error': 'Step information required'}), 400
    
    try:
        session = OutfitStylingSession.query.filter_by(id=session_id, user_id=user_id).first()
        if not session:
            return jsonify({'error': 'Styling session not found'}), 404
        
        # Update session progress
        current_step = data['step']
        session.current_step = current_step
        
        # Update completed steps
        completed_steps = json.loads(session.steps_completed) if session.steps_completed else []
        if current_step not in completed_steps:
            completed_steps.append(current_step)
            session.steps_completed = json.dumps(completed_steps)
        
        # Update progress percentage
        session.progress_percentage = (len(completed_steps) / session.total_steps) * 100
        
        # Update user choices
        user_choices = json.loads(session.user_choices) if session.user_choices else {}
        user_choices[current_step] = data.get('choices', {})
        session.user_choices = json.dumps(user_choices)
        
        # Generate step-specific AI suggestions
        step_suggestions = []
        if current_step == 'item_selection':
            step_suggestions = [
                {"suggestion": "Consider versatile pieces that can be mixed and matched", "confidence": 0.88},
                {"suggestion": "Balance proportions with fitted and loose pieces", "confidence": 0.82}
            ]
        elif current_step == 'color_coordination':
            step_suggestions = [
                {"suggestion": "Use the 60-30-10 color rule for balanced outfits", "confidence": 0.90},
                {"suggestion": "Add one pop of color to neutral bases", "confidence": 0.85}
            ]
        elif current_step == 'final_review':
            step_suggestions = [
                {"suggestion": "Check the outfit from different angles", "confidence": 0.87},
                {"suggestion": "Consider the occasion and weather", "confidence": 0.92}
            ]
        
        if step_suggestions:
            session.ai_suggestions = json.dumps(step_suggestions)
        
        # Check if session is complete
        if len(completed_steps) >= session.total_steps:
            session.session_status = 'completed'
            session.completed_at = datetime.utcnow()
            session.session_duration = (datetime.utcnow() - session.started_at).total_seconds() / 60
        
        db.session.commit()
        
        return jsonify({
            'message': f'Styling session updated - {current_step} completed',
            'session': session.to_dict(),
            'next_step': 'final_review' if current_step == 'color_coordination' else 'outfit_creation' if current_step == 'final_review' else 'color_coordination',
            'tagline': 'We girls have no time - One step closer to the perfect outfit!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update styling session: {str(e)}'}), 500

@outfit_visualization_bp.route('/quick-outfit', methods=['POST'])
def generate_quick_outfit():
    """
    Generate quick outfit suggestions
    "We girls have no time" - Instant outfit suggestions!
    """
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json() or {}
    
    try:
        # Get user's wardrobe items
        items = WardrobeItem.query.filter_by(user_id=user_id).all()
        
        if len(items) < 3:
            return jsonify({
                'message': 'Need at least 3 wardrobe items for outfit suggestions',
                'suggestions': [],
                'tagline': 'We girls have no time - Add more items to get outfit suggestions!'
            })
        
        # Filter items by occasion and season if specified
        occasion = data.get('occasion')
        season = data.get('season')
        
        filtered_items = items
        if occasion:
            filtered_items = [item for item in filtered_items if occasion in (json.loads(item.occasion_tags) if item.occasion_tags else [])]
        if season:
            filtered_items = [item for item in filtered_items if season in (json.loads(item.season_tags) if item.season_tags else [])]
        
        # Generate 3 quick outfit suggestions
        suggestions = []
        
        # Group items by category
        tops = [item for item in filtered_items if item.category == 'tops']
        bottoms = [item for item in filtered_items if item.category == 'bottoms']
        dresses = [item for item in filtered_items if item.category == 'dresses']
        shoes = [item for item in filtered_items if item.category == 'shoes']
        outerwear = [item for item in filtered_items if item.category == 'outerwear']
        
        # Generate outfit combinations
        for i in range(min(3, len(tops), len(bottoms))):
            if i < len(tops) and i < len(bottoms):
                outfit_name = f"Quick Outfit {i+1}"
                if occasion:
                    outfit_name += f" for {occasion}"
                
                suggestion = {
                    'name': outfit_name,
                    'items': {
                        'top': tops[i].to_dict(),
                        'bottom': bottoms[i].to_dict(),
                        'shoes': shoes[i % len(shoes)].to_dict() if shoes else None,
                        'outerwear': outerwear[i % len(outerwear)].to_dict() if outerwear else None
                    },
                    'style_score': random.uniform(0.7, 0.95),
                    'occasion_fit': random.uniform(0.8, 0.95),
                    'color_harmony': random.uniform(0.75, 0.9),
                    'styling_tips': [
                        "Add a belt to define the waist",
                        "Layer with accessories for visual interest",
                        "Consider the weather when choosing outerwear"
                    ]
                }
                suggestions.append(suggestion)
        
        # Add dress-based outfits if available
        for i, dress in enumerate(dresses[:2]):
            outfit_name = f"Dress Outfit {i+1}"
            if occasion:
                outfit_name += f" for {occasion}"
            
            suggestion = {
                'name': outfit_name,
                'items': {
                    'dress': dress.to_dict(),
                    'shoes': shoes[i % len(shoes)].to_dict() if shoes else None,
                    'outerwear': outerwear[i % len(outerwear)].to_dict() if outerwear else None
                },
                'style_score': random.uniform(0.75, 0.92),
                'occasion_fit': random.uniform(0.85, 0.95),
                'color_harmony': random.uniform(0.8, 0.95),
                'styling_tips': [
                    "Choose shoes that complement the dress length",
                    "Add layers for versatility",
                    "Consider accessories to complete the look"
                ]
            }
            suggestions.append(suggestion)
        
        return jsonify({
            'suggestions': suggestions,
            'total_suggestions': len(suggestions),
            'filters_applied': {
                'occasion': occasion,
                'season': season,
                'total_items_considered': len(filtered_items)
            },
            'tagline': 'We girls have no time - Quick outfit suggestions ready!'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate quick outfits: {str(e)}'}), 500

