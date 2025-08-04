from flask import Blueprint, jsonify, request
from src.models.user import User, db
from src.models.profile import StyleProfile, WardrobeItem, OutfitHistory, QuickStyleQuiz
from datetime import datetime, date
import json

profile_bp = Blueprint('profile', __name__)

def get_current_user():
    """Helper function to get current authenticated user"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    return User.verify_auth_token(token)

@profile_bp.route('/style-profile', methods=['GET'])
def get_style_profile():
    """
    Get user's style profile - "We girls have no time" for complex style analysis
    Quick access to personalized styling information
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    style_profile = user.style_profile
    if not style_profile:
        # Create default style profile if none exists
        style_profile = StyleProfile(user_id=user.id)
        db.session.add(style_profile)
        db.session.commit()
    
    return jsonify({
        'message': 'Style profile retrieved successfully',
        'tagline': 'We girls have no time - here\'s your quick style profile!',
        'style_profile': style_profile.to_dict()
    }), 200


@profile_bp.route('/style-profile', methods=['PUT'])
def update_style_profile():
    """
    Update style profile - quick style customization
    "We girls have no time" for lengthy style assessments
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        data = request.json
        
        style_profile = user.style_profile
        if not style_profile:
            style_profile = StyleProfile(user_id=user.id)
            db.session.add(style_profile)
        
        # Update basic body information
        if data.get('body_type'):
            style_profile.body_type = data['body_type']
        
        if data.get('height_range'):
            style_profile.height_range = data['height_range']
        
        if data.get('measurements'):
            style_profile.measurements = json.dumps(data['measurements'])
        
        # Update style personality
        if data.get('style_personality'):
            style_profile.style_personality = data['style_personality']
        
        if data.get('lifestyle'):
            style_profile.lifestyle = data['lifestyle']
        
        if data.get('activity_level'):
            style_profile.activity_level = data['activity_level']
        
        # Update color analysis
        if data.get('skin_tone'):
            style_profile.skin_tone = data['skin_tone']
        
        if data.get('hair_color'):
            style_profile.hair_color = data['hair_color']
        
        if data.get('eye_color'):
            style_profile.eye_color = data['eye_color']
        
        if data.get('color_season'):
            style_profile.color_season = data['color_season']
        
        # Update color preferences
        if data.get('favorite_colors'):
            style_profile.favorite_colors = json.dumps(data['favorite_colors'])
        
        if data.get('colors_to_avoid'):
            style_profile.colors_to_avoid = json.dumps(data['colors_to_avoid'])
        
        if data.get('preferred_fits'):
            style_profile.preferred_fits = json.dumps(data['preferred_fits'])
        
        if data.get('style_goals'):
            style_profile.style_goals = json.dumps(data['style_goals'])
        
        # Update occasion styles
        if data.get('work_style'):
            style_profile.work_style = data['work_style']
        
        if data.get('weekend_style'):
            style_profile.weekend_style = data['weekend_style']
        
        if data.get('evening_style'):
            style_profile.evening_style = data['evening_style']
        
        style_profile.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Style profile updated successfully',
            'tagline': 'We girls have no time - style profile updated in seconds!',
            'style_profile': style_profile.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Style profile update failed',
            'message': str(e)
        }), 500


@profile_bp.route('/quick-style-quiz', methods=['POST'])
def take_quick_style_quiz():
    """
    Take the 2-minute style quiz - "We girls have no time" for long assessments
    Rapid style personality assessment for instant AI training
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        data = request.json
        start_time = datetime.utcnow()
        
        # Create new quiz record
        quiz = QuickStyleQuiz(
            user_id=user.id,
            completion_time=data.get('completion_time', 120),  # Default 2 minutes
            style_inspiration=json.dumps(data.get('style_inspiration', [])),
            shopping_frequency=data.get('shopping_frequency'),
            budget_comfort=data.get('budget_comfort'),
            style_risk_level=data.get('style_risk_level', 3),
            preferred_outfits=json.dumps(data.get('preferred_outfits', [])),
            disliked_outfits=json.dumps(data.get('disliked_outfits', [])),
            daily_activities=json.dumps(data.get('daily_activities', [])),
            special_occasions=json.dumps(data.get('special_occasions', [])),
            climate_location=data.get('climate_location')
        )
        
        # Quick AI analysis of responses (simplified for demo)
        style_personality = analyze_style_personality(data)
        quiz.style_personality_result = style_personality
        quiz.confidence_score = 0.85  # Simulated AI confidence
        
        # Generate quick recommendations
        recommendations = generate_quick_recommendations(style_personality, data)
        quiz.recommendations = json.dumps(recommendations)
        
        db.session.add(quiz)
        
        # Update user's style profile with quiz results
        style_profile = user.style_profile
        if not style_profile:
            style_profile = StyleProfile(user_id=user.id)
            db.session.add(style_profile)
        
        style_profile.style_personality = style_personality
        style_profile.last_style_quiz = datetime.utcnow()
        
        # Update lifestyle and preferences based on quiz
        if data.get('daily_activities'):
            if 'work' in data['daily_activities']:
                style_profile.lifestyle = 'professional'
            elif 'school' in data['daily_activities']:
                style_profile.lifestyle = 'student'
            else:
                style_profile.lifestyle = 'casual'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Quick style quiz completed!',
            'tagline': 'We girls have no time - style personality discovered in 2 minutes!',
            'results': {
                'style_personality': style_personality,
                'confidence_score': quiz.confidence_score,
                'recommendations': recommendations,
                'completion_time': quiz.completion_time
            },
            'quiz_id': quiz.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Style quiz failed',
            'message': str(e)
        }), 500


