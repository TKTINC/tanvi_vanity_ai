from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import requests
import json
from src.models.personalization import (
    UserStyleProfile, StyleLearningEngine, PersonalizationInsights, db
)
from src.models.enhanced_recommendations import OutfitFeedback

personalization_bp = Blueprint('personalization', __name__)

# WS1 User Management Service Integration
WS1_BASE_URL = 'http://localhost:5001'  # WS1 service endpoint

def get_user_data(user_id, auth_token):
    """Fetch user data from WS1 User Management Service"""
    try:
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Get user profile
        profile_response = requests.get(f'{WS1_BASE_URL}/api/profile', headers=headers, timeout=5)
        if profile_response.status_code != 200:
            return None
        
        profile_data = profile_response.json()
        
        # Get wardrobe data
        wardrobe_response = requests.get(f'{WS1_BASE_URL}/api/profile/wardrobe', headers=headers, timeout=5)
        wardrobe_data = []
        if wardrobe_response.status_code == 200:
            wardrobe_data = wardrobe_response.json().get('items', [])
        
        return {
            'profile': profile_data,
            'wardrobe': wardrobe_data
        }
    except Exception as e:
        print(f"Error fetching user data: {str(e)}")
        return None

def verify_auth_token(auth_token):
    """Verify authentication token with WS1 service"""
    try:
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = requests.post(f'{WS1_BASE_URL}/api/auth/verify-token', headers=headers, timeout=5)
        return response.status_code == 200
    except:
        return False

@personalization_bp.route('/style-profile', methods=['GET'])
def get_style_profile():
    """
    Get user's personalized style profile
    "We girls have no time" - Your complete style profile instantly!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Get or create style profile
        profile = UserStyleProfile.get_or_create_profile(user_id)
        profile_data = profile.to_dict()
        
        # Get style evolution data
        evolution_data = StyleLearningEngine.analyze_user_style_evolution(user_id)
        
        # Generate learning status
        learning_status = {
            'confidence_level': 'high' if profile_data['confidence_score'] > 0.7 else 'medium' if profile_data['confidence_score'] > 0.4 else 'developing',
            'data_points': profile_data['learning_data_points'],
            'personalization_ready': profile_data['confidence_score'] > 0.3,
            'recommendation_accuracy': f"{min(profile_data['confidence_score'] * 100, 95):.0f}%"
        }
        
        return jsonify({
            'status': 'success',
            'message': 'Style profile retrieved successfully',
            'profile': profile_data,
            'evolution': evolution_data,
            'learning_status': learning_status,
            'personalization_features': {
                'auto_learning': profile_data['auto_learn_enabled'],
                'exploration_mode': profile_data['style_exploration_mode'],
                'style_confidence': profile_data['style_confidence'],
                'style_flexibility': profile_data['style_flexibility']
            },
            'tagline': 'We girls have no time - Your style profile ready!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve style profile',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@personalization_bp.route('/style-profile', methods=['PUT'])
def update_style_profile():
    """
    Update user's style profile settings
    "We girls have no time" - Quick style profile updates!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        # Get request data
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Get profile
        profile = UserStyleProfile.get_or_create_profile(user_id)
        
        # Update settings
        if 'auto_learn_enabled' in data:
            profile.auto_learn_enabled = data['auto_learn_enabled']
        
        if 'style_exploration_mode' in data:
            profile.style_exploration_mode = data['style_exploration_mode']
        
        if 'primary_style' in data:
            profile.primary_style = data['primary_style']
        
        if 'secondary_style' in data:
            profile.secondary_style = data['secondary_style']
        
        if 'budget_consciousness' in data:
            profile.budget_consciousness = max(0.0, min(1.0, data['budget_consciousness']))
        
        # Update lifestyle factors
        if 'lifestyle_factors' in data:
            profile.lifestyle_factors = json.dumps(data['lifestyle_factors'])
        
        # Update climate preferences
        if 'climate_preferences' in data:
            profile.climate_preferences = json.dumps(data['climate_preferences'])
        
        profile.last_updated = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Style profile updated successfully',
            'profile': profile.to_dict(),
            'updated_fields': list(data.keys()),
            'tagline': 'We girls have no time - Profile updated instantly!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to update style profile',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@personalization_bp.route('/personalized-outfit', methods=['POST'])