def analyze_style_personality(quiz_data):
    """Quick style personality analysis - simplified AI logic"""
    risk_level = quiz_data.get('style_risk_level', 3)
    activities = quiz_data.get('daily_activities', [])
    budget = quiz_data.get('budget_comfort', 'medium')
    
    if risk_level >= 4 and 'creative_work' in activities:
        return 'edgy'
    elif risk_level <= 2 and budget == 'high':
        return 'classic'
    elif 'work' in activities and risk_level <= 3:
        return 'minimalist'
    elif risk_level >= 4:
        return 'bohemian'
    else:
        return 'romantic'


def generate_quick_recommendations(style_personality, quiz_data):
    """Generate instant style recommendations based on personality"""
    recommendations = {
        'immediate_actions': [],
        'shopping_priorities': [],
        'style_tips': []
    }
    
    if style_personality == 'minimalist':
        recommendations['immediate_actions'] = [
            'Focus on neutral colors: black, white, gray, beige',
            'Invest in quality basics that mix and match',
            'Choose clean lines and simple silhouettes'
        ]
        recommendations['shopping_priorities'] = [
            'White button-down shirt',
            'Black blazer',
            'Well-fitted jeans',
            'Classic trench coat'
        ]
        recommendations['style_tips'] = [
            'Less is more - choose quality over quantity',
            'Stick to a cohesive color palette',
            'Focus on fit and fabric quality'
        ]
    
    elif style_personality == 'bohemian':
        recommendations['immediate_actions'] = [
            'Embrace flowing fabrics and relaxed fits',
            'Mix patterns and textures confidently',
            'Add vintage or artisanal accessories'
        ]
        recommendations['shopping_priorities'] = [
            'Flowy maxi dresses',
            'Fringe or tassel details',
            'Layering pieces',
            'Statement jewelry'
        ]
        recommendations['style_tips'] = [
            'Layer different textures and lengths',
            'Don\'t be afraid to mix prints',
            'Accessories are key to the boho look'
        ]
    
    # Add more personality types as needed
    
    return recommendations


@profile_bp.route('/wardrobe', methods=['GET'])
def get_wardrobe():
    """
    Get user's wardrobe items - quick wardrobe overview
    "We girls have no time" for complex wardrobe management
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Get query parameters for filtering
    category = request.args.get('category')
    favorite_only = request.args.get('favorite') == 'true'
    
    query = WardrobeItem.query.filter_by(user_id=user.id)
    
    if category:
        query = query.filter_by(category=category)
    
    if favorite_only:
        query = query.filter_by(favorite=True)
    
    items = query.order_by(WardrobeItem.updated_at.desc()).all()
    
    # Quick wardrobe stats
    stats = {
        'total_items': len(user.wardrobe_items),
        'categories': {},
        'most_worn': None,
        'least_worn': None,
        'favorites_count': len([item for item in user.wardrobe_items if item.favorite])
    }
    
    # Calculate category distribution
    for item in user.wardrobe_items:
        if item.category in stats['categories']:
            stats['categories'][item.category] += 1
        else:
            stats['categories'][item.category] = 1
    
    # Find most and least worn items
    if user.wardrobe_items:
        most_worn = max(user.wardrobe_items, key=lambda x: x.wear_count)
        least_worn = min(user.wardrobe_items, key=lambda x: x.wear_count)
        stats['most_worn'] = most_worn.name if most_worn.wear_count > 0 else None
        stats['least_worn'] = least_worn.name if least_worn.wear_count == 0 else None
    
    return jsonify({
        'message': 'Wardrobe retrieved successfully',
        'tagline': 'We girls have no time - here\'s your quick wardrobe overview!',
        'items': [item.to_dict() for item in items],
        'stats': stats
    }), 200


@profile_bp.route('/wardrobe', methods=['POST'])
def add_wardrobe_item():
    """
    Add new wardrobe item - quick item cataloging
    "We girls have no time" for complex item entry
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('name') or not data.get('category'):
            return jsonify({
                'error': 'Name and category are required',
                'message': 'Quick add needs just the basics!'
            }), 400
        
        # Create new wardrobe item
        item = WardrobeItem(
            user_id=user.id,
            name=data['name'],
            category=data['category'],
            subcategory=data.get('subcategory'),
            brand=data.get('brand'),
            primary_color=data.get('primary_color'),
            secondary_colors=json.dumps(data.get('secondary_colors', [])),
            pattern=data.get('pattern', 'solid'),
            material=data.get('material'),
            fit_type=data.get('fit_type'),
            style_tags=json.dumps(data.get('style_tags', [])),
            season_appropriate=json.dumps(data.get('season_appropriate', ['all'])),
            purchase_date=datetime.strptime(data['purchase_date'], '%Y-%m-%d').date() if data.get('purchase_date') else None,
            location=data.get('location', 'closet'),
            condition=data.get('condition', 'good'),
            favorite=data.get('favorite', False)
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify({
            'message': 'Wardrobe item added successfully',
            'tagline': 'We girls have no time - item cataloged in seconds!',
            'item': item.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to add wardrobe item',
            'message': str(e)
        }), 500


@profile_bp.route('/wardrobe/<int:item_id>', methods=['PUT'])
def update_wardrobe_item(item_id):
    """
    Update wardrobe item - quick item editing
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        item = WardrobeItem.query.filter_by(id=item_id, user_id=user.id).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        data = request.json
        
        # Update item attributes
        if data.get('name'):
            item.name = data['name']
        if data.get('category'):
            item.category = data['category']
        if data.get('subcategory'):
            item.subcategory = data['subcategory']
        if data.get('brand'):
            item.brand = data['brand']
        if data.get('primary_color'):
            item.primary_color = data['primary_color']
        if data.get('secondary_colors'):
            item.secondary_colors = json.dumps(data['secondary_colors'])
        if data.get('pattern'):
            item.pattern = data['pattern']
        if data.get('material'):
            item.material = data['material']
        if data.get('fit_type'):
            item.fit_type = data['fit_type']
        if data.get('style_tags'):
            item.style_tags = json.dumps(data['style_tags'])
        if data.get('season_appropriate'):
            item.season_appropriate = json.dumps(data['season_appropriate'])
        if data.get('location'):
            item.location = data['location']
        if data.get('condition'):
            item.condition = data['condition']
        if 'favorite' in data:
            item.favorite = data['favorite']
        
        item.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Wardrobe item updated successfully',
            'tagline': 'We girls have no time - item updated quickly!',
            'item': item.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to update wardrobe item',
            'message': str(e)
        }), 500


@profile_bp.route('/wardrobe/<int:item_id>/worn', methods=['POST'])
def mark_item_worn(item_id):
    """
    Mark item as worn - quick usage tracking
    "We girls have no time" for complex outfit logging
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        item = WardrobeItem.query.filter_by(id=item_id, user_id=user.id).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        item.increment_wear_count()
        
        return jsonify({
            'message': 'Item marked as worn',
            'tagline': 'We girls have no time - wear count updated instantly!',
            'item': item.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to update wear count',
            'message': str(e)
        }), 500


@profile_bp.route('/outfit-history', methods=['GET'])
def get_outfit_history():
    """
    Get outfit history - quick past outfit review
    "We girls have no time" for complex outfit analysis
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Get recent outfits
    recent_outfits = OutfitHistory.query.filter_by(user_id=user.id)\
        .order_by(OutfitHistory.worn_date.desc())\
        .limit(20).all()
    
    # Quick stats
    stats = {
        'total_outfits': len(user.outfit_history),
        'average_rating': 0,
        'most_successful_occasion': None,
        'favorite_season': None
    }
    
    if user.outfit_history:
        # Calculate average rating
        rated_outfits = [o for o in user.outfit_history if o.user_rating]
        if rated_outfits:
            stats['average_rating'] = sum(o.user_rating for o in rated_outfits) / len(rated_outfits)
        
        # Find most successful occasion
        occasion_scores = {}
        for outfit in user.outfit_history:
            if outfit.occasion and outfit.user_rating:
                if outfit.occasion not in occasion_scores:
                    occasion_scores[outfit.occasion] = []
                occasion_scores[outfit.occasion].append(outfit.user_rating)
        
        if occasion_scores:
            avg_scores = {occ: sum(scores)/len(scores) for occ, scores in occasion_scores.items()}
            stats['most_successful_occasion'] = max(avg_scores, key=avg_scores.get)
    
    return jsonify({
        'message': 'Outfit history retrieved successfully',
        'tagline': 'We girls have no time - here\'s your quick outfit review!',
        'outfits': [outfit.to_dict() for outfit in recent_outfits],
        'stats': stats
    }), 200


@profile_bp.route('/outfit-history', methods=['POST'])
def log_outfit():
    """
    Log a new outfit - quick outfit recording
    "We girls have no time" for detailed outfit documentation
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        data = request.json
        
        if not data.get('item_ids'):
            return jsonify({
                'error': 'Item IDs are required',
                'message': 'Quick outfit logging needs at least one item!'
            }), 400
        
        # Create outfit history record
        outfit = OutfitHistory(
            user_id=user.id,
            outfit_name=data.get('outfit_name'),
            item_ids=json.dumps(data['item_ids']),
            occasion=data.get('occasion'),
            weather=data.get('weather'),
            season=data.get('season'),
            location=data.get('location'),
            worn_date=datetime.strptime(data['worn_date'], '%Y-%m-%d').date() if data.get('worn_date') else date.today()
        )
        
        db.session.add(outfit)
        db.session.commit()
        
        # Update wear counts for items
        for item_id in data['item_ids']:
            item = WardrobeItem.query.filter_by(id=item_id, user_id=user.id).first()
            if item:
                item.increment_wear_count()
        
        return jsonify({
            'message': 'Outfit logged successfully',
            'tagline': 'We girls have no time - outfit recorded instantly!',
            'outfit': outfit.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to log outfit',
            'message': str(e)
        }), 500


@profile_bp.route('/outfit-history/<int:outfit_id>/rate', methods=['POST'])
def rate_outfit(outfit_id):
    """
    Rate an outfit - quick feedback for AI learning
    "We girls have no time" for complex outfit analysis
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        outfit = OutfitHistory.query.filter_by(id=outfit_id, user_id=user.id).first()
        if not outfit:
            return jsonify({'error': 'Outfit not found'}), 404
        
        data = request.json
        
        # Update ratings
        if data.get('user_rating'):
            outfit.user_rating = data['user_rating']
        if data.get('comfort_level'):
            outfit.comfort_level = data['comfort_level']
        if data.get('confidence_level'):
            outfit.confidence_level = data['confidence_level']
        if 'received_compliments' in data:
            outfit.received_compliments = data['received_compliments']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Outfit rated successfully',
            'tagline': 'We girls have no time - feedback recorded for better AI recommendations!',
            'outfit': outfit.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to rate outfit',
            'message': str(e)
        }), 500