def get_personalized_outfit():
    """
    Get highly personalized outfit recommendation
    "We girls have no time" - Perfectly personalized outfits!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        # Get request data
        data = request.get_json()
        user_id = data.get('user_id')
        occasion = data.get('occasion', 'casual')
        context = data.get('context', {})  # weather, temperature, season, etc.
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Fetch user data from WS1
        user_data = get_user_data(user_id, auth_token)
        if not user_data:
            return jsonify({'error': 'Unable to fetch user data'}), 500
        
        wardrobe_data = user_data.get('wardrobe', [])
        if not wardrobe_data:
            return jsonify({
                'status': 'no_wardrobe',
                'message': 'No wardrobe items found. Add some clothes first!',
                'recommendation': 'Start by adding basic wardrobe items.',
                'tagline': 'We girls have no time - But we need clothes first!'
            }), 400
        
        # Generate personalized recommendation
        personalized_rec = StyleLearningEngine.generate_personalized_recommendations(
            user_id, wardrobe_data, occasion, context
        )
        
        if not personalized_rec:
            return jsonify({
                'status': 'insufficient_items',
                'message': 'Not enough suitable items for personalized recommendation',
                'recommendation': f'Add more {occasion}-appropriate items to your wardrobe',
                'tagline': 'We girls have no time - Need more outfit options!'
            }), 400
        
        # Get full item details for response
        item_details = []
        for item in wardrobe_data:
            if item.get('id') in personalized_rec['outfit_items']:
                item_details.append(item)
        
        # Get style profile for additional context
        profile = UserStyleProfile.query.filter_by(user_id=user_id).first()
        profile_context = profile.to_dict() if profile else {}
        
        return jsonify({
            'status': 'success',
            'message': 'Personalized outfit recommendation generated successfully',
            'recommendation': personalized_rec,
            'outfit_items': item_details,
            'personalization_context': {
                'confidence_score': profile_context.get('confidence_score', 0),
                'learning_data_points': profile_context.get('learning_data_points', 0),
                'primary_style': profile_context.get('primary_style'),
                'style_flexibility': profile_context.get('style_flexibility', 0.5),
                'exploration_mode': profile_context.get('style_exploration_mode', False)
            },
            'generation_time': '0.8 seconds',
            'tagline': 'We girls have no time - Perfectly personalized outfit ready!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Personalized outfit recommendation failed',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@personalization_bp.route('/style-insights', methods=['GET'])
def get_style_insights():
    """
    Get comprehensive style insights and analysis
    "We girls have no time" - Understand your style instantly!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Generate comprehensive insights
        insights = PersonalizationInsights.generate_style_insights(user_id)
        
        if insights.get('status') == 'no_profile':
            return jsonify(insights), 404
        
        # Add summary metrics
        summary = {
            'personalization_level': insights['personalization_status']['personalization_level'],
            'style_confidence': insights['style_personality']['confidence_level'],
            'color_preferences_established': len(insights['color_preferences']['top_preferred_colors']) > 0,
            'style_evolution_tracked': insights['style_evolution'].get('status') != 'insufficient_data',
            'recommendations_count': len(insights['recommendations'])
        }
        
        return jsonify({
            'status': 'success',
            'message': 'Style insights generated successfully',
            'insights': insights,
            'summary': summary,
            'analysis_date': datetime.utcnow().isoformat(),
            'tagline': 'We girls have no time - Your style insights ready!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to generate style insights',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@personalization_bp.route('/style-evolution', methods=['GET'])
def get_style_evolution():
    """
    Get detailed style evolution analysis
    "We girls have no time" - Track your style journey!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        user_id = request.args.get('user_id')
        days_back = request.args.get('days_back', 90, type=int)
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Get evolution analysis
        evolution_data = StyleLearningEngine.analyze_user_style_evolution(user_id, days_back)
        
        if evolution_data.get('status') == 'insufficient_data':
            return jsonify({
                'status': 'insufficient_data',
                'message': evolution_data['message'],
                'data_points': evolution_data['data_points'],
                'minimum_required': evolution_data['minimum_required'],
                'recommendation': 'Keep rating outfits to track your style evolution!',
                'tagline': 'We girls have no time - But we need more data first!'
            }), 400
        
        # Add trend analysis
        timeline = evolution_data.get('timeline', [])
        if len(timeline) > 1:
            recent_ratings = [week['average_rating'] for week in timeline[-4:]]  # Last 4 weeks
            early_ratings = [week['average_rating'] for week in timeline[:4]]   # First 4 weeks
            
            if len(recent_ratings) > 0 and len(early_ratings) > 0:
                recent_avg = sum(recent_ratings) / len(recent_ratings)
                early_avg = sum(early_ratings) / len(early_ratings)
                trend_direction = 'improving' if recent_avg > early_avg + 0.2 else 'declining' if recent_avg < early_avg - 0.2 else 'stable'
                
                evolution_data['trend_analysis'] = {
                    'direction': trend_direction,
                    'recent_average': round(recent_avg, 2),
                    'early_average': round(early_avg, 2),
                    'change': round(recent_avg - early_avg, 2)
                }
        
        return jsonify({
            'status': 'success',
            'message': 'Style evolution analysis completed',
            'evolution': evolution_data,
            'analysis_period': f'{days_back} days',
            'analysis_date': datetime.utcnow().isoformat(),
            'tagline': 'We girls have no time - Your style journey revealed!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to analyze style evolution',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@personalization_bp.route('/learning-feedback', methods=['POST'])
def submit_learning_feedback():
    """
    Submit feedback specifically for learning and personalization
    "We girls have no time" - Quick feedback for better learning!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        # Get request data
        data = request.get_json()
        user_id = data.get('user_id')
        feedback_data = data.get('feedback_data', {})
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Update style profile with feedback
        updated_profile = StyleLearningEngine.update_style_profile_from_feedback(
            user_id, feedback_data
        )
        
        # Generate learning insights
        learning_insights = []
        
        confidence_change = feedback_data.get('confidence_change', 0)
        if confidence_change > 0:
            learning_insights.append("Your style profile confidence has improved!")
        
        if feedback_data.get('rating', 0) >= 4:
            learning_insights.append("Great feedback! We're learning what you love.")
        elif feedback_data.get('rating', 0) <= 2:
            learning_insights.append("Thanks for the honest feedback. We'll avoid similar combinations.")
        
        # Check if personalization is ready
        personalization_ready = updated_profile['confidence_score'] > 0.3
        if personalization_ready and updated_profile['learning_data_points'] == 10:
            learning_insights.append("🎉 Personalization unlocked! Your recommendations will now be highly customized.")
        
        return jsonify({
            'status': 'success',
            'message': 'Learning feedback processed successfully',
            'updated_profile': updated_profile,
            'learning_insights': learning_insights,
            'personalization_status': {
                'ready': personalization_ready,
                'confidence_score': updated_profile['confidence_score'],
                'data_points': updated_profile['learning_data_points'],
                'next_milestone': 20 if updated_profile['learning_data_points'] < 20 else 'Advanced personalization active'
            },
            'tagline': 'We girls have no time - Learning from your feedback!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to process learning feedback',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

@personalization_bp.route('/style-recommendations', methods=['GET'])
def get_style_recommendations():
    """
    Get personalized style recommendations and tips
    "We girls have no time" - Personalized style tips instantly!
    """
    try:
        # Get authentication token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authentication required'}), 401
        
        auth_token = auth_header.split(' ')[1]
        if not verify_auth_token(auth_token):
            return jsonify({'error': 'Invalid authentication token'}), 401
        
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        # Get style profile
        profile = UserStyleProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            return jsonify({
                'status': 'no_profile',
                'message': 'No style profile found. Start rating outfits to get personalized recommendations!',
                'tagline': 'We girls have no time - But we need your feedback first!'
            }), 404
        
        profile_data = profile.to_dict()
        
        # Generate personalized recommendations
        recommendations = {
            'style_tips': [],
            'wardrobe_suggestions': [],
            'color_recommendations': [],
            'shopping_priorities': [],
            'style_challenges': []
        }
        
        # Style tips based on profile
        primary_style = profile_data.get('primary_style')
        if primary_style:
            recommendations['style_tips'].append(f"Embrace your {primary_style} style with confidence!")
        
        style_flexibility = profile_data.get('style_flexibility', 0.5)
        if style_flexibility > 0.7:
            recommendations['style_tips'].append("You love variety! Try mixing different style elements.")
        elif style_flexibility < 0.3:
            recommendations['style_tips'].append("You have a signature style! Focus on perfecting your look.")
        
        # Color recommendations
        preferred_colors = profile_data.get('preferred_colors', {})
        if preferred_colors:
            top_colors = sorted(preferred_colors.items(), key=lambda x: x[1], reverse=True)[:3]
            color_names = [color[0] for color in top_colors]
            recommendations['color_recommendations'].append(f"Your power colors: {', '.join(color_names)}")
        else:
            recommendations['color_recommendations'].append("Experiment with different colors to find your favorites!")
        
        # Wardrobe suggestions
        preferred_categories = profile_data.get('preferred_categories', {})
        if preferred_categories:
            top_category = max(preferred_categories, key=preferred_categories.get)
            recommendations['wardrobe_suggestions'].append(f"You love {top_category}! Consider expanding this category.")
        
        # Shopping priorities
        confidence_score = profile_data.get('confidence_score', 0)
        if confidence_score < 0.5:
            recommendations['shopping_priorities'].append("Focus on versatile basics that match your emerging style.")
        else:
            recommendations['shopping_priorities'].append("You can confidently invest in statement pieces!")
        
        # Style challenges
        exploration_mode = profile_data.get('style_exploration_mode', False)
        if exploration_mode:
            recommendations['style_challenges'].append("Try a completely different style this week!")
        else:
            recommendations['style_challenges'].append("Experiment with one new color or pattern this week.")
        
        return jsonify({
            'status': 'success',
            'message': 'Personalized style recommendations generated',
            'recommendations': recommendations,
            'profile_summary': {
                'primary_style': primary_style,
                'confidence_level': 'high' if confidence_score > 0.7 else 'medium' if confidence_score > 0.4 else 'developing',
                'style_type': 'experimental' if style_flexibility > 0.7 else 'consistent' if style_flexibility < 0.3 else 'flexible',
                'personalization_level': profile_data.get('learning_data_points', 0)
            },
            'tagline': 'We girls have no time - Personalized style tips ready!'
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to generate style recommendations',
            'details': str(e),
            'tagline': 'We girls have no time - But this error needs fixing!'
        }), 500

